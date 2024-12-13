import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import wave
import pygame
import os
from pydub import AudioSegment

# Inicjalizacja pygame do obsługi dźwięku
pygame.mixer.init()
current_audio = None
library_path = ""
segment_length = 0  # Długość segmentu w sekundach
output_folder = "data/processed_sounds"  # Folder do zapisu przetworzonych dźwięków

# Funkcja do odtwarzania dźwięku
def play_audio():
    if current_audio:
        pygame.mixer.music.load(current_audio)
        pygame.mixer.music.play()

# Funkcja do zatrzymania dźwięku
def stop_audio():
    pygame.mixer.music.stop()

# Funkcja do otwierania pliku i wyświetlania wykresu
def open_file():
    global current_audio
    current_audio = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if current_audio:
        file_name.set(os.path.basename(current_audio))
        plot_waveform(current_audio)

# Funkcja do wyboru folderu biblioteki dźwięków
def select_library_folder():
    global library_path
    library_path = filedialog.askdirectory()
    if library_path:
        library_path_var.set(library_path)

# Funkcja do ustawienia długości segmentu
def set_segment_length():
    global segment_length
    try:
        segment_length = float(segment_length_var.get())
        if segment_length <= 0:
            raise ValueError
        segment_length_var.set(f"{segment_length} sek.")
    except ValueError:
        messagebox.showerror("Błąd", "Długość segmentu musi być liczbą dodatnią.")

# Funkcja do przetwarzania plików dźwiękowych w bibliotece
def process_sounds():
    if not library_path or segment_length <= 0:
        messagebox.showerror("Błąd", "Wybierz bibliotekę i ustaw długość segmentu.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(library_path):
        if filename.endswith(".wav"):
            file_path = os.path.join(library_path, filename)
            sound = AudioSegment.from_wav(file_path)
            # Dostosowanie długości pliku do segmentu
            sound_length_ms = len(sound)
            target_length_ms = segment_length * 1000  # Konwersja na milisekundy

            if sound_length_ms > target_length_ms:
                # Skracamy dźwięk
                sound = sound[:target_length_ms]
            elif sound_length_ms < target_length_ms:
                # Rozciągamy dźwięk
                sound = sound * (target_length_ms // sound_length_ms)

            # Zapisujemy nowy plik
            processed_file_path = os.path.join(output_folder, filename)
            sound.export(processed_file_path, format="wav")
            print(f"Przetworzono: {processed_file_path}")

    messagebox.showinfo("Sukces", "Wszystkie dźwięki zostały przetworzone.")

# Funkcja do wyświetlania wykresu
def plot_waveform(file_path):
    with wave.open(file_path, 'r') as wav_file:
        n_channels, _, _, n_frames, _, _ = wav_file.getparams()
        frames = wav_file.readframes(n_frames)
        audio_data = np.frombuffer(frames, dtype=np.int16)
        if n_channels > 1:
            audio_data = audio_data[::2]

    # Tworzenie wykresu
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(audio_data)
    ax.set_title('Waveform')
    ax.set_xlabel('Sample')
    ax.set_ylabel('Amplitude')

    # Wstawienie wykresu do okna Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

# Tworzenie GUI
root = tk.Tk()
root.title("Analiza Plików Dźwiękowych")
root.geometry("600x600")

# Pola tekstowe
file_name = tk.StringVar()
library_path_var = tk.StringVar()
segment_length_var = tk.StringVar()

tk.Label(root, text="Wybrany plik:").pack()
file_entry = tk.Entry(root, textvariable=file_name, state="readonly", width=50)
file_entry.pack(pady=5)

tk.Label(root, text="Ścieżka do biblioteki:").pack()
library_entry = tk.Entry(root, textvariable=library_path_var, state="readonly", width=50)
library_entry.pack(pady=5)

tk.Label(root, text="Długość segmentu (s):").pack()
segment_length_entry = tk.Entry(root, textvariable=segment_length_var, width=10)
segment_length_entry.pack(pady=5)

# Dodanie przycisków
open_button = tk.Button(root, text="Wybierz plik WAV", command=open_file)
open_button.pack(pady=10)

library_button = tk.Button(root, text="Wybierz bibliotekę dźwięków", command=select_library_folder)
library_button.pack(pady=10)

set_segment_button = tk.Button(root, text="Ustaw długość segmentu", command=set_segment_length)
set_segment_button.pack(pady=10)

process_button = tk.Button(root, text="Przetwórz dźwięki", command=process_sounds)
process_button.pack(pady=10)

play_button = tk.Button(root, text="▶️ Odtwórz", command=play_audio)
play_button.pack(pady=10)

stop_button = tk.Button(root, text="⏹️ Zatrzymaj", command=stop_audio)
stop_button.pack(pady=10)

root.mainloop()
