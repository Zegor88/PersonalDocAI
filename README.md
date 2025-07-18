# PrivateDocAI

PrivateDocAI is an intellectual assistant for individual therapy based on RAG (Retrieval Augmented Generation).

## Overview

PrivateDocAI acts as your personal medical consultant, leveraging a comprehensive knowledge base of your health data:

1. **Data Integration**
   - Medical history and current conditions
   - Laboratory test results and analyses
   - Health questionnaires and surveys
   - Daily health observations and symptoms

2. **Consultation Process**
   - The agent analyzes your complete health profile
   - Provides context-aware medical consultations
   - Maintains conversation history for continuous care
   - Offers personalized recommendations based on your data

3. **Usage**
   - Add your medical documents to `data/input/` in markdown format
   - Start a consultation session through the web interface
   - The agent references your health data during conversations
   - All interactions are private and stored locally

> Note: PrivateDocAI is an assistant tool and should not replace professional medical consultation. Always verify medical decisions with qualified healthcare providers.

## Key Features

- **RAG System:** Context-aware responses based on a knowledge base from `data/input`.
- **Asynchronous Architecture:** Built with `async/await`.
- **OpenAI Model:** Leverages GPT-4.1-mini.
- **Langchain:** Provides a flexible framework.
- **Memory:** Maintains conversation history and context across multiple sessions.
- **Prompting with Reasoning:** Uses structured prompts with explicit reasoning steps to generate more thoughtful and therapeutic responses.
- **UI**: Streamlit-based web interface with chat functionality and real-time responses from the AI therapist.

## Architecture

The application is organized in a modular way:

1. **Core Components (`src/familydoc_ai/`):**
> Currently implemented as a single agent, with plans to expand into a multi-agent system in future releases
   - `agent.py` - main logic of the therapy agent
   - `rag.py` - context retrieval and processing system
   - `app.py` - Streamlit web application providing an user interface for interacting with the agent

2. **RAG System Implementation:**
   - Uses `sentence-transformers/all-MiniLM-L6-v2` for text embeddings
   - Document processing:
     * Loads `.md` files from `data/input`
     * Splits documents into chunks (1000 chars with 200 char overlap)
     * Creates FAISS vector store for efficient similarity search
   - Fallback mechanisms:
     * Graceful handling of empty document directories
     * Fallback to no-context mode for very short documents
   - Async-ready retrieval interface for the agent

3. **Prompting and Configuration (`prompting/`):**
   - System prompt templates in YAML
   - Output schema validation via `output_schema.py` (*just for testing, were implementing the additional fields in responc**)
   - Utilities for building contextual prompts
   - With the possibility of choosing the *Reasoning* configuration

4. **State Management (`memory/`):**
   - Dialogue history stored in JSON format
   - Context managers for resources
   - Asynchronous operations with timeouts

## Project Structure

```
.
├── data/
│   └── input/              # Knowledge base markdown files
├── src/
│   └── familydoc_ai/      # Main application code
│       ├── agent.py       # Therapy agent implementation
│       ├── app.py         # Streamlit web interface
│       ├── rag.py         # RAG system implementation
│       ├── memory/        # Session and conversation history
│       └── prompting/     # Prompt engineering and configuration
│           ├── config_reasoning.yaml
│           ├── output_schema.py
│           ├── prompt_builder.py
│           ├── system_prompt.yaml
│           └── utils.py
├── pyproject.toml         # Project dependencies and configuration
├── run.py                 # Application entry point
└── LICENSE
```

## Getting Started

### Requirements

- Python ≥3.12
- `uv` package manager
- OpenAI API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Zegor88/PersonalDocAI.git
   cd PersonalDocAI
   ```

2. **Create a virtual environment:**
   ```bash
   # Create and activate virtual environment
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # OR
   .venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```bash
   # Install from pyproject.toml (development mode)
   uv pip install -e .[dev]
   
   # OR install from requirements.txt
   uv pip install -r requirements.txt
   ```


### Development

For development purposes, you can:

1. **Update requirements.txt:**
   ```bash
   uv pip freeze > requirements.txt
   ```

2. **Install development dependencies:**
   ```bash
   uv pip install -e .[dev]
   ```

### Running the Application

1. **Prepare your data:**
   - Place `.md` files in `data/input/`

2. **Start the application:**
   ```bash
   python run.py
   ```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.