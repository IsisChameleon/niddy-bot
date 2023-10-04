import streamlit as st
from dotenv import load_dotenv
import os

import pickle


def load_api_key():
    """
    Loads the OpenAI API key
    """
    user_api_key = st.sidebar.text_input(
        label="#### Your OpenAI API key 👇", placeholder="sk-...", type="password"
    )
    if user_api_key:
        st.sidebar.success("API key loaded from sidebar", icon="🚀")
        return user_api_key

    load_dotenv(override=True)
    return os.getenv("OPENAI_API_KEY")


def pickleSave(object, name, folder=".", silent=False):
    filename = folder + "/" + name + ".pkl"
    if silent == False:
        print("Saving object {} to pickle file {}".format(name, filename))
    with open(filename, mode="wb") as fipkl:
        pickle.dump(object, fipkl)


def pickleLoad(name, folder: str, silent=False):
    filename = folder + "/" + name + ".pkl"
    if silent == False:
        print("Loading object {} from pickle file {}".format(name, filename))

    try:
        with open(filename, mode="rb") as fipkl:
            myObject = pickle.load(fipkl)
        return myObject
    except IOError:
        print("Pickle file {} not found, returning None object".format(filename))
        return None
