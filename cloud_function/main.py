from time import perf_counter
from google.cloud import storage
from openai import OpenAI
import pandas as pd

bucket = "openai-ass-api-public"
file = "api_response_times.csv"
# Note the cache-busting parameter. Default cache is 1 hour.
df = pd.read_csv(f"https://storage.googleapis.com/{bucket}/{file}?x={perf_counter()}")

# Call the API, time the response
client = OpenAI()
assistant = client.beta.assistants.create(model="gpt-4o-mini")
thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="hi",
)
start_time = perf_counter()
client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
)
duration = perf_counter() - start_time

# Add the response time to the DF
new_row = pd.DataFrame(
    data=[[pd.Timestamp.utcnow(), duration]],
    columns=df.columns,
)
df = pd.concat([df, new_row], ignore_index=True)

# Write the DF back to the storage bucket
storage_client = storage.Client()
blob = storage_client.get_bucket(bucket).blob(file)
blob.upload_from_string(df.to_csv(index=False), content_type="text/csv")
