# sentiment_api
A demo about how to use `uv` to get stated with a Python (FastAPI) project in 30 minutes

## how to get started

Install uv from Astral's installer or your package manager, then:
```bash
uv sync
```

## how to run api

```bash
export SENTIMENT_MODEL="azure:<your-deployment-name>"
export AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com"
export AZURE_OPENAI_API_KEY="..."
export OPENAI_API_VERSION="<api-version-for-your-deployment>"

uv run uvicorn sentiment_api.main:app --reload
```

### verify the api

```bash
curl -s localhost:8000/sentiment -H 'content-type: application/json' \
  -d '{"reviews": ["Setup took two minutes, love it.", "Broke after a week. Support ignored me."]}'
```

## how to play unit-test

Write whatever unit-test under `test/`, then:

```bash
uv run pytest
```
