from django.contrib import admin
from registro.models import (
    Funcionario, ColetaFaces, Treinamento)

class ColetaFacesInline(admin.StackedInline):
    model = ColetaFaces
    extra = 0

class FuncionarioAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']
    inlines = (ColetaFacesInline,)
 
admin.site.register(Funcionario, FuncionarioAdmin)

admin.site.register(Treinamento)

# Customização do título da janela e do cabeçalho

admin.site.site_header = 'Administração do Reconhecimento Facial'
admin.site.site_title = 'Login - Administrativo'
admin.site.index_title = 'Painel do Controle de Ponto'

# admin.site.register(Funcionario)
# admin.site.register(ColetaFaces)



# ver o resultado: python manage.py runserver
# criar usuário: python manage.pycreatesuperuser = titoapaiva - email:t_a_paiva@proton.me - 
# senha: 1234

# acessar no navegador e fazer login: http://127.0.0.1:8000/admin/
