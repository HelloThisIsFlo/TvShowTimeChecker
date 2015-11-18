import guessit
import os

import credentials_secret
import tvshowtime


def print_file_info(guess):
    print "//////////////////////////////////////////////////////////////////////////////"
    print "Name : " + get_value('series', guess)
    print "Season : " + get_value('season', guess)
    print "Episode : " + get_value('episode', guess)
    print "//////////////////////////////////////////////////////////////////////////////"
    print


def get_value(key, dictionary):
    if key in dictionary:
        return str(dictionary[key])
    else:
        return ""


# Create the list of TV Shows
list_tv_show = os.walk(r"R.Torrent\Tv Shows")

# Store the tv show names in a set
set_tv_show = set()
for root, dirs, files in list_tv_show:
    for file_name in files:
        guess = guessit.guess_episode_info(file_name)
        # print_file_info(guess)
        set_tv_show.add(get_value('series', guess))

# Create the TvShowTime Object
tvst = tvshowtime.TvShowTime(credentials_secret.temp_token_showtime)

print "////////////////////////"
print "// LAST AIRED EPISODE //"
print "////////////////////////"

for tv_show in set_tv_show:
    last_aired = tvst.get_last_aired_episode(tv_show)
    print tv_show
    print "Downloaded : "  #todo add latest episode dowloaded
    print "Last aired : " + str(last_aired)




