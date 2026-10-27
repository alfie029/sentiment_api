import json
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic_ai import Agent
from pydantic_ai.exceptions import UnexpectedModelBehavior

from .agent import get_agent
from .models import BatchSentiment, ReviewRequest, ReviewVerdict, SentimentResponse

app = FastAPI(title="Sentiment API")
AgentDep = Annotated[Agent[None, BatchSentiment], Depends(get_agent)]


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/sentiment", response_model=SentimentResponse)
async def analyze(req: ReviewRequest, agent: AgentDep) -> SentimentResponse:
    payload = json.dumps([{"index": i, "review": r} for i, r in enumerate(req.reviews)])

    try:
        run = await agent.run(payload)
    except UnexpectedModelBehavior as exc:
        raise HTTPException(status_code=502, detail="Model returned unusable output") from exc

    by_index = {item.index: item for item in run.output.results}
    if len(run.output.results) != len(req.reviews) or set(by_index) != set(range(len(req.reviews))):
        raise HTTPException(status_code=502, detail="Model did not return exactly one verdict per review")

    results = [ReviewVerdict(review=r, sentiment=by_index[i]) for i, r in enumerate(req.reviews)]
    avg = sum(v.sentiment.score for v in results) / len(results)
    return SentimentResponse(results=results, average_score=avg)
