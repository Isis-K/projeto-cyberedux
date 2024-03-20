# Documentação

Aqui, você deve elaborar um "guia" para desenvolvedores que queiram contribuir livremente com seu projeto. Estruture este documento como achar melhor. Embora já hajam algumas seções pré-definidas, elas são apenas sugestões de qual estrutura seguir e o que escrever.

Pastas:
    * Cadastro: Cadastro das tabelas
    * Editar: Editar as tabelas
    * Pastas com os nomes das tabelas: Esta dentro os templates relacionados a tabela, com uma pequena execeção de escola.Já que nessa página existe subpaginas que são direcionadas por meio de links



**Não seja prolixo. Escreva de forma rápida, objetiva e sem informações óbvias.**

## Instruções de deploy

Faça uma pequena pesquisa sobre como fazer o [*deploy*](https://en.wikipedia.org/wiki/Software_deployment) de um projeto web com Python e Django e escreva aqui algumas orientações breves.  Fazer o *deploy* não é obrigatório para a avaliação, mas é importante que os desenvolvedores do projeto tenham ao menos uma noção de como isso é feito.

Sugestões de serviços de hospedagem para pesquisar:
* Vercell
* PythonAnywhere
* AWS Elastic Beanstalk (não recomendamos o uso deste serviço sem supervisão, pois pode gerar cobranças inesperadas)

## Modelagem de banco de dados

Coloque aqui a modelagem do banco de dados desenvolvido no projeto. Você pode colocar diagramas conceituais e lógicos, ou até mesmo descrever textualmente o que cada uma das tabelas e atributos representam. 

CREATE TABLE Cidade (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL
);

CREATE TABLE Escola (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT,
  cidade_id INTEGER,
  endereco TEXT,
  tipo TEXT,
  imagem TEXT,
  FOREIGN KEY (cidade_id) REFERENCES Cidade(id)
);

CREATE TABLE Materia (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT
);

CREATE TABLE Professor (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT,
  materia_id INTEGER,
  escola_id INTEGER,
  cpf TEXT,
  FOREIGN KEY (materia_id) REFERENCES Materia(id),
  FOREIGN KEY (escola_id) REFERENCES Escola(id)
);

CREATE TABLE Turma (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  serie TEXT,
  qtd_alunos INTEGER,
  escola_id INTEGER,
  professor_id INTEGER,
  FOREIGN KEY (escola_id) REFERENCES Escola(id),
  FOREIGN KEY (professor_id) REFERENCES Professor(id)
);

CREATE TABLE Aluno (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT,
  falta INTEGER,
  turma_id INTEGER,
  FOREIGN KEY (turma_id) REFERENCES Turma(id)
);
