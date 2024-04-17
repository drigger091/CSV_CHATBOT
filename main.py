
import streamlit as st

def main():
    st.title("Simple Greeting App")
    st.write("Enter your name:")

    name = st.text_input("Name")

    if st.button("Greet"):
        if name:
            st.write(f"Hello, {name}!")
        else:
            st.write("Please enter your name.")

if __name__ == "__main__":
    main()
