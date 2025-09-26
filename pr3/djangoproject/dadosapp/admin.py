from django.contrib import admin
from .models import *

class EspecieAdmin(admin.ModelAdmin):
    list_display = ["especie_nome", "pais_mais_comum", "letal"]
    

admin.site.register(Especie, EspecieAdmin)

class AcidenteAdmin(admin.ModelAdmin):
    list_display = ["nome_acidentado", "pais_de_ocorrencia", "especie_que_mordeu","data_ocorrencia","sobreviveu"]
    

admin.site.register(Acidente, AcidenteAdmin)
# Register your models here.
