import tkinter as tk
from tkinter import filedialog
from PIL import Image
import pytesseract
import pytesseract

# Especifica la ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ruisc\OneDrive\Escritorio\tesseract.exe'

# Función para manejar el botón de selección de imágenes
def seleccionar_imagenes():
    rutas_imagenes = filedialog.askopenfilenames()
    if rutas_imagenes:
        for ruta_imagen in rutas_imagenes:
            leer_placa(ruta_imagen)
    else:
        print("No se seleccionaron imágenes.")

# Función para leer la placa de una imagen dada
def leer_placa(ruta_imagen):
    try:
        imagen_placa = Image.open(ruta_imagen)
        texto_placa = pytesseract.image_to_string(imagen_placa)
        if texto_placa.strip():  # Verifica si hay texto en la placa
            print("Texto de la placa:", texto_placa)
            # Aquí puedes agregar la lógica para el registro del vehículo utilizando el texto de la placa
        else:
            print("No se pudo leer la placa en", ruta_imagen)
    except Exception as e:
        print("¡Ocurrió un error durante el procesamiento de la imagen", ruta_imagen, ":", str(e))

# Crear una ventana tkinter
ventana = tk.Tk()
ventana.title("Seleccionar Imágenes de Placas")

# Botón para seleccionar imágenes
boton_seleccionar = tk.Button(ventana, text="Seleccionar Imágenes", command=seleccionar_imagenes)
boton_seleccionar.pack(padx=20, pady=10)

# Ejecutar el bucle de eventos de la ventana
ventana.mainloop()