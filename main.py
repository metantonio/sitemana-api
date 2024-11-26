import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel, Text, Scrollbar
import requests
import json

# Constante de la API key
API_KEY = "602540f74e99dc5183bf563fca795c70"

def show_custom_messagebox(title, message, width=800, height=400):
    # Crear una ventana Toplevel
    top = Toplevel()
    top.title(title)
    top.geometry(f"{width}x{height}")
    
    # Crear un Text widget con scrollbars
    text_area = Text(top, wrap='word', bg="white", fg="black")
    text_area.insert(tk.END, message)
    text_area.config(state=tk.DISABLED)  # Hacer el Text widget de solo lectura

    # Crear y configurar Scrollbar
    scrollbar = Scrollbar(top, command=text_area.yview)
    text_area.config(yscrollcommand=scrollbar.set)
    
    # Colocar Text widget y Scrollbar en la ventana
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def get_daily_report():
    domain_id = domain_id_entry.get()
    url = f"https://api.sitemana.com/v1/dailyreports?apikey={API_KEY}"
    if domain_id:
        url += f"&domainId={domain_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            formatted_data = json.dumps(data, indent=4)
            show_custom_messagebox("Daily Report", formatted_data)
            save_json_to_file(data)
        else:
            messagebox.showerror("Error", f"Failed to fetch data. Status code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def get_last_100_visitors():
    domain_id = domain_id_entry.get()
    if not domain_id:
        messagebox.showwarning("Input Error", "Please enter a domain ID")
        return
    url = f"https://api.sitemana.com/v1/visitors?apikey={API_KEY}&domainId={domain_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            formatted_data = json.dumps(data, indent=4)
            show_custom_messagebox("Visitors", formatted_data)
            save_json_to_file(data)
        else:
            messagebox.showerror("Error", f"Failed to fetch data. Status code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def suppress_account_level():
    email = email_entry.get()
    if not email:
        messagebox.showwarning("Input Error", "Please enter an email")
        return
    url = f"https://api.sitemana.com/v1/suppressContact?apikey={API_KEY}&email={email}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            formatted_data = json.dumps(data, indent=4)
            show_custom_messagebox("Suppress Account Level", formatted_data)
            save_json_to_file(data)
        else:
            messagebox.showerror("Error", f"Failed to suppress contact. Status code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def suppress_domain_level():
    email = email_entry.get()
    host = host_entry.get()
    if not email or not host:
        messagebox.showwarning("Input Error", "Please enter both email and host")
        return
    url = f"https://api.sitemana.com/v1/suppressContact?apikey={API_KEY}&email={email}&host={host}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            formatted_data = json.dumps(data, indent=4)
            show_custom_messagebox("Suppress Domain Level", formatted_data)
            save_json_to_file(data)
        else:
            messagebox.showerror("Error", f"Failed to suppress contact. Status code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def save_json_to_file(data):
    formatted_data = json.dumps(data, indent=4)
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(formatted_data)
        messagebox.showinfo("Success", f"File saved to {file_path}")

# Crear la ventana principal
root = tk.Tk()
root.title("Sitemana API Application with QLX API Key")

# Crear campos de entrada
tk.Label(root, text="Domain ID:").grid(row=0, column=0)
domain_id_entry = tk.Entry(root)
domain_id_entry.grid(row=0, column=1)

tk.Label(root, text="Email:").grid(row=1, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=1, column=1)

tk.Label(root, text="Host:").grid(row=2, column=0)
host_entry = tk.Entry(root)
host_entry.grid(row=2, column=1)

# Crear botones
tk.Button(root, text="Get Daily Report", command=get_daily_report).grid(row=3, column=0, pady=10)
tk.Button(root, text="Get Last 100 Visitors", command=get_last_100_visitors).grid(row=3, column=1, pady=10)
tk.Button(root, text="Suppress Account Level", command=suppress_account_level).grid(row=4, column=0, pady=10)
tk.Button(root, text="Suppress Domain Level", command=suppress_domain_level).grid(row=4, column=1, pady=10)

# Ejecutar el bucle principal de Tkinter
root.mainloop()
