import streamlit as st
import os
import pandas as pd
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Projeto_2", layout="centered")

st.title("Obtenha informações de um dataframe")
st.markdown("Nessa página, o dataframe de link https://www.kaggle.com/datasets/zadafiyabhrami/global-crocodile-species-dataset pode ser analisado pela IA")

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

df=pd.read_csv("./crocodile_dataset.csv")

def Perguntar(dataframe, questao):    
    prompt=f"""Por favor, levando em conta o banco de dados enviado a esse sistema, na forma de planilha responda à pergunta em questão, caso a pergunta não se refira ao dataframe, fale apenas que a pergunta não é referente ao dataframe.

        Dataframe:
        {dataframe}

        Pergunta:
        {questao}

        Por favor, retorne a análise em um formato estruturado e claro.
        """
    resposta=client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="Você é um analista de dados experiente."),
            contents=prompt,
        )
    return resposta

client = genai.Client()

pergunta=st.text_input(label="Pergunte alguma coisa sobre o documento")
perguntar=st.button("Perguntar")

if perguntar and len(pergunta)>0:
    try:
        st.markdown("### Resposta")
        resposta=Perguntar(df, pergunta)
        st.markdown(resposta.text)
        perguntar = False
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")