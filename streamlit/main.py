import pandas as pd
import streamlit as st


# Cache, mostly just for development. The CSV in GCP has a cache of 1 hour.
@st.cache_data(ttl=3600)
def get_df():
    df = pd.read_csv(
        "https://storage.googleapis.com/openai-ass-api-public/api_response_times.csv",
        index_col="Timestamp",
        parse_dates=["Timestamp"],
    )

    # Add mock old data
    # from random import uniform
    #
    # min_date = df.index.min()
    # for i in range(1, 24 * 20):
    #     timestamp = min_date - pd.Timedelta(hours=i)
    #     df.loc[timestamp, "ResponseTime"] = uniform(1.8, 2.2)
    # df = df.sort_index()
    return df


df = get_df()


st.title("OpenAI Assistant API Response Times")
st.header("Past week, hourly")
hourly_df = df.resample("h").min().tail(24 * 7)  # past week
st.line_chart(
    data=hourly_df,
    x=None,
    y="ResponseTime",
    y_label="Response Time (s)",
    x_label="Time",
)

# st.header("Past year, daily")
# daily_df = df.resample("D").min().tail(365)  # past year
# st.line_chart(
#     data=daily_df,
#     x=None,
#     y="ResponseTime",
#     y_label="Response Time (s)",
#     x_label="Time",
# )

st.write(
    "Response times are for the simplest possible call to the Assistants API using `gpt-4o-mini`."
)
with st.expander("Show the code"):
    st.code(
        """\
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
    """
    )
