# cuentas.py
# Funciones para crear y consultar cuentas bancarias
import random
from sqlalchemy.orm import Session
from models import Cuenta
from datetime import date


def generar_numero_cuenta():
    """
    Genera un número de cuenta aleatorio de 8 dígitos, como texto.
    random.randint
    """
    numero = random.randint(10000000, 99999999)
    return str(numero)


def crear_cuenta(db: Session, id_usuario: int, tipo_cuenta: str):
    """
    Crea una cuenta nueva para un usuario, con saldo inicial en 0.
    Devuelve el objeto Cuenta creado.
    """
    nueva_cuenta = Cuenta(
        id_usuario=id_usuario,
        numero_de_cuenta=generar_numero_cuenta(),
        tipo_cuenta=tipo_cuenta,
        estado_cuenta="activa",
        fecha_creacion=date.today(),
        saldo=0.00
    )

    db.add(nueva_cuenta)
    db.commit()
    db.refresh(nueva_cuenta)

    return nueva_cuenta