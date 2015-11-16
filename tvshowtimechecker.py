import credentials_secret
import tvshowtime
from pprint import pprint


# Main script for the application
tvst = tvshowtime.TvShowTime(
    client_id=credentials_secret.client_id,
    client_secret=credentials_secret.client_secret,
    user_agent=credentials_secret.user_agent_showtime,
    token=credentials_secret.temp_token_showtime
)

parameters = {
    'show_id': '153021'
}

# res = tvst.make_tvshowtime_request("show", parameters)
# pprint(res)

serie_id = tvst.test("The walking dead")
print "Serie_id = " + serie_id