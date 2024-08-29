@echo off

echo Deploying Cloud Function...

gcloud functions deploy openai-assistant-api-tester ^
    --runtime python312 ^
    --trigger-http ^
    --source . ^
    --entry-point main ^
    --memory 256MB ^
    --timeout 60s ^
    --set-env-vars OPENAI_API_KEY="%OPENAI_API_KEY%"

echo Deployment complete.
