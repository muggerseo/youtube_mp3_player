import tkinter
import customtkinter as ctk
import pygame
from PIL import Image, ImageTk
from threading import *
import os, random, time
# from tkinter import filedialog, messagebox
# import time, math

from music_player_utils import play_on_clicks, center_window, scroll_song_name, scroll_text, progress_bar_update, load_music, add_music 


ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

pygame.mixer.init()
pygame.display.set_mode((1, 1))  # Initialize Pygame display module to prevet "video system not initialized"error

class MusicPlayer:

    def center_window(self, window, width, height):
        center_window(self, window, width, height)
        
    def __init__(self, root):
        self.root = root
        self.is_paused = False

        root.title('Music Player')
        root.geometry('600x480')
        root.resizable(False, False)
        
        self.list_of_songs = []
        self.list_of_covers = ["1.jpg", "2.jpg"]
        self.current_files = []
        self.current_song_index = 0
        self.song_index = 1   
        self.play_music()
        self.check_music_end()    

        self.center_window(root, 400, 600)

# play track after track
# seek the track
# pause and resume the track on Play button click and pause button click
# timer for current track
# fix play button freeze
# scrollbar keep showing first track name played when press on next_song button
# add volume control slider
# after track paused next track will not be played
# add album cover
       
        # Album cover label
        self.album_cover_label = ctk.CTkFrame(master=root)
        self.album_cover_label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        # Frame holds Listbox and Scrollbar
        self.frame = ctk.CTkFrame(master=root, width=300, height=200)
        self.frame.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(self.frame, orientation="vertical")
        self.scrollbar.pack(side="right", fill="y")
        
        # Listbox (Song Listbox)
        self.song_listbox = tkinter.Listbox(self.frame, width=45, height=10, yscrollcommand=self.scrollbar.set)
        self.song_listbox.pack(side="left", fill="both", expand=True)
        
        # Link Scrollbar to Listbox
        self.scrollbar.configure(command=self.song_listbox.yview)

        self.song_listbox.bind("<Double-1>", self.play_on_clicks)

        # Buttons
        self.song_name_label = ctk.CTkLabel(master=root, text="", font=("Helvetica", 12))
        self.song_name_label.place(relx=0.5, rely=0.05, anchor=tkinter.CENTER)
        self.scroll_text_id = None

        self.play_button = ctk.CTkButton(master=root, text='Play', command=self.play_music)
        self.play_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        self.skip_forward_button = ctk.CTkButton(master=root, text='>', command=self.skip_forward, width=50)
        self.skip_forward_button.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)

        self.skip_backward_button = ctk.CTkButton(master=root, text='<', command=self.skip_backward, width=50)
        self.skip_backward_button.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)

        self.load_button = ctk.CTkButton(master=root, text='Load', command=self.load_music, width=2)
        self.load_button.place(relx=0.3, rely=0.8, anchor=tkinter.CENTER)

        self.add_button = ctk.CTkButton(master=root, text='Add', command=self.add_music, width=2)
        self.add_button.place(relx=0.4, rely=0.8, anchor=tkinter.CENTER)

        self.pause_button = ctk.CTkButton(master=root, text='Pause', command=self.pause_music, width=2)
        self.pause_button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        self.slider = ctk.CTkSlider(master=root, from_=0, to=100, command=self.volume, width=210)
        self.slider.place(relx=0.5, rely=0.87, anchor=tkinter.CENTER)
        self.slider.set(25)  # volume slider 50% default
        self.volume(25)  # Set initial volume to 50%

        self.timer_label = ctk.CTkLabel(master=root, text="00:00 / 00:00", font=("Helvetica", 10))
        self.timer_label.place(relx=0.5, rely=0.95, anchor=tkinter.CENTER)

        self.progress_bar = ctk.CTkProgressBar(master=root, progress_color='#32a85a', width=250)
        self.progress_bar.place(relx=0.5, rely=0.92, anchor=tkinter.CENTER)
        self.progress_bar.set(0)
        self.progress_bar.bind("<ButtonRelease-1>", lambda event: self.set_song_position(self.progress_bar.get()))

    def scroll_song_name(self, song_name):
        scroll_song_name(self, song_name)

    def scroll_text(self, text, pos):
        scroll_text(self, text, pos)

    def play_on_clicks(self, event):
        play_on_clicks(self, event)
    
    def load_music(self):
        load_music(self)
        print(f"Loaded songs: {self.list_of_songs}")

    def add_music(self):  # Add to current songlist instead of replacing it
        add_music(self)

    def random_play(self):
        if not self.current_files:
            print("No songs loaded")
            return
        while True:
            random_song = random.choice(self.current_files)
            print(f"Attempting to play: {random_song}")  # Debugging output
            try:
                pygame.mixer.music.stop()  # Stop any currently playing music
                time.sleep(0.1)  # Small delay to ensure the stop command is processed
                pygame.mixer.music.load(random_song)
                pygame.mixer.music.play()
                song_name = os.path.splitext(os.path.basename(random_song))[0]  # Remove the .mp3 extension
                self.song_name_label.configure(text=f"Now playing: {os.path.basename(song_name)}")
                self.scroll_song_name(os.path.basename(song_name))
                self.threading()
                break
            except Exception as e:
                print(f"Error loading song: {e}")

    def get_albom_cover(self, song_name, current_song_index):  # PIL works
        try:
            if self.list_of_covers and 0 <= current_song_index < len(self.list_of_covers):
                image_path = self.list_of_covers[current_song_index] # open and resize the cover image
                image = Image.open(image_path)
                image = image.resize((100, 100), Image.ANTIALIAS)  # Resize to fit the label

                photo = ImageTk.PhotoImage(image) 
                if hasattr(self, 'cover_label'):
                    self.cover_label.configure(image=photo)
                    self.cover_label.image = photo  # Keep reference to avoid garbage collection
                else:
                    self.cover_label = ctk.CTkLabel(master=root, image=photo)
                    self.cover_label.image = photo
                    self.cover_label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
            else:
                print(f"Invalid album cover index: {current_song_index}")
        except Exception as e:
            print(f"Error loading album cover: {e}")

            stripped_string = song_name[29:-4]  # remove path out the file name
            self.song_name_label = tkinter.Label(text=stripped_string, bg='#222222', fg='white')
            self.song_name_label.place(relx=0.4, rely=0.6)

    def threading(self):
        t1 = Thread(target=self.progress_bar_update)
        t1.start()

    def update_timer(self):
        try:
            song_len = pygame.mixer.Sound(self.list_of_songs[self.current_song_index]).get_length()
            current_pos = pygame.mixer.music.get_pos() / 1000 # Convert milliseconds to seconds

            elapsed_time = time.strftime("%M:%S", time.gmtime(current_pos))
            total_time = time.strftime("%M:%S", time.gmtime(song_len))
                                       
            self.timer_label.configure(text=f"{elapsed_time} / {total_time}")

            if pygame.mixer.music.get_busy():
                self.root.after(1000, self.update_timer)  # Update every second
            else:
                self.timer_label.configure(text="00:00 / 00:00")   # Reset when new song starts
        except Exception as e:
            print(f"Error updating timer: {e}")

    def progress_bar_update(self):
        progress_bar_update(self)

    def play_music(self):
        try: 
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_pauses = False
                print("Music resumed")
            elif self.list_of_songs:
                song_name = self.list_of_songs[self.current_song_index]
                print(f"Playing: {os.path.basename(song_name)}")
                pygame.mixer.music.load(song_name)
                pygame.mixer.music.play()
                print("song is now playing")
                pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set event to be triggered when song ends
                print("USEREVENT set for song end")
                self.threading()  # Start updating the progress bar in a separate thread to avoid freezing the GUI
            else:
                self.random_play()
        except Exception as e:
            print(f"Error loading song: {e}")
            

    def skip_forward(self):
        try:
            if self.list_of_songs:
                print(f"Skipping to next song. Current index: {self.current_song_index}")
                pygame.mixer.music.stop()  # Stop current song to prevent error playing next song
                self.current_song_index = (self.current_song_index + 1) % len(self.list_of_songs)
                print(f"New index: {self.current_song_index}")
                self.play_music()
        except Exception as e:
            print(f"Error loading next song: {e}")
            

    def skip_backward(self):
        song_path = self.list_of_songs[self.current_song_index]
        try:
            if self.list_of_songs:
                pygame.mixer.music.stop()  # stop current song to prevent error playing next song
                self.current_song_index = (self.current_song_index - 1) % len(self.list_of_songs)
                self.play_music()
        except Exception as e:
            print(f"Error playing previous song:{os.path.basename(song_path)}, {e}")

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True
            print("Music paused")

    def volume(self, value):
        volume = int(value) / 100
        pygame.mixer.music.set_volume(volume)

    def set_song_position(self, value):
        if self.list_of_songs:
            try:
                song_len = pygame.mixer.Sound(self.list_of_songs[self.current_song_index]).get_length() # Get song length in seconds
                new_pos = float(value) * song_len # Calculate new position in seconds
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()
                pygame.mixer.music.set_pos(new_pos) # Set new position
                print(f"Set song pos to {new_pos} seconds")
                self.progress_bar.set(value)
            except Exception as e:
                print(f"Error setting song position: {e}")

    def check_music_end(self):
        print("Checking for USEREVENT...")
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                print("USEREVENT detected. Skipping to next song...")
                self.skip_forward()
        self.root.after(1500, self.check_music_end)

if __name__ == "__main__":
    root = ctk.CTk()
    app = MusicPlayer(root)
    root.mainloop()