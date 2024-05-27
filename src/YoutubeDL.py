import yt_dlp
import configparser
from DBMS import MySQL


class YoutubeDL(object):

    def __init__(self, url: str, audio_only: bool = True, write_to_db: bool = True):
        # Initializing YoutubeDL class with url, options for audio only and writing metadata to DB
        self.url = url
        self.output_path = "../data"
        self.ffmpeg_location = ""
        self.import_config()
        self.audio_only = audio_only
        self.write_to_db = write_to_db
        if self.write_to_db:
            self.Audio_DB = self.initialize_audiovisual_db()

    def import_config(self):
        # Importing configuration from config.ini
        config = configparser.ConfigParser(interpolation=None)
        config.read('../.config/config.ini')
        self.ffmpeg_location = config["ffmpeg"]["ffmpeg_location"]

    def set_audio_only_options(self, filename: str):
        # Setting options for audio only in the best quality and returning dictionary
        options = {
            'format': 'bestaudio',
            'ffmpeg_location ': self.ffmpeg_location,
            'keepvideo': False,
            'outtmpl': self.output_path + f"\{filename}",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        return options

    def set_audiovisual_options(self, filename: str):
        # Setting options for audiovisual in the best quality and returning dictionary
        options = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'ffmpeg_location ': self.ffmpeg_location,
            'outtmpl': self.output_path + f"\{filename}"
        }
        return options

    def get_track_content(self):
        # Getting extracted info from URL and returning it
        track_content = yt_dlp.YoutubeDL().extract_info(url=self.url, download=False)
        return track_content

    def get_playlist_content(self):
        # Getting extracted info from Playlist URL and returning it
        playlist_info = yt_dlp.YoutubeDL().extract_info(url=self.url, download=False)
        playlist_content = playlist_info["entries"]
        return playlist_content

    def get_playlist_length(self, playlist_content: dict):
        # Get length of playlist from content and return integer with length
        playlist_len = int(playlist_content[-1]["playlist_index"])
        print(f"Videos in Playlist: {playlist_len}")
        return playlist_len

    def generate_filename_from_track_content(self, track_content: dict):
        # Generate filename with track and artist if available otherwise take the title, return filename
        media_title = track_content["title"]

        key_list = []
        for item in track_content:
            key_list.append(item)

        if "track" and "artists" in key_list:
            media_track = track_content["track"]
            media_track = media_track.split(" (")
            media_track = media_track[0]
            media_artist = track_content["artists"][0]
            filename = f"{media_artist} - {media_track}".capitalize()
        else:
            media_title = media_title.split(" (")
            media_title = media_title[0]
            filename = f"{media_title}".capitalize()

        print(f"FILENAME: {filename}")
        return filename

    def download_from_youtube(self, options: dict):
        # Download media using options as an argument
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([self.url])
            print("Download finished")
        except Exception as e:
            print(e)

    def execute_playlist_download(self):
        # Execute downloading media from playlist
        playlist_content = self.get_playlist_content()
        playlist_length = self.get_playlist_length(playlist_content)

        for index in range(playlist_length):
            track_content = playlist_content[index]
            self.url = track_content["original_url"]
            self.execute_track_download()

    def execute_track_download(self):
        # Execute downloading media
        track_content = self.get_track_content()
        track_filename = self.generate_filename_from_track_content(track_content)

        if self.audio_only:
            options = self.set_audio_only_options(track_filename)
        else:
            options = self.set_audiovisual_options(track_filename)

        self.download_from_youtube(options)

        if self.write_to_db:
            self.write_metadata_to_audiovisual_db(track_content)
        print("DOWNLOAD: FINISHED")

    def get_metadata(self, track_content: dict):
        # Get metadata from track content and return a tuple for writing to DB
        missing = "NA"
        key_list = []
        for item in track_content:
            key_list.append(item)

        title = track_content["title"]
        if "artists" in key_list:
            artists = track_content["artists"][0]
        else:
            artists = missing
        if "track" in key_list:
            track = track_content["track"]
        else:
            track = missing
        if "album" in key_list:
            album = track_content["album"]
        else:
            album = missing
        duration = int(track_content["duration"])
        filename = self.generate_filename_from_track_content(track_content)
        url = track_content["original_url"]

        # media_table_columns = ("title", "artists", "track", "album", "duration", "filename", "original_url")
        track_metadata = (title, artists, track, album, duration, filename, url)
        return track_metadata

    def write_metadata_to_audiovisual_db(self, track_content):
        # Get metadata and write them to DB
        metadata = self.get_metadata(track_content)
        self.Audio_DB.insert_row_into_table(metadata)

    def initialize_audiovisual_db(self):
        # Initialize Audiovisual DB and create necessary tables
        start_db = "db_root"
        yt_db = "db_youtube_av"
        if self.audio_only:

            table_name = "youtube_music"
        else:
            table_name = "youtube_video"
        column_content = {
            "col_name": ["id", "title", "artists", "track", "album", "duration", "filename", "original_url"],
            "col_type": ["INT", "VARCHAR(100)", "VARCHAR(100)", "VARCHAR(100)", "VARCHAR(100)", "INT", "VARCHAR(200)",
                         "VARCHAR(200)"],
            "col_add": ["PRIMARY KEY AUTO_INCREMENT", "", "", "", "", "", "", ""]
        }

        Audiovisual_DB = MySQL(start_db)
        Audiovisual_DB.create_new_database(yt_db)
        Audiovisual_DB.switch_to_database(yt_db)
        Audiovisual_DB.create_new_table_from_dict(table_name, column_content)
        Audiovisual_DB.set_current_table(table_name)

        return Audiovisual_DB


if __name__ == '__main__':
    print('### TEST ###')

    # TRACK TEST
    s_url = "https://www.youtube.com/watch?v=9ao4FEaDGhQ"
    Test_YT = YoutubeDL(s_url, True, True)
    Test_YT.execute_track_download()
    Test_YT = YoutubeDL(s_url, False, True)
    Test_YT.execute_track_download()

    # PLAYLIST TEST
    #t_url = "https://www.youtube.com/watch?v=Dpe4FgGDmcA&list=PL91EbznIQz17bowB66x-rLT0AEc7LueS6"
    #Test_YT = YoutubeDL(t_url, True)
    #Test_YT.execute_playlist_download()
