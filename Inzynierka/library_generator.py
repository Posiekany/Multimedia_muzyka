import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from scipy.io.wavfile import write
import os

def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_var.set(folder_selected)


def clear_folder(folder):
    # Usuwanie wszystkich plików w folderze
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Nie udało się usunąć {file_path}: {e}")


def generate_and_save_sounds():
    folder = folder_var.get()
    duration = duration_var.get()
    freq_min = freq_min_var.get()
    freq_max = freq_max_var.get()
    num_sounds = num_sounds_var.get()

    if not folder or duration <= 0 or freq_min <= 0 or freq_max <= 0 or num_sounds <= 0:
        messagebox.showerror("Błąd", "Upewnij się, że wszystkie parametry są poprawne.")
        return

    clear_folder(folder)

    sample_rate = 44100  # Częstotliwość próbkowania (44,1 kHz - standard CD)
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)  # Oś czasu

    # Generowanie dźwięków
    for i in range(num_sounds):
        freq = np.random.randint(freq_min, freq_max + 1)  # Losowa częstotliwość
        waveform = 0.5 * np.sin(2 * np.pi * freq * t)  # Generowanie fali sinusoidalnej
        waveform = np.int16(waveform * 32767)  # Konwersja do 16-bitów

        # Tworzenie i zapisywanie pliku WAV
        file_name = f"sound_{i + 1}_{freq}Hz.wav"
        file_path = os.path.join(folder, file_name)
        write(file_path, sample_rate, waveform)
        print(f"Zapisano: {file_path}")

    messagebox.showinfo("Sukces", f"Wygenerowano {num_sounds} dźwięków.")

# Główne okno aplikacji
root = tk.Tk()
root.title("Generator Dźwięków")

# Zmienna dla folderu
folder_var = tk.StringVar()

# Tworzenie i rozmieszczanie elementów interfejsu
tk.Label(root, text="Wybierz folder zapisu:").grid(row=0, column=0, sticky="w")
tk.Button(root, text="Wybierz folder", command=select_folder).grid(row=0, column=1)
tk.Entry(root, textvariable=folder_var, width=40).grid(row=0, column=2)

tk.Label(root, text="Długość dźwięku (s):").grid(row=1, column=0, sticky="w")
duration_var = tk.DoubleVar()
tk.Entry(root, textvariable=duration_var).grid(row=1, column=1)

tk.Label(root, text="Częstotliwość minimalna (Hz):").grid(row=2, column=0, sticky="w")
freq_min_var = tk.IntVar()
tk.Entry(root, textvariable=freq_min_var).grid(row=2, column=1)

tk.Label(root, text="Częstotliwość maksymalna (Hz):").grid(row=3, column=0, sticky="w")
freq_max_var = tk.IntVar()
tk.Entry(root, textvariable=freq_max_var).grid(row=3, column=1)

tk.Label(root, text="Ilość dźwięków:").grid(row=4, column=0, sticky="w")
num_sounds_var = tk.IntVar()
tk.Entry(root, textvariable=num_sounds_var).grid(row=4, column=1)

tk.Button(root, text="Zatwierdź", command=generate_and_save_sounds).grid(row=5, column=1, pady=10)

# Uruchomienie pętli głównej
root.mainloop()
