from fastapi import APIRouter, HTTPException
from model.participante import Participante
from service.sistema_service import sistema

router = APIRouter(prefix="/participantes", tags=["Participantes"])


def buscar_ou_404(participante_id):
    participante = sistema.buscar_participante(participante_id)
    if participante is None:
        raise HTTPException(status_code=404, detail="Participante não encontrado.")
    return participante


@router.post("", status_code=201)
def criar_participante(dados: Participante):
    try:
        return sistema.criar_participante(dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("")
def listar_participantes():
    return sistema.listar_participantes()


@router.get("/{participante_id}")
def consultar_participante(participante_id: int):
    return buscar_ou_404(participante_id)


@router.put("/{participante_id}")
def atualizar_participante(participante_id: int, dados: Participante):
    buscar_ou_404(participante_id)
    try:
        return sistema.atualizar_participante(participante_id, dados)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.delete("/{participante_id}", status_code=204)
def excluir_participante(participante_id: int):
    buscar_ou_404(participante_id)
    sistema.remover_participante(participante_id)
