import tkinter as tk
from tkinter import messagebox, font
from datetime import datetime
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Archivo donde se guardarán los registros
archivo = "contability.csv"

# Función para cargar registros previos desde el archivo
def cargar_registros():
    registros = []
    try:
        with open(archivo, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['monto'] = float(row['monto']) # Convertir a float
                registros.append(row)
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}, se creará uno nuevo.")
    return registros

# Función para guardar los registros actuales en el archivo
def guardar_registros(registros):
    with open(archivo, mode='w', newline='') as file:
        fieldnames = ['fecha', 'tipo', 'monto', 'descripcion']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(registros)

# Función para registrar un ingreso o gasto
def registrar(tipo, monto, descripcion):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    registro = {'fecha': fecha, 'tipo': tipo, 'monto': float(monto), 'descripcion': descripcion}
    registros.append(registro)
    actualizar_grafico()
    actualizar_historial()

# Función para mostrar el balance actual
def mostrar_balance():
    total_ingresos = sum(float(r['monto']) for r in registros if r['tipo'] == 'ingreso')
    total_gastos = sum(float(r['monto']) for r in registros if r['tipo'] == 'gasto')
    balance = total_ingresos - total_gastos
    messagebox.showinfo("Balance actual", f"Total de ingresos: {total_ingresos:.2f}\nTotal de gastos: {total_gastos:.2f}\nBalance actual: {balance:.2f}")

# Función para registrar un ingreso a través de la interfaz gráfica
def registrar_ingreso():
    monto = entry_monto_ingreso.get()
    descripcion = entry_descripcion_ingreso.get()
    if monto and descripcion:
        registrar('ingreso', monto, descripcion)
        messagebox.showinfo("Ingreso", "Ingreso registrado con éxito")
        entry_monto_ingreso.delete(0, tk.END)
        entry_descripcion_ingreso.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingresa una cantidad y una descripción")

# Función para registrar un gasto a través de la interfaz gráfica
def registrar_gasto():
    monto = entry_monto_gasto.get()
    descripcion = entry_descripcion_gasto.get()
    if monto and descripcion:
        registrar('gasto', monto, descripcion)
        messagebox.showinfo("Gasto", "Gasto registrado con éxito")
        entry_monto_gasto.delete(0, tk.END)
        entry_descripcion_gasto.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingresa una cantidad y una descripción")

# Función para borrar todos los registros
def borrar_datos():
    global registros
    registros = []
    guardar_registros(registros)
    actualizar_grafico()
    actualizar_historial()
    messagebox.showinfo("Datos Borrados", "Todos los registros han sido borrados.")

# Función para salir y guardar los registros
def salir():
    guardar_registros(registros)
    root.quit()

