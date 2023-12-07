#!/usr/local/bin/python3.12

import os
import time
import pygame
from tkinter import *
from tkinter import ttk, filedialog
from pygame import mixer
from threading import Thread

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Music Player")
        self.window.resizable(0, 0)
        self.window.config(bg="black")
        self.previous_volume = 1.0
        self.duration = 0
        self.playing = False  # Indicateur si la musique est en cours de lecture

        # Initialise la largeur de la fenêtre
        self.width_window = 0
        # Initialise le chemin du dossier
        self.folder_path = None

        # Initialise le module mixer
        mixer.init()

        # Appelle la fonction pour ajuster la taille de la fenêtre
        self.adjust_window()

        self.in_window()

        self.window.mainloop()

    # Fonction pour ajuster la taille de la fenêtre
    def adjust_window(self):
        # Obtention de la taille de l'écran
        width_screen = self.window.winfo_screenwidth()
        height_screen = self.window.winfo_screenheight()

        # Calcul d'une taille raisonnable pour la fenêtre (par exemple, 80% de la taille de l'écran)
        self.width_window = int(0.8 * width_screen)
        height_window = int(0.8 * height_screen)

        # Définir la taille de la fenêtre
        self.window.geometry(f"{self.width_window}x{height_window}")

    def in_window(self):
        # Titre de l'App
        title_window = Label(self.window, text="Music Player", fg="white", bg="black", font=("", 60, "bold"))
        title_window.pack(pady=30, padx=10, side=TOP)

        frame = Frame(self.window, bg="black")
        frame.pack(expand=True, fill="both")

        # Bouton pour ouvrir un fichier
        open_file_button = Button(frame, text="Open File", font=("", 20), command=self.open_file_button_click)
        open_file_button.pack(side=TOP, pady=10)

        # Rectangle de visualisation des pistes audios ou logo musique
        cadre_pistes_audios = ttk.Frame(frame, width=int(0.8 * self.width_window),
                                        height=int(0.4 * self.window.winfo_height()),
                                        relief='solid', borderwidth=2)
        cadre_pistes_audios.pack(expand=True, fill="both", pady=10, padx=30)

        # Listbox pour afficher les fichiers MP3
        self.file_listbox = Listbox(cadre_pistes_audios, selectmode=SINGLE, font=("", 16))
        self.file_listbox.pack(expand=True, fill="both")

        # Playback progress bar
        self.progress_bar = ttk.Progressbar(frame, orient='horizontal', mode='determinate', length=800)
        self.progress_bar.pack(pady=10, padx=(0, 10))
        
        # Libellé pour le temps restant
        self.remaining_time_label = Label(frame, text="0:00", fg="white", bg="black", font=("", 16))
        self.remaining_time_label.pack(side=LEFT, pady=10, padx=(0, 10))

        # Libellé pour le temps maximum
        self.max_time_label = Label(frame, text="0:00", fg="white", bg="black", font=("", 16))
        self.max_time_label.pack(side=RIGHT, pady=10, padx=(10, 0))

        # Frame pour les boutons
        button_frame = Frame(frame, bg="black")
        button_frame.pack(side=BOTTOM)

        # Boutons Play, Pause, Stop, Next, Previous, Volume, Mute
        button_icons = ["⏮", "▶", "⏸", "⏹", "⏭", "\U0001f507", "🔉", "🔊"]
        button_commands = [self.previous_button_click, self.play_button_click, self.pause_button_click,
                           self.stop_button_click, self.next_button_click, self.mute_button_click,
                           self.volume_min_button_click, self.volume_max_button_click]

        for icon, command in zip(button_icons, button_commands):
            button = Button(button_frame, text=icon, command=command, font=("", 20))
            button.pack(side=LEFT, pady=100, padx=30)

    def open_file_button_click(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])

        if file_paths:
            self.file_listbox.delete(0, END)  # Efface les éléments précédents dans la Listbox
            for file_path in file_paths:
                mp3_file = os.path.basename(file_path)
                self.file_listbox.insert(END, mp3_file)

            # Sélectionne le premier fichier MP3 dans la Listbox (s'il y en a)
            self.file_listbox.selection_set(0)
            self.file_listbox.activate(0)

            # Met à jour le chemin du dossier (utilisez le répertoire du premier fichier sélectionné)
            self.folder_path = os.path.dirname(file_paths[0])

            # Retourne l'index du premier fichier MP3 dans la Listbox
            return 0
        return None

    def get_audio_duration(self, mp3_file):
        sound = mixer.Sound(os.path.join(self.folder_path, mp3_file))
        return sound.get_length()

    def update_progress_bar(self):
        while self.playing:
            current_time = mixer.music.get_pos() / 1000  # Convertit le temps en secondes
            self.progress_bar["value"] = current_time
            self.remaining_time_label["text"] = self.format_time(int(current_time))
            self.window.update()

    def play_audio_with_progress(self, mp3_file):
        self.duration = self.get_audio_duration(mp3_file)

        minutes = int(self.duration // 60)
        seconds = int(self.duration % 60)
        max_time_str = f"{minutes}:{seconds:02}"
        self.max_time_label["text"] = max_time_str

        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(self.folder_path, mp3_file))
        pygame.mixer.music.play()

        # Lance la lecture avec la barre de progression
        self.playing = True
        progress_thread = Thread(target=self.update_progress_bar, daemon=True)
        progress_thread.start()

    # Ajoutez les méthodes pour les autres boutons avec la logique appropriée
    def previous_button_click(self):
        # Récupère l'index actuel de la piste en cours de lecture
        current_index = self.file_listbox.curselection()

        # Vérifie si une piste est sélectionnée et qu'il y a plus d'une piste
        if current_index and len(current_index) > 0 and current_index[0] > 0:
            # Obtient l'index de la piste précédente
            previous_index = current_index[0] - 1

            # Obtient le nom du fichier de la piste précédente
            previous_file = self.file_listbox.get(previous_index)

            # Charge et joue la piste précédente
            self.play_audio_with_progress(previous_file)

            # Sélectionne la piste précédente dans la Listbox
            self.file_listbox.selection_clear(0, END)
            self.file_listbox.selection_set(previous_index)
            self.file_listbox.activate(previous_index)

    def play_button_click(self):
        if not self.file_listbox.curselection():
            return  # Aucune piste sélectionnée, ne faites rien

        # Obtient l'index de la piste sélectionnée
        selected_index = self.file_listbox.curselection()[0]

        # Obtient le nom du fichier de la piste sélectionnée
        selected_file = self.file_listbox.get(selected_index)

        if hasattr(self, "paused_time") and self.paused_time is not None:
            # Reprend la musique à partir de la position mémorisée
            pygame.mixer.music.unpause()
            self.playing = True
            progress_thread = Thread(target=self.update_progress_bar, daemon=True)
            progress_thread.start()
        else:
            # Joue la piste sélectionnée avec la barre de progression
            self.play_audio_with_progress(selected_file)

    def pause_button_click(self):
        if not self.playing:
            return  # Aucune musique en cours de lecture, donc ne faites rien

        # Mémorise la position actuelle avant de mettre en pause
        current_time = mixer.music.get_pos() / 1000

        # Met en pause la musique
        pygame.mixer.music.pause()

        # Stocke la position actuelle pour la reprise
        self.paused_time = current_time

    def stop_button_click(self):
        # Arrête la lecture de la piste en cours
        pygame.mixer.music.stop()
        self.playing = False

    def next_button_click(self):
        # Récupère l'index actuel de la piste en cours de lecture
        current_index = self.file_listbox.curselection()

        # Vérifie s'il y a une piste sélectionnée et qu'il y a plus d'une piste
        if current_index and len(current_index) > 0 and current_index[0] < self.file_listbox.size() - 1:
            # Obtient l'index de la piste suivante
            next_index = current_index[0] + 1

            # Obtient le nom du fichier de la piste suivante
            next_file = self.file_listbox.get(next_index)

            # Charge et joue la piste suivante
            self.play_audio_with_progress(next_file)

            # Sélectionne la piste suivante dans la Listbox
            self.file_listbox.selection_clear(0, END)
            self.file_listbox.selection_set(next_index)
            self.file_listbox.activate(next_index)

    def mute_button_click(self):
        # Vérifie si la musique est actuellement en mode muet
        if pygame.mixer.music.get_volume() == 0.0:
            # Si c'est le cas, rétablir le volume précédent
            pygame.mixer.music.set_volume(self.previous_volume)
        else:
            # Sinon, sauvegarder le volume actuel et mettre en mode muet
            self.previous_volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(0.0)

    def volume_max_button_click(self):
        # Obtient le volume actuel
        current_volume = pygame.mixer.music.get_volume()

        # Augmente le volume de 10% (vous pouvez ajuster cela selon vos préférences)
        new_volume = min(current_volume + 0.1, 1.0)

        # Définit le nouveau volume
        pygame.mixer.music.set_volume(new_volume)

    def volume_min_button_click(self):
        # Obtient le volume actuel
        current_volume = pygame.mixer.music.get_volume()

        # Diminue le volume de 10% (vous pouvez ajuster cela selon vos préférences)
        new_volume = max(current_volume - 0.1, 0.0)

        # Définit le nouveau volume
        pygame.mixer.music.set_volume(new_volume)

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes)}:{seconds:02}"

app = App()