import sqlite3
import hashlib
import pandas as pd


def create_database(nombre_db):
    """
    Crea una base de datos SQLite con tres tablas: usuarios, productos y categorías.
    
    Args:
        nombre_db (str): Nombre del archivo de la base de datos.
    
    Returns:
        None
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    ''')

    # Tabla de categorías
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
    ''')

    # Tabla de productos (con relación a categorías)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER DEFAULT 0,
            precio REAL NOT NULL,
            categoria_id INTEGER,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    ''')

     # Tabla movimientos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT NOT NULL,
            tipo TEXT CHECK(tipo IN ('compra', 'venta')) NOT NULL,
            cantidad INTEGER NOT NULL,
            stock_resultante INTEGER NOT NULL,
            momento INTEGER NOT NULL
        )
    ''')

    conexion.commit()
    conexion.close()

def insertar_categorias(nombre_db):
    """
    Inserta categorías de ejemplo en la tabla 'categorias'. Si ya existen, las ignora.

    Args:
        nombre_db (str): Nombre del archivo de la base de datos.

    Returns:
        None
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    categorias_ejemplo = [
        "Electrónica",
        "Ropa",
        "Alimentos",
        "Juguetes",
        "Hogar",
        "Deportes",
        "Libros",
        "Accesorios",
        "Videojuegos",
        "Belleza y Cuidado Personal"
    ]

    for categoria in categorias_ejemplo:
        try:
            cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (categoria,))
        except sqlite3.IntegrityError:
            # Ya existe la categoría, la ignoramos
            pass

    conexion.commit()
    conexion.close()

def mostrar_categorias(nombre_db):
    """
    Muestra todas las categorías en la tabla 'categorias'.

    Args:
        nombre_db (str): Nombre del archivo de la base de datos.

    Returns:
        None
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()

    if not categorias:
        print("No hay categorías disponibles.")
    else:
        print("Categorías disponibles:")
        for i, categoria in enumerate(categorias):
            print(f"{i + 1}. {categoria[1]}")

    conexion.close()

def insertar_usuario(nombre_db, nombre_usuario, contrasena):
    """
    Inserta un nuevo usuario con su contraseña hasheada usando SHA-256.

    Args:
        nombre_db (str): Nombre del archivo de la base de datos.
        nombre_usuario (str): Nombre de usuario único.
        contrasena (str): Contraseña del usuario (en texto plano).

    Returns:
        None
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    # Hashear la contraseña
    contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()

    # Insertar el usuario en la base de datos
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (?, ?)",
            (nombre_usuario, contrasena_hash)
        )
        conexion.commit()
        print("Registro exitoso. Ahora puede iniciar sesión.")
    except sqlite3.IntegrityError:
        print(f"El nombre de usuario '{nombre_usuario}' ya existe. Por favor, elige otro.")
    finally:
        conexion.close()

def iniciar_sesion(nombre_db, nombre_usuario, contrasena):
    """
    Verifica si un usuario y contraseña son válidos para iniciar sesión.

    Args:
        nombre_db (str): Nombre del archivo de la base de datos.
        nombre_usuario (str): Nombre de usuario.
        contrasena (str): Contraseña (en texto plano).

    Returns:
        bool: True si las credenciales son correctas, False en caso contrario.
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    # Hashear la contraseña ingresada
    contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()

    # Verificar las credenciales
    cursor.execute(
        "SELECT * FROM usuarios WHERE nombre_usuario = ? AND contrasena = ?",
        (nombre_usuario, contrasena_hash)
    )
    usuario = cursor.fetchone()

    if usuario:
        print(f"Bienvenido, {nombre_usuario}! Has iniciado sesión correctamente.")
        return True
    else:
        print("Nombre de usuario o contraseña incorrectos.")
        return False
    
def insertar_producto(nombre_db, nombre_producto, descripcion, cantidad, precio, categoria_nombre):
    """
    Inserta un nuevo producto en la base de datos.

    Args:
        nombre_db (str): Nombre del archivo de la base de datos.
        nombre_producto (str): Nombre del producto.
        descripcion (str): Descripción del producto.
        cantidad (int): Cantidad del producto.
        precio (float): Precio del producto.
        categoria_nombre (str): Nombre de la categoría del producto.

    Returns:
        None
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    #Revisar si la categoría existe
    cursor.execute("SELECT id FROM categorias WHERE nombre = ?", (categoria_nombre,))
    categoria = cursor.fetchone()
    
    if not categoria:
        print(f"La categoría '{categoria_nombre}' no existe.")
        conexion.close()
        return
    
    categoria_id = categoria[0]

    # Verificar si el producto ya existe
    cursor.execute("SELECT * FROM productos WHERE nombre = ?", (nombre_producto,))
    producto_existente = cursor.fetchone()
    if producto_existente:
        print(f"El producto '{nombre_producto}' ya existe en la base de datos.")
        conexion.close()
        return

    # Insertar el producto en la base de datos
    try:
        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria_id) VALUES (?, ?, ?, ?, ?)",
            (nombre_producto, descripcion, cantidad, precio, categoria_id)
        )
        conexion.commit()
       
        print(f"Producto '{nombre_producto}' insertado correctamente en la categoría '{categoria_nombre}'.")
    finally:
        conexion.close()


