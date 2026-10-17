from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client(access_token: str = None) -> Client:
    """
    Cria uma instância do Supabase. Se um token JWT for fornecido (do usuário logado no front-end),
    o cliente atuará com as permissões restritas daquele usuário, garantindo o Multitenancy.
    """
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    
    if access_token:
        # Injeta o token do usuário na sessão atual do banco
        supabase.postgrest.auth(access_token)
        
    return supabase