import tkinter as tk
from tkinter import ttk
import hashlib
import time
from tkinter import messagebox
from tkinter import filedialog

# Función para calcular el hash
def calcular_hash(algoritmo, palabra):
    if algoritmo == 'md5':
        return hashlib.md5(palabra.encode()).hexdigest()
    elif algoritmo == 'sha1':
        return hashlib.sha1(palabra.encode()).hexdigest()
    elif algoritmo == 'sha256':
        return hashlib.sha256(palabra.encode()).hexdigest()
    else:
        raise ValueError(f'Algoritmo de hash no soportado: {algoritmo}')

# Función para crackear la contraseña
def crackear_password(hash_cifrado, diccionario, algoritmo='md5'):
    intentos = 0
    try:
        with open(diccionario, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                palabra = linea.strip()
                intentos += 1
                hash_palabra = calcular_hash(algoritmo, palabra)
                if hash_palabra == hash_cifrado:
                    messagebox.showinfo("Contraseña encontrada", f'Contraseña encontrada: {palabra}\nIntentos realizados: {intentos}')
                    return

        messagebox.showwarning("Contraseña no encontrada", f'Contraseña no encontrada en el diccionario.\nTotal de intentos realizados: {intentos}')
    except FileNotFoundError:
        messagebox.showerror("Error", f'Error: El archivo "{diccionario}" no encontrado.')
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Función para manejar el evento de clic en el botón "Crackear"
def crackear():
    hash_cifrado = hash_entry.get()
    diccionario = diccionario_entry.get()
    algoritmo = algoritmo_combobox.get().lower()
    
    inicio = time.time()
    crackear_password(hash_cifrado, diccionario, algoritmo)
    tiempo_total = time.time() - inicio
    tiempo_label.config(text=f'Tiempo transcurrido: {tiempo_total:.2f} segundos')

# Crear la ventana principal
root = tk.Tk()
root.title("Crackear Contraseña")

# Crear y posicionar los widgets
hash_label = ttk.Label(root, text="Hash cifrado:")
hash_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

hash_entry = ttk.Entry(root, width=40)
hash_entry.grid(row=0, column=1, padx=10, pady=10)

diccionario_label = ttk.Label(root, text="Archivo de diccionario:")
diccionario_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

diccionario_entry = ttk.Entry(root, width=30)
diccionario_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

def buscar_diccionario():
    diccionario_file = filedialog.askopenfilename()
    diccionario_entry.delete(0, tk.END)
    diccionario_entry.insert(0, diccionario_file)

buscar_button = ttk.Button(root, text="Buscar", command=buscar_diccionario)
buscar_button.grid(row=1, column=2, padx=10, pady=10)

algoritmo_label = ttk.Label(root, text="Algoritmo de hash:")
algoritmo_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

algoritmos = ['MD5', 'SHA1', 'SHA256']
algoritmo_combobox = ttk.Combobox(root, values=algoritmos, width=10)
algoritmo_combobox.grid(row=2, column=1, padx=10, pady=10, sticky="w")
algoritmo_combobox.current(0)  # Seleccionar MD5 por defecto

crackear_button = ttk.Button(root, text="Crackear", command=crackear)
crackear_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

tiempo_label = ttk.Label(root, text="")
tiempo_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Ejecutar el bucle principal de la interfaz gráfica
root.mainloop()
