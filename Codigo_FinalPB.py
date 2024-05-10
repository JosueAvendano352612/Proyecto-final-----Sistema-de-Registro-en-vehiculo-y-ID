import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image
import pytesseract
import cv2

# Ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\josue\Desktop\Algoritmo\programas\Proyecto\tesseract.exe'

# Lista para almacenar registros de placas e IDs
registros = []

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
        registros[-1]["Nombre"] = nombre_ingresado  # Asocia el nombre a la última placa registrada
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
