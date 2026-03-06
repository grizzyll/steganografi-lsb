import streamlit as st
from PIL import Image
import io

def text_to_bin(text):
    return ''.join(format(ord(i), '08b') for i in text)

def encode_logic(img, secret_data):
    binary_msg = text_to_bin(secret_data) + '1111111111111110' 
    data_index = 0
    img = img.convert('RGB')
    pixels = list(img.getdata())
    new_pixels = []

    for pixel in pixels:
        pixel = list(pixel)
        for i in range(3): 
            if data_index < len(binary_msg):
                pixel[i] = pixel[i] & ~1 | int(binary_msg[data_index])
                data_index += 1
        new_pixels.append(tuple(pixel))

    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    return new_img

def decode_logic(img):
    img = img.convert('RGB')
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

# --- TAMPILAN WEB ---
st.title("🛡️ Web Steganografi LSB")
st.write("Sembunyikan pesan rahasia di dalam gambar dengan teknik Least Significant Bit.")

menu = ["Penyisipan (Encode)", "Ekstraksi (Decode)"]
choice = st.sidebar.selectbox("Pilih Menu", menu)

if choice == "Penyisipan (Encode)":
    uploaded_file = st.file_uploader("Upload Gambar (PNG)", type=["png"])
    pesan = st.text_input("Masukkan Pesan Rahasia")
    
    if uploaded_file and pesan:
        img = Image.open(uploaded_file)
        if st.button("Proses & Download"):
            result_img = encode_logic(img, pesan)
            buf = io.BytesIO()
            result_img.save(buf, format="PNG")
            st.image(result_img, caption="Hasil Stegano (Siap Download)")
            st.download_button(label="Download Gambar Rahasia", data=buf.getvalue(), file_name="stego_web.png", mime="image/png")

elif choice == "Ekstraksi (Decode)":
    uploaded_file = st.file_uploader("Upload Gambar Stegano", type=["png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        if st.button("Lihat Pesan"):
            rahasia = decode_logic(img)
            st.success(f"Pesan Ditemukan: {rahasia}")