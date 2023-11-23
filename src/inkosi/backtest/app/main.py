import random
import string

import matplotlib.pyplot as plt

# import numpy as np
import pandas as pd
import streamlit as st

from inkosi.utils.utils import EnhancedStrEnum


# from inkosi.database.postgresql.database import PostgreSQLCrud
class DataSourceType(EnhancedStrEnum):
    FILE: str = "File"
    URL: str = "URL"


if "count" not in st.session_state:
    st.session_state.count = 0


@st.cache_data
def load_data():
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, parse_dates=True, index_col="date")
        return data
    return None


def add_new_row():
    st.sidebar.text_input(
        "Combination",
        key=random.choice(string.ascii_uppercase) + str(random.randint(0, 999999)),
    )


st.title("Trading Strategy Backtest")
token = st.experimental_get_query_params().get("token", [])

if not len(token):
    st.error("No token authentication has been provided", icon="🚨")
else:
    # postgresql = PostgreSQLCrud()
    # if not postgresql.valid_backtesting_token(token):
    if token[0] != "ciao":
        st.error("Unable to authenticate through the token provided", icon="🚨")

    else:
        st.markdown(
            """
            It is important to recognize
            ...
            """
        )

        st.sidebar.header("Settings")

        source_type = st.sidebar.selectbox(
            "Select the Data Source Type",
            options=DataSourceType.list(),
        )
        uploaded_file = st.sidebar.file_uploader(
            "Upload your input CSV file", type=["csv"]
        )
        start_date = st.sidebar.date_input("Start Date")
        end_date = st.sidebar.date_input("End Date", max_value=None)

        short_window = st.sidebar.slider("Short Window", 5, 50, 20)
        long_window = st.sidebar.slider("Long Window", 51, 200, 100)

        if st.sidebar.button("Backtest"):
            st.session_state.count += 1
            add_new_row()
            if st.session_state.count > 1:
                for i in range(st.session_state.count - 1):
                    add_new_row()

        data = load_data()

        if data is not None:
            data = data[start_date:end_date]

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(data.index, data["close"], label="Price")

            ax.set(title="Backtest Result", ylabel="Price")
            ax.legend()

            st.pyplot(fig)

        else:
            st.write("Please upload a CSV file with columns 'date' and 'close'.")

        # st.dataframe(data)
