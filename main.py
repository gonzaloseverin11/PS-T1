# -*- coding: utf-8 -*-
import db_functions as db
import pandas as pd
from getpass import getpass
from productos_simulados import PRODUCTOS_SIMULADOS

DATABASE_NAME = "inventario.db"

def main():

    #Preguntar al usuario si desea cargar los productos simulados
    cargar_simulados = input("¿Desea cargar productos simulados? (s/n): ").strip().lower()
    if cargar_simulados == "s":
        # Cargar productos simulados desde el archivo CSV
        db.poblar_productos(DATABASE_NAME, PRODUCTOS_SIMULADOS)
        print("Productos simulados cargados exitosamente. \n")

    print("REGISTRO DE INVENTARIO DE PRODUCTOS")
    print("Bienvenido al sistema de gestión de inventario.")
    print("Inicia sesión para continuar.")

    db.create_database(DATABASE_NAME)

    # Inicio de sesión o registro
    while True:
        print("\n1. Registro")
        print("2. Iniciar sesión")
        print("3. Salir")
        choice = input("Seleccione una opción: ").strip()

        if choice == "1":
            nombre = input("Ingrese su usuario: ").strip()
            contrasena = getpass("Ingrese una contraseña: ").strip()
            confirmar_contrasena = getpass("Confirme su contraseña: ").strip()
            if contrasena == confirmar_contrasena:
                db.insertar_usuario(DATABASE_NAME, nombre, contrasena)
            else:
                print("Las contraseñas no coinciden. Intente nuevamente.")

        elif choice == "2":
            nombre = input("Ingrese su usuario: ").strip()
            contrasena = getpass("Ingrese su contraseña: ").strip()
            if db.iniciar_sesion(DATABASE_NAME, nombre, contrasena):
                break  # Salir del bucle si el inicio de sesión es exitoso

        elif choice == "3":
            print("Saliendo del programa.")
            exit()
        else:
            print("Opción no válida. Intente de nuevo.")


    # Menú principal después de iniciar sesión
    db.insertar_categorias(DATABASE_NAME)
    while True:
        print("\nMENU PRINCIPAL")
        print("1. Agregar producto")
        print("2. Mostrar productos")
        print("3. Editar producto")
        print("4. Eliminar producto")
        print("5. Agregar inventario")
        print("6. Vender inventario")
        print("7. Buscar producto")
        print("8. Obtener reporte")
        print("9. Historial de compra/venta")
        print("10. Salir")

        choice = input("Seleccione una opción: ").strip()

        if choice == "1":
            print("\nAGREGAR PRODUCTO")
            db.mostrar_categorias(DATABASE_NAME)
            nombre_producto = input("Nombre del producto: ").strip()
            descripcion = input("Descripción del producto: ").strip()
            cantidad = int(input("Cantidad del producto: ").strip())
            precio = float(input("Precio del producto: ").strip())
            categoria_nombre = input("Nombre de la categoría: ").strip()
            db.insertar_producto(DATABASE_NAME, nombre_producto, descripcion, cantidad, precio, categoria_nombre)

        elif choice == "2":
            db.mostrar_productos(DATABASE_NAME)

        elif choice == "3":
            print("\nEDITAR PRODUCTO")
            nombre_producto = input("Nombre del producto que desee modificar: ").strip()
            db.modificar_producto(DATABASE_NAME, nombre_producto)
            
        elif choice == "4":
            print("\nELIMINAR PRODUCTO")
            nombre_producto = input("Nombre del producto que desee eliminar: ").strip()
            db.borrar_producto(DATABASE_NAME, nombre_producto)

        elif choice == "5":
            print("\nAGREGAR INVENTARIO")
            nombre_producto = input("Nombre del producto a actualizar: ").strip()
            cantidad = int(input("Cantidad a agregar: ").strip())
            db.comprar_producto(DATABASE_NAME, nombre_producto, cantidad)
        
        elif choice == "6":
            print("\nVENDER INVENTARIO")
            nombre_producto = input("Nombre del producto a vender: ").strip()
            cantidad = int(input("Cantidad a vender: ").strip())
            db.vender_producto(DATABASE_NAME, nombre_producto, cantidad)
        elif choice == "7":
            print("\nBUSCAR PRODUCTO")
            db.filtrar_productos(DATABASE_NAME)

        elif choice == "8":
            print("\nOBTENER REPORTE")
            db.reporte_inventario(DATABASE_NAME)

        elif choice == "9":
            print("\nHISTORIAL DE COMPRA/VENTA")
            num_movimientos = int(input("¿Cuántos movimientos desea ver?: ").strip())
            db.ver_ultimos_movimientos(DATABASE_NAME, num_movimientos)

        elif choice == "10":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
        
    #Preguntar al usuario si desea guardar los cambios
    guardar_cambios = input("¿Deseas limpiar la base de datos? (s/n): ").strip().lower()
    if guardar_cambios == "s":
        db.limpiar_base_datos(DATABASE_NAME)
        print("Base de datos limpiada exitosamente.")
    
if __name__ == "__main__":
    main()