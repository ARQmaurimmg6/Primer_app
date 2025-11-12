import tkinter as tk
from tkinter import messagebox
import time

# --- 1. CONFIGURACIÓN DE FUNCIONES ---

# Funciones de la Barra de Menú
def mostrar_opcion(opcion):
    """Función que se ejecuta al seleccionar una opción de la barra de menú."""
    messagebox.showinfo("Menú Seleccionado", f"Has seleccionado: {opcion}")

# Función del Reloj
def hora():
    """Obtiene la hora actual y la actualiza en el Label del reloj."""
    # Usando el formato de 24 horas (%H:%M:%S)
    tiempo_actual = time.strftime('%H:%M:%S')
    reloj_label.config(text=tiempo_actual)
    ventana.after(1000, hora)

# Funciones de la Lista de Tareas (Adaptado de tu código)
def agregar_tarea():
    """Añade una tarea del campo de entrada a la Listbox."""
    tarea = ingreso_tarea.get() # Usando tu variable 'ingreso_tarea'
    if tarea:
        # Asegurarse de que 'lista_tareas' esté vinculada a la Scrollbar
        lista_tareas.insert(tk.END, tarea)
        ingreso_tarea.delete(0, tk.END)

def eliminar_tarea():
    """Elimina la tarea seleccionada de la Listbox."""
    seleccion = lista_tareas.curselection() # Usando variable 'lista_tareas'
    if seleccion:
        lista_tareas.delete(seleccion)
    else:
        messagebox.showwarning("Advertencia", "Debes seleccionar una tarea para eliminar.")


# --- 2. CONFIGURACIÓN DE LA VENTANA PRINCIPAL ---
ventana = tk.Tk()
ventana.title("Aplicación Completa")
ventana.geometry("700x500")

# Configurar el grid para la expansión 
ventana.columnconfigure(0, weight=3)  # Listbox/Scrollbar ocupa más espacio
ventana.columnconfigure(1, weight=1)  # Reloj y Controles de Tarea
ventana.rowconfigure(1, weight=1)     # Fila de la lista debe expandirse


# --- 3. BARRA DE MENÚ SUPERIOR (tk.Menu) ---
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)
menu_principal = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label='Principal', menu=menu_principal)
submenu = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label='Opciones', menu=submenu)
submenu.add_command(label='Opción 1', command=lambda: mostrar_opcion('Opción 1'))
submenu.add_command(label='Opción 2', command=lambda: mostrar_opcion('Opción 2'))


# --- 4. RELOJ SIMPLE (tk.Label) ---
reloj_label = tk.Label(
    ventana,
    font=('Arial', 24, 'bold'),
    bg='blue',
    fg='white'
)
reloj_label.grid(row=0, column=1, padx=10, pady=10, sticky="ne") # Posición superior derecha
hora() # Iniciar el reloj


# --- 5. LISTA DE TAREAS Y BARRA DE DESPLAZAMIENTO ---

# Frame contenedor para la lista y la barra (ocupa Fila 1, Columna 0)
marco_lista = tk.Frame(ventana)
marco_lista.grid(row=1, column=0, rowspan=3, padx=10, pady=5, sticky="nsew") 

# Crear la barra de desplazamiento
scrollbar = tk.Scrollbar(marco_lista)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Crear la Listbox (Usando variable: lista_tareas)
lista_tareas = tk.Listbox(
    marco_lista,
    yscrollcommand=scrollbar.set, # Vincula la lista a la scrollbar
    width=50,
    height=15
)
lista_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 

# ¡La vinculación de la scrollbar!
scrollbar.config(command=lista_tareas.yview) 

# Tareas de ejemplo
lista_tareas.insert(tk.END, "Tarea de Ejemplo: Llamar al cliente A")
lista_tareas.insert(tk.END, "Tarea de Ejemplo: Comprar suministros")
for i in range(10):
    lista_tareas.insert(tk.END, f"Tarea Larga {i+1} (para probar Scrollbar)")


# --- 6. CONTROLES DE LA LISTA DE TAREAS (Entrada y Botones) ---
# Se usan variables: ingreso_tarea, boton_agregar, boton_eliminar

# Campo de entrada de la nueva tarea
ingreso_tarea = tk.Entry(ventana, width=30)
ingreso_tarea.grid(row=1, column=1, padx=10, pady=5, sticky="n")

# Botón para añadir
boton_agregar = tk.Button(ventana, text="Agregar Tarea", command=agregar_tarea)
boton_agregar.grid(row=2, column=1, padx=10, pady=5, sticky="n")

# Botón para eliminar
boton_eliminar = tk.Button(ventana, text="Eliminar Tarea", command=eliminar_tarea)
boton_eliminar.grid(row=3, column=1, padx=10, pady=5, sticky="n")


# --- 7. INICIO DEL BUCLE PRINCIPAL ---
ventana.mainloop()