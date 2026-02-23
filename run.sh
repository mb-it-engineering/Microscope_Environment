#!/bin/bash

if [ "$APP_MODE" = "full" ]; then
    echo "Starting server + LLM agent..."
    uvicorn src.edge.simulation.api:app --host 0.0.0.0 --port 8000 &
    edge-llm
else
    echo "Starting server only..."
    uvicorn src.edge.simulation.api:app --host 0.0.0.0 --port 8000
fi