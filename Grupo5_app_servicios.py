import tkinter as tk
from tkinter import messagebox
import time

# --- 1. BASE DE DATOS DE SERVICIOS ---
# Almacenamos los datos de los proveedores y el tiempo de llegada (en segundos)
SERVICIOS = {
    "Seleccionar Servicio": [], # Opción inicial
    "Plomería": [
        {"nombre": "Juan Pérez", "tel": "362-41234", "email": "juan@plomeria.com", "llegada": None},
        {"nombre": "Ana Gómez", "tel": "362-44321", "email": "ana@plomeria.com", "llegada": None}
    ],
    "Electricista": [
        {"nombre": "Luis Castro", "tel": "362-46789", "email": "luis@electrico.com", "llegada": None},
        {"nombre": "Marta Diaz", "tel": "362-49876", "email": "marta@electrico.com", "llegada": None}
    ],
    "Construcción en Seco": [
        {"nombre": "Empresa DryWall", "tel": "362-41234", "email": "drywall@empresa.com", "llegada": None}
    ],
    # Servicios de Urgencia: tienen un tiempo de llegada definido (en segundos)
    "🚨 URGENCIAS": [
        {"nombre": "Cerrajero 24/7", "tel": "362-40001", "email": "cerrajero@urgencia.com", "llegada": 300}, # 5 minutos
        {"nombre": "Plomero 24/7", "tel": "362-40002", "email": "plomero@urgencia.com", "llegada": 600}      # 10 minutos
    ]
}

# --- 2. VARIABLES DE ESTADO ---
tiempo_restante_segundos = 0
timer_activo = False
proveedor_actual = None


# --- 3. CONFIGURACIÓN DE FUNCIONES ---

def actualizar_timer():
    """Función que maneja el temporizador de cuenta regresiva (solo para urgencias)."""
    global tiempo_restante_segundos, timer_activo

    if timer_activo and tiempo_restante_segundos > 0:
        # Convertir segundos a formato MM:SS
        minutos = tiempo_restante_segundos // 60
        segundos = tiempo_restante_segundos % 60
        tiempo_formateado = f"{minutos:02}:{segundos:02}"
        
        # Actualizar el Label del reloj
        reloj_label.config(text=f"Llegada en: {tiempo_formateado}")
        
        tiempo_restante_segundos -= 1
        
        # Repetir después de 1 segundo
        ventana.after(1000, actualizar_timer)
    elif tiempo_restante_segundos == 0 and timer_activo:
        reloj_label.config(text="¡SERVICIO EN SITIO!")
        timer_activo = False
    else:
        # Si no está activo o es un servicio normal, mostrar la hora actual
        hora_actual = time.strftime('%H:%M:%S')
        reloj_label.config(text=f"Hora Actual: {hora_actual}")


def actualizar_listbox(*args):
    """
    Se llama cuando se cambia la opción del menú desplegable.
    Actualiza la Listbox con los proveedores del servicio seleccionado.
    """
    global timer_activo, proveedor_actual
    
    # Detener cualquier timer activo
    timer_activo = False
    reloj_label.config(text=f"Hora Actual: {time.strftime('%H:%M:%S')}")
    
    servicio_seleccionado = var_servicio.get()
    proveedores = SERVICIOS.get(servicio_seleccionado, [])
    
    # 1. Limpiar Listbox
    lista_proveedores.delete(0, tk.END)
    
    # 2. Rellenar Listbox con nombres
    for p in proveedores:
        lista_proveedores.insert(tk.END, p["nombre"])
        
    # 3. Limpiar acciones y proveedor actual
    proveedor_actual = None
    info_contacto.config(text="Selecciona un proveedor para ver las acciones.")
    
    # Deshabilitar botones de acción hasta que se seleccione un proveedor
    boton_mensaje.config(state=tk.DISABLED)
    boton_llamar.config(state=tk.DISABLED)
    boton_email.config(state=tk.DISABLED)


def seleccionar_proveedor(event):
    """Se llama cuando se hace clic en un proveedor de la Listbox."""
    global proveedor_actual, tiempo_restante_segundos, timer_activo

    seleccion = lista_proveedores.curselection()
    if not seleccion:
        return

    indice = seleccion[0]
    nombre_proveedor = lista_proveedores.get(indice)
    servicio_seleccionado = var_servicio.get()
    proveedores = SERVICIOS.get(servicio_seleccionado, [])
    
    # Buscar el objeto del proveedor
    proveedor_actual = next((p for p in proveedores if p["nombre"] == nombre_proveedor), None)

    if proveedor_actual:
        # Habilitar botones de acción
        boton_mensaje.config(state=tk.NORMAL)
        boton_llamar.config(state=tk.NORMAL)
        boton_email.config(state=tk.NORMAL)
        
        # Mostrar información de contacto
        info_contacto.config(
            text=f"Proveedor: {proveedor_actual['nombre']}\nTel: {proveedor_actual['tel']}\nEmail: {proveedor_actual['email']}",
            fg="darkgreen"
        )
        
        # LÓGICA DEL RELOJ/TIMER DE URGENCIA
        if proveedor_actual["llegada"] is not None:
            # Es un servicio de urgencia: Iniciar el timer
            tiempo_restante_segundos = proveedor_actual["llegada"]
            timer_activo = True
            messagebox.showinfo("¡URGENCIA!", f"Llamando a {proveedor_actual['nombre']}. El tiempo de llegada ha iniciado la cuenta regresiva.")
            actualizar_timer()
        else:
            # Servicio normal: Detener el timer y mostrar hora actual
            timer_activo = False
            actualizar_timer()


