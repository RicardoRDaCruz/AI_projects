import streamlit as st
import os
import io
import PyPDF2
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Projeto_1", layout="centered")

st.title("Suba um documento e tenha um resumo")
st.markdown("Faça o upload de um documento")

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

uploaded_file=st.file_uploader("Faça o upload de um documento (PDF ou TXT)", type=["pdf","txt"])

analisar=st.button("Analisar documento")

client=genai.Client(api_key=GEMINI_API_KEY)
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

def Analisar():
    file_content = extract_text_from_file(uploaded_file)
    if not file_content.strip():
        st.error("Arquivo sem conteúdo")
        st.stop()
    prompt=f"""Por favor, analise esse documento e retorne, em um único parágrafo, uma síntese de sua origem, objetivo e comprimento

    Documento:
    {file_content}
    Por favor, retorne a análise em um formato estruturado e claro.
    """
    #client=genai.Client(api_key=GEMINI_API_KEY)
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="Você é um analista experiente."),
        contents=prompt,
    )
    return response     

def Perguntar():
    file_content = extract_text_from_file(uploaded_file)
    prompt=f"""Por favor, levando em conta o documento enviado, responda à pergunta em questão, caso a pergunta não se refira ao documento, diga apenas 'Pergunta não referente ao documento'.

        Documento:
        {file_content}

        Pergunta:
        {pergunta}

        Por favor, retorne a análise em um formato estruturado e claro.
        """
    resposta=client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="Você é um analista experiente."),
            contents=prompt,
        )
    return resposta

if analisar and uploaded_file:
    try:
        st.markdown("### Resultados")
        analise=Analisar()
        st.markdown(analise.text)        
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

pergunta=st.text_input(label="Pergunte alguma coisa sobre o documento")
perguntar=st.button("Perguntar")

if perguntar and len(pergunta)>0:
    try:
        st.markdown("### Resposta")
        resposta=Perguntar()
        st.markdown(resposta.text)
        perguntar = False
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
