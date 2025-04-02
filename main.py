import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel, Text, Scrollbar, StringVar, OptionMenu
import requests
import json
import csv

# Constante de la API key
API_KEY = "602540f74e99dc5183bf563fca795c70"

# Lista de Domain IDs conocidos
KNOWN_DOMAIN_IDS = [
    {"name":"www.qlx.com","id":"1111"}
    ]

# Crear un diccionario para acceder a los IDs por nombre
KNOWN_DOMAIN_DICT = {domain["name"]: domain["id"] for domain in KNOWN_DOMAIN_IDS}

def show_custom_messagebox(title, message, width=900, height=400):
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

def get_domain_id():
    domain_id_text = domain_id_entry.get().strip()
    if domain_id_text:
        return domain_id_text
    else:
        return KNOWN_DOMAIN_DICT[domain_id_var.get()]

def get_daily_report():
    domain_id = get_domain_id()
    url = f"https://api.sitemana.com/v1/dailyreports?apikey={API_KEY}"
    if domain_id:
        url += f"&domainId={domain_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            formatted_data = json.dumps(data, indent=4)
            show_custom_messagebox("Daily Report", formatted_data)
            save_data_to_file(data)
        else:
            messagebox.showerror("Error", f"Failed to fetch data. Status code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def get_last_100_visitors():
    domain_id = get_domain_id()
    if not domain_id:
        messagebox.showwarning("Input Error", "Please enter or select a domain ID")
        return
    url = f"https://api.sitemana.com/v1/visitors?apikey={API_KEY}&domainId={domain_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            formatted_data = json.dumps(data, indent=4)
            show_custom_messagebox("Visitors", formatted_data)
            save_data_to_file(data)
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
            save_data_to_file(data)
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
            save_data_to_file(data)
        else:
            messagebox.showerror("Error", f"Failed to suppress contact. Status code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def suppress_contact_csv():
    host = host_entry.get()
    csv_url = csv_url_entry.get()
    if not csv_url or not host:
        messagebox.showwarning("Input Error", "Please enter both CSV URL and host")
        return
    url = f"https://api.sitemana.com/v1/suppressContactCSV?apikey={API_KEY}"
    payload = {
        "host": host,
        "csv": csv_url
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            formatted_data = json.dumps(data, indent=4)
            show_custom_messagebox("Suppress Contact CSV", formatted_data)
            save_data_to_file(data)
        else:
            messagebox.showerror("Error", f"Failed to suppress contact CSV. Status code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def save_data_to_file(data):
    # Preguntar al usuario si quiere guardar el archivo en formato JSON o CSV
    file_types = [("CSV files", "*.csv"), ("JSON files", "*.json")]
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=file_types)
    if file_path:
        if file_path.endswith('.json'):
            save_json_to_file(data, file_path)
        elif file_path.endswith('.csv'):
            save_csv_to_file(data, file_path)

def save_json_to_file(data, file_path):
    formatted_data = json.dumps(data, indent=4)
    with open(file_path, 'w') as file:
        file.write(formatted_data)
    messagebox.showinfo("Success", f"File saved to {file_path}")

def save_csv_to_file(data, file_path):
    if "results" in data and isinstance(data["results"], list):
        keys = set()
        for entry in data["results"]:
            keys.update(entry.keys())
        keys = list(keys)

        with open(file_path, 'w', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=keys)
            csvwriter.writeheader()
            csvwriter.writerows(data["results"])
        messagebox.showinfo("Success", f"File saved to {file_path}")
    else:
        messagebox.showwarning("Error", "Data does not contain 'results' key or it's not a list.")

# Crear la ventana principal
root = tk.Tk()
root.title("Sitemana API Application with QLX API Key")

# Crear variables de Tkinter
domain_id_var = StringVar(root)
#domain_id_var.set(KNOWN_DOMAIN_IDS[0])  # Establecer el valor predeterminado
domain_id_var.set(list(KNOWN_DOMAIN_DICT.keys())[0]) # New default value

# Crear campos de entrada
tk.Label(root, text="Domain ID:").grid(row=0, column=0)
domain_id_entry = tk.Entry(root)
domain_id_entry.grid(row=0, column=1)
tk.Label(root, text="Or select Domain ID from this websites:").grid(row=1, column=0)
#domain_id_menu = OptionMenu(root, domain_id_var, *KNOWN_DOMAIN_IDS)
domain_id_menu = OptionMenu(root, domain_id_var, *KNOWN_DOMAIN_DICT.keys())
domain_id_menu.grid(row=1, column=1)

tk.Label(root, text="Email:").grid(row=2, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=2, column=1)

tk.Label(root, text="Host:").grid(row=3, column=0)
host_entry = tk.Entry(root)
host_entry.grid(row=3, column=1)

tk.Label(root, text="CSV URL:").grid(row=4, column=0)
csv_url_entry = tk.Entry(root)
csv_url_entry.grid(row=4, column=1)

# Crear botones
tk.Button(root, text="Get Daily Report", command=get_daily_report).grid(row=5, column=0, pady=10)
tk.Button(root, text="Get Last 100 Visitors", command=get_last_100_visitors).grid(row=5, column=1, pady=10)
tk.Button(root, text="Suppress Account Level", command=suppress_account_level).grid(row=6, column=0, pady=10)
tk.Button(root, text="Suppress Domain Level", command=suppress_domain_level).grid(row=6, column=1, pady=10)
tk.Button(root, text="Suppress Contact CSV", command=suppress_contact_csv).grid(row=7, column=0, pady=10)

# Ejecutar el bucle principal de Tkinter
root.mainloop()
