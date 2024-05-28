# YoutubeExtractor

YoutubeExtractor is a Python application that can be used to download videos or entire playlists from YouTube.
With the possibility of downloading only the audio, the output gets either converted into MP3 or MP4.
In addition, the history and metadata can optionally be saved to a MySQL database. 


YoutubeExtractor is developed using [yt-dlp](https://github.com/yt-dlp/yt-dlp).

**NOTE:** *Please note that downloading videos/audios of content you do not own might be illegal in your country. 
This is for educational purposes only. I'm not responsible for any misuse of this program.*

<p align="center">
  <img src="res/Downloading.png" />
</p>

## Table of Contents

- [Instructions](#Instructions)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Source code](#source-code)
- [Contributing](#contributing)
- [License](#license)

## Instructions
Simply enter the YouTube url from a playlist or single track into the python program 
and specify if you want to download only the audio 
and/or write the data to the MySQL database.

If you decide to write metadata to database, the installation of MySQL is required manually. 
The program will create a new schema **db_youtube_av** and following tables **youtube_music**, **youtube_video**

## Requirements
- [Python 3.x](https://www.python.org/downloads/)
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/)
- [MySQL](https://dev.mysql.com/downloads/installer/)  **( optional )**


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
   cd YoutubeExtractor\.config\config.ini
   ```
4. Setup virtual environment and install requirements.txt

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
   ```
   
5. Activate virtual environment and run program

    ```bash
    python src\main.py
   ```
   
### Source Code
The source code of the YoutubeExtractor is located in the **src** directory, 
organized into the separate modules **main**, **YoutubeDL** and **DBMS**.

In **main** the user input gets handled and after verification forwarded to **YoutubeDL**.
Leveraging the [yt-dlp](https://github.com/yt-dlp/yt-dlp) library, 
the program is downloading the media in the best available quality.
If selected the metadata of the downloaded file are getting saved to the MySQL database using the **DBMS**.

### Contributing
Contributions to this project are welcome! If you would like to contribute, 
please open an issue to discuss potential changes or submit a pull request.
For more details please visit the [contributing page](docs/CONTRIBUTING.md).

### License

This project is licensed under the [MIT License](LICENSE.md). 
You are free to use, modify, and distribute this code as permitted by the license.