#define la forma que deben tener los datos que llegan en cada peticion
#pydantic valida automaiticamente si un campo o tipo esta mal
#fastApi rechaza la peti, antes que el codigo la procese

from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class UsuarioCrear(BaseModel):
    nombre:str
    apellido:str
    email:str
    password: str
    dni: str
    sexo:str | None= None
    telefono:str | None=None
    fecha_de_nacimiento:date | None=None
    

class loginRequest(BaseModel):
    email:str
    password:str
    
class CuentaCrear(BaseModel):
    id_usuario: int
    tipo_cuenta: str #ahorro,corriente
    
class TarjetaCrear(BaseModel):
    id_cuenta: int
    tipo_tarjeta:str #debito/credito
    
class DepositoRetiro(BaseModel):
    id_cuenta: int
    monto:Decimal
    
class TransferenciaRequest(BaseModel):
    id_cuenta:int
    monto:Decimal
    
class TransferenciaRequest(BaseModel):
    id_cuenta_origen:int
    id_cuenta_destino: int
    monto: Decimal 
    
