# APS 2 - Eventos acadêmicos

API em Python e FastAPI para cadastrar eventos e participantes e realizar inscrições.
Os dados ficam em listas na memória e são apagados quando o servidor reinicia.
Não utiliza banco de dados nem exige uma página HTML: as operações podem ser feitas pelo Swagger.

## Organização

- `main.py`: cria a aplicação e registra as rotas.
- `controller/`: recebe requisições e devolve respostas e códigos HTTP.
- `model/`: define os campos e a validação com Pydantic.
- `service/sistema_service.py`: guarda os dados e aplica as regras de negócio.

A organização segue a adaptação de MVC sugerida no enunciado. As respostas JSON fazem o papel de apresentação dos dados. O serviço reúne eventos, participantes e inscrições para manter as regras relacionadas no mesmo lugar.

## Instalação e execução

No terminal, dentro da pasta que contém `main.py` e `requirements.txt`, execute:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn main:app --reload
```

As versões do `requirements.txt` foram extraídas dos arquivos das aulas.
Abra http://127.0.0.1:8000/docs para usar o Swagger.
Em cada operação, clique em **Try it out**, preencha os campos e clique em **Execute**.

## Rotas

| Método | Rota | Função | Sucesso |
| --- | --- | --- | --- |
| POST | `/eventos` | Cadastrar evento | 201 |
| GET | `/eventos` | Listar eventos | 200 |
| GET | `/eventos/{evento_id}` | Consultar evento | 200 |
| PUT | `/eventos/{evento_id}` | Atualizar todos os dados do evento | 200 |
| DELETE | `/eventos/{evento_id}` | Excluir evento e suas inscrições | 204 |
| POST | `/participantes` | Cadastrar participante | 201 |
| GET | `/participantes` | Listar participantes | 200 |
| GET | `/participantes/{participante_id}` | Consultar participante | 200 |
| PUT | `/participantes/{participante_id}` | Atualizar todos os dados do participante | 200 |
| DELETE | `/participantes/{participante_id}` | Excluir participante e suas inscrições | 204 |
| POST | `/eventos/{evento_id}/inscricoes/{participante_id}` | Inscrever participante | 201 |
| GET | `/eventos/{evento_id}/inscricoes` | Listar os participantes inscritos | 200 |

Os IDs são gerados automaticamente e não precisam ser enviados no cadastro.
O PUT recebe os mesmos campos obrigatórios do POST. O DELETE retorna uma resposta sem corpo.

## Exemplos para o Swagger

### 1. Cadastrar um evento

Envie em `POST /eventos`:

```json
{
  "titulo": "Introdução ao FastAPI",
  "descricao": "Palestra sobre criação de APIs com Python.",
  "data": "2026-10-20",
  "horario": "19:00:00",
  "local": "Auditório",
  "capacidade": 1,
  "categoria": "Palestra"
}
```

Em uma execução nova, a resposta será `201`:

```json
{
  "id": 1,
  "titulo": "Introdução ao FastAPI",
  "descricao": "Palestra sobre criação de APIs com Python.",
  "data": "2026-10-20",
  "horario": "19:00:00",
  "local": "Auditório",
  "capacidade": 1,
  "categoria": "Palestra"
}
```

### 2. Cadastrar um participante

Envie em `POST /participantes`:

```json
{
  "nome": "Lucas",
  "email": "lucas@example.com",
  "curso": "Sistemas de Informação"
}
```

O e-mail e o curso acima são dados fictícios para teste. A resposta será `201`:

```json
{
  "id": 1,
  "nome": "Lucas",
  "email": "lucas@example.com",
  "curso": "Sistemas de Informação"
}
```

### 3. Inscrever e consultar

Execute `POST /eventos/1/inscricoes/1`, sem corpo JSON. Resposta `201`:

```json
{"evento_id": 1, "participante_id": 1}
```

Execute `GET /eventos/1/inscricoes`. Resposta `200`:

```json
[
  {"id": 1, "nome": "Lucas", "email": "lucas@example.com", "curso": "Sistemas de Informação"}
]
```

### 4. Atualizar e excluir

Use `PUT /eventos/1` com o JSON completo do cadastro, trocando `local` para `Sala 2`.
Confirme a alteração com `GET /eventos/1`.
Use `PUT /participantes/1` com nome, e-mail e curso, trocando o nome para `Lucas Silva`.
Confirme a alteração em `GET /participantes/1` e na lista de inscritos.

Execute `DELETE /participantes/1` e depois `DELETE /eventos/1`.
As duas exclusões retornam `204`, sem JSON. Consultar os IDs excluídos retorna `404`.

## Regras e cenários de erro

Teste os erros antes de excluir os registros:

| Situação | Resultado esperado |
| --- | --- |
| Consultar, atualizar ou excluir ID inexistente | 404 |
| Inscrever em evento ou com participante inexistente | 404 |
| Repetir a inscrição do mesmo participante | 400 |
| Cadastrar outro participante e tentar inscrevê-lo no evento já lotado | 400 |
| Diminuir a capacidade para menos que o número de inscritos | 400 |
| Título ou nome contendo apenas espaços | 400 |
| Omitir campo obrigatório | 422 |
| Título ou nome vazio | 422 |
| E-mail sem formato válido | 422 |
| Data impossível, como `2026-02-30` | 422 |
| Horário inválido, como `25:00:00` | 422 |
| Capacidade zero ou negativa | 422 |

Exemplos de respostas:

```json
{"detail": "Evento não encontrado."}
```

```json
{"detail": "Participante já está inscrito neste evento."}
```

```json
{"detail": "Não existem vagas disponíveis para este evento."}
```

Excluir um participante remove suas inscrições e libera vagas. Excluir um evento remove suas inscrições, mas mantém os participantes cadastrados. As categorias do enunciado são exemplos, portanto o campo aceita texto.

## Entrega

Entregue os arquivos desta pasta, incluindo `requirements.txt` e este README.
Não inclua a pasta `.venv` nem arquivos `__pycache__`.
O enunciado também pede o link do repositório no GitHub e a demonstração das operações no Swagger.
O repositório ainda não foi publicado.

## Validação e verificação

`EmailStr` valida o formato do e-mail; não verifica se a caixa de e-mail existe.
`date` valida a data, informada como `AAAA-MM-DD`, e `time` valida o horário, informado como `HH:MM:SS`.
A capacidade usa `Field(gt=0)`. Os campos do cadastro são obrigatórios; o ID é gerado pelo sistema.

Foram realizadas 53 verificações HTTP automatizadas: CRUD dos dois recursos, campos obrigatórios, nomes e títulos vazios, e-mail/data/horário inválidos, capacidade inválida, IDs inexistentes, inscrições duplicadas, lotação e limpeza das inscrições nas exclusões. As rotas `/docs` e `/openapi.json` também responderam corretamente.

Os prints abaixo registram os testes de sucesso realizados no Swagger. Não incluem a consulta dos inscritos nem os cenários de erro descritos acima.


## Prints dos testes no Swagger

- [Cadastro de evento — 201](01-cadastro-evento.png)
- [Cadastro de participante — 201](02-cadastro-participante.png)
- [Consulta de eventos e participantes — 200](03-consulta-eventos-e-participantes.png)
- [Atualização de evento — 200](05-atualizacao-evento.png)
- [Atualização de participante — 200](06-atualizacao-participante.png)
- [Inscrição em evento — 201](07-inscricao.png)
- [Exclusão de participante e evento — 204](18-exclusao-participante-e-evento.png)
