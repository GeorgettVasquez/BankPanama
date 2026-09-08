#funciones CRUD de usuario (crear_usuario, buscar_usuario...)

from sqlalchemy.orm import Session
from models import Usuario
from autenticacion import hashear_password

def buscar_usuario_por_email(db: Session, email:str):
    # buscamos al usuario por su email y devuelve el objeto si existe
    #db.query(Usuario): quiero consultar en la tabla usuario
    #.filter(Usuario.email ==email): es un where email=X en sql
    #.first() = trae solo el primer resultado (o None, si no hay ninguno)

    return db.query(Usuario).filter(Usuario.email ==email).first()

def crear_usuario(db:Session, nombre, apellido, email, password_plano,
                  dni, sexo=None, telefono=None, fecha_de_nacimiento=None, rol="cliente"):
    
    #validar duplicado
    existente = buscar_usuario_por_email(db,email)
    if existente:
        return None 
    
    # Aquí se hashea, justo antes de guardar, nunca guardar el texto plano
    passw_hash = hashear_password(password_plano)
    
    #crear objeto pyth que representa fila
    nuevo_usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        email=email,
        passw_hash=passw_hash, 
        dni=dni, 
        sexo=sexo,
        telefono=telefono,
        fecha_de_nacimiento=fecha_de_nacimiento,
        rol=rol
    )
    
    #poner insert
    db.add(nuevo_usuario)
    #ejecutar insert
    db.commit()
    #hacer refrersh para que traiga el id de usuario
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario


def verificar_login(db:Session, email:str,passw_hash: str):
    #verificamos credenciales
    #bloque inicio session
    
    usuario = buscar_usuario_por_email(db,email)
    if usuario is None: 
        return None 
    if usuario.passw_hash != passw_hash:
        return None  #existe pero contra no es igual
    return usuario #login exitoso

    
    