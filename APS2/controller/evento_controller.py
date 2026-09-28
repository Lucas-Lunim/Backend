from fastapi import APIRouter, HTTPException
from model.evento import Evento
from service.sistema_service import sistema

router = APIRouter(prefix="/eventos", tags=["Eventos"])


def buscar_ou_404(evento_id):
    evento = sistema.buscar_evento(evento_id)
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")
    return evento


@router.post("", status_code=201)
def criar_evento(dados: Evento):
    try:
        return sistema.criar_evento(dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("")
def listar_eventos():
    return sistema.listar_eventos()


@router.get("/{evento_id}")
def consultar_evento(evento_id: int):
    return buscar_ou_404(evento_id)


@router.put("/{evento_id}")
def atualizar_evento(evento_id: int, dados: Evento):
    buscar_ou_404(evento_id)
    try:
        return sistema.atualizar_evento(evento_id, dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.delete("/{evento_id}", status_code=204)
def excluir_evento(evento_id: int):
    buscar_ou_404(evento_id)
    sistema.remover_evento(evento_id)


@router.post("/{evento_id}/inscricoes/{participante_id}", status_code=201)
def inscrever_participante(evento_id: int, participante_id: int):
    buscar_ou_404(evento_id)
    if sistema.buscar_participante(participante_id) is None:
        raise HTTPException(status_code=404, detail="Participante não encontrado.")
    try:
        return sistema.inscrever(evento_id, participante_id)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/{evento_id}/inscricoes")
def listar_inscricoes(evento_id: int):
    buscar_ou_404(evento_id)
    return sistema.listar_inscricoes(evento_id)
