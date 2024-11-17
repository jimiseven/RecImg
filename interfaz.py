from tkinter import Tk, filedialog, Label, Button, StringVar, messagebox
import subprocess

def seleccionar_video():
    video_path.set(filedialog.askopenfilename(filetypes=[("Archivos de Video", "*.mp4;*.avi;*.mov")]))
    
def seleccionar_carpeta_salida():
    carpeta_salida.set(filedialog.askdirectory())

def seleccionar_carpeta_filtrado():
    carpeta_filtrado.set(filedialog.askdirectory())

def ejecutar_extraccion():
    if not video_path.get() or not carpeta_salida.get():
        messagebox.showwarning("Advertencia", "Selecciona un video y una carpeta de salida.")
        return

    try:
        subprocess.run(
            ["python", "extraer_imagenes.py", video_path.get(), carpeta_salida.get()],
            check=True
        )
        messagebox.showinfo("Completado", "Extracción de imágenes finalizada.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Hubo un problema al ejecutar el script de extracción.")

def ejecutar_filtrado():
    if not carpeta_filtrado.get():
        messagebox.showwarning("Advertencia", "Selecciona una carpeta para filtrar imágenes.")
        return

    try:
        subprocess.run(
            ["python", "eliminar_repetidas.py", carpeta_filtrado.get()],
            check=True
        )
        messagebox.showinfo("Completado", "Filtrado de imágenes repetidas finalizado.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Hubo un problema al ejecutar el script de filtrado.")

root = Tk()
root.title("Gestor de Diapositivas")
root.geometry("500x300")

video_path = StringVar()
carpeta_salida = StringVar()
carpeta_filtrado = StringVar()

Label(root, text="Seleccionar video:").pack(pady=5)
Button(root, text="Seleccionar Video", command=seleccionar_video).pack()
Label(root, textvariable=video_path, wraplength=400).pack(pady=5)

Label(root, text="Seleccionar carpeta de salida:").pack(pady=5)
Button(root, text="Seleccionar Carpeta", command=seleccionar_carpeta_salida).pack()
Label(root, textvariable=carpeta_salida, wraplength=400).pack(pady=5)

Button(root, text="Extraer Imágenes", command=ejecutar_extraccion).pack(pady=10)

Label(root, text="Seleccionar carpeta para filtrar imágenes:").pack(pady=5)
Button(root, text="Seleccionar Carpeta", command=seleccionar_carpeta_filtrado).pack()
Label(root, textvariable=carpeta_filtrado, wraplength=400).pack(pady=5)

Button(root, text="Filtrar Imágenes Repetidas", command=ejecutar_filtrado).pack(pady=10)

root.mainloop()
