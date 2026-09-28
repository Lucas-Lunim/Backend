from fastapi import FastAPI
from controller.evento_controller import router as eventos_router
from controller.participante_controller import router as participantes_router

app = FastAPI(title="APS 2 - Eventos acadêmicos")
app.include_router(eventos_router)
app.include_router(participantes_router)


@app.get("/")
def raiz():
    return {"mensagem": "API de eventos acadêmicos. Acesse /docs para testar."}
