import credentials_secret
import tvshowtime
from pprint import pprint


# Main script for the application
tvst = tvshowtime.TvShowTime()

parameters = {
    'show_id': '153021'
}

# res = tvst.make_tvshowtime_request("show", parameters)
# pprint(res)

serie_id = tvst.test("The walking dead")
print "Serie_id = " + serie_id