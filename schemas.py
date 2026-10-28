"""Request/response models for the AI Code Explainer API."""

from pydantic import BaseModel, Field


class ExplainRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Source code to explain")
    language: str = Field("python", description="Programming language of the snippet")
    level: str = Field(
        "beginner",
        pattern="^(beginner|intermediate|expert)$",
        description="Detail level: beginner, intermediate or expert",
    )


class LineExplanation(BaseModel):
    line: str
    explanation: str


class ExplainResponse(BaseModel):
    demo: bool = False
    overview: str
    line_by_line: list[LineExplanation] = []
    key_concepts: list[str] = []
    possible_bugs: list[str] = []
    improvements: list[str] = []
    model: str = "demo"