# Función para actualizar el gráfico y el balance
def actualizar_grafico():
    total_ingresos = sum(float(r['monto']) for r in registros if r['tipo'] == 'ingreso')
    total_gastos = sum(float(r['monto']) for r in registros if r['tipo'] == 'gasto')
    balance = total_ingresos - total_gastos

    # Limpiar el gráfico actual
    ax.clear()

    # Cambiar el fondo de la gráfica
    ax.set_facecolor(color_fondo)

    # Verificar si hay datos para graficar
    if total_ingresos > 0 or total_gastos > 0:
        # Datos para el gráfico de pastel
        datos = [total_ingresos, total_gastos]
        etiquetas = ['Ingresos', 'Gastos']
        colores = ['#4CAF50', '#F44336']  # Verde para ingresos, rojo para gastos

        # Crear gráfico circular
        ax.pie(datos, labels=etiquetas, colors=colores, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Para que el gráfico sea un círculo
    else:
        # Mostrar un gráfico de pastel gris
        datos = [1]  # Un solo segmento
        colores = ['#B0BEC5']  # Color gris
        ax.pie(datos, colors=colores, startangle=90)
        ax.axis('equal')  # Para que el gráfico sea un círculo
        ax.text(0, 0, 'Sin datos', horizontalalignment='center', verticalalignment='center', fontsize=16, color='black')

    # Actualizar el gráfico en la interfaz
    canvas.draw()

    # Mostrar el balance en la etiqueta debajo del gráfico
    label_balance_total.config(text=f"Balance Total: {balance:.2f}")

# Función para actualizar el historial
def actualizar_historial():
    # Limpiar las tablas
    for widget in frame_historial_ingresos.winfo_children():
        widget.destroy()
    for widget in frame_historial_gastos.winfo_children():
        widget.destroy()

    # Crear encabezados de las tablas
    tk.Label(frame_historial_ingresos, text="Descripción", font=('Helvetica', 10, 'bold'), bg=color_fondo, fg=color_texto).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(frame_historial_ingresos, text="Cantidad", font=('Helvetica', 10, 'bold'), bg=color_fondo, fg=color_texto).grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame_historial_gastos, text="Descripción", font=('Helvetica', 10, 'bold'), bg=color_fondo, fg=color_texto).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(frame_historial_gastos, text="Cantidad", font=('Helvetica', 10, 'bold'), bg=color_fondo, fg=color_texto).grid(row=0, column=1, padx=10, pady=5)

    # Llenar las tablas con datos
    fila_ingreso = 1
    fila_gasto = 1
    for r in registros:
        if r['tipo'] == 'ingreso':
            tk.Label(frame_historial_ingresos, text=r['descripcion'], bg=color_fondo, fg=color_texto).grid(row=fila_ingreso, column=0, padx=10, pady=5)
            tk.Label(frame_historial_ingresos, text=f"{r['monto']:.2f}", bg=color_fondo, fg=color_texto).grid(row=fila_ingreso, column=1, padx=10, pady=5)
            fila_ingreso += 1
        elif r['tipo'] == 'gasto':
            tk.Label(frame_historial_gastos, text=r['descripcion'], bg=color_fondo, fg=color_texto).grid(row=fila_gasto, column=0, padx=10, pady=5)
            tk.Label(frame_historial_gastos, text=f"{r['monto']:.2f}", bg=color_fondo, fg=color_texto).grid(row=fila_gasto, column=1, padx=10, pady=5)
            fila_gasto += 1

# Cargar los registros existentes
registros = cargar_registros()

# Crear la ventana principal
root = tk.Tk()
root.title("Contabilidad Personal")

# Ampliar el tamaño de la ventana
root.geometry("1200x500")  # Ventana más amplia

# Colores de la interfaz
color_fondo = "#2E2E2E"  # Color de fondo gris oscuro
color_primario = "#BB86FC"  # Color morado claro
color_secundario = "#03DAC5"  # Color aqua
color_texto = "#FFFFFF"  # Color de texto blanco

# Establecer color de fondo
root.configure(bg=color_fondo)

# Crear un frame principal para dividir la ventana en columnas
frame_principal = tk.Frame(root, padx=10, pady=10, bg=color_fondo)
frame_principal.pack(fill=tk.BOTH, expand=True)

# Crear un frame para la sección de ingreso/gasto
frame_izquierda = tk.Frame(frame_principal, bg=color_fondo, padx=20, pady=20)
frame_izquierda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Ventana de ingreso
label_ingreso = tk.Label(frame_izquierda, text="Registrar Ingreso", font=('Helvetica', 14, 'bold'), bg=color_fondo, fg=color_texto)
label_ingreso.grid(row=1, columnspan=2, pady=10)

label_monto_ingreso = tk.Label(frame_izquierda, text="Cantidad:", bg=color_fondo, fg=color_texto)
label_monto_ingreso.grid(row=2, column=0, pady=5)
entry_monto_ingreso = tk.Entry(frame_izquierda, width=25, font=('Helvetica', 12), bd=2, relief=tk.SUNKEN)
entry_monto_ingreso.grid(row=2, column=1, pady=5)

label_descripcion_ingreso = tk.Label(frame_izquierda, text="Descripción:", bg=color_fondo, fg=color_texto)
label_descripcion_ingreso.grid(row=3, column=0, pady=5)
entry_descripcion_ingreso = tk.Entry(frame_izquierda, width=25, font=('Helvetica', 12), bd=2, relief=tk.SUNKEN)
entry_descripcion_ingreso.grid(row=3, column=1, pady=5)

btn_registrar_ingreso = tk.Button(frame_izquierda, text="Registrar Ingreso", command=registrar_ingreso, bg=color_secundario, fg='black', font=('Helvetica', 12), bd=0)
btn_registrar_ingreso.grid(row=4, columnspan=2, pady=10)

