#login, verificación de contraseña

import bcrypt
from sqlalchemy.orm import Session
from models import Usuario

def hashear_password(password_plano:str):
    
    # bcrypt trabaja con bytes por eso .encode()
    password_bytes = password_plano.encode("utf-8")

    # gensalt() genera el "salt" aleatorio 
    salt = bcrypt.gensalt()

    # hashpw() combina la contraseña + salt y genera el hash final
    hash_bytes = bcrypt.hashpw(password_bytes, salt)

    # Lo guardamos como texto (str) en la base de datos, no como bytes
    return hash_bytes.decode("utf-8")

def verificar_password(password_plano: str, hash_guardado: str):
    #se compara contra con el hashguardado
    
    password_bytes = password_plano.encode("utf-8")
    hash_bytes = hash_guardado.encode("utf-8")

    # checkpw() extrae el salt del hash guardado,
    # vuelve a hashear el password_plano con ese mismo salt,
    # y compara los resultados  por eso no guardamos el salt aparte,
    # bcrypt ya lo incluye dentro del propio hash_guardado.
    return bcrypt.checkpw(password_bytes, hash_bytes)

def login(db: Session, email: str, password_plano: str):
   #verificamos credenciales 
   
    usuario = db.query(Usuario).filter(Usuario.email==email).first()

    if usuario is None:
        return None  # ese email no existe

    if not verificar_password(password_plano, usuario.passw_hash):
        return None  # contraseña incorrecta

    return usuario  # login exitoso
