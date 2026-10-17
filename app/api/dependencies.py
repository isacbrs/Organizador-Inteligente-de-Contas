from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.supabase_client import get_supabase_client

security = HTTPBearer()

def get_current_user_client(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependência do FastAPI. Intercepta o token Bearer enviado pelo Front-end.
    Retorna um cliente do banco de dados restrito aos dados deste usuário.
    """
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação ausente"
        )
    
    # Retorna o cliente do Supabase já autenticado como o usuário que fez a requisição
    return get_supabase_client(access_token=token)