# Ventana de gasto
label_gasto = tk.Label(frame_izquierda, text="Registrar Gasto", font=('Helvetica', 14, 'bold'), bg=color_fondo, fg=color_texto)
label_gasto.grid(row=5, columnspan=2, pady=10)

label_monto_gasto = tk.Label(frame_izquierda, text="Cantidad:", bg=color_fondo, fg=color_texto)
label_monto_gasto.grid(row=6, column=0, pady=5)
entry_monto_gasto = tk.Entry(frame_izquierda, width=25, font=('Helvetica', 12), bd=2, relief=tk.SUNKEN)
entry_monto_gasto.grid(row=6, column=1, pady=5)

label_descripcion_gasto = tk.Label(frame_izquierda, text="Descripción:", bg=color_fondo, fg=color_texto)
label_descripcion_gasto.grid(row=7, column=0, pady=5)
entry_descripcion_gasto = tk.Entry(frame_izquierda, width=25, font=('Helvetica', 12), bd=2, relief=tk.SUNKEN)
entry_descripcion_gasto.grid(row=7, column=1, pady=5)

btn_registrar_gasto = tk.Button(frame_izquierda, text="Registrar Gasto", command=registrar_gasto, bg=color_secundario, fg='black', font=('Helvetica', 12), bd=0)
btn_registrar_gasto.grid(row=8, columnspan=2, pady=10)

# Botón para mostrar el balance actual
btn_balance = tk.Button(frame_izquierda, text="Mostrar Balance", command=mostrar_balance, bg="#2196F3", fg='white', font=('Helvetica', 12), bd=0)
btn_balance.grid(row=9, columnspan=2, pady=10)

# Botón para borrar todos los datos
btn_borrar_datos = tk.Button(frame_izquierda, text="Borrar Todos los Datos", command=borrar_datos, bg="#FF5722", fg='white', font=('Helvetica', 12), bd=0)
btn_borrar_datos.grid(row=10, columnspan=2, pady=10)

# Botón para salir y guardar
btn_salir = tk.Button(frame_izquierda, text="Salir y Guardar", command=salir, bg="#F44336", fg='white', font=('Helvetica', 12), bd=0)
btn_salir.grid(row=11, columnspan=2, pady=10)

# Crear un frame para el gráfico
frame_derecha = tk.Frame(frame_principal, bg=color_fondo, padx=20, pady=20)
frame_derecha.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Gráfico
figura = plt.Figure(figsize=(4, 4), dpi=100)  # Reducir tamaño del gráfico
ax = figura.add_subplot(111)

# Crear el gráfico en un canvas
canvas = FigureCanvasTkAgg(figura, master=frame_derecha)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Etiqueta para mostrar el balance total
label_balance_total = tk.Label(frame_derecha, text="Balance Total: 0.00", font=('Helvetica', 12), bg=color_fondo, fg=color_texto)
label_balance_total.pack(side=tk.BOTTOM, pady=(10, 0))

# Crear un frame para el historial
frame_historial = tk.Frame(frame_principal, padx=10, pady=10, bg=color_fondo)
frame_historial.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Frame para historial de ingresos
frame_historial_ingresos = tk.Frame(frame_historial, padx=10, pady=10, bg=color_fondo)
frame_historial_ingresos.pack(fill=tk.BOTH, expand=True)

# Frame para historial de gastos
frame_historial_gastos = tk.Frame(frame_historial, padx=10, pady=10, bg=color_fondo)
frame_historial_gastos.pack(fill=tk.BOTH, expand=True)

# Títulos de los frames de historial
tk.Label(frame_historial_ingresos, text="Historial de Ingresos", font=('Helvetica', 14, 'bold'), bg=color_fondo, fg=color_primario).pack(pady=10)
tk.Label(frame_historial_gastos, text="Historial de Gastos", font=('Helvetica', 14, 'bold'), bg=color_fondo, fg=color_primario).pack(pady=10)

# Crear las tablas para historial de ingresos y gastos
actualizar_historial()

# Actualizar el gráfico inicialmente
actualizar_grafico()

# Ejecutar la aplicación
root.mainloop()
