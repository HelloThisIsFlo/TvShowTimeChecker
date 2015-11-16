import credentials_secret
import tvshowtime
from pprint import pprint


# Main script for the application
tvst = tvshowtime.TvShowTime(credentials_secret.temp_token_showtime)

response = tvst.get_last_aired_episode("The walking dead")
pprint(response)