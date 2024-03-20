"""
URL configuration for projetoEscolar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from escola import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.Login,name='login'),
    path('cadastro/',views.Cadastro,name='cadastro'),
    path('sair/',views.Sair,name='sair'),
    
    path('cadastro_cidade/',views.Cadastro_cidade,name='cadastroCidade'),
    path('cadastroEscola',views.Cadastro_escola,name='cadastroEscola'),
    path('cadastroProfessor/',views.Cadastro_professor,name='cadastroProfessor'),
    path('<int:id_escola>/<int:id_turma>/cadastroAluno/',views.Cadastro_aluno,name='cadastroAluno'),
    path('cadastroMateria/',views.Cadastro_materia,name='cadastroMateria'),
    path('<int:id_escola>/cadastroTurma/',views.Cadastro_turma,name='cadastroTurma'),
    
    # Por parte de escola
    
    path('',views.Visualisar_escola,name='visualizar_escola'),
    path('<int:id_escola>/view_escola/',views.View_escola,name='view_escola'),
    path('<int:id_escola>/view_professor/',views.View_professor,name='view_professor'),
    path('<int:id_escola>/view_professor/view_professor_escola/',views.View_professor_escola,name='view_professor_escola'),
    path('<int:id_escola>/<int:id_professor>/retirar_professor/',views.Escola_retirar_professor,name='retirar_professor'),

    # Turma

    path('<int:id_escola>/view_turma/',views.View_turma,name='view_turma'),
    path('<int:id_escola>/view_turma/<int:id_turma>/view_turma_professor',views.View_turma_professor,name='view_turma_professor'),
    path('<int:id_escola>/view_aluno/',views.View_aluno,name='view_aluno'),
    path('<int:id_escola>/<int:id_turma>/retirar_professor_turma/',views.Retirar_professor_turma,name='RetirarProfessorTurma'),

    #Aluno

     path('<int:id_escola>/view_turma/<int:id_turma>/view_alunos',views.View_aluno,name='view_alunos'),
     
    # professor

    path('visualisar_professor/',views.Visualizar_professor,name='visualizar_professor'),
    path('visualisar_professor/<int:id_professor>/modal/',views.visualizar_professor_modal,name='visualizar_professor_model'),
    path('visualisar_professor/<int:id_professor>/Retirar_materia_professor/',views.Retirar_materia_professor,name='Retirar_materia_professor'),
    
    
    #Cidade
    
    path('visualisar_cidade/',views.Visualizar_cidade,name='visualizar_cidade'),

    #materia 

    path('visualisar_materia/',views.Visualizar_materia,name='visualizar_materia'),

    # delete
    path('delete_cidade/<int:id>',views.Excluir_cidade,name='excluirCidade'),
    path('delete_escola/<int:id>',views.Excluir_escola,name='excluirEscola'),
    path('delete_materia/<int:id>',views.Excluir_materia,name='excluirMateria'),
    path('delete_professor/<int:id>',views.Excluir_professor,name='excluirProfessor'),
    path('<int:id_escola>/delete_turma/<int:id>',views.Excluir_turma,name='excluirTurma'),
    path('<int:id_escola>/view_turma/<int:id_turma>/<int:id_aluno>/DeleteAluno',views.Excluir_aluno,name='DeleteAluno'),
    

    # editar

    path('<int:id_escola>/editar_escola/',views.Editar_escola,name='EditarEscola'),
    path('<int:id_cidade>/editar_cidade/',views.Editar_cidade,name='EditarCidade'),
    path('<int:id_materia>/editar_materia/',views.Editar_materia,name='EditarMateria'),
    path('<int:id_escola>/<int:id_turma>/editar_turma/',views.Editar_turma,name='EditarTurma'),
    path('<int:id_escola>/view_turma/<int:id_turma>/view_alunos/<int:id_aluno>/EditarAluno',views.Editar_aluno,name='editar_aluno'),
    


   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

