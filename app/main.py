from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.auth import router as auth_router
from app.api.routes.contas import router as contas_router # <-- IMPORTAÇÃO

app = FastAPI(
    title="API - Organizador Inteligente de Contas",
    description="Back-end MVP",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(contas_router) # <-- CONEXÃO DA ROTA

@app.get("/")
async def root():
    return {"status": "online", "message": "API rodando e pronta para receber requisições!"}