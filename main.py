import tkinter as tk
from tkinter import messagebox
import requests

def make_api_call():
    url = "https://api.ejemplo.com/data"  # Cambia esto a tu API
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            messagebox.showinfo("API Response", f"Data: {data}")
        else:
            messagebox.showerror("Error", f"Failed to fetch data. Status code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación con API")

# Crear un botón que haga la llamada a la API
button = tk.Button(root, text="Llamar a la API", command=make_api_call)
button.pack(pady=20)

# Ejecutar el bucle principal de Tkinter
root.mainloop()
