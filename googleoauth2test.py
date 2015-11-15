import pprint
import sys
import httplib2
from googleapiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from credentials_secret import api_key, client_id, client_secret
import dialog
import json


def test_api_books():
    # Get the search text
    dialog_box = dialog.Dialog("Search book : ")
    search_text = dialog_box.result

    print "Searched text via dialog : {text}".format(text=search_text)

    # Returns and instance of an API service object that can be used to make API calls
    service = build("books", "v1", developerKey=api_key)

    # Then check the API library to see all the available functionalities
    # Make a request
    request = service.volumes().list(source="public", q=search_text)
    response = request.execute()


    # Print the number of books retrieved
    print "Found {length} books!".format(length=len(response['items']))

    for book in response.get('items', []):  # Return an empty list if no items, so it's still "iterable"
        volume_info = book.get('volumeInfo', [])

        print "/////////////////////////////////"
        try:
            print unicode("The book '{title}' has the following authors : ".format(title=volume_info['title']))
        except UnicodeEncodeError:
            pass

        i = 0
        for author in volume_info.get('authors', []):
            i += 1
            try:
                print unicode("Author {i} : {author}".format(i=i, author=author))
            except UnicodeEncodeError:
                pass

        print "/////////////////////////////////"
        print
        print


def get_credentials(scope_url):


    # Create a flow object
    flow = OAuth2WebServerFlow(client_id, client_secret, scope_url)

    # Create storage to store the token
    storage = Storage("credentials.dat")

    # Get the OAuth2Credentials object at this point (for the first launch) should be null
    credentials = storage.get()

    # If credential_data is null (first launch) or expired.
    # Create new credential (opens web browser)
    if not credentials or credentials.invalid:
        credentials = tools.run_flow(flow, storage, tools.argparser.parse_args()) # todo Check what the argparser does
        # credentials = tools

    return credentials


def authenticate_http(http, scope_url):
    credentials = get_credentials(scope_url)
    http = credentials.authorize(http)  # Authorise the new client

    return http


# MAIN

# Set the scope url
# scope url (required) I hope it's provided infos by the APIs
scope_url = "https://www.googleapis.com/auth/drive.metadata.readonly"

# Create the connection
http = httplib2.Http()

# Authenticate the connection
authenticate_http(http, scope_url)

# Do stuff with the now authenticated url

# Define the base url for the drive api
base_url = "https://www.googleapis.com/drive/v2"

# Define AND make the request
(response, content) = http.request(base_url + "/files")

# NOW WE HAVE THE CONTENT WOOOHOOO!!!!!!!
# print content

# Transform the content string into a dictionary
content_dict = json.loads(content)


for item in content_dict.get('items', []):
    print item['title']


print "END"





