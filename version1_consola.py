import json
import os
import random
from datetime import datetime

ARCHIVO= r'C:/Users/georg/Downloads/Python Geor/usuarios_nuevos.json'
#print("Archivo que uso:", os.path.abspath(ARCHIVO))

# Función para cargar usuarios guardados
def cargar_usuarios():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO) as archivo:
            return json.load(archivo)  # Retorna lista de dicts
    else:
        return []  # Lista vacía

# Función para guardar usuarios

def guardar_usuarios(lista_usuarios):
    with open(ARCHIVO, 'w') as archivo:
        json.dump(lista_usuarios, archivo, indent=4)
        
#Limpiar lista de usaurios

def reiniciar_usuarios():
    with open(ARCHIVO, 'w') as archivo:
        json.dump([], archivo, indent=4)   
    print("\n==============================")
    print(" Archivo usuarios.json reiniciado (vacío).")
    print("==============================\n")

    
#funcion para limpiar el historial de algun usuario 

def reiniciar_histo_usua(nombre_usua):
    lista_usuarios=cargar_usuarios()
    for u in lista_usuarios:
        if u['nombre']==nombre_usua:
            u['historial']=[]
            guardar_usuarios(lista_usuarios)
            print(f'\n>>>Historial reiniciado para el usuario{nombre_usua} <<<\n')
            return
        print('\n>>>usuario no encontrado <<<\n')
            
#saldos en usuarios

def actualizar_usuarios_con_saldo():
    lista = cargar_usuarios()
    for usuario in lista:
        if "saldo" not in usuario:
            usuario["saldo"] = 0.0
    guardar_usuarios(lista)
    print("\n>>>Todos los usuarios ahora tienen un campo de saldo.<<<\n")

# funcion para depositar dinero

def deposito(nombre_usua):
    while True:
        try:
            cantidad = pedir_float('\n¿Cuánto dinero desea depositar? $')
            if cantidad <= 0:
                print(' [Error]  La cantidad a depositar debe ser mayor a cero.')
                continue  # vuelve a pedir
            break  # si pasó validación, salir del bucle
        except ValueError:
            print('[Error] Por favor, ingresa un número válido.')
            
    lista_usuarios = cargar_usuarios()  # cargamos la lista actual

    for usuario in lista_usuarios:
        if usuario["nombre"] == nombre_usua:
                saldo_actual = usuario.get("saldo",0.0)  # obtiene saldo o pone 0.0 si no hay
                nuevo_saldo = saldo_actual + cantidad
                usuario["saldo"] = nuevo_saldo  # actualiza el saldo
                agregar_mov(usuario,'deposito',cantidad)
                guardar_usuarios(lista_usuarios)  # guardamos los cambios
                print(f'\n>>>Depósito exitoso. Nuevo saldo: ${nuevo_saldo:.2f}<<<\n')
                break
    else: 
            print('Usuario no encontrado')

    
#funcion para retirar dinero 

def retiro(nombre_usua2):
    while True:
        try:
            cantidad2 = pedir_float('\n¿Cuánto dinero desea retirar? $')
            if cantidad2 <= 0:
                print('[Error]La cantidad a retirar debe ser mayor a cero.')
                continue
            break
        except ValueError:
            print('[Error] Por favor, ingresa un número válido.')

    lista_usuarios = cargar_usuarios()

    for usuario in lista_usuarios:
        if usuario["nombre"] == nombre_usua2:
            if usuario.get("saldo", 0.0) >= cantidad2:
                saldo_actual = usuario.get("saldo", 0.0)
                nuevo_saldo = saldo_actual - cantidad2
                usuario["saldo"] = nuevo_saldo
                agregar_mov(usuario, 'retiro', cantidad2)
                guardar_usuarios(lista_usuarios)
                print(f'\n>>> Retiro exitoso. Nuevo saldo: ${nuevo_saldo:.2f}<<<\n')
            else:
                print('\n[Error] Saldo insuficiente\n')
            break
    else:
        print('\n[Error] Usuario no encontrado\n')


# funcion para consultar saldo

def consultar(nombre_usua3, contra, cuenta_ingre):
    lista_usuarios=cargar_usuarios()
    for usuario in lista_usuarios:
        if usuario['nombre']==nombre_usua3 and usuario['contra']==contra and usuario['cuenta']==cuenta_ingre: 
            saldo_actual=usuario.get('saldo', 0.0)
            print(f'\n>>>Su saldo es de : {saldo_actual:.2f}<<<\n')
            break
    else:
            print('\n[Error] Intente de nuevo, algo esta incorrecto\n')

#Funcion para mostrar historial

def agregar_mov(usuario, tipo, monto):
    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # ← arreglé también el formato
    movimiento = {
        'tipo': tipo,
        'monto': monto,
        'fecha': ahora
    }
    if "historial" not in usuario:
        usuario["historial"] = []
    
    usuario["historial"].append(movimiento)  # ← ahora siempre se agrega

 # Guardar la lista completa con el historial actualizado
    lista_usuarios = cargar_usuarios()
    for u in lista_usuarios:
        if u["nombre"] == usuario["nombre"]:
            u.update(usuario)
            break
    guardar_usuarios(lista_usuarios)


