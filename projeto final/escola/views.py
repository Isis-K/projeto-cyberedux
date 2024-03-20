from django.shortcuts import render, redirect
from .models import Cidade , Escola, Turma, Professor, Materia,Aluno
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login,  logout
from django.contrib.auth.decorators import login_required

# Create your views here.

# TELA INICIAL
def Login(request):
   if request.method == 'GET':
        return render(request,'login.html')
   elif request.method =='POST':
       email = request.POST.get('email')
       senha = request.POST.get('senha')
       # ultiliza a autentificação 
       user = authenticate(request, username=email ,password=senha)

       if user is not None:
           login(request,user)
           return redirect('/')
       else:
            # Se a autenticação falhar, exiba uma mensagem de erro e redirecione de volta para a página de login
            messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.')
            return redirect('/login')
       
@login_required(login_url='/login')
def Sair (request):
    logout(request)
    return redirect('/login')



def Cadastro(request):
     if request.method == 'GET':
          return render(request,'cadastro.html')
     elif request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        data_nascimento = request.POST.get('data_nascimento')
        confirmar_senha = request.POST.get('confimarSenha')
        if senha != confirmar_senha :
            messages.error(request,'Senhas não compativeis')
            redirect('/cadastro')
        else:
            # Verificar se o nome de usuário já existe
            if get_user_model().objects.filter(username=email).exists():
                messages.error(request, 'Esse email já existe. Por favor, escolha outro.')
                return redirect('/cadastro')
             # Obtenha o modelo de usuário personalizado
            Customizar_usuario = get_user_model()
            user = Customizar_usuario.objects.create_user(username=email,email=email,password=senha)
            #usuario personalisado
            user.data_nascimento = data_nascimento
            user.save()
            login(request, user)
            return redirect('/')
        
  



#-------------------------------------------

# Views de escola

# cadastrar escola

def Cadastro_escola(request):
    cidades = Cidade.objects.all()
    if( request.method == 'GET'):
        return render(request,'cadastro/cadastro_escola.html',{'cidades':cidades})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        endereco = request.POST.get('endereco')
        cidade_id = request.POST.get('cidade')
        imagem =request.FILES.get('imagem')        
        # Verifica se a cidade já existe no banco de dados
        cidade= Cidade.objects.filter(id=cidade_id).first()
        if nome and cidade and tipo and endereco and imagem:
            nova_escola = Escola(nome = nome,tipo= tipo, endereco = endereco, cidade = cidade,imagem=imagem)
            nova_escola.save()
            messages.success(request,' Uma nova escola foi criada')
            return redirect('/cadastroEscola')
        else:
            messages.error(request,'Insira todos os dados')
            return redirect('/cadastroEscola')
             

# visualisar por parte de escola
@login_required(login_url='/login')
def Visualisar_escola(request):
    escolas = Escola.objects.all()
    cidades = Cidade.objects.all()
    #quantidade
    escolas_por_cidades={}
    #nome
    escolasCidades = {}
    # For para determinar a quantidade de escolas em uma cidade
    for cidade in cidades:
        quant_escola = Escola.objects.filter(cidade = cidade).count()
        escolas_por_cidades[cidade.nome] = quant_escola
    #For para determinar as escolas em uma cidade
    for cidade in cidades:
        escola_em_cidade = Escola.objects.filter(cidade=cidade)
        escolasCidades[cidade.nome]= escola_em_cidade

    
    return render(request,'escola/visualizar_escola.html',{'escolas':escolas,'escolas_por_cidades':escolas_por_cidades,'escolaCidade':escolasCidades})

def View_escola(request,id_escola):
      escola = Escola.objects.get(id=id_escola)
      professor = Professor.objects.filter(escolas__id=id_escola).count()
      turmas = Turma.objects.filter(escola = escola)
      # total de alunos
      totalAlunos = 0
      for turma in turmas:
         totalAlunos+= Aluno.objects.filter(turma=turma).count()
    # # alunos em cada turma
    #   alunos_por_turmas={}  
    #   for turma in turmas:
    #       alunos= Aluno.objects.filter(turma=turma).count()
    #       alunos_por_turmas[turma.serie]=alunos
   
      return render(request,'escola/view_escola.html',{'escola':escola,'professor':professor,'aluno':totalAlunos,})

