from django.db import models 
from django.core.validators import RegexValidator 
from django.core.exceptions import ValidationError  # lidar com erros de validação
from django.utils.text import slugify  # Importa a função para criar slugs (URLs amigáveis)
from random import randint  # gerar números aleatórios

class Funcionario(models.Model):  # Define um modelo chamado Funcionarios que herda de models.Model
    slug = models.SlugField(max_length=200, unique=True)  # Campo para armazenar um slug único.
    foto = models.ImageField(upload_to='foto/')  # Campo para armazenar uma imagem, que será enviada para a pasta 'foto/'
    nome = models.CharField(max_length=100)  # armazenar o nome do funcionário, com um máximo de 100 caracteres
    cpf = models.CharField(    
        max_length=14,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-d{2}$',
                message='ATENÇÃO: CPF Inválido.'
            )
        ] 
    )
    nascimento = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{2}/\d{2}/\d{4}$',
                message='ATENÇÃO: Data de Nascimento inválida!'
            )
        ]
    )
    
    def __str__(self):  # Método especial que define como o objeto é representado como string
        return self.nome  # Retorna o nome do funcionário quando o objeto é convertido em string
    
    def save(self, *args, **kwargs):  # Método sobrescrito para personalizar o comportamento de salvamento do modelo
        seq = self.nome + ' _FUNC' + str(randint(1000000, 9999999))  # Cria uma sequência única usando o nome e um número aleatório
        self.slug = slugify(seq)  # Gera um slug a partir da sequência criada
        super().save(*args, **kwargs)  # Chama o método save da classe pai para salvar o objeto no banco de dados

class ColetaFaces(models.Model): # coleta de faces
    funcionario = models.ForeignKey(Funcionario,
            on_delete=models.CASCADE, related_name='funcionarios_coletas')
    image = models.ImageField(upload_to='roi/')

class Treinamento(models.Model): # modelo de treinamento / armazenar o classificador
    modelo = models.FileField(upload_to='treinamento/')

    class Meta:
        verbose_name = 'Treinamento'
        verbose_name = 'Treinamentos'
    
    def __str__(self):
        return 'Classicador (frontalface)'

    def clean(self): # limita a um único arquivo
        model = self.__class__
        if model.objects.exclude(id=self.id).exists():
            raise ValidationError('ATENÇÃO: Só pode haver um arquivo salvo.')

# Importante: instalar pip install pillow  
# para posteriormente rodar o comando para criar as migrações (Funcionario - Treinamento - ColetaFaces): 
# python manage.py makemigrations  
# python manage.py migrate
        