from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Customizar_usuario(AbstractUser):
    username = models.EmailField(unique=True)
    data_nascimento=models.CharField(max_length=10)
     # Adicione related_names únicos para evitar conflitos
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions')


class Cidade(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    class Meta:
        ordering = ['nome']
    def __str__(self):
        return self.nome

class Escola (models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, related_name='cidade')
    endereco = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10)
    imagem = models.ImageField(upload_to='imagens/')
    class Meta:
       ordering = ['nome']


class Materia(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, unique=True)
    
class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    nome=models.CharField(max_length=50)
    materias = models.ManyToManyField(Materia, related_name='professores')
    escolas = models.ManyToManyField(Escola, related_name='professores')
    cpf= models.CharField(max_length=20)


class Turma(models.Model):
    id = models.AutoField(primary_key=True)
    serie = models.CharField(max_length=4)
    qtd_alunos = models.IntegerField()
    escola = models.ForeignKey(Escola,on_delete=models.CASCADE,related_name='Turmas')
    Professores = models.ManyToManyField(Professor,related_name='professores')
    
class Aluno (models.Model):
    id= models.AutoField(primary_key=True)
    nome=models.CharField(max_length=50)
    falta=models.IntegerField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE,related_name='turma')