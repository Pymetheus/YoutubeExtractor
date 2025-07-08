import os
import yt_dlp
import configparser
from src.database_handler import DatabaseOperations
from sqlalchemy_dbtoolkit.utils.sanitization import sanitize_nan_to_none


class YoutubeDL(object):
    """
    A class to handle downloading media (audio or video) from YouTube and storing metadata optional in a database.
    """

    def __init__(self, url: str, audio_only: bool = True, write_to_db: bool = True, dbms: str = "sqlite",
                 config_path: str = '../.config/config.ini', output_path: str = "../data"):
        """
        Initialize YoutubeDL instance with configuration and optional database integration.

        Args:
            url (str): URL of the YouTube video or playlist.
            audio_only (bool): If True, download only audio; else, download video.
            write_to_db (bool): If True, write metadata to the database.
            dbms (str): Database management system ('sqlite', 'mysql', etc.).
            config_path (str): Path to configuration file.
            output_path (str): Directory to save downloaded media.
        """

        self.url = url
        self.audio_only = audio_only
        self.config_path = config_path
        self.output_path = output_path
        self.ffmpeg_location = None
        self.import_config()

        self.write_to_db = write_to_db
        if self.write_to_db:
            self.DB_Ops = DatabaseOperations(dbms=dbms)
            self.DB_Ops.create_tables_if_not_exists()

    def import_config(self):
        """
        Load configuration settings (e.g., FFmpeg location) from the config file.
        """
        config = configparser.ConfigParser(interpolation=None)
        config.read(self.config_path)
        self.ffmpeg_location = config["ffmpeg"]["ffmpeg_location"]

    def set_audio_only_options(self, filename: str):
        """
        Set yt_dlp options for downloading audio only.

        Args:
            filename (str): Output filename for the downloaded file.

        Returns:
            dict: yt_dlp configuration options for audio-only downloads.
        """

        options = {
            'format': 'bestaudio',
            'ffmpeg_location': self.ffmpeg_location,
            'keepvideo': False,
            'outtmpl': os.path.join(self.output_path, filename),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        return options

    def set_audiovisual_options(self, filename: str):
        """
        Set yt_dlp options for downloading audio and video.

        Args:
            filename (str): Output filename for the downloaded file.

        Returns:
            dict: yt_dlp configuration options for full audio-visual downloads.
        """

        options = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'ffmpeg_location': self.ffmpeg_location,
            'outtmpl': os.path.join(self.output_path, filename)
        }
        return options

    def get_track_content(self):
        """
        Extract metadata from the YouTube video URL without downloading.

        Returns:
            dict: Metadata for the track.
        """

        track_content = yt_dlp.YoutubeDL().extract_info(url=self.url, download=False)
        return track_content

    def get_playlist_content(self):
        """
        Extract metadata from the YouTube playlist URL without downloading.

        Returns:
            list: List of track metadata dictionaries in the playlist.
        """

        playlist_info = yt_dlp.YoutubeDL().extract_info(url=self.url, download=False)
        playlist_content = playlist_info["entries"]
        return playlist_content

    def generate_filename_from_track_content(self, track_content: dict):
        """
        Generate a filename based on track content metadata.

        Args:
            track_content (dict): Metadata dictionary of a YouTube track.

        Returns:
            str: Sanitized and formatted filename.
        """

        media_title = track_content["title"]

        if "track" in track_content and "artists" in track_content:
            media_track = track_content["track"]
            media_track = media_track.split(" (")
            media_track = str(media_track[0])
            media_artist = track_content["artists"][0]
            filename = f"{media_artist} - {media_track}"
        else:
            media_title = media_title.split(" (")
            media_title = media_title[0]
            media_title = media_title.split(" [")
            media_title = media_title[0]
            filename = f"{media_title}"

        print(f"FILENAME: {filename}")
        return filename

    def download_from_youtube(self, options: dict):
        """
        Download media from YouTube using yt_dlp with the given options.

        Args:
            options (dict): yt_dlp configuration dictionary.
        """

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([self.url])
            print("Download finished")
        except Exception as e:
            print(e)

    def execute_playlist_download(self):
        """
        Download all media items from a playlist URL.
        """

        playlist_content = self.get_playlist_content()
        playlist_length = len(playlist_content)

        for index in range(playlist_length):
            track_content = playlist_content[index]
            self.url = track_content["original_url"]
            self.execute_track_download()

    def execute_track_download(self):
        """
        Download a single media item based on current self.url and store its metadata.
        """

        track_content = self.get_track_content()
        track_filename = self.generate_filename_from_track_content(track_content)

        if self.audio_only:
            options = self.set_audio_only_options(track_filename)
            if self.write_to_db:
                table = self.DB_Ops.music_table
        else:
            options = self.set_audiovisual_options(track_filename)
            if self.write_to_db:
                table = self.DB_Ops.video_table

        self.download_from_youtube(options)

        if self.write_to_db:
            self.write_metadata_to_audiovisual_db(table, track_content)
        print("DOWNLOAD: FINISHED")

    def get_metadata(self, track_content: dict):
        """
        Extract and sanitize metadata from track content for database insertion.

        Args:
            track_content (dict): Metadata dictionary from yt_dlp.

        Returns:
            tuple: Cleaned metadata (title, artist, track, album, duration, filename, url).
        """

        missing = sanitize_nan_to_none("NaN")

        title = track_content["title"]
        if "artists" in track_content:
            artists = track_content["artists"][0]
        else:
            artists = missing
        if "track" in track_content:
            track = track_content["track"]
        else:
            track = missing
        if "album" in track_content:
            album = track_content["album"]
        else:
            album = missing
        duration = int(track_content["duration"])
        filename = self.generate_filename_from_track_content(track_content)
        url = track_content["original_url"]

        track_metadata = (title, artists, track, album, duration, filename, url)
        return track_metadata

    def write_metadata_to_audiovisual_db(self, table, track_content: dict):
        """
        Write track metadata to the specified database table.

        Args:
            table: Database table object or name.
            track_content (dict): Track metadata from yt_dlp.
        """

        try:
            metadata = self.get_metadata(track_content)
            self.DB_Ops.insert_data_in_table(Table=table, data=metadata)
        except Exception as e:
            print(f"Failed writing to database: {e}")
