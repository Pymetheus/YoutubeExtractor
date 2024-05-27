from YoutubeDL import YoutubeDL


def execute_youtube_extractor(url: str, playlist: bool = False, audio_only: bool = True, write_to_db: bool = True):
    if playlist:
        YT = YoutubeDL(url, audio_only=audio_only, write_to_db=write_to_db)
        YT.execute_playlist_download()
    else:
        YT = YoutubeDL(url, audio_only=audio_only, write_to_db=write_to_db)
        YT.execute_track_download()

def verify_url():
    pass

if __name__ == '__main__':
    print("MAIN")

my_url = "https://www.youtube.com/watch?v=9ao4FEaDGhQ"
execute_youtube_extractor(my_url, playlist=False, audio_only=True, write_to_db=True)
execute_youtube_extractor(my_url, playlist=False, audio_only=False, write_to_db=True)

