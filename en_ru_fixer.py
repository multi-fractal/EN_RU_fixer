import tkinter as tk
import pyperclip
import threading
import keyboard

# --- Keyboard layouts ---
en_chars = '`1234567890-=' + 'qwertyuiop[]\\' + 'asdfghjkl;\'zxcvbnm,./'
en_shifted = '~!@#$%^&*()_+' + 'QWERTYUIOP{}|' + 'ASDFGHJKL:"ZXCVBNM<>?'

ru_chars = 'ё1234567890-=' + 'йцукенгшщзхъ\\фывапролджэячсмитьбю.'
ru_shifted = 'Ё!"№;%:?*()_+' + 'ЙЦУКЕНГШЩЗХЪ/ФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,'

en_to_ru_map = str.maketrans(en_chars + en_shifted, ru_chars + ru_shifted)
ru_to_en_map = str.maketrans(ru_chars + ru_shifted, en_chars + en_shifted)

def detect_language(text):
    ru_score = sum(c in ru_chars + ru_shifted for c in text)
    en_score = sum(c in en_chars + en_shifted for c in text)
    return 'en' if en_score > ru_score else 'ru'

def fix_layout(text):
    lang = detect_language(text)
    return text.translate(en_to_ru_map if lang == 'en' else ru_to_en_map)

def fix_clipboard():
    text = pyperclip.paste()
    if not text.strip():
        update_status("Буфер пуст", "orange")
        return
    fixed = fix_layout(text)
    pyperclip.copy(fixed)
    update_status("✅ Исправлено горячей клавишей", "green")

def update_status(message, color="black"):
    status_label.config(text=message, fg=color)

def on_fix_button():
    fix_clipboard()

def listen_hotkey():
    keyboard.add_hotkey('ctrl+shift+q', fix_clipboard)
    keyboard.wait()

# --- GUI ---
root = tk.Tk()
root.title("Исправление раскладки")
root.geometry("360x120")
root.resizable(False, False)

btn = tk.Button(root, text="Исправить буфер обмена", command=on_fix_button, font=("Arial", 12))
btn.pack(pady=15)

status_label = tk.Label(root, text="", font=("Arial", 10))
status_label.pack()

# --- Run the hotkey handler in a separate thread ---
threading.Thread(target=listen_hotkey, daemon=True).start()

root.mainloop()