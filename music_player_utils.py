import tkinter
import customtkinter as ctk
import pygame
from PIL import Image, ImageTk
from threading import *
from tkinter import filedialog, messagebox
import time, math
import os, random

def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")

def play_on_clicks(self, event):
    try:  # Get the index of the clicked song
        index = self.song_listbox.curselection()[0]
        song_path = self.list_of_songs[index]
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        song_name = os.path.splitext(os.path.basename(song_path))[0]
        self.scroll_song_name(song_name)
        Thread(target=self.progress_bar_update, daemon=True).start()
        print(f"Play_on_clicks: Playing song: {song_name}")
    except pygame.error as e:
        print(f"Error loading song:{os.path.basename(song_path)}, {e}")
        self.random_play()
    except Exception as e:
        print(f"Error: {e}")
        self.random_play()

def scroll_song_name(self, song_name):
        if self.scroll_text_id:
            self.song_name_label.after_cancel(self.scroll_text_id)
        self.song_name_label.configure(text=song_name)
        self.scroll_text(song_name, 0)

def scroll_text(self, text, pos):
    display_text = text[pos:] + " -=- " + text[:pos]
    self.song_name_label.configure(text=display_text)
    self.scroll_text_id = self.song_name_label.after(130, self.scroll_text, text, (pos + 1) % len(text))

def progress_bar_update(self):
        song_len = pygame.mixer.Sound(self.list_of_songs[self.current_song_index]).get_length()
        while pygame.mixer.music.get_busy():  # Update while music is playing
            current_pos = pygame.mixer.music.get_pos() / 1000  # Position in seconds
            progress = min(current_pos / song_len, 1.0)  # Normalize progress (0.0 to 1.0)
            self.progress_bar.set(progress)
            #time.sleep(0.3)
        self.progress_bar.set(0)  # Reset after song finished

def load_music(self):
    self.current_files = filedialog.askopenfilenames(
        title="Select music Files",
        filetypes=[("Music files", "*.mp3 *.wav")])
    if self.current_files:
        self.list_of_songs = list(self.current_files)
        self.current_song_index = 0
        # Clear the current playlist
        self.song_listbox.delete("0", "end")
        # Add new songs to the playlist
        for file in self.list_of_songs:
            song_name = os.path.splitext(os.path.basename(file))[0]  # Extract filename only
            self.song_listbox.insert("end", f"{self.song_index}. {song_name}\n")
            self.song_index += 1

def add_music(self):  # Add to current songlist instead of replacing it
    self.current_files = filedialog.askopenfilenames(
        title="Select music Files",
        filetypes=[("Music files", "*.mp3 *.wav")]
    )
    if self.current_files:
        new_songs_list = list(self.current_files)
        self.list_of_songs.extend(new_songs_list)

        # Add new songs to the playlist
        for file in new_songs_list:
            song_name = os.path.basename(file)  # Extract filename only
            self.song_listbox.insert("end", f"{self.song_index}. {song_name}\n")
            self.song_index += 1