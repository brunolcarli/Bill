<table align="center"><tr><td align="center" width="9999">

<img src="https://cdn.bulbagarden.net/upload/thumb/0/0b/FireRed_LeafGreen_Bill.png/125px-FireRed_LeafGreen_Bill.png" align="center" width="150" alt="Project icon">

# Bill API

ABP Backend

<hr />

>![Generic badge](https://img.shields.io/badge/version-0.0.6-silver.svg)
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

`Em desenvolvimento`
