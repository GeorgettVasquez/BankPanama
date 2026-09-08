#aqui se conecta todo mediante fastapi, recibe peticiones http y llama funciones

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import UsuarioCrear, loginRequest, CuentaCrear,TarjetaCrear, DepositoRetiro, TransferenciaRequest
from usuarios import crear_usuario
from autenticacion import login
from transacciones import depositar, retirar, transferir,consultar_saldo, obtener_historial_completo
from cuentas import crear_cuenta
from tarjetas import crear_tarjeta

'''notes:  post cuando alguien  haga una peticion a la url registro se ejecuta 
la funcion de abajo
get es usualmente para consultar sin modificar nada

{id_cuenta} en la URL — es un path parameter. Permite que la URL sea dinámica:
/saldo/5 consulta la cuenta 5, /saldo/12 consulta la cuenta 12, sin necesitar un endpoint distinto para cada cuenta.
depends get_db llama a la base en database.py entrega session nueva y cierra'''

app= FastAPI()

@app.post("/registro")
def registro(datos:UsuarioCrear, db:Session = Depends(get_db)):
    #endpoint para crear usuario nuevo
    nuevo_usuario = crear_usuario(
        db=db,
        nombre=datos.nombre,
        apellido=datos.apellido,
        email=datos.email,
        password_plano=datos.password,
        dni=datos.dni,
        sexo=datos.sexo,
        telefono=datos.telefono,
        fecha_de_nacimiento=datos.fecha_de_nacimiento
    )
    
    if nuevo_usuario is None: 
        #httpexc, le dice a fast que codigo de error devolver
        #400=bad request, el cliente mando algo invalido
        raise HTTPException(status_code=400, detail="El email o Dni ya esta registrado")
    return {'mensaje': "Usuario creado", "id_usuario": nuevo_usuario.id_usuario}

@app.post("/login")
def iniciar_sesion(datos: loginRequest, db: Session = Depends(get_db)):
    usuario = login(db, datos.email, datos.password)

    if usuario is None:
        # 401 = "Unauthorized" -- credenciales incorrectas
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    return {"mensaje": f"Bienvenido {usuario.nombre}", "id_usuario": usuario.id_usuario}

@app.post("/crear_cuenta")
def abrir_cuenta(datos:CuentaCrear, db:Session=Depends(get_db)):
   nueva_cuenta = crear_cuenta(db, datos.id_usuario, datos.tipo_cuenta)
   return {
        "mensaje": "Cuenta creada",
        "id_cuenta": nueva_cuenta.id_cuenta,
        "numero_de_cuenta": nueva_cuenta.numero_de_cuenta
    }

@app.post("/crear-tarjeta")
def emitir_tarjeta(datos: TarjetaCrear, db: Session = Depends(get_db)):
    nueva_tarjeta = crear_tarjeta(db, datos.id_cuenta, datos.tipo_tarjeta)
    return {
        "mensaje": "Tarjeta emitida",
        "id_tarjeta": nueva_tarjeta.id_tarjeta,
        "num_tarjeta": nueva_tarjeta.num_tarjeta,
        "fecha_expiracion": nueva_tarjeta.fecha_expiracion
    }


@app.post("/depositar")
def hacer_deposito (datos:DepositoRetiro, db:Session = Depends(get_db)):
    cuenta =depositar (db, datos.id_cuenta, datos.monto)
    
    if cuenta is None:
        raise HTTPException(status_code=400, detail= "cuenta no encontrada o monto invalido")
    return {'mensaje': 'Deposito exitoso', 'nuevo_saldo':float(cuenta.saldo)}

@app.post("/retirar")
def hacer_retiro (datos:DepositoRetiro, db:Session= Depends(get_db)):
    cuenta = retirar (db, datos.id_cuenta, datos.monto)
    
    if cuenta is None:
        raise HTTPException(status_code=400, detail="Cuenta no encontrada, monto inválido o saldo insuficiente")

    return {"mensaje": "Retiro exitoso", "nuevo_saldo": float(cuenta.saldo)}


@app.post("/transferir")
def hacer_transferencia(datos: TransferenciaRequest, db: Session = Depends(get_db)):
    resultado = transferir(db, datos.id_cuenta_origen, datos.id_cuenta_destino, datos.monto)

    if resultado is None:
        raise HTTPException(status_code=400, detail="No se pudo completar la transferencia")

    return {"mensaje": "Transferencia exitosa"}

@app.get("/saldo/{id_cuenta}")
def ver_saldo(id_cuenta: int, db: Session = Depends(get_db)):

    saldo = consultar_saldo(db, id_cuenta)

    if saldo is None:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    return {"id_cuenta": id_cuenta, "saldo": float(saldo)}


@app.get("/historial/{id_cuenta}")
def ver_historial(id_cuenta: int, db: Session = Depends(get_db)):
    historial = obtener_historial_completo(db, id_cuenta)
    
    if historial is None:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    return historial