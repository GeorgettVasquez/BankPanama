import random
from sqlalchemy.orm import Session
from models import Tarjeta
from datetime import date, timedelta


def generar_numero_tarjeta():
    """
    genera numero de tarjeta de 16 digits
    """
    numero = "".join([str(random.randint(0, 9)) for _ in range(16)])
    return numero


def crear_tarjeta(db: Session, id_cuenta: int, tipo_tarjeta: str):
    # Crea una tarjeta nueva asociada a una cuenta existente.
   # Vence 5 años después de la fecha de expedición 
    
    hoy = date.today()
    fecha_expiracion = hoy.replace(year=hoy.year + 5)

    nueva_tarjeta = Tarjeta(
        id_cuenta=id_cuenta,
        num_tarjeta=generar_numero_tarjeta(),
        tipo_tarjeta=tipo_tarjeta,
        fecha_expedicion=hoy,
        estado_tarjeta="activa",
        fecha_expiracion=fecha_expiracion
    )

    db.add(nueva_tarjeta)
    db.commit()
    db.refresh(nueva_tarjeta)

    return nueva_tarjeta