def mostrar_productos(nombre_db):
    """
    Muestra todos los productos disponibles en formato tabla:
    Incluye ID, nombre, descripción, cantidad, precio y categoría.

    Args:
        nombre_db (str): Nombre del archivo de la base de datos.

    Returns:
        None
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    cursor.execute('''
        SELECT prod.id, prod.nombre, prod.descripcion, prod.cantidad, prod.precio, cat.nombre
        FROM productos prod
        INNER JOIN categorias cat ON prod.categoria_id = cat.id
    ''')
    productos = cursor.fetchall()

    if not productos:
        print("NO HAY PRODUCTOS DISPONIBLES.")
    else:
        print("\nPRODUCTOS DISPONIBLES:\n")
        print("| {:<3} | {:<25} | {:<35} | {:>8} | {:>10} | {:<15} |".format(
            "ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"
        ))
        print("|" + "-"*5 + "|" + "-"*27 + "|" + "-"*37 + "|" + "-"*10 + "|" + "-"*12 + "|" + "-"*17 + "|")

        for prod in productos:
            print("| {:<3} | {:<25} | {:<35} | {:>8} | {:>10.2f} | {:<15} |".format(
                prod[0], prod[1], prod[2][:35], prod[3], prod[4], prod[5]
            ))

    conexion.close()


def modificar_producto(nombre_db, nombre_producto):
    """
    Modifica interactívamente la descripción, precio y categoría de un producto.
    Muestra los valores actuales y permite ingresar nuevos mediante inputs.
    Si algún campo se deja vacío, se conserva el valor original.
    La categoría solo se actualiza si existe en la base de datos.

    Args:
        nombre_db (str): Nombre del archivo de la base de datos.
        nombre_producto (str): Nombre del producto a modificar.

    Returns:
        None
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    # Obtener información actual del producto
    cursor.execute('''
        SELECT prod.descripcion, prod.precio, cat.nombre 
        FROM productos prod
        INNER JOIN categorias cat ON prod.categoria_id = cat.id
        WHERE prod.nombre = ?
    ''', (nombre_producto,))
    resultado = cursor.fetchone()

    if not resultado:
        print(f"El producto '{nombre_producto}' no existe.")
        conexion.close()
        return

    descripcion_actual, precio_actual, categoria_actual = resultado

    print(f"\n Información actual del producto '{nombre_producto}':")
    print(f"  Descripción : {descripcion_actual}")
    print(f"  Precio      : ${precio_actual}")
    print(f"  Categoría   : {categoria_actual}")

    # Inputs para nuevos valores
    nueva_descripcion = input("\nNueva descripción (Enter para mantener): ").strip()
    nuevo_precio_input = input("Nuevo precio (Enter para mantener): ").strip()
    nueva_categoria = input("Nueva categoría (Enter para mantener): ").strip()

    # Determinar valores finales
    descripcion_final = nueva_descripcion if nueva_descripcion else descripcion_actual

    try:
        precio_final = float(nuevo_precio_input) if nuevo_precio_input else precio_actual
    except ValueError:
        print("Precio inválido. Se mantendrá el original.")
        precio_final = precio_actual

    if nueva_categoria:
        cursor.execute("SELECT id FROM categorias WHERE nombre = ?", (nueva_categoria,))
        categoria = cursor.fetchone()
        if categoria:
            categoria_id_final = categoria[0]
        else:
            print(f"La categoría '{nueva_categoria}' no existe. Se mantendrá la categoría original.")
            cursor.execute("SELECT id FROM categorias WHERE nombre = ?", (categoria_actual,))
            categoria_id_final = cursor.fetchone()[0]
    else:
        cursor.execute("SELECT id FROM categorias WHERE nombre = ?", (categoria_actual,))
        categoria_id_final = cursor.fetchone()[0]

    # Actualizar en la base de datos
    cursor.execute('''
        UPDATE productos
        SET descripcion = ?, precio = ?, categoria_id = ?
        WHERE nombre = ?
    ''', (descripcion_final, precio_final, categoria_id_final, nombre_producto))

    conexion.commit()
    conexion.close()
    print(f"\nProducto '{nombre_producto}' actualizado.")