# Funciones de las Tareas/Acciones
def simular_accion(accion):
    """Simula las acciones de la lista de tareas."""
    if proveedor_actual:
        nombre = proveedor_actual['nombre']
        contacto = ""
        
        if accion == "mensaje":
            contacto = proveedor_actual['tel']
        elif accion == "llamar":
            contacto = proveedor_actual['tel']
        elif accion == "email":
            contacto = proveedor_actual['email']
            
        messagebox.showinfo(
            "Acción Ejecutada", 
            f"Simulando '{accion.upper()}' a {nombre}.\nContacto usado: {contacto}"
        )
    else:
        messagebox.showwarning("Error", "Primero debes seleccionar un proveedor.")


# --- 4. CONFIGURACIÓN DE LA VENTANA PRINCIPAL ---
ventana = tk.Tk()
ventana.title("Buscador de Servicios - Ejercicio Práctico")
ventana.geometry("800x600")

# Configurar el grid para la expansión
ventana.columnconfigure(0, weight=2)  # Columna de la Lista de Proveedores
ventana.columnconfigure(1, weight=1)  # Columna de Acciones y Reloj
ventana.rowconfigure(1, weight=1)     # Fila de la lista debe expandirse


# --- 5. MENÚ DESPLEGABLE DE SERVICIOS (OptionMenu) ---
frame_menu = tk.Frame(ventana, bg="#f0f0f0", padx=10, pady=10)
frame_menu.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

tk.Label(frame_menu, text="Elige un Servicio:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)

opciones_servicio = list(SERVICIOS.keys())
var_servicio = tk.StringVar(ventana)
var_servicio.set(opciones_servicio[0]) # Opción inicial
var_servicio.trace_add("write", actualizar_listbox) # Vincula el cambio del menú a la función

menu_desplegable = tk.OptionMenu(
    frame_menu,
    var_servicio,
    *opciones_servicio
)
menu_desplegable.config(width=25, font=("Arial", 10))
menu_desplegable.pack(side=tk.LEFT)


# --- 6. RELOJ / TIMER (Label) ---
reloj_label = tk.Label(
    ventana,
    text="Cargando Hora...",
    font=('Arial', 14, 'bold'),
    bg='darkblue',
    fg='white',
    padx=10, pady=5
)
# Posición superior derecha
reloj_label.grid(row=0, column=1, padx=10, pady=10, sticky="ne")
actualizar_timer() # Iniciar el reloj (que luego se convierte en timer)


# --- 7. LISTA DE PROVEEDORES Y BARRA DE DESPLAZAMIENTO ---
frame_listado = tk.Frame(ventana, bd=2, relief=tk.SUNKEN)
# El listado ocupa la columna 0 y se expande
frame_listado.grid(row=1, column=0, rowspan=2, padx=10, pady=5, sticky="nsew") 

scrollbar = tk.Scrollbar(frame_listado)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_proveedores = tk.Listbox(
    frame_listado,
    yscrollcommand=scrollbar.set,
    font=("Arial", 12),
    selectmode=tk.SINGLE # Solo permitir una selección a la vez
)
lista_proveedores.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 
scrollbar.config(command=lista_proveedores.yview)

# Vincula el clic en la lista a la función seleccionar_proveedor
lista_proveedores.bind('<<ListboxSelect>>', seleccionar_proveedor)


# --- 8. BARRA DE TAREAS / ACCIONES DE CONTACTO ---
frame_acciones = tk.Frame(ventana, bd=2, relief=tk.GROOVE, padx=10, pady=10)
frame_acciones.grid(row=1, column=1, padx=10, pady=5, sticky="nwe")

tk.Label(frame_acciones, text="-- Opciones de Contacto --", font=("Arial", 10, "italic")).pack(pady=5)

# Área para mostrar la información del contacto
info_contacto = tk.Label(frame_acciones, text="Selecciona un proveedor...", justify=tk.LEFT, fg="gray")
info_contacto.pack(pady=10)

# Botones de Acción (Simulación de "Lista de Tareas")
boton_mensaje = tk.Button(frame_acciones, text="💬 Mandar Mensaje (WhatsApp)", command=lambda: simular_accion("mensaje"), state=tk.DISABLED, width=30)
boton_mensaje.pack(pady=5)

boton_llamar = tk.Button(frame_acciones, text="📞 Llamar a la Persona", command=lambda: simular_accion("llamar"), state=tk.DISABLED, width=30)
boton_llamar.pack(pady=5)

boton_email = tk.Button(frame_acciones, text="📧 Mandar Email", command=lambda: simular_accion("email"), state=tk.DISABLED, width=30)
boton_email.pack(pady=5)


# --- 9. INICIO DEL BUCLE PRINCIPAL ---
actualizar_listbox() # Cargar la lista inicial al inicio
ventana.mainloop()
