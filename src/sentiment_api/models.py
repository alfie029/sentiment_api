from typing import Literal

from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    reviews: list[str] = Field(min_length=1, max_length=20)


class SentimentResult(BaseModel):
    label: Literal["positive", "neutral", "negative"]
    score: float = Field(ge=-1.0, le=1.0)
    rationale: str = Field(description="One short sentence justifying the label.")


class IndexedSentiment(SentimentResult):
    index: int = Field(ge=0, description="Index of the review this verdict belongs to.")


class BatchSentiment(BaseModel):
    results: list[IndexedSentiment]


class ReviewVerdict(BaseModel):
    review: str
    sentiment: SentimentResult


class SentimentResponse(BaseModel):
    results: list[ReviewVerdict]
    average_score: float
