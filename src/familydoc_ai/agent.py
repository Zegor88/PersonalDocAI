import os
from typing import cast
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from familydoc_ai.prompting.output_schema import DoctorAdvice
from familydoc_ai.prompting.prompt_builder import build_prompt_from_config
from familydoc_ai.prompting.utils import load_yaml_config
from familydoc_ai.rag import RAGSystem

load_dotenv()


class TherapistAgent:
    """An AI agent that acts as a therapist, using RAG for context."""

    def __init__(self) -> None:
        """
        Initializes the TherapistAgent.
        """
        # --- Configuration and LLM ---
        prompt_config_path = "src/familydoc_ai/prompting/system_prompt.yaml"
        self.prompt_config = load_yaml_config(prompt_config_path)[
            "family_doctor_chatbot_prompt"
        ]
        self.reasoning_config = load_yaml_config(
            "src/familydoc_ai/prompting/config_reasoning.yaml"
        )

        # --- LLM ---
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0.3,
            api_key=SecretStr(os.getenv("OPENAI_API_KEY") or ""),
        )
        self.structured_llm = self.llm.with_structured_output(DoctorAdvice)

        # --- Memory ---
        # TODO: The memory directory must be created for the agent to work.
        # TODO: For a web app like Streamlit, it is better to store history in the session state.
        self.memory = FileChatMessageHistory(
            file_path="src/familydoc_ai/memory/chat_history.json"
        )

        # --- RAG ---
        self.rag_system = RAGSystem(data_path=Path("data/input"))

    async def run(self, user_message: str) -> DoctorAdvice:
        """
        Builds a prompt with RAG context and sends it to the LLM.

        Args:
            user_message: The user's message.

        Returns:
            The answer from the LLM in a structured format.
        """

        # 1. Get the relevant context from RAG
        # TODO: add the rephrasing of the user's question to stand-alone question for the RAG
        rag_context_docs = await self.rag_system.as_retriever().ainvoke(user_message)
        rag_context = "\n\n".join([doc.page_content for doc in rag_context_docs])

        # 2. Build the system prompt
        system_prompt = build_prompt_from_config(
            config=self.prompt_config,
            config_reasoning=self.reasoning_config,
        )

        # 3. Build the prompt template, including the RAG context
        prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessage(
                    content=f"""
Analyze the following context from the patient's questionnaire and answer the question. If the context is not relevant, ignore it.

### Context from the questionnaire:
{rag_context}

### User's question:
{user_message}
"""
                ),
            ]
        )

        # 4. Create the chain
        process_chat = prompt_template | self.structured_llm

        # 5. Execute the chain
        response = cast(
            DoctorAdvice,
            await process_chat.ainvoke({"chat_history": self.memory.messages}),
        )

        # 6. Save the "clean" user's question in the memory
        self.memory.add_user_message(user_message)
        self.memory.add_ai_message(response.direct_answer)

        return response
