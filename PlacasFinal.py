import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image
import pytesseract
import cv2
import mysql.connector

# Ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\josue\Desktop\Algoritmo\programas\Proyecto\tesseract.exe'

# Lista para almacenar registros de placas e IDs
registros = []

# Clase para manejar la base de datos
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
            CREATE TABLE IF NOT EXISTS placas_info (
                id INT AUTO_INCREMENT PRIMARY KEY,
                placa VARCHAR(255),
                nombre VARCHAR(255)
            )
            """
            with self.conexion.cursor() as cursor:
                cursor.execute(create_table_query)
                print("Tabla creada correctamente.")
        except mysql.connector.Error as e:
            print(f"Error al crear la tabla: {e}")

    def insertar_datos(self, placa, nombre):
        try:
            insert_query = "INSERT INTO placas_info (placa, nombre) VALUES (%s, %s)"
            with self.conexion.cursor() as cursor:
                cursor.execute(insert_query, (placa, nombre))
                self.conexion.commit()
                print("Datos insertados correctamente.")
        except mysql.connector.Error as e:
            print(f"Error al insertar datos: {e}")

    def consultar_datos(self):
        try:
            select_query = "SELECT * FROM placas_info"
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

# Instancia global de la base de datos
db = BaseDatos("localhost", "root", "Lozacev209403$", "placas_info", 3307)
db.conectar()
db.crear_tabla()

# Función para manejar el botón de selección de imágenes
def seleccionar_imagenes():
    ruta_imagen = filedialog.askopenfilename()
    if ruta_imagen:
        leer_placa(ruta_imagen)
    else:
        print("No se seleccionó ninguna imagen.")

# Función para leer la placa de una imagen dada
def leer_placa(ruta_imagen):
    try:
        # Preprocesamiento de la imagen
        imagen_placa = cv2.imread(ruta_imagen)
        imagen_placa_gris = cv2.cvtColor(imagen_placa, cv2.COLOR_BGR2GRAY)
        
        # Aplicar operaciones de preprocesamiento adicionales si es necesario
        _, imagen_placa_umbralizada = cv2.threshold(imagen_placa_gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Realizar la detección de regiones de interés (ROIs)
        contornos, _ = cv2.findContours(imagen_placa_umbralizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contorno_placa = max(contornos, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(contorno_placa)
        region_placa = imagen_placa_gris[y:y+h, x:x+w]

        # Reconocimiento de texto con Tesseract solo en la región de la placa
        texto_placa = pytesseract.image_to_string(region_placa)
        
        if texto_placa.strip():  # Verifica si hay texto en la placa
            print("Texto de la placa:", texto_placa)
            registros.append({"Placa": texto_placa, "Nombre": ""})  # Agrega la placa al registro
            mostrar_registros()
        else:
            print("No se pudo leer la placa en", ruta_imagen)
    except Exception as e:
        print("¡Ocurrió un error durante el procesamiento de la imagen", ruta_imagen, ":", str(e))

# Función para manejar el botón de ingreso de ID o nombre
def ingresar_nombre():
    nombre_ingresado = simpledialog.askstring("Ingresar Nombre", "Por favor ingresa el Nombre:")
    if nombre_ingresado:
        registro = registros[-1]  # Último registro
        registro["Nombre"] = nombre_ingresado  # Asocia el nombre a la última placa registrada
        db.insertar_datos(registro["Placa"], registro["Nombre"])  # Inserta los datos en la base de datos
        mostrar_registros()

# Función para mostrar los registros en una ventana
def mostrar_registros():
    # Verificar si la ventana ya está abierta
    if hasattr(mostrar_registros, 'ventana_registros') and mostrar_registros.ventana_registros:
        mostrar_registros.ventana_registros.destroy()  # Si está abierta, destruir la ventana existente

    ventana_registros = tk.Toplevel(root)
    ventana_registros.title("Registros de Placas e IDs")
    
    etiqueta_registros = tk.Label(ventana_registros, text="Placas y Nombres Registrados")
    etiqueta_registros.pack()
    
    for registro in registros:
        tk.Label(ventana_registros, text=f"Placa: {registro['Placa']}, Nombre: {registro['Nombre']}").pack()

    # Guardar la referencia de la ventana para futuras operaciones
    mostrar_registros.ventana_registros = ventana_registros

# Funciones de la GUI original
def abrir_registro():
    ventana_registro = tk.Toplevel(root)
    ventana_registro.title("Registro de Placas")
    ventana_registro.geometry("300x150")
    ventana_registro.configure(bg="#FFFFFF")  # Fondo blanco para ventana
    ventana_registro.attributes('-alpha', 0.95)  # Transparencia para efecto moderno

    # Estilo Neoformismo para botones
    estilo_btn = {'font': ('Arial', 12), 'bg': '#2ECC71', 'fg': '#FFFFFF', 'activebackground': '#27AE60'}

    btn_subir_placa = tk.Button(ventana_registro, text="Subir Imagen de Placa", **estilo_btn, command=seleccionar_imagenes)
    btn_subir_placa.pack(pady=10, padx=20, fill=tk.X)

    btn_subir_id = tk.Button(ventana_registro, text="Ingresar Nombre", **estilo_btn, command=ingresar_nombre)
    btn_subir_id.pack(pady=10, padx=20, fill=tk.X)

def abrir_registros():
    mostrar_registros()

# Crear una ventana tkinter
root = tk.Tk()
root.title("Sistema de Registro de Placas")
root.geometry("400x200")
root.configure(bg="#000000")  # Fondo negro para ventana principal

etiqueta_bienvenida = tk.Label(root, text="Bienvenido", fg="#FFFFFF", bg="#000000", font=("Arial", 24))
etiqueta_bienvenida.pack(pady=20)

btn_registrar = tk.Button(root, text="Registrar Placa Nueva", font=("Arial", 16), command=abrir_registro)
btn_registrar.pack(pady=10)

btn_ver_registros = tk.Button(root, text="Ver Registros de Placas", font=("Arial", 16), command=abrir_registros)
btn_ver_registros.pack(pady=10)

# Ejecutar el bucle de eventos de la ventana
root.mainloop()

# Cerrar la conexión a la base de datos al final
db.cerrar_conexion()
