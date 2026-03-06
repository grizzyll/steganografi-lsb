import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def text_to_bin(text):
    # Mengubah teks menjadi biner
    return ''.join(format(ord(i), '08b') for i in text)

def encode_logic(img_path, secret_data, save_path):
    img = Image.open(img_path)
    binary_msg = text_to_bin(secret_data) + '1111111111111110' 
    
    data_index = 0
    pixels = list(img.getdata())
    new_pixels = []

    for pixel in pixels:
        pixel = list(pixel)
        for i in range(3): 
            if data_index < len(binary_msg):
                pixel[i] = pixel[i] & ~1 | int(binary_msg[data_index])
                data_index += 1
        new_pixels.append(tuple(pixel))

    img.putdata(new_pixels)
    img.save(save_path)
    messagebox.showinfo("Sukses", f"Pesan berhasil disimpan di:\n{save_path}")

def decode_logic(img_path):
    img = Image.open(img_path)
    pixels = list(img.getdata())
    binary_msg = ""
    for pixel in pixels:
        for i in range(3):
            binary_msg += str(pixel[i] & 1)

    end_marker = "1111111111111110"
    if end_marker in binary_msg:
        binary_msg = binary_msg[:binary_msg.index(end_marker)]
    
    message = ""
    for i in range(0, len(binary_msg), 8):
        byte = binary_msg[i:i+8]
        message += chr(int(byte, 2))
    return message

# --- FUNGSI UI ---
def open_encode_window():
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if file_path:
        pesan = entry_pesan.get()
        if not pesan:
            messagebox.showwarning("Peringatan", "Isi pesan dulu!")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".png")
        if save_path:
            encode_logic(file_path, pesan, save_path)

def open_decode_window():
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if file_path:
        hasil = decode_logic(file_path)
        messagebox.showinfo("Pesan Rahasia", f"Isi Pesan: {hasil}")

# --- SETUP WINDOW ---
root = tk.Tk()
root.title("Stegano LSB Project")
root.geometry("400x300")

tk.Label(root, text="STEGANOGRAFI LSB", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Masukkan Pesan (untuk Encode):").pack()
entry_pesan = tk.Entry(root, width=40)
entry_pesan.pack(pady=5)

tk.Button(root, text="Pilih Gambar & Sembunyikan Pesan", command=open_encode_window, bg="lightblue").pack(pady=10)
tk.Button(root, text="Pilih Gambar & Lihat Pesan", command=open_decode_window, bg="lightgreen").pack(pady=10)

root.mainloop()