def borrar_producto(nombre_db, nombre_producto):
    """
    Borra un producto de la base de datos.

    Args:
        nombre_db (str): Nombre del archivo de la base de datos.
        nombre_producto (str): Nombre del producto a borrar.

    Returns:
        None
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    # Verificar si el producto existe
    cursor.execute("SELECT * FROM productos WHERE nombre = ?", (nombre_producto,))
    producto = cursor.fetchone()

    if not producto:
        print(f"El producto '{nombre_producto}' no existe.")
        conexion.close()
        return

    # Borrar el producto
    cursor.execute("DELETE FROM productos WHERE nombre = ?", (nombre_producto,))
    conexion.commit()
    conexion.close()
    print(f"Producto '{nombre_producto}' borrado.")

def comprar_producto(nombre_db, nombre_producto, cantidad_compra):
    """
    Aumenta el stock de un producto existente.

    Args:
        nombre_db (str): Nombre del archivo de la base de datos.
        nombre_producto (str): Nombre del producto a modificar.
        cantidad_compra (int): Cantidad a sumar al stock actual.

    Returns:
        None
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    # Verificar si el producto existe
    cursor.execute("SELECT cantidad FROM productos WHERE nombre = ?", (nombre_producto,))
    resultado = cursor.fetchone()

    if not resultado:
        print(f"El producto '{nombre_producto}' no existe.")
        conexion.close()
        return

    cantidad_actual = resultado[0]
    nueva_cantidad = cantidad_actual + cantidad_compra

    # Actualizar el stock
    cursor.execute("UPDATE productos SET cantidad = ? WHERE nombre = ?", (nueva_cantidad, nombre_producto))

    # Registrar movimiento
    momento = obtener_momento_actual(cursor)
    cursor.execute('''
        INSERT INTO movimientos (producto, tipo, cantidad, stock_resultante, momento)
        VALUES (?, 'compra', ?, ?, ?)
    ''', (nombre_producto, cantidad_compra, nueva_cantidad, momento))

    conexion.commit()
    conexion.close()
    print(f"Se han agregado {cantidad_compra} unidades a '{nombre_producto}'. Nuevo stock: {nueva_cantidad}")


