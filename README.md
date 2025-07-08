# YoutubeExtractor

YouTubeExtractor is a Python application used to download videos or entire playlists from YouTube. 
It supports downloading audio-only or audio with video, saving files in MP3 or MP4 formats.
Optionally, it can save metadata to a database (SQLite by default, with support for MySQL and PostgreSQL).

YoutubeExtractor leverages the powerful [yt-dlp](https://github.com/yt-dlp/yt-dlp) library.

<p align="center">
  <img src="res/Downloading.png" />
</p>

**NOTE:** *Downloading videos or audio of content you do not own might be illegal in your country. 
This program is intended for educational purposes only. 
The author is not responsible for any misuse of this program.*

## Table of Contents

- [Instructions](#Instructions)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Source code](#source-code)
- [Contributing](#contributing)
- [License](#license)

## Instructions
Run the program and enter the YouTube URL for either a playlist or a single video.
Then select whether to download audio only or audio and video, and whether to write metadata to the database.

By default, metadata is stored in a local SQLite database.
If you choose to use MySQL or PostgreSQL, ensure you have the respective database installed and configured.
The program will automatically create necessary tables if they do not exist.

Downloaded media files are saved automatically to the data/ folder.

## Requirements
- [Python 3.x](https://www.python.org/downloads/)
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/)
- [sqlalchemy-dbtoolkit](https://github.com/Pymetheus/sqlalchemy-dbtoolkit)


## Getting Started
### Installation

1. [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) the repository to your local machine:

    ```bash
    git clone https://github.com/Pymetheus/YoutubeExtractor.git
    ```

2. Change into the project directory:

    ```bash
    cd  YoutubeExtractor
    ```
3. Update the API keys in the config.ini

    ```bash
   cd YoutubeExtractor\.config
   ```
4. Setup virtual environment and install requirements.txt

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
   ```
   
5. Run program

    ```bash
    python src\main.py
   ```
   
### Source Code
The application code is organized under the src/ directory, split into three modules:
- main.py — Handles user interaction, input validation, and program flow.
- YoutubeDL.py — Wraps the yt-dlp functionality to download media.
- database_handler.py — Manages metadata storage with support for SQLite, MySQL, and PostgreSQL.

The program uses yt-dlp to fetch the best quality media and stores it under data/. 
Metadata is saved depending on user choice and configured database.

### Contributing
Contributions to this project are welcome! If you would like to contribute, 
please open an issue to discuss potential changes or submit a pull request.
For more details please visit the [contributing page](docs/CONTRIBUTING.md).

### License

This project is licensed under the [MIT License](LICENSE.md). 
You are free to use, modify, and distribute this code as permitted by the license.