def View_professor(request,id_escola):
    escola = Escola.objects.get(id=id_escola)
    if request.method == 'GET':
        professores = Professor.objects.filter(escolas=id_escola)
        return render(request,'escola/view_professor.html',{'escola':escola,'professores':professores})

# View feita para porder adicionar professor em uma escola

def View_professor_escola(request,id_escola):
    escola = Escola.objects.get(id=id_escola)
    if request.method=='GET':
        materias = Materia.objects.all()
        pesquisa = request.GET.get('materia')
        if pesquisa:
            resultado = Professor.objects.filter(materias__id=pesquisa)
            print("Resultado da pesquisa:", resultado) 
        else:
            resultado = Professor.objects.all()
        return render(request,'escola/view_escola_professor.html',{'escola':escola,'materias':materias,'resultado':resultado})
    
    elif request.method =='POST':
        professor_nome = request.POST.get('professor_id')
        professor = Professor.objects.get(id=professor_nome)
        
        if professor.escolas.filter(id=id_escola).exists():
             messages.error(request, 'Este professor já está cadastrado nesta escola.')
             return redirect('view_professor_escola', id_escola=id_escola)
        else:
            professor.escolas.add(escola)
            professor.save()
        return redirect(f'/{id_escola}/view_professor/')


# VIEWS DE TURMA


def Cadastro_turma(request,id_escola):
    escola = Escola.objects.get(id=id_escola)
    if request.method =='GET':
        return render(request,'cadastro/cadastrar_turma.html',{'escola':escola})
    elif request.method =='POST':
        nome = request.POST.get('nome')
        qtd_alunos = request.POST.get('qtd_alunos')
        if nome and qtd_alunos:
            nova_turma=Turma(serie=nome, qtd_alunos=qtd_alunos,escola=escola)
            nova_turma.save()
            messages.success(request,'Turma criada com sucesso')
            return redirect(f'/{id_escola}/view_turma/')



def View_turma(request,id_escola):
   escola = Escola.objects.get(id=id_escola)
   turmas = Turma.objects.filter(escola=id_escola)
   if request.method =='GET':
    return render(request,'escola/view_turma.html',{'escola':escola,'turmas':turmas})
   elif request.method =='POST':
     return redirect('view_turma_professor',id_escola=id_escola)

def View_turma_professor(request,id_escola,id_turma):
    escola = Escola.objects.get(id=id_escola)
    turma= Turma.objects.get(id=id_turma)
    if request.method =='GET':
        materias = Materia.objects.all()
        pesquisa = request.GET.get('materia')
        professor_escola = Professor.objects.filter(escolas=id_escola)
        if pesquisa:
            resultado = professor_escola.filter(materias__id=pesquisa) 
        else:
            resultado = professor_escola.all()
        return render(request,'escola/view_turma_professor.html',{'escola':escola,'materias':materias,'resultado':resultado})
    elif request.method =='POST':
        professor_id = request.POST.get('professor_id')
        professor = Professor.objects.get(id=professor_id)
        turma.Professores.add(professor)
        turma.save()
        return redirect('view_turma',id_escola=id_escola)

    

# VIEWS DE ALUNO :

def Cadastro_aluno(request,id_turma,id_escola):
    escola = Escola.objects.get(id=id_escola)
    turma = Turma.objects.get(id=id_turma)
    alunos = Aluno.objects.filter(turma = turma).count()
    if request.method=='GET':
        return render(request,'cadastro/cadastrar_aluno.html',{'turma':turma,'escola':escola})
    elif request.method =='POST':
        if turma.qtd_alunos == alunos:
            messages.error(request,'Essa turma já esta cheia')
            return redirect('cadastroAluno', id_turma=id_turma)
        else:
            nome = request.POST.get('nome')
            falta = request.POST.get('faltas')
            if nome and falta:
                aluno = Aluno(nome=nome,falta=falta,turma=turma)
                aluno.save()
                messages.success(request,'Este aluno foi cadastrado')
                return redirect('cadastroAluno', id_turma=id_turma ,id_escola=id_escola)
            else:
                messages.error(request,'Preencha todos os requisitos')
                return redirect('cadastroAluno', id_turma=id_turma,id_escola=id_escola)


