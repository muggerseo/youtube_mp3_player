    try:
            if self.list_of_songs:
                pygame.mixer.music.stop()  # Stop current song to prevent error playing next song
                self.current_song_index = (self.current_song_index + 1) % len(self.list_of_songs)
                self.play_music()
        except Exception as e:
            print(f"Error loading next song: {e}")