<table align="center"><tr><td align="center" width="9999">

<img src="https://cdn.bulbagarden.net/upload/thumb/0/0b/FireRed_LeafGreen_Bill.png/125px-FireRed_LeafGreen_Bill.png" align="center" width="150" alt="Project icon">

# Bill API

ABP Backend

<hr />

>![Generic badge](https://img.shields.io/badge/version-0.0.8-silver.svg)
[![Generic badge](https://img.shields.io/badge/docs-blue.svg)](https://github.com/brunolcarli/Bill/wiki)

Demo:
> [![Run on Repl.it](https://repl.it/badge/github/brunolcarli/Bill)](https://Bill-1.brunolcarli.repl.co/graphql/)



</td></tr></table>


# Rodando a API

Ref: Unix Systems (Linux, Mac)

## - Localmente

Em uma virtualenv instalar as dependências:

```
$ make install
```

Crie um arquivo `env` contendo as configurações de ambiente:

```
export DJANGO_SECRET_KEY=<sua_django_secret_key>
export DB_NAME=<seu_db_name>
export DB_USER=<seu_db_user>
export DB_PASS=<seu_db_password>
export DB_PORT=<sua_porta_padra_para_o_db>
```

Acione as variáveis de ambiente:

```
$ source env
```

Rode as migrações do banco de dados:

```
$ make migrate
```

Finalmente, rode a plataforma:

```
$ make run
```

A API estará rodando em `http://localhost:3122/graphql`

## - Docker

<table align="center"><tr><td align="center" width="9999">

<img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/9a69a317-6725-4dc9-b409-c84e21d9b78f/datq7t4-548d4c57-e5af-4c4d-8b99-d982bffde44d.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzlhNjlhMzE3LTY3MjUtNGRjOS1iNDA5LWM4NGUyMWQ5Yjc4ZlwvZGF0cTd0NC01NDhkNGM1Ny1lNWFmLTRjNGQtOGI5OS1kOTgyYmZmZGU0NGQuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.Eppxbm2hLjOE4mWxZVvxL20Qb8v_EtZnl38bXgvBsPU" align="center" width="150" alt="Project icon">


</td></tr></table>


Crie um arquivo `env/bill.env`:

```
$ mkdir env
$ touch env/bill.env
```

Insira e preencha neste arquivo as seguintes variáveis de ambiente:

```
DJANGO_SECRET_KEY=<your_secret_key>
DJANGO_SETTINGS_MODULE=bill.settings.docker

MYSQL_ROOT_PASSWORD=<your_database_root_password>
MYSQL_USER=<your_database_user>
MYSQL_DATABASE=<your_database_name>
MYSQL_PASSWORD=<your_database_password>
```

Instale o docker compose:

```
$ pip install docker-compose
```

Suba os containers com:

```
$ make container
```
