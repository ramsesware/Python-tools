import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from bs4 import BeautifulSoup
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import os


# Crear ventana principal
root = tk.Tk()
root.title("Herramientas de Ciberseguridad - Modo Oscuro")
root.geometry("1200x900")  # Aumentar tamaño de la ventana
root.configure(bg="#2d2d2d")  # Fondo gris oscuro, estilo "modo oscuro"

# Variable global para almacenar el diccionario seleccionado
diccionario_seleccionado = []
# Variable para controlar la detención del análisis
detener_escaneo = False

# Crear contenedor principal
contenedor = ttk.Frame(root, padding="10")
contenedor.pack(fill="both", expand=True)

# Crear diccionario para almacenar los frames de las herramientas
herramientas_frames = {}

# Ajustar el tamaño de los componentes
font_style = ("Consolas", 16)

# Crear menú
menu = tk.Menu(root, bg="#2d2d2d", fg="lime", activebackground="gray", activeforeground="black", font=font_style)
root.config(menu=menu)

# Crear menú Herramientas
herramientas_menu = tk.Menu(menu, font=font_style, tearoff=0, bg="#2d2d2d", fg="lime")
menu.add_cascade(label="Herramientas", menu=herramientas_menu, font=font_style)
herramientas_menu.add_command(label="Análisis de Directorios Web", command=lambda: cambiar_herramienta("analisis_directorios"))
herramientas_menu.add_command(label="Analisis de Metadatos", command=lambda: cambiar_herramienta("busqueda_imagenes"))

# Frame para el análisis de directorios web
frame_directorios = ttk.Frame(contenedor)
frame_directorios.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Centrar el frame
frame_directorios.config(style="TFrame")
herramientas_frames["analisis_directorios"] = frame_directorios

# Frame para la busqueda de imagenes
frame_imagenes = ttk.Frame(contenedor)
frame_imagenes.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Centrar el frame
frame_imagenes.config(style="TFrame")
herramientas_frames["busqueda_imagenes"] = frame_imagenes

# Función para seleccionar diccionario
def seleccionar_diccionario():
    global diccionario_seleccionado
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, "r") as f:
            diccionario_seleccionado = f.read().splitlines()
        diccionario_label.config(text=f"Diccionario seleccionado: {os.path.basename(filepath)}")  # Mostrar solo el nombre del archivo
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó ningún diccionario")

# Función para realizar las peticiones HTTP
def realizar_peticion(url, directorio):
    full_url = f"{url}/{directorio}"
    response = requests.get(full_url)
    if response.status_code == 200:
        return directorio

# Función para detener el escaneo
def detener_analisis():
    global detener_escaneo
    detener_escaneo = True
    messagebox.showinfo("Escaneo detenido", "El escaneo de directorios ha sido detenido.")

# Función para limpiar el cuadro de texto de resultados
def limpiar_resultados():
    resultado_texto.delete("1.0", tk.END)
    progreso["value"] = 0  # Reiniciar la barra de progreso a 0
    messagebox.showinfo("Resultados limpiados", "El cuadro de texto y la barra de progreso han sido limpiados.")

def buscar_imagenes():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Advertencia", "Por favor, introduce una URL válida.")
        return

    # Ejemplo de lógica para buscar imágenes en una URL
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_links = [img.get('src') for img in soup.find_all('img')]
        if not image_links:
            messagebox.showinfo("Resultado", "No se encontraron imágenes en la URL proporcionada.")
        else:
            for img_link in image_links:
                resultado_texto.insert(tk.END, f"Imagen encontrada: {img_link}\n", "green_text")
                resultado_texto.see(tk.END)
    else:
        messagebox.showwarning("Advertencia", "No se pudo acceder a la URL proporcionada.")


# Función para realizar el análisis de directorios web
def analizar_directorios():
    global detener_escaneo
    detener_escaneo = False  # Resetear el control de detención
    url = url_entry.get()
    if diccionario_seleccionado:
        progreso["maximum"] = len(diccionario_seleccionado)
        
        def realizar_peticiones():
            def peticion_individual(url, directorio):
                if detener_escaneo:  # Si se ha activado la bandera de detención
                    return None
                result = realizar_peticion(url, directorio)
                if result:
                    # Actualiza el área de texto en tiempo real con el directorio encontrado
                    resultado_texto.insert(tk.END, f"Directorio encontrado: {result}\n", "green_text")
                    resultado_texto.see(tk.END)  # Hacer scroll automáticamente al final
                return result

            # Crea un ejecutor para paralelizar las peticiones
            with ThreadPoolExecutor(max_workers=10) as executor:  # 10 hilos para paralelizar
                future_to_directorio = {executor.submit(peticion_individual, url, directorio): directorio for directorio in diccionario_seleccionado}
                
                for i, future in enumerate(future_to_directorio):
                    if detener_escaneo:  # Si se ha activado la bandera de detención, salir del bucle
                        break
                    future.result()  # Bloquea hasta que el thread actual termine
                    
                    # Actualiza la barra de progreso y la interfaz
                    progreso["value"] = i + 1
                    root.update_idletasks()  # Asegura que la interfaz se actualice inmediatamente

            if not detener_escaneo:
                messagebox.showinfo("Finalizado", "Análisis completado.")
        
        thread = threading.Thread(target=realizar_peticiones)
        thread.start()
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó ningún diccionario")

