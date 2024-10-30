import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import qrcode
import io
from tkinter.filedialog import askopenfilename

# Autenticación de Google Drive
def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

drive = authenticate_drive()

# Función para subir archivo a Google Drive
def upload_to_drive(image_path):
    file_drive = drive.CreateFile({'title': 'captura.jpg'})
    file_drive.SetContentFile(image_path)
    file_drive.Upload()
    file_drive.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
    return file_drive['alternateLink']

# Función para generar QR
def generate_qr_code(link):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(link)
    qr.make(fit=True)
    qr_img = qr.make_image(fill="black", back_color="white")
    qr_img.show()

# Clase de la aplicación
class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Seleccionar Cámara")
        self.camera_label = tk.Label(root)
        self.camera_label.pack()
        
        self.cameras = []
        self.selected_camera = tk.StringVar()
        
        # Listar cámaras disponibles
        self.list_cameras()
        
        # Botones
        self.capture_button = tk.Button(root, text="Capturar Foto", command=self.capture_photo)
        self.capture_button.pack()
        
        self.upload_button = tk.Button(root, text="Subir a Google Drive", command=self.upload_photo)
        self.upload_button.pack()
        
        # Lista desplegable
        self.camera_dropdown = ttk.Combobox(root, values=self.cameras, textvariable=self.selected_camera)
        self.camera_dropdown.pack()
        
        # Video Capture
        self.cap = None
        self.photo_path = None
        self.update_frame()

    def list_cameras(self):
        index = 0
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                self.cameras.append(f"Camara {index}")
            cap.release()
            index += 1

    def update_frame(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk)
        self.root.after(10, self.update_frame)

    def capture_photo(self):
        camera_index = int(self.selected_camera.get().split(" ")[1])
        self.cap = cv2.VideoCapture(camera_index)
        ret, frame = self.cap.read()
        if ret:
            self.photo_path = "captura.jpg"
            cv2.imwrite(self.photo_path, frame)
            messagebox.showinfo("Foto Capturada", "Foto tomada con éxito.")

    def upload_photo(self):
        if self.photo_path:
            link = upload_to_drive(self.photo_path)
            messagebox.showinfo("Foto Subida", f"Enlace público: {link}")
            generate_qr_code(link)
        else:
            messagebox.showwarning("Advertencia", "Primero captura una foto.")

# Ejecución de la app
if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()

//todo para revisar
