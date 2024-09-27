# API de Ordem de produção

Este é um projeto de um webservice para uma empresa de petiscos para cães e MVP para o curso de **Desenvolvimento Full Stack Básico** da PUC-RIO.

---

## Objetivo

O objetivo desse projeto é organizar um fluxo de produção interno da empresa facilitando a transformação de pedidos separados em ordens de produção
únicas. 

Com isso, o trabalho ficará organizado de uma forma mais abstrata e de fácil compreensão para funcionários da produção compreenderem.

As funcionalidades são de gerar uma ordem de produção com base em várias notas de pedido contendo diversos produtos, esses produtos são adicionados a lista
de forma separada e ao final, quando a ordem for gerada, são unificados para que haja apenas o total.

Há a possibilidade de consultar todas as ordens de produção já geradas e deletar caso necessário.

Por fim, é possível anexar uma observação a uma ordem de produção caso haja necessidade de registro de informações adicionais e a deleção dessas.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5003
```
Caso não tenha um ambiente virtual, pode ser executado diretamente utilizando o comando abaixo pelo terminal na pasta raiz: 

```
$ python app.py
```

Abra o [http://localhost:5003/#/](http://localhost:5003/#/) no navegador para verificar o status da API em execução.


### Como executar (Docker)

Basta realizar o comando docker build -t ordens-app .
Em seguida: docker run -p 5003:5003 ordens-app