# Función para cambiar de herramienta
def cambiar_herramienta(herramienta):
    # Ocultar todos los frames
    for frame in herramientas_frames.values():
        frame.pack_forget()

    # Mostrar el frame correspondiente a la herramienta seleccionada
    herramientas_frames[herramienta].pack(fill="both", expand=True)


#cambiar_herramienta("analisis_directorios")

# Campo para ingresar la URL
ttk.Label(frame_directorios, text="URL:", font=font_style, foreground="lime", background="#2d2d2d").grid(row=0, column=0, padx=5, pady=5)
url_entry = ttk.Entry(frame_directorios, width=50, font=font_style, foreground="black", background="gray", style="Custom.TEntry")
url_entry.grid(row=0, column=1, padx=5, pady=5)

# Botón para seleccionar diccionario
diccionario_btn = tk.Button(frame_directorios, text="Seleccionar Diccionario", command=seleccionar_diccionario, height="2", width="25", font=font_style, bg="#3c3f41", fg="lime", activebackground="gray", activeforeground="black")
diccionario_btn.grid(row=1, column=0, padx=5, pady=5)

# Etiqueta para mostrar el diccionario seleccionado
diccionario_label = ttk.Label(frame_directorios, text="Diccionario no seleccionado", font=font_style, foreground="lime", background="#2d2d2d")
diccionario_label.grid(row=1, column=1, padx=5, pady=5)

# Botón para iniciar el análisis
analizar_btn = tk.Button(frame_directorios, text="Analizar", command=analizar_directorios, height="2", width="15", font=font_style, bg="#3c3f41", fg="lime", activebackground="gray", activeforeground="black")
analizar_btn.grid(row=2, column=0, padx=5, pady=5)

# Botón para detener el análisis
detener_btn = tk.Button(frame_directorios, text="Detener", command=detener_analisis, height="2", width="15", font=font_style, bg="#3c3f41", fg="lime", activebackground="gray", activeforeground="black")
detener_btn.grid(row=3, column=0, padx=5, pady=5)

# Botón para limpiar los resultados
limpiar_btn = tk.Button(frame_directorios, text="Limpiar", command=limpiar_resultados, height="2", width="15", font=font_style, bg="#3c3f41", fg="lime", activebackground="gray", activeforeground="black")
limpiar_btn.grid(row=3, column=1, padx=5, pady=5)

# Barra de progreso
progreso = ttk.Progressbar(frame_directorios, orient="horizontal", length=500, mode="determinate", style="Custom.Horizontal.TProgressbar")  # Aumentar longitud de la barra
progreso.grid(row=4, columnspan=2, padx=5, pady=5)

# Área de texto con scroll para mostrar resultados
frame_resultado = ttk.Frame(frame_directorios)
frame_resultado.grid(row=5, columnspan=2, padx=5, pady=5)
resultado_texto = tk.Text(frame_resultado, height=20, width=80, font=font_style, bg="#3c3f41", fg="lime", insertbackground="white")  # Aumentar tamaño del área de texto
resultado_texto.tag_configure("green_text", foreground="lime")  # Texto verde suave para destacar resultados
scrollbar = ttk.Scrollbar(frame_resultado, orient="vertical", command=resultado_texto.yview)
resultado_texto.configure(yscrollcommand=scrollbar.set)
resultado_texto.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Frame para la busqueda de imagenes

boton1 = tk.Button(frame_imagenes, text="Botón 1", height=2, width=20, font=font_style, bg="#3c3f41", fg="lime", activebackground="gray", activeforeground="black")
boton1.grid(row=0, column=0, padx=20, pady=20)

boton2 = tk.Button(frame_imagenes, text="Botón 2", height=2, width=20, font=font_style, bg="#3c3f41", fg="lime", activebackground="gray", activeforeground="black")
boton2.grid(row=0, column=1, padx=20, pady=20)

boton3 = tk.Button(frame_imagenes, text="Botón 3", height=2, width=20, font=font_style, bg="#3c3f41", fg="lime", activebackground="gray", activeforeground="black")
boton3.grid(row=1, column=0, padx=20, pady=20)

boton4 = tk.Button(frame_imagenes, text="Botón 4", height=2, width=20, font=font_style, bg="#3c3f41", fg="lime", activebackground="gray", activeforeground="black")
boton4.grid(row=1, column=1, padx=20, pady=20)

# Estilo personalizado para ttk widgets
style = ttk.Style()
style.configure("TFrame", background="#2d2d2d")
style.configure("TLabel", background="#2d2d2d", foreground="lime")
style.configure("TEntry", fieldbackground="#3c3f41", foreground="lime")
style.configure("Custom.Horizontal.TProgressbar", troughcolor="#3c3f41", background="#5a5e62")

root.mainloop()
