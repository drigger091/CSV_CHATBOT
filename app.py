from langchain_openai import OpenAI
from langchain_experimental.agents import create_csv_agent
import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv


def main():
    load_dotenv()

    # Load the OpenAI API key from the environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None or openai_api_key == "":
        st.error("OPENAI_API_KEY is not set")
        st.stop()

    st.set_page_config(page_title="Ask Dipayan about your csv ")
    st.title("Ask your chatbot ")

    # Upload the CSV files
    holdings_csv_file = st.file_uploader("Upload the holdings file", type="csv")
    trading_csv_file = st.file_uploader("Upload the trading file", type="csv")

    if holdings_csv_file is not None and trading_csv_file is not None:

        # Read the contents of the uploaded CSV files
        holdings_df = pd.read_csv(holdings_csv_file)
        trading_df = pd.read_csv(trading_csv_file)

        # Concatenate the DataFrames
        combined_df = pd.concat([holdings_df, trading_df], ignore_index=True)

        # convert DataFrame to CSV string
        csv_string = combined_df.to_csv(index=False)

        cleaned_csv_string = csv_string.replace('\n', '')

        # Create the agent
        agent = create_csv_agent(OpenAI(temperature=0), cleaned_csv_string, verbose=True)

        # Get user question
        user_question = st.text_input("Ask your question")

        if user_question:
            with st.spinner("Bot is thinking..."):
                response = agent.run(user_question)

            if response.strip() == "":
                st.write("I don't know")
            else:
                st.write(response)


if __name__ == "__main__":
    main()