def vender_producto(nombre_db, nombre_producto, cantidad_venta):
    """
    Disminuye el stock de un producto si hay suficiente cantidad disponible.

    Args:
        nombre_db (str): Nombre del archivo de la base de datos.
        nombre_producto (str): Nombre del producto a modificar.
        cantidad_venta (int): Cantidad a restar del stock actual.

    Returns:
        None
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    # Verificar si el producto existe
    cursor.execute("SELECT cantidad FROM productos WHERE nombre = ?", (nombre_producto,))
    resultado = cursor.fetchone()

    if not resultado:
        print(f"El producto '{nombre_producto}' no existe.")
        conexion.close()
        return

    cantidad_actual = resultado[0]

    if cantidad_venta > cantidad_actual:
        print(f"No hay suficiente stock. Stock actual: {cantidad_actual}")
        conexion.close()
        return

    nueva_cantidad = cantidad_actual - cantidad_venta

    # Actualizar el stock
    cursor.execute("UPDATE productos SET cantidad = ? WHERE nombre = ?", (nueva_cantidad, nombre_producto))

    # Registrar movimiento
    momento = obtener_momento_actual(cursor)
    cursor.execute('''
        INSERT INTO movimientos (producto, tipo, cantidad, stock_resultante, momento)
        VALUES (?, 'venta', ?, ?, ?)
    ''', (nombre_producto, cantidad_venta, nueva_cantidad, momento))

    conexion.commit()
    conexion.close()
    print(f"Se han vendido {cantidad_venta} unidades de '{nombre_producto}'. Nuevo stock: {nueva_cantidad}")



def reporte_inventario(nombre_db):
    """
    Muestra un reporte del inventario de productos:
    - Tabla con productos con stock > 0 (nombre, stock, valor total)
    - Total del valor del inventario
    - Listado numerado de productos agotados (cantidad = 0)
    - Si no hay productos registrados, lo informa

    Args:
        nombre_db (str): Nombre del archivo de la base de datos

    Returns:
        None
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    cursor.execute("SELECT nombre, cantidad, precio FROM productos")
    productos = cursor.fetchall()

    if not productos:
        print("No existen productos registrados en el inventario.")
        conexion.close()
        return

    # Separar productos con y sin stock
    productos_con_stock = [p for p in productos if p[1] > 0]
    productos_sin_stock = [p[0] for p in productos if p[1] == 0]

    if not productos_con_stock:
        print("Todos los productos están agotados. No hay stock disponible.\n")
    else:
        print("Inventario actual (productos con stock):\n")
        print("| {:<30} | {:>8} | {:>12} |".format("Producto", "Stock", "Valor Total"))
        print("|" + "-"*32 + "|" + "-"*10 + "|" + "-"*14 + "|")

        total_inventario = 0.0

        for nombre, cantidad, precio in productos_con_stock:
            valor_total = cantidad * precio
            total_inventario += valor_total
            print("| {:<30} | {:>8} | {:>12.2f} |".format(nombre, cantidad, valor_total))

        print("\nValor total del inventario: ${:.2f}".format(total_inventario))

    # Mostrar productos agotados solo si hay alguno
    if productos_sin_stock and productos_con_stock:
        print("\nProductos agotados:")
        for i, nombre in enumerate(productos_sin_stock):
            print(f"{i+1}. {nombre}")
    elif productos_sin_stock and not productos_con_stock:
        print("Productos agotados:")
        for i, nombre in enumerate(productos_sin_stock):
            print(f"{i+1}. {nombre}")

    conexion.close()