#Funcion historial
def mostrar_historial(nombre_usua):
    lista_usuarios = cargar_usuarios()
    for usuario in lista_usuarios:
        if usuario["nombre"] == nombre_usua:
            historial = usuario.get("historial", [])
            if not historial:
                print("\n>>>No hay movimientos registrados.<<<\n")
                return
            print("\n==========Últimos movimientos==========")
            for mov in historial:  # Mostrar últimos 5 movimientos [-5:]:
                print(f"{mov['fecha']} - {mov['tipo'].capitalize()}: ${mov['monto']}")
            print("=========================================\n")
            return
    print("\n[Error]Usuario no encontrado.\n")

# Funcion para confirmar que el usuario ingresa valor flotnate correcto
def pedir_float(mensaje):
    while True: 
        valor = input(mensaje)
        try:
            return float(valor)   # Devuelve el número si es válido
        except ValueError:
            print("[Error] Por favor, ingresa un número válido.")

        
# Menu de inicio de sessión
def tareas_bank(nombreUser, contra):
    
    while True: 
        print('----------------------------------------------')
        print(f'Hola, {nombreUser}! ¿Que deseas hacer hoy?')
        print('1. Consultar Saldo')
        print('2. Depositar dinero')
        print('3. Retirar dinero')
        print('4. Historial de Movimientos')
        print('5. Salir')
        print('----------------------------------------------')
        opcion2=input('Ingrese una opcion: ')
        
        if opcion2 =='1':
             cuenta_ingre=str(input('ingrese su numero de cuenta:'))
             consultar(nombreUser, contra, cuenta_ingre)
        elif opcion2 =='2': 
            deposito(nombreUser)
        elif opcion2=='3': 
            retiro(nombreUser)
        elif opcion2=='4':
            mostrar_historial(nombreUser)
        elif opcion2=='5':
            print('\nGracias por visitarnos, buen dia\n')
            break
        else: 
            print('\n[Error] Ingrese una opcion valida :)\n')
        
def ver_usuarios():
   cargar_usuarios()
            
                 
def admin():
 while True:
        print("\n=== Menú Admin ===")
        print("1. Ver todos los usuarios")
        print("2. Eliminar usuario")
        print("3. Reiniciar historial de un usuario")
        print("4. Cambiar clave de un usuario")
        print("5. Eliminar usuarios duplicados")
        print("6. Reiniciar toda la base de datos (usuarios)")
        print("7. Salir Admin")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            ver_usuarios()
        elif opcion == '2':
            eliminar_usuario()
        elif opcion == '3':
            reiniciar_historial_usuario()
        elif opcion == '4':
            cambiar_clave_usuario()
        elif opcion == '5':
            eliminar_duplicados()
        elif opcion == '6':
           print('Lista limpiada correctamente', reiniciar_usuarios())
        elif opcion == '7':
            print("Saliendo del menú Admin...\n")
            break
        else:
            print("Opción inválida, intente de nuevo.")


 # inicio de programa
print('==============================================')
print('Bienvenido al sistema bancario de BankPanama')
print('==============================================\n')

while True:
    print('Elija una opción:')
    print('1. Crear Cuenta')
    print('2. Iniciar Sesión')
    print('3. Salir')
    print('==============================================')
    
    opcion = input('Ingrese su opción: ')
    
    if opcion == '1':
        print("\n----- Creación de Cuenta -----")
        nombre = str(input('Ingrese su nombre de usuario: '))
        contra = input('Ingrese su contraseña: ')
        numero_cuenta = str(random.randint(10000000, 99999999))

        lista_usuarios = cargar_usuarios()

        # Verifica si ya existe ese nombre
        if any(usuario["nombre"] == nombre for usuario in lista_usuarios):
            print("\n[Error] Ese nombre de usuario ya existe. Intente otro.\n")
        else:
            nuevo_usuario = {
                "nombre": nombre,
                "contra": contra,
                "cuenta": numero_cuenta
            }
            lista_usuarios.append(nuevo_usuario)
            guardar_usuarios(lista_usuarios)

            print(f'\n Cuenta creada exitosamente. Su número de cuenta es: {numero_cuenta}\n')

    elif opcion == '2':
        print("\n----- Inicio de Sesión -----")
        nombreUser =str(input('Ingrese su nombre de usuario: '))
        contra = input('Ingrese su contraseña: ')
        
        lista_usuarios = cargar_usuarios()
        #u== usuario
        usuario_encontrado = next((u for u in lista_usuarios if u["nombre"] == nombreUser and u["contra"] == contra), None)

        if usuario_encontrado:
            print(f'\nInicio de sesión exitoso. Bienvenido {nombreUser}. \n')
            tareas_bank(nombreUser, contra)
        else:
            print('\nUsuario o contraseña incorrectos.\n')

    elif opcion == '3':
        print('\nGracias por usar BankPanama. ¡Buen día! :)')
        break
        
    elif opcion.lower()=='admin':  #comando secret 
       contra=str(input('Ingrese su contraseña'))
       if contra=='admin123':
           print('Acceso aprobado')
           admin()
       elif contra=='asistente123':
           print('Acceso Aprobado')
           #imprimir menu 
       else: 
           print('Intente de nuevo, ¡intruso! corre, viene la policia')
        #meter otro menu aqui para admi que pida contraseña para poder usarlo
        #print("Lista de usuarios guardados:", lista_usuarios)
       #guardar_usuarios(lista_usuarios)
       #break
    else:
        print('\n[Error] Opción inválida, intente de nuevo.\n')
