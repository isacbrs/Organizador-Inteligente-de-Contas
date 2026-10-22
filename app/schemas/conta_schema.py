from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class ContaBase(BaseModel):
    nome: str
    valor: float
    data_vencimento: date
    tipo: str = Field(..., description="Deve ser: mensal, parcelado ou unico")
    status: Optional[str] = "pendente"

class ContaCreate(ContaBase):
    pass

class ContaResponse(ContaBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True