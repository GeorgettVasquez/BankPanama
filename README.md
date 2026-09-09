# BankPanama

Simulador de sistema bancario desarrollado como proyecto personal de aprendizaje, con el objetivo de practicar arquitectura backend moderna, control de versiones y desarrollo full-stack.

## Descripción

BankPanama comenzó como un sistema bancario simple en Python (consola, con persistencia en JSON) y evolucionó hacia una arquitectura modular real, usando una base de datos relacional, un ORM, y una API REST documentada.

El proyecto está en desarrollo activo — algunos módulos (panel de administración, frontend) aún están en construcción.

## Tecnologías utilizadas

- **Backend:** Python + [FastAPI](https://fastapi.tiangolo.com/)
- **Base de datos:** PostgreSQL
- **ORM:** SQLAlchemy
- **Seguridad:** bcrypt (hash de contraseñas)
- **Control de versiones:** Git / GitHub
- **Frontend:** HTML, CSS, JavaScript (planeado) — con posible migración a React

## Estructura del proyecto

```
BankPanama/
├── main.py              # Conecta todo con FastAPI (endpoints)
├── database.py          # Conexión a PostgreSQL (engine, sesión)
├── models.py             # Tablas como clases (Usuario, Cuenta, Transaccion, Tarjeta, Auditoria)
├── schemas.py             # Validación de datos de entrada (Pydantic)
├── usuarios.py            # Lógica de negocio: crear/buscar usuarios
├── autenticacion.py       # Login y hasheo de contraseñas (bcrypt)
├── cuentas.py              # Creación de cuentas bancarias
├── transacciones.py       # Depósito, retiro, transferencia, historial
├── tarjetas.py             # Emisión de tarjetas
├── admin.py                # Panel de administración (en construcción)
├── init_db.py               # Script para crear las tablas en la base de datos
├── version1_consola.py    # Versión original del proyecto (consola, sin BD real)
└── .env                     # Variables de entorno (no se sube a git)
```

## Modelo de datos

El sistema cuenta con 5 tablas relacionadas:

- **Usuarios** — información personal y credenciales
- **Cuentas** — cuentas bancarias asociadas a un usuario (relación 1:N)
- **Transacciones** — depósitos, retiros y transferencias entre cuentas
- **Tarjeta** — tarjetas asociadas a una cuenta
- **Auditoria** — registro de acciones relevantes del sistema

## Instalación y configuración

### Requisitos previos

- Python 3.11+
- PostgreSQL instalado (local o remoto)

### Pasos

1. Clona el repositorio:
```bash
git clone https://github.com/GeorgettVasquez/BankPanama.git
cd BankPanama
```

2. Instala las dependencias:
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv bcrypt
```

3. Crea un archivo `.env` en la raíz del proyecto con tu cadena de conexión:
```
db_url=postgresql://usuario:contraseña@localhost:5432/bankpanama
```

4. Crea la base de datos `bankpanama` en PostgreSQL (por ejemplo, desde pgAdmin).

5. Corre el script de inicialización para crear las tablas:
```bash
python init_db.py
```

6. Levanta el servidor:
```bash
uvicorn main:app --reload
```

7. Abre la documentación interactiva de la API en:
```
http://127.0.0.1:8000/docs
```

## Endpoints disponibles

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/registro` | Crear un usuario nuevo |
| POST | `/login` | Iniciar sesión |
| POST | `/crear-cuenta` | Abrir una cuenta bancaria |
| POST | `/crear-tarjeta` | Emitir una tarjeta |
| POST | `/depositar` | Depositar dinero en una cuenta |
| POST | `/retirar` | Retirar dinero de una cuenta |
| POST | `/transferir` | Transferir dinero entre cuentas |
| GET | `/saldo/{id_cuenta}` | Consultar saldo de una cuenta |
| GET | `/historial/{id_cuenta}` | Ver historial de movimientos |

## Seguridad

- Las contraseñas se almacenan hasheadas con **bcrypt**, nunca en texto plano.
- Las credenciales de la base de datos se manejan mediante variables de entorno (`.env`), excluido del control de versiones.

## Roadmap

- [x] Migración de script de consola a arquitectura modular
- [x] Base de datos relacional con SQLAlchemy
- [x] API REST con FastAPI
- [x] Autenticación con bcrypt
- [ ] Panel de administración (`admin.py`)
- [ ] Frontend (HTML/CSS/JS)
- [ ] Migración de frontend a React
- [ ] Sistema de migraciones con Alembic

## Autor

**Georgett Vásquez** — Estudiante de Ingeniería en Sistemas

## Licencia

Proyecto de uso educativo/personal.
