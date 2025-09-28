from django.db import models


class Especie(models.Model):
    especie_nome = models.CharField(max_length=200)
    pais_mais_comum=models.CharField(max_length=200)
    data_descobrimento = models.DateTimeField("data descobrimento")
    letal=models.BooleanField()

    def __str__(self):
        return self.especie_nome



class Acidente(models.Model):
    nome_acidentado=models.CharField(max_length=200)
    pais_de_ocorrencia=models.CharField(max_length=200)
    especie_que_mordeu = models.ForeignKey(Especie, on_delete=models.CASCADE)
    data_ocorrencia = models.DateTimeField("data ocorrência")
    sobreviveu = models.BooleanField()
    longitude=models.FloatField(blank=True)
    latitude=models.FloatField(blank=True)

    def __str__(self):
        return self.nome_acidentado

# Create your models here.
