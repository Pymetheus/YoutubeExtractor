import requests
from YoutubeDL import YoutubeDL


def execute_youtube_extractor(url: str, audio_only: bool = True, write_to_db: bool = True):
    # Control if url is from a playlist or track and continue execution
    playlist_string = "list="
    if playlist_string in url:
        print("Recognized playlist url, downloading all entries")
        YT = YoutubeDL(url, audio_only=audio_only, write_to_db=write_to_db)
        YT.execute_playlist_download()
    else:
        print("Recognized track url, downloading entry")
        YT = YoutubeDL(url, audio_only=audio_only, write_to_db=write_to_db)
        YT.execute_track_download()


def is_youtube_url(url):
    # Control if url is from YouTube
    youtube_string = "www.youtube.com/watch"
    if youtube_string in url:
        return True
    else:
        print(f"The url {url} is not compatible with the program")
        return False


def is_connected_to_url(url):
    # Control if program can connect to url
    try:
        response = requests.get(url, timeout=15)
        return True
    except requests.ConnectionError:
        print(f"Cant connect to {url}")
        return False
    except Exception as e:
        print(e)
        return False


def verify_url(url):
    # Verify if url is executable
    if is_connected_to_url(url):
        if is_youtube_url(url):
            return True

    print("Verification failed")


def user_input():
    # Handle user input and return user response as a list for further execution
    user_url_response = user_url_request()
    user_audio_only_response = user_audio_request()
    user_db_response = user_db_request()

    user_response = [user_url_response, user_audio_only_response, user_db_response]
    return user_response


def user_url_request():
    # Handle user url request and return url
    user_url = str(input("Enter the youtube url you want to download from: "))
    return user_url


def user_audio_request():
    # Handle user audio request and return option
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
    # Handle user db request and return option
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
    # Handle user continuation request and return option
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
    # Execute main program
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
        print(e)


if __name__ == '__main__':

execute_main()