def View_aluno(request,id_escola,id_turma):
    escola = Escola.objects.get(id=id_escola)
    turma =Turma.objects.get(id=id_turma)
    alunos =Aluno.objects.filter(turma_id=id_turma) 
    alunos_qtd= Aluno.objects.filter(turma=turma).count()
    return render(request,'aluno/aluno.html',{'escola':escola,'turma':turma,'alunos':alunos , 'quantidadeMaxima':alunos_qtd})



# VIEWS DE PROFESSOR


def Cadastro_professor(request):
    materias_view = Materia.objects.all()
    if request.method =='GET':
     return render (request,'cadastro/cadastrar_professor.html',{'materias':materias_view})
    elif request.method =='POST':
        nome = request.POST.get('nome')
        #nome_materia = request.POST.get('materia')
        #materia = Materia.objects.get(id=nome_materia)
        cpf = request.POST.get('cpf')
        if nome and cpf:
            novo_professor = Professor(nome=nome, cpf=cpf)
            novo_professor.save()
            
            messages.success(request,'Professor cadastrado com sucesso')
            return redirect('/cadastroProfessor/')

        else:
            messages.error(request,'Preencha todas as colunas!')
            return redirect('/cadastroProfessor/')


def Visualizar_professor(request):
    materias = Materia.objects.all()
    professores = Professor.objects.all()
    if request.method=='GET':
     return render(request,'professor/visualisar_professor.html',{'professores':professores,'materias':materias})

def visualizar_professor_modal(request, id_professor):
    professor = Professor.objects.get(pk=id_professor)
    materias = Materia.objects.all()   
    if request.method =='GET':    
        return render(request,'professor/modal.html',{'professor':professor,'materias':materias})
    elif request.method =='POST':
        materia_nome = request.POST.get('materia')
        materia = Materia.objects.get(id=materia_nome)
        # Adicionando a matéria ao conjunto de matérias do professor usando o método set()
        professor.materias.add(materia)
        professor.save()
        return redirect('/visualisar_professor/')

def Retirar_materia_professor(request,id_professor):
    professor = Professor.objects.get(id=id_professor)
    if request.method=='GET':
        return render(request,'Professor/retirar_materia_professor.html',{'professor':professor})
    
    elif request.method =='POST':
        materia_removida = request.POST.getlist('MateriaRemove')
        for materia in materia_removida:
            professor.materias.remove(materia)
        return redirect('/visualisar_professor/')

    

# Views de CIDADE

def Cadastro_cidade(request):
    if request.method == 'GET':
        return render (request,'cadastro/cadastrar_cidade.html')
    elif request.method =='POST':
        nome = request.POST.get('nome')

        # Se nome for diference de nulo ira criar a cidade
        if nome:
          cidade = Cidade(nome=nome)
          cidade.save()
          messages.success(request, 'Cidade criada com sucesso!')
          return redirect('/cadastro_cidade/')
    else:
        # Caso o nome não seja fornecido, você pode querer retornar um erro ou redirecionar de volta para o formulário
         messages.error(request, 'Nome da cidade não fornecido.')
         return redirect('/cadastro_cidade/')
    

def Visualizar_cidade(request):
    cidades = Cidade.objects.all()
    return render(request,'cidade/visualizar_cidade.html',{'cidades':cidades})

# VIEWS DE MATERIA :

def Cadastro_materia(request):
    if request.method == 'GET':
     return render(request,'cadastro/cadastrar_materia.html')
    
    elif request.method =='POST':
        nome = request.POST.get('nome')
        if nome:
            nova_materia = Materia(nome=nome)
            nova_materia.save()
            messages.success(request,'Matéria criada com sucesso!')
            return redirect('/visualisar_materia/')

def Visualizar_materia(request):
    materias = Materia.objects.all()
    return render(request,'materia/visualisar_materia.html',{'materias':materias})



#EDITAR

