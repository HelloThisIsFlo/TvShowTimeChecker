import httplib2
from credentials_secret import client_id_showtime, client_secret_showtime, user_agent_showtime, temp_token_showtime
import string
import random
from urllib import urlencode
from pprint import pprint
import urllib2
import json
import dialog
from xml.etree import ElementTree


def random_string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class TvShowTime:
    """ This class is a utility class to connect to the TvShowTime API

    Simply enter your auth infos and use the method : 'make_tvshowtime_request'
    """

    base_url = "https://api.tvshowtime.com/v1"
    base_url_tvdb = "http://thetvdb.com/api/GetSeries.php/api/GetSeries.php"

    def __init__(self, client_id=None, client_secret=None, user_agent=None, token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.token = token

        self.device_code = ''

        if not token and client_id and client_secret and user_agent:
            # Start the authentication process
            self.__make_step_1()
            self.__make_step_2()
        elif not token:
            raise Exception("Please init token OR client_id, client_secret and user_agent")
        # if token present : do nothing

    def __make_tvst_post(self, url, data):
        f = urllib2.Request(url)
        f.add_header('User-Agent', self.user_agent)

        res = urllib2.urlopen(f, data)  # Specifying the data argument transform makes a POST request instead of GET
        return json.load(res)

    def __make_step_1(self):
        step_1_url = "https://api.tvshowtime.com/v1/oauth/device/code?"
        step_1_parameters = urlencode({"client_id": self.client_id})

        step_1_dict = self.__make_tvst_post(step_1_url, step_1_parameters)

        # Print the authentification url and user code
        print "//////////////////////////"
        print "///   AUTHENTICATION   ///"
        print "//////////////////////////"
        print
        print "Please go to this url : " + step_1_dict.get('verification_url', '')
        print "And enter this code : " + step_1_dict.get('user_code', 'ERROR')
        print
        device_code = step_1_dict.get('device_code', '')

        if device_code is '':
            raise Exception('No DEVICE_CODE . . . error somewhere! ^_^')

        # ok_dialog = dialog.Dialog()
        # ok_dialog.make_ok_dialog("Click 'Ok' when authenticated on TvShowTime")
        raw_input("Press Enter to continue...")

        self.device_code = device_code

    def __make_step_2(self):
        step_2_url = "https://api.tvshowtime.com/v1/oauth/access_token"
        step_2_parameters = urlencode({
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": self.device_code
        })
        step_2_dict = self.__make_tvst_post(step_2_url, step_2_parameters)
        token = step_2_dict.get('access_token', '')

        if token is '':
            raise Exception('No TOKEN . . . error somewhere! ^_^')

        self.token = token
        print "Token = " + token
        print

    def make_tvshowtime_request(self, method, parameters):
        # Add token & encode parameters
        parameters['access_token'] = self.token
        encoded_parameters = urlencode(parameters)

        # Make the url
        url = self.base_url + "/" + method + "?" + encoded_parameters
        res = urllib2.urlopen(url)
        return json.load(res)

    def _get_tvdb_serie_id(self, tv_show_name):
        # Create and encode parameters
        parameters = {
            'seriesname': tv_show_name
        }
        encoded_parameters = urlencode(parameters)

        # Make the url
        url = self.base_url_tvdb + "?" + encoded_parameters

        # Make request
        response = urllib2.urlopen(url)

        # Parse response
        response_tree = ElementTree.parse(response).getroot()
        return response_tree.find('Series/seriesid').text  #serie_id

    def test(self, test_arg):
        return self._get_tvdb_serie_id(test_arg)