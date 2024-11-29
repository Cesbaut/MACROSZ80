import re
import tkinter as tk
from tkinter import messagebox, filedialog

def expand_macros(input_code):
    # Expansor de macros como antes (sin cambios)
    lines = [line.strip() for line in input_code.split('\n')]
    macros = {}
    expanded_code = []
    in_macro = False
    macro_name = ''
    macro_content = []
    macro_params = []

    for line in lines:
        if ': MACRO' in line:
            in_macro = True
            parts = line.split(':')
            macro_name = parts[0].strip()
            macro_params = [
                param.strip()
                for param in parts[1].replace('MACRO', '').strip().split(',')
            ]
            macro_content = []
            continue
        if line == 'ENDM':
            in_macro = False
            macros[macro_name] = {"content": macro_content, "params": macro_params}
            continue
        if in_macro:
            macro_content.append(line)
        else:
            expanded_code.append(line)

    final_code = []
    for line in expanded_code:
        macro_call_match = re.match(r'^(\w+)\s*(.*)$', line)
        if macro_call_match:
            call_name, args_string = macro_call_match.groups()
            if call_name in macros:
                args = [arg.strip() for arg in args_string.split(',')]
                macro_body = macros[call_name]["content"]
                macro_params = macros[call_name]["params"]

                for macro_line in macro_body:
                    expanded_line = macro_line
                    for index, arg in enumerate(args):
                        macro_arg = macro_params[index]
                        expanded_line = re.sub(rf'\b{macro_arg}\b', arg, expanded_line)
                    final_code.append(expanded_line)
            else:
                final_code.append(line)
        else:
            final_code.append(line)

    return '\n'.join(final_code)

def handle_expand():
    try:
        input_code = input_text.get("1.0", tk.END).strip()
        expanded_code = expand_macros(input_code)
        output_text.delete("1.0", tk.END)
        output_text.insert("1.0", expanded_code)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def copy_to_clipboard():
    expanded_code = output_text.get("1.0", tk.END).strip()
    if expanded_code:
        root.clipboard_clear()
        root.clipboard_append(expanded_code)
        root.update()
        messagebox.showinfo("Copiar", "Código expandido copiado al portapapeles.")
    else:
        messagebox.showwarning("Advertencia", "No hay código expandido para copiar.")

def save_to_file():
    expanded_code = output_text.get("1.0", tk.END).strip()
    if expanded_code:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(expanded_code)
            messagebox.showinfo("Guardar", f"Código expandido guardado en: {file_path}")
    else:
        messagebox.showwarning("Advertencia", "No hay código expandido para guardar.")

def load_from_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "r") as file:
                content = file.read()
                input_text.delete("1.0", tk.END)
                input_text.insert("1.0", content)
                messagebox.showinfo("Cargar", f"Archivo cargado desde: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

# Efecto hover para botones
def on_enter(button):
    button.configure(bg="#0074D9")  # Azul más claro

def on_leave(button):
    button.configure(bg="#005bb5")  # Azul más oscuro

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Expansor de Macros")
root.geometry("800x1000")
root.configure(bg="#000000")

# Estilo global
montserrat_font_large = ("Montserrat", 12)
montserrat_bold_font = ("Montserrat", 14, "bold")

# Crear widgets
frame = tk.Frame(root, padx=10, pady=10, bg="#1c1c1c")
frame.pack(fill=tk.BOTH, expand=True)

load_button = tk.Button(
    frame, text="Importar Archivo", font=montserrat_bold_font, bg="#005bb5", fg="white",
    command=load_from_file, relief="flat", highlightthickness=0
)
load_button.pack(pady=(0, 10), ipadx=10)

# Título input alineado a la izquierda
input_label = tk.Label(frame, text="Código con Macros:", font=montserrat_font_large, bg="#1c1c1c", fg="white", anchor="w")
input_label.pack(fill=tk.X, padx=100)

input_text = tk.Text(frame, height=10, bg="#2b2b2b", fg="white", font=montserrat_font_large, insertbackground="white", wrap=tk.WORD, relief="flat")
input_text.pack(fill=tk.X, expand=True, pady=(0, 10), ipadx=10, padx=100)

expand_button = tk.Button(
    frame, text="Expandir Macros", font=montserrat_bold_font, bg="#005bb5", fg="white",
    command=handle_expand, relief="flat", highlightthickness=0, height=2
)
expand_button.pack(pady=(10, 10), ipadx=10)

# Título output alineado a la izquierda
output_label = tk.Label(frame, text="Código Expandido:", font=montserrat_font_large, bg="#1c1c1c", fg="white", anchor="w")
output_label.pack(fill=tk.X, padx=100)

output_text = tk.Text(frame, height=10, bg="#2b2b2b", fg="white", font=montserrat_font_large, insertbackground="white", wrap=tk.WORD, relief="flat")
output_text.pack(fill=tk.X, expand=True, pady=(0, 10), ipadx=10, padx=100)

button_frame = tk.Frame(frame, bg="#1c1c1c")
button_frame.pack(fill=tk.X, pady=(5, 0))

copy_button = tk.Button(
    button_frame, text="Copiar al Portapapeles", font=montserrat_bold_font, bg="#005bb5", fg="white",
    command=copy_to_clipboard, relief="flat", highlightthickness=0
)
copy_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

save_button = tk.Button(
    button_frame, text="Guardar en Archivo", font=montserrat_bold_font, bg="#005bb5", fg="white",
    command=save_to_file, relief="flat", highlightthickness=0
)
save_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Aplicar hover a botones
for button in [load_button, expand_button, copy_button, save_button]:
    button.bind("<Enter>", lambda e, b=button: on_enter(b))
    button.bind("<Leave>", lambda e, b=button: on_leave(b))

# Iniciar la aplicación
root.mainloop()