def Editar_escola(request,id_escola):
    escola = Escola.objects.get(id = id_escola)
    cidades = Cidade.objects.all()
    if request.method =='GET':
         return render(request, 'editar/editar_escola.html',{'escola':escola,'cidades':cidades})
    elif request.method =='POST':
        escola.nome = request.POST.get('nome')
        escola.endereco = request.POST.get('endereco')
        escola.tipo = request.POST.get('tipo')
        cidade_post = request.POST.get('cidade')
        cidade_edit = Cidade.objects.get(nome=cidade_post)
        escola.cidade = cidade_edit
        escola.save()
        return redirect('/')

def Editar_cidade(request,id_cidade):
    cidade = Cidade.objects.get(id = id_cidade)

    if request.method =='GET':
        return render(request,'editar/editar_cidade.html',{'cidade':cidade})
    
    elif request.method=='POST':
        cidade.nome = request.POST.get('nome')
        cidade.save()
        return redirect('visualizar_cidade')

def Editar_materia(request,id_materia):
    materia = Materia.objects.get(id=id_materia)
    
    if request.method =='GET':
        return render(request,'editar/editar_materia.html',{'materia':materia})
    
    elif request.method=='POST':
        materia.nome = request.POST.get('nome')
        materia.save()
        return redirect('visualizar_materia')

def Editar_turma(request,id_turma,id_escola):
    turma = Turma.objects.get(id=id_turma)
    
    if request.method =='GET':
        return render(request,'editar/editar_turma.html',{'turma':turma})
    elif request.method =='POST':
        turma.serie = request.POST.get('nome')
        turma.qtd_alunos = request.POST.get('qtd_alunos')
        turma.save()
        return redirect('view_turma', id_escola=id_escola)
    

def Editar_aluno(request,id_turma,id_escola,id_aluno): 
    aluno = Aluno.objects.get(id = id_aluno)
    if request.method == 'GET': 
        return render(request,'editar/editar_aluno.html',{'aluno':aluno})  
    elif request.method=='POST':
        aluno.nome = request.POST.get('nome')
        aluno.falta = request.POST.get('falta')
        aluno.save()
        return redirect('view_alunos',id_escola=id_escola , id_turma = id_turma )
        
        

# EXCLUIR

def Excluir_cidade(request,id):
    cidade = Cidade.objects.get(id=id)
    cidade.delete()
    return redirect('visualizar_cidade')

def Excluir_escola(request,id):

    escola = Escola.objects.get(id=id)
    escola.delete()
    return redirect('visualizar_escola')

def Excluir_materia(request,id):
    
    materia = Materia.objects.get(id=id)
    materia.delete()
    return redirect('visualizar_materia')

def Excluir_professor(request,id):
    professor = Professor.objects.get(id=id)
    professor.delete()
    return redirect('visualizar_professor')

def Excluir_turma(request,id, id_escola):
    turma = Turma.objects.get(id=id)
    turma.delete()
    return redirect('view_turma', id_escola = id_escola)

def Excluir_aluno(request,id_aluno,id_turma,id_escola):
    aluno = Aluno.objects.get(id=id_aluno)
    aluno.delete()
    return redirect('view_alunos', id_escola=id_escola, id_turma=id_turma)
    




def Retirar_professor_turma(request,id_turma,id_escola):
    turma = Turma.objects.get(id =id_turma)
    professor_da_turma = turma.Professores.all()
    if request.method=='GET':  
        return render(request,'turma/Retirar_professor_turma.html',{'professores':professor_da_turma,'turma':turma})
    elif request.method=='POST':
        professores_id = request.POST.getlist('professsores_id')
        for professor in professores_id:
            turma.Professores.remove(professor)
        turma.save()
        return redirect('view_turma' ,id_escola = id_escola)

#retirar professor de escola

def Escola_retirar_professor(request,id_escola,id_professor):
    escola = Escola.objects.get(id = id_escola)
    turmas = Turma.objects.filter(escola_id = id_escola)
    professor = Professor.objects.get(id=id_professor)
    professor.escolas.remove(escola)
    for turma in turmas:
        turma.Professores.remove(professor)
    return redirect('view_professor',id_escola=id_escola)

# retirar materia de professor


    
    
    