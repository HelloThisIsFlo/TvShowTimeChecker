import guessit
import fileparser
import dialog
import tvshowtime
import credentials_secret


def print_file_info(guess):
    print "//////////////////////////////////////////////////////////////////////////////"
    print "Name : " + get_value('series', guess)
    print "Season : " + get_value('season', guess)
    print "Episode : " + get_value('episode', guess)
    # print
    # if get_value('series', guess) is not "":
    #     last_aired = tvst.get_last_aired_episode(get_value('series', guess))
    #     if last_aired is not None:
    #         print "Last aired : " + str(tvst.get_last_aired_episode(get_value('series', guess)))
    print "//////////////////////////////////////////////////////////////////////////////"
    print


def get_value(key, dictionary):
    if key in dictionary:
        return str(dictionary[key])
    else:
        return ""

# Create the fileParser
parser = fileparser.FileParser(r"R:\Torrent\Tv Shows")
tv_show_path = "Tv Shows"
list_tv_show = parser.walk_torrent()

tvst = tvshowtime.TvShowTime(credentials_secret.temp_token_showtime)

# Store the tv show names in a set
set_tv_show = set()
for root, dirs, files in parser.walk_torrent():
    for file_name in files:
        guess = guessit.guess_episode_info(file_name)
        # print_file_info(guess)
        set_tv_show.add(get_value('series', guess))

print "////////////////////////"
print "// LAST AIRED EPISODE //"
print "////////////////////////"

for tv_show in set_tv_show:
    last_aired = tvst.get_last_aired_episode(tv_show)
    print tv_show
    print "Downloaded : "  #todo add latest episode dowloaded
    print "Last aired : " + str(last_aired)




