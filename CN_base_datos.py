import mysql.connector

def conectar(host, usuario, contraseña, base_datos,puerto):
    # Función para conectar a la base de datos
    return mysql.connector.connect(
        host=host,
        user=usuario,
        password=contraseña,
        database=base_datos,
        port=puerto
    )

def crear_tabla(conexion):
    # Función para crear una tabla en la base de datos
    create_table_query = """
    CREATE TABLE IF NOT EXISTS mi_tabla (
        id INT AUTO_INCREMENT PRIMARY KEY,
        columna1 VARCHAR(255),
        columna2 VARCHAR(255)
    )
    """
    with conexion.cursor() as cursor:
        cursor.execute(create_table_query)
        print("Tabla creada correctamente.")

def insertar_datos(conexion, valores):
    # Función para insertar datos en la base de datos
    insert_query = "INSERT INTO mi_tabla (columna1, columna2) VALUES (%s, %s)"
    with conexion.cursor() as cursor:
        cursor.execute(insert_query, valores)
        conexion.commit()
        print("Datos insertados correctamente.")

def consultar_datos(conexion):
    # Función para consultar datos en la base de datos
    select_query = "SELECT * FROM mi_tabla"
    with conexion.cursor() as cursor:
        cursor.execute(select_query)
        resultados = cursor.fetchall()
        print("Resultados de la consulta:")
        for fila in resultados:
            print(fila)

def main():
    # Parámetros de conexión
    host = "localhost"
    puerto = 3307
    usuario = "root"
    contraseña = "Lozacev209403$"
    base_datos = "placas_info"
  

    # Conectar a la base de datos
    conexion = conectar(host, usuario, contraseña, base_datos,puerto)

    # Crear tabla
    crear_tabla(conexion)

    # Insertar datos
    valores = ("dato1", "dato2")
    insertar_datos(conexion, valores)


    # Consultar datos
    consultar_datos(conexion)

    # Cerrar conexión
    conexion.close()

if __name__ == "__main__":
    main()
