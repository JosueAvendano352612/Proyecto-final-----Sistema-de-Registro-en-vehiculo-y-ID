import mysql.connector

class BaseDatos:
    def __init__(self, host, usuario, contraseña, base_datos, puerto=3306):
        self.host = host
        self.usuario = usuario
        self.contraseña = contraseña
        self.base_datos = base_datos
        self.puerto = puerto
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.contraseña,
                database=self.base_datos,
                port=self.puerto
            )
            print("Conexión establecida correctamente.")
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def crear_tabla(self):
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS mi_tabla (
                id INT AUTO_INCREMENT PRIMARY KEY,
                columna1 VARCHAR(255),
                columna2 VARCHAR(255)
            )
            """
            with self.conexion.cursor() as cursor:
                cursor.execute(create_table_query)
                print("Tabla creada correctamente.")
        except mysql.connector.Error as e:
            print(f"Error al crear la tabla: {e}")

    def insertar_datos(self, valores):
        try:
            insert_query = "INSERT INTO mi_tabla (columna1, columna2) VALUES (%s, %s)"
            with self.conexion.cursor() as cursor:
                cursor.execute(insert_query, valores)
                self.conexion.commit()
                print("Datos insertados correctamente.")
        except mysql.connector.Error as e:
            print(f"Error al insertar datos: {e}")

    def consultar_datos(self):
        try:
            select_query = "SELECT * FROM mi_tabla"
            with self.conexion.cursor() as cursor:
                cursor.execute(select_query)
                resultados = cursor.fetchall()
                print("Resultados de la consulta:")
                for fila in resultados:
                    print(fila)
        except mysql.connector.Error as e:
            print(f"Error al consultar datos: {e}")

    def cerrar_conexion(self):
        try:
            self.conexion.close()
            print("Conexión cerrada correctamente.")
        except mysql.connector.Error as e:
            print(f"Error al cerrar la conexión: {e}")

def main():
    # Parámetros de conexión
    host = "localhost"
    puerto = 3307
    usuario = "root"
    contraseña = "Lozacev209403$"
    base_datos = "placas_info"

    # Crear instancia de la base de datos
    base_de_datos = BaseDatos(host, usuario, contraseña, base_datos, puerto)

    # Conectar a la base de datos
    base_de_datos.conectar()

    # Crear tabla
    base_de_datos.crear_tabla()

    # Insertar datos
    valores = ("dato1", "dato2")
    base_de_datos.insertar_datos(valores)

    # Consultar datos
    base_de_datos.consultar_datos()

    # Cerrar conexión
    base_de_datos.cerrar_conexion()

if __name__ == "__main__":
    main()
