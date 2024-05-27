# YoutubeExtractor

YoutubeExtractor is a Python application that can be used to download videos or entire playlists from YouTube.
With the possibility of downloading only the audio, the output gets either converted into MP3 or MP4.
In addition, the history and metadata can optionally be saved to a MySQL database. 


YoutubeExtractor is developed using [yt-dlp](https://github.com/yt-dlp/yt-dlp).

**NOTE:** *Please note that downloading videos/audios of a content you do not own might be illegal in your country. This is for educational purposes only. I'm not responsible for any misuse of this program.*

![Download](res/Downloading.png)

## Table of Contents

- [Instructions](#Instructions)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Source code](#source-code)
- [Contributing](#contributing)
- [License](#license)

## Instructions
Simply enter the YouTube url into the python program and specify if you want to download only the audio 
and/or write the data to the MySQL database.

If you decide to write the metadata to database, the installation of MySQL is required manually. 
The program will create a new schema **db_youtube_av** and following tables **youtube_music**, **youtube_video**

## Requirements
- [Python 3.x](https://www.python.org/downloads/)
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/)
- [MySQL](https://dev.mysql.com/downloads/installer/)  **( optional )**


## Getting Started
### Installation