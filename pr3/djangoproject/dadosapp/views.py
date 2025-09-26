from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import time
from google import genai
from google.genai import types
import pandas as pd

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import *

API_KEY=###################################

'''
@api_view(['POST'])
def process_prompt(request):
    prompt=request.data.get('prompt','')
    print(prompt)
    #Simulate AI processing (replace with AI model later)
    time.sleep(1)
    response = f"Recebi seu prompt: '{prompt}', Essa é uma reposta simulada"

    return Response({'response': response}, status=status.HTTP_200_OK)
'''

@api_view(['POST'])
def process_prompt(request):
    acidentes_list = pd.DataFrame(list(Acidente.objects.all().values()))
    especies_list = pd.DataFrame(list(Especie.objects.all().values()))
    pergunta=request.data.get('prompt','')
    prompt=f"""Por favor, levando em conta o banco de desse, na forma de planilhas, responda à pergunta em questão. Caso a pergunta não se refira a esse conjunto do dataframe, fale apenas que a pergunta não é referente ao dataframe.

        PLanilhas do Dataframe:
        {acidentes_list} e {especies_list}

        Pergunta:
        {pergunta}

        Por favor, retorne a análise em um formato estruturado e claro.
        """
    client = genai.Client(api_key=API_KEY)
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            config=types.GenerateContentConfig(
                system_instruction="Você é um analista de dados experiente."),
            contents=prompt
        )
        ai_response = response.text
        return Response({'response': ai_response}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def index(request):
    acidentes_list = Acidente.objects.all()
    especies_list = Especie.objects.all()
    context = {
        "acidentes_list": acidentes_list,
        "especies_list": especies_list
        }
    return render(request, "html/index.html", context)
