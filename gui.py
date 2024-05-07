import tkinter as tk

def abrir_registro():
    ventana_registro = tk.Toplevel(root)
    ventana_registro.title("Registro de Placas")
    ventana_registro.geometry("300x150")
    ventana_registro.configure(bg="#FFFFFF")  # Fondo blanco para ventana
    ventana_registro.attributes('-alpha', 0.95)  # Transparencia para efecto moderno

    # Estilo Neoformismo para botones
    estilo_btn = {'font': ('Arial', 12), 'bg': '#2ECC71', 'fg': '#FFFFFF', 'activebackground': '#27AE60'}

    btn_subir_placa = tk.Button(ventana_registro, text="Subir Imagen de Placa", **estilo_btn)
    btn_subir_placa.pack(pady=10, padx=20, fill=tk.X)

    btn_subir_id = tk.Button(ventana_registro, text="Subir Imagen de ID", **estilo_btn)
    btn_subir_id.pack(pady=10, padx=20, fill=tk.X)

def abrir_registros():
    ventana_registros = tk.Toplevel(root)
    ventana_registros.title("Registros de Placas")
    ventana_registros.geometry("600x400")
    # Agrega los elementos para mostrar los registros aquí

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

root.mainloop()
