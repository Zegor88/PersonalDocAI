from pydantic import BaseModel, Field


class DoctorAdvice(BaseModel):
    """
    Data model for the doctor's advice.
    Just for testing I added the explanation and recommendations fields.
    """

    direct_answer: str = Field(
        description="A direct and concise answer to the user's question."
    )
    explanation: str = Field(
        description="A more detailed explanation of the reasoning behind the answer."
    )
    recommendations: list[str] = Field(
        description="A list of actionable recommendations for the user."
    ) 