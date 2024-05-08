import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pytesseract
import cv2

# Ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ruisc\OneDrive\Escritorio\tesseract.exe'

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
            registros.append({"Placa": texto_placa, "ID": ""})  # Agrega la placa al registro
            mostrar_registros()
        else:
            print("No se pudo leer la placa en", ruta_imagen)
    except Exception as e:
        print("¡Ocurrió un error durante el procesamiento de la imagen", ruta_imagen, ":", str(e))

# Función para manejar el botón de ingreso de ID
def ingresar_id():
    id_ingresada = tk.simpledialog.askstring("Ingresar ID", "Por favor ingresa la ID:")
    if id_ingresada:
        registros[-1]["ID"] = id_ingresada  # Asocia la ID a la última placa registrada
        mostrar_registros()

# Función para mostrar los registros en una ventana separada
def mostrar_registros():
    ventana_registros = tk.Toplevel(ventana)
    ventana_registros.title("Registros de Placas e IDs")
    
    etiqueta_registros = tk.Label(ventana_registros, text="Placas y IDs Registradas")
    etiqueta_registros.pack()
    
    for registro in registros:
        tk.Label(ventana_registros, text=f"Placa: {registro['Placa']}, ID: {registro['ID']}").pack()

# Crear una ventana tkinter
ventana = tk.Tk()
ventana.title("Seleccionar Imágenes de Placas")

# Botón para seleccionar imágenes
boton_seleccionar = tk.Button(ventana, text="Seleccionar Imagen de Placa", command=seleccionar_imagenes)
boton_seleccionar.pack(padx=20, pady=10)

# Botón para ingresar ID
boton_ingresar_id = tk.Button(ventana, text="Ingresar ID", command=ingresar_id)
boton_ingresar_id.pack(padx=20, pady=10)

# Ejecutar el bucle de eventos de la ventana
ventana.mainloop()
