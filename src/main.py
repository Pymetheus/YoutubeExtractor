import requests
from YoutubeDL import YoutubeDL


def execute_youtube_extractor(url: str, audio_only: bool = True, write_to_db: bool = True, dbms="sqlite"):
    """
    Execute download process for a YouTube track or playlist.

    Determines whether the URL points to a single video or a playlist, and triggers
    the appropriate download handler.

    Args:
        url (str): The YouTube video or playlist URL.
        audio_only (bool): If True, download only audio. Defaults to True.
        write_to_db (bool): If True, write metadata to the database. Defaults to True.
        dbms (str): Database type to use (e.g., "sqlite", "mysql", "postgresql"). Defaults to "sqlite".
    """

    playlist_string = "list="
    if playlist_string in url:
        print("Recognized playlist url, downloading all entries")
        YT = YoutubeDL(url, audio_only=audio_only, write_to_db=write_to_db, dbms=dbms)
        YT.execute_playlist_download()
    else:
        print("Recognized track url, downloading entry")
        YT = YoutubeDL(url, audio_only=audio_only, write_to_db=write_to_db, dbms=dbms)
        YT.execute_track_download()


def is_youtube_url(url: str):
    """
    Check if the provided URL is a valid YouTube video URL.

    Args:
        url (str): The URL to verify.

    Returns:
        bool: True if the URL is a YouTube video URL, False otherwise.
    """

    youtube_string = "www.youtube.com/watch"
    if youtube_string in url:
        return True
    else:
        print(f"The url {url} is not compatible with the program")
        return False


def is_connected_to_url(url: str):
    """
    Verify that the program can establish a connection to the given URL.

    Args:
        url (str): The target URL.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """

    try:
        response = requests.get(url, timeout=15)
        return True
    except requests.ConnectionError:
        print(f"Cant connect to {url}")
        return False
    except Exception as e:
        print(e)
        return False


def verify_url(url: str):
    """
    Perform full verification of the URL including connectivity and YouTube format.

    Args:
        url (str): The URL to verify.

    Returns:
        bool: True if the URL is valid and reachable, False otherwise.
    """

    if is_connected_to_url(url):
        if is_youtube_url(url):
            return True
    print("Verification failed")
    return False


def user_input():
    """
    Prompt the user for input regarding the download parameters.

    Returns:
        list: A list containing user responses:
              [0] -> YouTube URL (str),
              [1] -> audio_only flag (bool),
              [2] -> write_to_db flag (bool).
    """

    user_url_response = user_url_request()
    user_audio_only_response = user_audio_request()
    user_db_response = user_db_request()

    user_response = [user_url_response, user_audio_only_response, user_db_response]
    return user_response


def user_url_request():
    """
    Prompt the user for the YouTube URL.

    Returns:
        str: The entered YouTube URL.
    """

    user_url = str(input("Enter the youtube url you want to download from: "))
    return user_url


def user_audio_request():
    """
    Prompt the user to choose between audio-only or full video download.

    Returns:
        bool: True if audio-only is selected, False otherwise.
    """

    user_audio_choice = str(input(
        """
        Select from the options:
        [1] Audio only
        [2] Audio & Video
        >>> """))

    valid_options = ["1", "2"]
    if user_audio_choice in valid_options:
        if user_audio_choice == "1":
            print("Selected audio only")
            return True
        else:
            print("Selected audio & video")
            return False
    else:
        print(f"{user_audio_choice} is not a valid option")
        user_audio_request()


def user_db_request():
    """
    Prompt the user to choose whether to write metadata to the database.

    Returns:
        bool: True if writing to the database is selected, False otherwise.
    """

    user_db_choice = str(input(
        """
        Select from the options:
        [1] Write to DB
        [2] Don't write to DB
        >>> """))

    valid_options = ["1", "2"]
    if user_db_choice in valid_options:
        if user_db_choice == "1":
            print("Selected write to DB")
            return True
        else:
            print("Selected don't write to DB")
            return False
    else:
        print(f"{user_db_choice} is not a valid option")
        user_db_request()


def user_program_continuation():
    """
    Prompt the user to decide whether to continue or terminate the program.

    Returns:
        bool: True if the user wants to continue, False to stop.
    """

    user_choice = str(input(
        """
        Select from the options:
        [1] Download from another link
        [2] Stop program
        >>> """))

    valid_options = ["1", "2"]
    if user_choice in valid_options:
        if user_choice == "1":
            print("To be continued...")
            return True
        else:
            print("Ending program")
            return False
    else:
        print(f"{user_choice} is not a valid option")
        user_program_continuation()


def execute_main():
    """
    Run the main program loop.

    Continuously prompts the user for input and handles YouTube download requests
    until the user chooses to terminate the session.
    """

    try:
        run_program = True
        while run_program:
            response = user_input()
            request_url = response[0]
            request_audio = response[1]
            request_db = response[2]

            if verify_url(request_url):
                execute_youtube_extractor(request_url, audio_only=request_audio, write_to_db=request_db)

            run_program = user_program_continuation()

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':

    execute_main()
