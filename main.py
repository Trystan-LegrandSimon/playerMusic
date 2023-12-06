from tkinter import ttk, filedialog
from pygame import mixer
from tkinter import *
import os

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Music Player")
        self.window.resizable(0, 0)
        self.window.config(bg="black")
        self.previous_volume = 1.0

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
        progress_bar = ttk.Progressbar(frame, orient='horizontal', mode='determinate', length=1000)
        progress_bar.pack()

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
        folder_path = filedialog.askdirectory()
        if folder_path:
            mp3_files = [f for f in os.listdir(folder_path) if f.endswith(".mp3")]
            self.file_listbox.delete(0, END)  # Efface les éléments précédents dans la Listbox
            for mp3_file in mp3_files:
                self.file_listbox.insert(END, mp3_file)

            # Sélectionne le premier fichier MP3 dans la Listbox (s'il y en a)
            if mp3_files:
                self.file_listbox.selection_set(0)
                self.file_listbox.activate(0)

                # Met à jour le chemin du dossier
                self.folder_path = folder_path

            # Retourne l'index du premier fichier MP3 dans la Listbox
            return 0 if mp3_files else None
        return None

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
            
            # Construit le chemin complet du fichier
            file_path = os.path.join(self.folder_path, previous_file)
            
            # Charge et joue la piste précédente
            mixer.music.load(file_path)
            mixer.music.play()

            # Sélectionne la piste précédente dans la Listbox
            self.file_listbox.selection_clear(0, END)
            self.file_listbox.selection_set(previous_index)
            self.file_listbox.activate(previous_index)

    def play_button_click(self):
        # Vérifie s'il y a une piste sélectionnée dans la Listbox
        if self.file_listbox.curselection():
            # Obtient l'index de la piste sélectionnée
            selected_index = self.file_listbox.curselection()[0]

            # Obtient le nom du fichier de la piste sélectionnée
            selected_file = self.file_listbox.get(selected_index)

            # Construit le chemin complet du fichier
            file_path = os.path.join(self.folder_path, selected_file)

            # Charge et joue la piste sélectionnée
            mixer.music.load(file_path)
            mixer.music.play()

    def pause_button_click(self):
        # Met en pause la piste en cours de lecture
        mixer.music.pause()

    def stop_button_click(self):
        # Arrête la lecture de la piste en cours
        mixer.music.stop()

    def next_button_click(self):
        # Récupère l'index actuel de la piste en cours de lecture
        current_index = self.file_listbox.curselection()

        # Vérifie s'il y a une piste sélectionnée et qu'il y a plus d'une piste
        if current_index and len(current_index) > 0 and current_index[0] < self.file_listbox.size() - 1:
            # Obtient l'index de la piste suivante
            next_index = current_index[0] + 1

            # Obtient le nom du fichier de la piste suivante
            next_file = self.file_listbox.get(next_index)

            # Construit le chemin complet du fichier
            file_path = os.path.join(self.folder_path, next_file)

            # Charge et joue la piste suivante
            mixer.music.load(file_path)
            mixer.music.play()

            # Sélectionne la piste suivante dans la Listbox
            self.file_listbox.selection_clear(0, END)
            self.file_listbox.selection_set(next_index)
            self.file_listbox.activate(next_index)

    def mute_button_click(self):
        # Vérifie si la musique est actuellement en mode muet
        if mixer.music.get_volume() == 0.0:
            # Si c'est le cas, rétablir le volume précédent
            mixer.music.set_volume(self.previous_volume)
        else:
            # Sinon, sauvegarder le volume actuel et mettre en mode muet
            self.previous_volume = mixer.music.get_volume()
            mixer.music.set_volume(0.0)

    def volume_max_button_click(self):
        # Obtient le volume actuel
        current_volume = mixer.music.get_volume()

        # Augmente le volume de 10% (vous pouvez ajuster cela selon vos préférences)
        new_volume = min(current_volume + 0.1, 1.0)

        # Définit le nouveau volume
        mixer.music.set_volume(new_volume)

    def volume_min_button_click(self):
        # Obtient le volume actuel
        current_volume = mixer.music.get_volume()

        # Diminue le volume de 10% (vous pouvez ajuster cela selon vos préférences)
        new_volume = max(current_volume - 0.1, 0.0)

        # Définit le nouveau volume
        mixer.music.set_volume(new_volume)


app = App()