import os
import guessit
from prettytable import PrettyTable

import credentials_secret
import tvshowtime


def display_file_infos(guess):
    print "//////////////////////////////////////////////////////////////////////////////"
    print "Name : " + get_string_value('series', guess)
    print "Season : " + get_string_value('season', guess)
    print "Episode : " + get_string_value('episode', guess)
    print "//////////////////////////////////////////////////////////////////////////////"
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
    show_name = get_string_value('series', guess)
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


# Walk the 'Tv Show' directory
test = os.walk(top=r'R:\Torrent\Tv Shows', topdown=False)
shows = dict()
for _, _, files_current_dir in os.walk(r'R:\Torrent\Tv Shows'):
    for file in files_current_dir:
        # Guess the file infos
        guess = guessit.guess_episode_info(file)

        # Save the infos in the dictionary
        save_episode_progress(shows, guess)

# Create the TvShowTime Object
tvst = tvshowtime.TvShowTime(credentials_secret.temp_token_showtime)

print "////////////////////////"
print "// LAST AIRED EPISODE //"
print "////////////////////////"

for tv_show_name, progress in shows.iteritems():
    last_aired = tvst.get_last_aired_episode(tv_show_name)

    progress_table = PrettyTable(["", "Season", "Episode"])
    progress_table.align[""] = "l"
    progress_table.add_row(["Dowloaded", progress['season'], progress['episode']])
    progress_table.add_row(["Last aired", last_aired['season_number'], last_aired['number']])

    print
    print " " + tv_show_name
    print progress_table
