from fastapi import APIRouter, HTTPException, status
from app.schemas.auth_schema import UserCredentials, TokenResponse
from app.services.supabase_client import get_supabase_client

# O APIRouter agrupa nossas rotas para não virar uma bagunça no arquivo principal
router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/signup", summary="Cria um novo usuário")
async def signup(credentials: UserCredentials):
    """
    Recebe email e senha. Tenta criar um usuário no Supabase.
    """
    # Pegamos o cliente do Supabase sem token, pois o usuário ainda não existe
    supabase = get_supabase_client() 
    
    try:
        # Chama a função nativa do Supabase para registrar
        response = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password
        })
        return {"message": "Usuário criado com sucesso! Verifique o e-mail se necessário.", "user_id": response.user.id}
    except Exception as e:
        # Se o email já existir ou a senha for fraca, disparamos um erro 400 (Bad Request)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar usuário: {str(e)}"
        )

@router.post("/login", response_model=TokenResponse, summary="Faz login e retorna o Token JWT")
async def login(credentials: UserCredentials):
    """
    Verifica as credenciais no Supabase. Se corretas, devolve o token de acesso (JWT) 
    que o front-end usará nas próximas requisições.
    """
    supabase = get_supabase_client()
    
    try:
        # Tenta fazer o login com email e senha
        response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        
        # Monta a resposta exatamente como definimos no nosso TokenResponse (DTO)
        return TokenResponse(
            access_token=response.session.access_token,
            user_id=response.user.id
        )
    except Exception as e:
        # Se a senha estiver errada, disparamos erro 401 (Não Autorizado)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas."
        )