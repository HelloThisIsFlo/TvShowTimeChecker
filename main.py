import os
import guessit
from prettytable import PrettyTable

import credentials_secret
import tvshowtime


def display_file_infos(guess):
    print("//////////////////////////////////////////////////////////////////////////////")
    print("Name : " + get_string_value('series', guess))
    print("Season : " + get_string_value('season', guess))
    print("Episode : " + get_string_value('episode', guess))
    print("//////////////////////////////////////////////////////////////////////////////")
    print


def get_string_value(key, dictionary):
    if key in dictionary:
        return str(dictionary[key])
    else:
        return ""


def get_int_value(key, dictionary):
    if key in dictionary:
        return int(dictionary[key])
    else:
        return 0


def save_episode_progress(shows, guess):
    # Debug
    name = get_string_value('series', guess)

    # Get progress
    new_episode = get_int_value('episodeNumber', guess)
    new_season = get_int_value('season', guess)
    new_progress = {'episode': new_episode, 'season': new_season}

    current_progress = shows.get(get_string_value('series', guess), dict())

    # Compare progress
    progress = compare_episode_progress(new_progress, current_progress)

    # Save progress
    show_name = get_string_value('series', guess).title()
    if show_name is not "":
        shows[show_name] = progress


def compare_episode_progress(new_progress, current_progress):
    """
    Compare progress in a specific Tv show.
     Most advanced episode in the most advanced season

    :param new_progress: Dict : New progress
    :param current_progress: Dict : Current progress
    :return: Dict : Most advanced progress in the Tv Show
    """
    current_episode = current_progress.get('episode', 0)
    current_season = current_progress.get('season', 0)

    new_episode = new_progress.get('episode', 0)
    new_season = new_progress.get('season', 0)

    result_progress = dict()
    # First compare the season
    if new_season > current_season:
        result_progress = new_progress
    elif new_season < current_season:
        result_progress = current_progress
    else:  # new_season == season
        if new_episode > current_episode:
            result_episode = new_episode
            result_season = current_season
        else: # new_episode <= current_episode
            result_episode = current_episode
            result_season = current_season

        result_progress['episode'] = result_episode
        result_progress['season'] = result_season

    return result_progress

# TODO : Get path from command line argument
# TODO : Pack the app in an exe, and check for the token 'saving place'
# Print hello message
print("////////////////////////////////")
print("// WELCOME TO TV SHOW CHECKER //")
print("////////////////////////////////")
print()

# Try to read token from file
token = None
try:
    token_file = open("token.dat", "r")
    token = token_file.read()
    token_file.close()
    print("Authentication : Token found! Skipping authentication")
except FileNotFoundError:
    print("Authentication : Token not found, prompting authentication")
print()

# Create the TvShowTime Object
if token:
    tvst = tvshowtime.TvShowTime(token)
else:
    tvst = tvshowtime.TvShowTime()

# Check authentication
if not tvst.is_authenticated():
    # Get token
    token = tvst.generate_token(
        credentials_secret.client_id_showtime,
        credentials_secret.client_secret_showtime,
        credentials_secret.user_agent_showtime
    )

    # Save token
    token_file = open("token.dat", "w")
    token_file.write(token)
    token_file.close()

# Walk the 'Tv Show' directory
test = os.walk(top=r'R:\Torrent\Tv Shows', topdown=False)
shows = dict()
for _, _, files_current_dir in os.walk(r'R:\Torrent\Tv Shows'):
    for file in files_current_dir:
        # Guess the file infos
        guess = guessit.guess_episode_info(file)

        # Save the infos in the dictionary
        save_episode_progress(shows, guess)


print("////////////////////////")
print("// LAST AIRED EPISODE //")
print("////////////////////////")

for tv_show_name, progress in shows.items():
    show_infos, _ = tvst.get_show_infos(tv_show_name)

    progress_table = PrettyTable(["", "Season", "Episode"])
    progress_table.align[""] = "l"
    progress_table.add_row(
        ["Last aired", show_infos['last_aired']['season_number'], show_infos['last_aired']['number']]
    )
    progress_table.add_row(["Downloaded", progress['season'], progress['episode']])
    last_seen = show_infos['last_seen']
    if last_seen is not None:
        progress_table.add_row(
            ["Last seen", last_seen['season_number'], last_seen['number']]
        )

    print()
    print(" " + tv_show_name)
    print(progress_table)
