#funciones de negocio (deposito, retiro,historial...) — AQUÍ va lo 

from sqlalchemy.orm import Session
from models import Cuenta, Transaccion
from datetime import date
from sqlalchemy import or_ 


def obtener_cuenta(db:Session, id_cuenta:int):
    #busca la cuenta por su id
    
    return db.query(Cuenta).filter(Cuenta.id_cuenta == id_cuenta).first()

def depositar(db: Session, id_cuenta: int, monto: float):
    if monto <= 0:
        return None

    cuenta = obtener_cuenta(db, id_cuenta)
    if cuenta is None:
        return None

    cuenta.saldo += monto  

    nueva_transaccion = Transaccion(
        id_cuenta=id_cuenta,
        tipo_transaccion="deposito",
        monto=monto,
        fecha=date.today(),
        descripcion="Depósito en efectivo"
    )
    db.add(nueva_transaccion)
    db.commit()
    db.refresh(cuenta)

    return cuenta
def retirar(db: Session, id_cuenta:int, monto:float):
    #retira dinero de una cuenta
    if monto <=0:
        return None
    cuenta=obtener_cuenta(db, id_cuenta)
    if cuenta is None:
        return None
    if cuenta.saldo < monto: 
        return None #saldo insuficiente
    cuenta.saldo -= monto
    
    nueva_transaccion = Transaccion(
        id_cuenta=id_cuenta,
        tipo_transaccion="retiro",
        monto=monto,
        fecha=date.today(),
        descripcion="Retiro en efectivo"
    )
    db.add(nueva_transaccion)
    db.commit()
    db.refresh(cuenta)

    return cuenta


def consultar_saldo(db: Session, id_cuenta: int):
    #devuelve saldo 
    
    cuenta = obtener_cuenta(db, id_cuenta)
    if cuenta is None:
        return None
    return cuenta.saldo


def obtener_historial(db: Session, id_cuenta: int):
    #devuelve lista de transacciones que hizo el usuario
    #de mas recientes a mas antigua
    return (
        db.query(Transaccion)
        .filter(Transaccion.id_cuenta == id_cuenta)
        .order_by(Transaccion.fecha.desc())
        .all()
    ) 
    
def obtener_historial_completo(db:Session, id_cuenta:int):
    #devuelve todas las transacciones de la cuenta, sea destino o origen
    cuenta=obtener_cuenta(db, id_cuenta)
    
    if cuenta is None:
        return None
    
    return (
        db.query(Transaccion)
        .filter(or_(Transaccion.id_cuenta == id_cuenta,
                    Transaccion.cuenta_destino == id_cuenta))
        .order_by(Transaccion.fecha.desc())
                .all()
            ) 
    

    
def transferir(db: Session, id_cuenta_origen: int, id_cuenta_destino: int, monto:float):
#transfiere dinero de una cuenta a otra , devuelve true si funciono, none si fallo(cuenta no existe, saldo insuficiente, monto invalido)
    
    if monto <=0:
        return None
    
    
    cuenta_origen= obtener_cuenta(db, id_cuenta_origen)
    cuenta_destino=obtener_cuenta(db,id_cuenta_destino)
    
    if cuenta_origen is None or cuenta_destino is None:
        return None
    if cuenta_origen.saldo < monto:
        return None #no alcanzo el saldo, se deniega
    
    #operaciones pasan juntas
    cuenta_origen.saldo -= monto
    cuenta_destino.saldo += monto
    
    #Una sola fila de Transaccion representa toda la transferencia
    
    nueva_transaccion = Transaccion(
        id_cuenta= id_cuenta_origen,
        cuenta_destino = id_cuenta_destino,
        tipo_transaccion="transferencia",
        monto=monto,
        fecha=date.today(),
        descripcion=f'Transferencia a cuenta{id_cuenta_destino}'
    )

    db.add(nueva_transaccion)
    db.commit()
    db.refresh(cuenta_origen)
    db.refresh(cuenta_destino)
    
    return True