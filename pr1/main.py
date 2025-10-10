import streamlit as st
import io
import PyPDF2
import requests
import json

st.set_page_config(page_title="Projeto_1", layout="centered")
st.title("Suba um documento e tenha um resumo")
st.markdown("Faça o upload de um documento")
uploaded_file=st.file_uploader("Faça o upload de um documento (PDF ou TXT)", type=["pdf","txt"])
analisar=st.button("Analisar documento")

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

def llama_analise():
    file_content = extract_text_from_file(uploaded_file)
    url = "http://localhost:11434/api/generate"
    if not file_content.strip():
        st.error("Arquivo sem conteúdo")
        st.stop()
    prompt=f"""Por favor, analise esse documento e retorne, em um único parágrafo, uma síntese de sua origem, objetivo e comprimento

    Documento:
    {file_content}
    Por favor, retorne a análise em um formato estruturado e claro.
    """
    data = {
        "model": "llama3.2",
        "prompt": prompt,
    }
    response = requests.post(url, json=data, stream=True)
    resposta=""
    if response.status_code == 200:
        print("Generated text:", end=" ", flush=True)
        for line in response.iter_lines():
            if line:
                decoded_line=line.decode("utf-8")
                result=json.loads(decoded_line)
                generated_text=result.get("response", "")
                resposta+=generated_text
                print(generated_text, end="", flush=True)
    else:
        resposta="Error: "+response.status_code+" "+response.text
        print("Error:", response.status_code, response.text)
    return resposta

def llama_pergunta():
    file_content = extract_text_from_file(uploaded_file)
    url = "http://localhost:11434/api/generate"
    prompt=f"""Por favor, levando em conta o documento enviado, responda à pergunta em questão, caso a pergunta não se refira ao documento, diga apenas 'Pergunta não referente ao documento'.

        Documento:
        {file_content}

        Pergunta:
        {pergunta}

        Por favor, retorne a análise em um formato estruturado e claro.
        """
    data = {
        "model": "llama3.2",
        "prompt": prompt,
    }
    response = requests.post(url, json=data, stream=True)
    resposta=""
    if response.status_code == 200:
        print("Generated text:", end=" ", flush=True)
        for line in response.iter_lines():
            if line:
                decoded_line=line.decode("utf-8")
                result=json.loads(decoded_line)
                generated_text=result.get("response", "")
                resposta+=generated_text
                print(generated_text, end="", flush=True)
    else:
        resposta="Error: "+response.status_code+" "+response.text
        print("Error:", response.status_code, response.text)
    return resposta

if analisar and uploaded_file:
    try:
        st.markdown("### Resultados")
        analise=llama_analise()
        st.markdown(analise)           
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

pergunta=st.text_input(label="Pergunte alguma coisa sobre o documento")
perguntar=st.button("Perguntar")

if perguntar and len(pergunta)>0:
    try:
        st.markdown("### Resposta")
        resposta=llama_pergunta()
        st.markdown(resposta)
        perguntar = False
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
