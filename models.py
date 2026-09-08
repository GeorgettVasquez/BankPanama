# creacion de tablas==clases (Usuario, Cuenta,Transaccion, Tarjeta, Auditoria)

from sqlalchemy import Column, Integer, String, CHAR, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__="usuarios" #nombre real de la tabla en post
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre= Column(String(50), nullable=False)
    apellido= Column(String(50), nullable=False)
    email= Column(String(255), unique=True, nullable=False)
    rol=Column(String(50))
    telefono=Column(String(20))
    sexo=Column(CHAR(1)) # 'M' o 'F'
    fecha_de_nacimiento=Column(Date)
    dni=Column(String(20), unique=True)
    passw_hash=Column(String(100), nullable=False) #no guardar en texto plano
    
    cuentas= relationship("Cuenta", back_populates="usuario")
    auditorias =relationship("Auditoria", back_populates="usuario")
    
class Cuenta(Base):
    __tablename__="cuentas"
    
    id_cuenta=Column(Integer, primary_key=True, index=True)
    id_usuario=Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    numero_de_cuenta=Column(String(100), unique=True, nullable=False)
    tipo_cuenta= Column(String(50))
    estado_cuenta=Column(String(50))
    fecha_creacion=Column(Date)
    saldo=Column(Numeric(12,2), default=0.00)
    
    usuario= relationship("Usuario", back_populates="cuentas")
    tarjetas = relationship("Tarjeta", back_populates="cuenta")
    
    transacciones_origen= relationship(
        "Transaccion", foreign_keys="Transaccion.id_cuenta", back_populates="cuenta_origen"
    )
    transacciones_recibidas = relationship(
        "Transaccion", foreign_keys="Transaccion.cuenta_destino", back_populates="cuenta_destino_rel"
    )
    
class Transaccion(Base):
    __tablename__="transaccciones"
    
    id_transaccion=Column(Integer, primary_key=True, index=True)
    id_cuenta = Column(Integer, ForeignKey("cuentas.id_cuenta"), nullable=False)
    cuenta_destino = Column(Integer, ForeignKey("cuentas.id_cuenta"), nullable=True)
    # nullable=True porque no toda transacción tiene destino (ej. un depósito no lo necesita)
    tipo_transaccion = Column(String(50))
    monto = Column(Numeric(12, 2), nullable=False)
    fecha = Column(Date)
    descripcion = Column(String(300))
    
    cuenta_origen = relationship(
        "Cuenta", foreign_keys=[id_cuenta], back_populates="transacciones_origen"
    )
    cuenta_destino_rel = relationship(
        "Cuenta", foreign_keys=[cuenta_destino], back_populates="transacciones_recibidas"
    )


class Tarjeta(Base):
    __tablename__ = "tarjeta"

    id_tarjeta = Column(Integer, primary_key=True, index=True)
    id_cuenta = Column(Integer, ForeignKey("cuentas.id_cuenta"), nullable=False)
    num_tarjeta = Column(String(100), unique=True, nullable=False)
    tipo_tarjeta = Column(String(50))
    fecha_expedicion = Column(Date)
    estado_tarjeta = Column(String(50))
    fecha_expiracion = Column(Date)
    
    
    cuenta = relationship("Cuenta", back_populates="tarjetas")


class Auditoria(Base):
    __tablename__ = "auditoria"

    id_auditoria = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    descripcion = Column(String(300))
    fecha = Column(Date)
    accion_realizada = Column(String(300))
    registro_id = Column(String(50))
    ip = Column(String(100))
    tabla_afectada = Column(String(50))

    usuario = relationship("Usuario", back_populates="auditorias")
    