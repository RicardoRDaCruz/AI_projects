from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import time
from google import genai
from google.genai import types
import pandas as pd
import folium
import json 
import io
from PIL import Image

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import TemplateView
from .models import *

API_KEY=############################################

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
    # Make the map
    map = folium.Map(
        location = [-25.40, -40.78],
        zoom_start = 7,
        tiles = 'OpenStreetMap')
    
    for acidente in acidentes_list:
        coordenadas=(acidente.latitude,acidente.longitude)
        folium.Marker(coordenadas).add_to(map)

    context = {
        "acidentes_list": acidentes_list,
        "especies_list": especies_list,
        "map": map._repr_html_(),
        }
    return render(request, "index.html", context)

def mapa_prompt(request):
    if request.method == 'POST':
        try:
            acidentes_list = Acidente.objects.all()
            acidentes_pd=pd.DataFrame(list(acidentes_list.values()))
            exemplo_pontos=[[-20,-40],[-22,45],[-15,-48]]
            vazio=[[]]
            # Parse the JSON data from the request body
            data = json.loads(request.body)            
            # Access the data
            texto = data.get('texto')
            prompt=f"""Por favor, levando em conta o banco de acidentes de mordidas de cobra presente nesse sistema, na forma de dataframe, você deve observar o COMANDO presende no texto a seguir. Caso o COMMANDO contenha a primeira palavra como
            'Marque', você deve aplicar um filtro na planilha de acidentes, caso seja necessário, e retornar apenas um objeto do tupi 'array' contento as coordenadas dos pontos aos quais o COMANDO está se referindo. O formato do retorno deve ser da seguinte forma:
            '[[latitude_ponto_1,longitude_ponto_1],[latitude_ponto_2,longitude_ponto_2],...,[latitude_ponto_n,longitude_ponto_n]]', da mesma forma que o 'array' {exemplo_pontos}. Caso o COMMANDO não contenha a primeira palavra 'Marque', apenas retorne o 'array' {vazio}
            COMANDO:
            {texto}
            Dataframe de acidentes de cobra:
            {acidentes_pd}
            
            Por favor, retorne apenas o 'array' na saída da resposta, poupando as explicações e elementos de diálogo e de apresentação de código.
            """ 
            client = genai.Client(api_key=API_KEY)
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    
                    contents=prompt
                )
                ai_response = {'pontos': response.text.split('\n')[1]}  
                print(response.text.split('\n')[1])
                pontos=eval(response.text.split('\n')[1])
                map = folium.Map(
                location = [0, 0],
                zoom_start = 1,
                tiles = 'OpenStreetMap')
                for ponto in pontos:
                    coordenadas=(ponto[0],ponto[1])
                    folium.Marker(coordenadas).add_to(map)
                img_data = map._to_png(5)
                img = Image.open(io.BytesIO(img_data))
                img.save('image.png')

                return JsonResponse({'response': ai_response}, status=status.HTTP_200_OK)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                     
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
