import pandas as pd
import streamlit as st


@st.cache_data(ttl=3600)
def get_df():
    # Bust GCP's Cache, use Streamlit's cache
    cache_bust = pd.Timestamp.now().toordinal()
    df = pd.read_csv(
        f"https://storage.googleapis.com/openai-ass-api-public/api_response_times.csv?x={cache_bust}",
        index_col="Timestamp",
        parse_dates=["Timestamp"],
    )

    # Add mock data
    # from random import uniform
    #
    # for i in range(24 * 20):
    #     timestamp = pd.Timestamp.utcnow().tz_convert(None) - pd.Timedelta(hours=i)
    #     df.loc[timestamp, "ResponseTime"] = uniform(2, 2.5)
    return df


df = get_df()


st.title("OpenAI Assistant API Response Times")

st.header("Past day, hourly")
hourly_df = df.resample("h").min().tail(24)  # past week
# TODO (@davidgilbertson): smarter x axis labels.
st.line_chart(
    data=hourly_df,
    x=None,
    y="ResponseTime",
    y_label="Response Time (s)",
    x_label="Time",
)

st.header("Past year, daily")
daily_df = df.resample("D").min().tail(365)  # past year
st.line_chart(
    data=daily_df,
    x=None,
    y="ResponseTime",
    y_label="Response Time (s)",
    x_label="Time",
)
