import guessit
import fileparser
import dialog

def get_value(key, dictionary):
    if key in dictionary:
        return str(dictionary[key])
    else:
        return ""

# Create the fileParser
parser = fileparser.FileParser(r"R:\Torrent")
tv_show_path = "Tv Shows"
list_tv_show = parser.list_file(tv_show_path)

for root, dirs, files in parser.walk_torrent():
    for file_name in files:
        print file_name
        guess = guessit.guess_episode_info(file_name)
        print "Name : " + get_value('series', guess)
        print "Season : " + get_value('season', guess)
        print "Episode : " + get_value('season', guess)
        print

dialog_box = dialog.Dialog("Search book : ")
dialog_box.show()