from pydantic import BaseModel, EmailStr

# Modelo do que ESPERAMOS RECEBER do Front-end na hora do login/cadastro
class UserCredentials(BaseModel):
    email: EmailStr # O Pydantic já valida automaticamente se tem '@' e '.com'
    password: str

# Modelo do que VAMOS DEVOLVER para o Front-end após o login dar certo
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str