def filtrar_productos(nombre_db):
    """
    Permite al usuario aplicar distintos filtros para ver productos con nombre y descripción.
    Filtros disponibles: por categoría, por rango de precio, o por cantidad mínima disponible.

    Args:
        nombre_db (str): Nombre del archivo de la base de datos.

    Returns:
        None
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    print("\n🔍 ¿Cómo deseas filtrar los productos?")
    print("1. Por categoría")
    print("2. Por rango de precio")
    print("3. Por cantidad disponible mínima")
    opcion = input("Elige una opción (1-3): ").strip()

    if opcion == "1":
        mostrar_categorias(nombre_db)
        categoria = input("Ingresa el nombre de la categoría: ").strip()
        cursor.execute('''
            SELECT productos.nombre, productos.descripcion
            FROM productos
            JOIN categorias ON productos.categoria_id = categorias.id
            WHERE categorias.nombre = ?
        ''', (categoria,))
    elif opcion == "2":
        try:
            precio_min = float(input("Precio mínimo: ").strip())
            precio_max = float(input("Precio máximo: ").strip())
            cursor.execute('''
                SELECT nombre, descripcion
                FROM productos
                WHERE precio BETWEEN ? AND ?
            ''', (precio_min, precio_max))
        except ValueError:
            print("Error: Debes ingresar valores numéricos válidos para el precio.")
            conexion.close()
            return
    elif opcion == "3":
        try:
            cantidad_min = int(input("Cantidad mínima disponible: ").strip())
            cursor.execute('''
                SELECT nombre, descripcion
                FROM productos
                WHERE cantidad >= ?
            ''', (cantidad_min,))
        except ValueError:
            print("Error: Debes ingresar un número válido para la cantidad.")
            conexion.close()
            return
    else:
        print("Opción inválida.")
        conexion.close()
        return

    resultados = cursor.fetchall()

    if not resultados:
        print("\nNo se encontraron productos con ese criterio.")
    else:
        print("\nResultados de la búsqueda:")
        print("| {:<30} | {:<50} |".format("Nombre del Producto", "Descripción"))
        print("|" + "-"*32 + "|" + "-"*52 + "|")
        for nombre, descripcion in resultados:
            print("| {:<30} | {:<50} |".format(nombre, descripcion[:50]))

    conexion.close()


def obtener_momento_actual(cursor):
    """
    Obtiene el siguiente número de 'momento' basado en el valor máximo actual en la tabla movimientos.

    Args:
        cursor: Cursor de la conexión SQLite.

    Returns:
        int: Siguiente valor de momento.
    """
    cursor.execute("SELECT MAX(momento) FROM movimientos")
    max_momento = cursor.fetchone()[0]
    return (max_momento or 0) + 1

def ver_ultimos_movimientos(nombre_db, num_movimientos):
    """
    Muestra los últimos N movimientos registrados en la base de datos, ordenados del más reciente al más antiguo.

    Args:
        nombre_db (str): Nombre del archivo de la base de datos.
        num_movimientos (int): Número de últimos movimientos a mostrar.

    Returns:
        None
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    cursor.execute('''
        SELECT producto, tipo, cantidad, stock_resultante, momento
        FROM movimientos
        ORDER BY momento DESC
        LIMIT ?
    ''', (num_movimientos,))
    movimientos = cursor.fetchall()

    if not movimientos:
        print("No hay movimientos registrados.")
        conexion.close()
        return

    print(f"\nÚltimos {min(len(movimientos), num_movimientos)} movimientos:")
    print("| {:<25} | {:<8} | {:>8} | {:>16} | {:>8} |".format(
        "Producto", "Tipo", "Cantidad", "Stock Resultante", "Momento"
    ))
    print("|" + "-"*27 + "|" + "-"*10 + "|" + "-"*10 + "|" + "-"*18 + "|" + "-"*10 + "|")

    for producto, tipo, cantidad, stock, momento in movimientos:
        print("| {:<25} | {:<8} | {:>8} | {:>16} | {:>8} |".format(
            producto, tipo, cantidad, stock, momento
        ))

    conexion.close()

def poblar_productos(nombre_db, productos):
    """
    Inserta productos desde un DataFrame a la base de datos.
    Verifica o crea las categorías necesarias antes de insertar cada producto.

    Args:
        nombre_db (str): Nombre del archivo de la base de datos.
        df (dict): diccionario con columnas: nombre, descripcion, cantidad, precio, categoria

    Returns:
        None
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    for prod in productos:
        nombre = prod["nombre"]
        descripcion = prod["descripcion"]
        cantidad = int(prod["cantidad"])
        precio = float(prod["precio"])
        categoria_nombre = prod["categoria"]

        # Verificar o insertar la categoría
        cursor.execute("SELECT id FROM categorias WHERE nombre = ?", (categoria_nombre,))
        categoria = cursor.fetchone()
        if not categoria:
            cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (categoria_nombre,))
            categoria_id = cursor.lastrowid
        else:
            categoria_id = categoria[0]

        # Verificar si el producto ya existe
        cursor.execute("SELECT id FROM productos WHERE nombre = ?", (nombre,))
        existe = cursor.fetchone()
        if existe:
            continue

        # Insertar producto
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, descripcion, cantidad, precio, categoria_id))

    conexion.commit()
    conexion.close()

def limpiar_base_datos(nombre_db):
    """
    Elimina todos los registros de las tablas 'movimientos', 'productos' y 'categorias'.
    No afecta la tabla de usuarios.

    Args:
        nombre_db (str): Nombre del archivo de la base de datos.

    Returns:
        None
    """
    conexion = sqlite3.connect(nombre_db)
    cursor = conexion.cursor()

    try:
        cursor.execute("DELETE FROM movimientos")
        cursor.execute("DELETE FROM productos")
        cursor.execute("DELETE FROM categorias")
        conexion.commit()
    except Exception as e:
        print(f"Error al limpiar la base de datos: {e}")
    finally:
        conexion.close()