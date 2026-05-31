# Apresentação



## Desafio: API Bancária Assíncrona com FastAPI

Neste desafio, foi projetada e implementada uma API RESTful assíncrona para gerenciar operações bancárias de depósitos e saques, vinculadas a contas correntes. Este desafio proporcionou a experiência de construir uma aplicação backend moderna e eficiente utilizando autenticação JWT e práticas recomendadas de design de APIs.



## Objetivos e Funcionalidades

O objetivo deste desafio é desenvolver uma API com as seguintes funcionalidades:

- **Cadastro de transações:** Permite o cadastro de transações bancárias, como depósitos e saques.
- **Exibição de extrato:** Foi implementado um endpoint para exibir o extrato de uma conta, mostrando todas as transações realizadas.
- **Autenticação com JWT:** Foi utilizado JWT (JSON Web Tokens) para garantir que apenas usuários autenticados possam acessar os endpoints que exigem autenticação.

## Requisitos técnicos

Foram atendidos os seguintes requisitos técnicos:

- **FastAPI:** Foi utilizado o framework FastAPI, aproveitando os seus recursos assíncronos para lidar com operações de I/O de forma eficiente.
- **Modelagem de dados:** foram criados modelos de dados adequados para representar contas correntes e transações, garantindo que as transações estejam relacionadas a uma conta corrente, e que contas possam ter múltiplas transações.
- **Validação de operações:** não são permitidos depósitos e saques com valores não positivos. O usuário deve ter saldo para realizar um saque (sem cheque especial).
- **Segurança:** foi implementada segurança usando JWT para proteger os endpoints que necessitam de acesso autenticado.
- **Documentação com OpenAPU:** a API foi documentada incluindo descrições adequadas para cada endpoint, parâmetros e modelos de dados.

# Requerimentos

O projeto e suas dependências foram criados usando o Poetry, mais adequado para gerenciar projetos comerciais. Requer python 3.12+.

# Instruções

Para acessar a documentação automaticamente gerada pelo Swagger, enquanto o servidor estiver rodando, vá para:

http://localhost:8000/docs#/

Foi usado o VSCode no Windows para desenvolvimento. O teste da API foi feito usando o Insomnia.

1) **Clonar o repositório**:

```bash
git clone https://github.com/ntorresamendola/dio-luizalabs-back-end-com-python-fastapi
```

2) **Instalar o Poetry**

O Poetry é instalado usando pipx, cuja instalação depende do sistema operaciona

[Instalação pipx](https://pipx.pypa.io/stable/how-to/install-pipx/)

No Windows a instalação pode ser feita via pip:

```bash
# If you installed python using Microsoft Store, replace `py` with `python3` in the next line.
py -m pip install --user pipx
```



O que provavelmente gerará um WARNING:

```bash
WARNING: The script pipx.exe is installed in `<USER folder>\AppData\Roaming\Python\Python3x\Scripts` which is not on PATH
```



Vá para o diretório mencionado: 

```bash
cd <USER folder>\AppData\Roaming\Python\Python3x\Scripts
```

E execute o comando que irá adicionar tanto a pasta Scripts quanto o %USERPROFILE%\.local\bin ao path:

```bash
.\pipx.exe ensurepath
```



3 - **Configurar o Poetry e as dependências**

Volte para o diretório onde o repositório clonado foi baixado e execute o comando:



```bash
poetry init
```



Isso chamará um assistente que irá criar o arquivo de configuração pyproject.toml para você.

Foram usados os parâmetros:

```
Package name: dio-banco
Version: 0.1.0
Description: A basic asyncronous bank API using FastAPI 
Author: <valor padrão>
License: Apache 2.0
Compatilhe Python versions: >= 3.12
Define your main dependencies interactively? no
Define your development dependencies interactively? no
```



É criado um arquivo chamado pyproject.toml



### Configurando as dependências (cria um ambiente virtual):

A última versão do fastapi e suas dependências:

```powershell
poetry add "fastapi=*"
```

Execute o comando abaixo e copie o caminho(Path)  do Virtualenv:

```powershell
poetry env info
```

Coloque esse caminho como interpretador(interpreter path) do Python(CTRL + SHIFT + P).

Abra um novo terminal para a virtual env ser selecionada.

Para adicionar o uvicorn(servidor que rodará a aplicação localmente):

```powershell
poetry add "uvicorn[standard]"
```

Instalando as outras dependências:

```powershell
poetry add "sqlalchemy"
```

```powershell
poetry add "databases"
```

```powershell
poetry add "pydantic_settings"
```

```powershell
poetry add "PyJWT[crypto]"
```

```bash
poetry add "aiosqlite"
```

````bash
poetry add "alembic=*"
````



### Configurando o alembic do zero(pasta alembic)

````bash
alembic init alembic
````

Atualize o arquivo alembic/env.py antes de rodar o seguinte comando (migração inicial):

````bash
alembic revision --autogenerate -m "Add initial tables"
````

Atualiza o banco de dados

````bash
alembic upgrade head
````



Autenticação: auth->Bearer Token. Prefixo: Bearer. É devolvido pelo endpoint público de login.

Rodando a aplicação:



```bash
uvicorn src.main:app --reload
```



## Documentação da API (gerada pelo Swagger)



![image-20260530220214460](C:\Users\natan\Desktop\dio\backend com python\4-fast-api\apis-assincronas\API-BANCARIA-ASSINCRONA\images\1-API.png)

## Como obter uma autorização via Insomnia

Usando o endpoint público login

![2-login](C:\Users\natan\Desktop\dio\backend com python\4-fast-api\apis-assincronas\API-BANCARIA-ASSINCRONA\images\2-login.png)



## Exemplo de uso com autenticação

![image-20260530221444701](C:\Users\natan\Desktop\dio\backend com python\4-fast-api\apis-assincronas\API-BANCARIA-ASSINCRONA\images\3-create_account.png)

# Melhorias possíveis:

* Criar uma tabela só para usuários.
* Adicionar mais informações de usuário além do id.

* Contas só podem ser criadas para usuários que já possuem id (do jeito que está o usuário passado como parâmetro é criado se não existe).
* Filtrar contas por id de usuário.

* Criar uma tabela com usuários e senhas criptografadas. O login irá verificar o usuário e a senha.
* Criar uma tabela de log que registra quando e quem fez login ou realizou alguma operação.
* Garantir que o usuário logado só possa criar contas em seu nome.
* Garantir que o usuário logado só possa efetuar saques em seu nome.
* Porém permitir que efetue depósito em qualquer conta.
* Filtrar o extrato por tipo de operação (saque, depósito).
* Cobrar uma taxa a partir do terceiro saque da conta. O saldo deve cobrir tanto o valor do saque da conta quanto a taxa.
* Permitir transferência entre contas (o usuário logado poderá transferir diretamente seu saldo para uma outra conta que exista).
* Permitir que uma conta seja fechada. Contas fechadas não efetuam depósitos nem saques. 
* Obrigar que os depósitos e saques sejam necessariamente valores monetários válidos, com até duas casas decimais. Como está a API arredonda valores com mais de duas casas decimais.

