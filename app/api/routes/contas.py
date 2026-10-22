from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from supabase import Client
from fastapi.security import HTTPAuthorizationCredentials
from app.schemas.conta_schema import ContaCreate, ContaResponse
from app.api.dependencies import get_current_user_client, security

router = APIRouter(prefix="/contas", tags=["Contas a Pagar"])

@router.post("/", response_model=ContaResponse, status_code=status.HTTP_201_CREATED)
async def criar_conta(
    conta: ContaCreate, 
    supabase: Client = Depends(get_current_user_client),
    token_auth: HTTPAuthorizationCredentials = Depends(security)
):
    """Cria uma nova conta atrelada ao utilizador logado."""
    try:
        # Passamos o JWT explícito para obter os dados do utilizador
        user_response = supabase.auth.get_user(token_auth.credentials)
        user_id = user_response.user.id

        conta_data = conta.model_dump()
        conta_data["data_vencimento"] = conta_data["data_vencimento"].isoformat()
        conta_data["user_id"] = user_id

        response = supabase.table("contas").insert(conta_data).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao guardar conta: {str(e)}")

@router.get("/", response_model=List[ContaResponse])
async def listar_contas(supabase: Client = Depends(get_current_user_client)):
    """Lista todas as contas do utilizador logado."""
    try:
        response = supabase.table("contas").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))