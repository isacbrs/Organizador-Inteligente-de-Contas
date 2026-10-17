from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.auth import router as auth_router # <-- NOVA IMPORTAÇÃO

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

# <-- CONECTANDO AS ROTAS DE AUTENTICAÇÃO AO APLICATIVO
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"status": "online", "message": "API rodando e pronta para receber requisições!"}