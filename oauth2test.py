import pprint
import sys
from googleapiclient.discovery import build
import credentials

# Returns and instance of an API service object that can be used to make API calls
service = build("books", "v1", developerKey=credentials.api_key)

# Then check the API library to see all the available functionalities
# Make a request
request = service.volumes().list(source="public", q="android")

response = request.execute()
pprint.pprint(response)

# Print the number of books retrieved
print "Found {length} books!".format(length=len(response['items']))
for book in response.get('items',[]): # Return an empty list if no items, so it's still "iterable"
    pprint.pprint(book)
    print "///////////////////////////////////////////////////////////////////////"
    print

    # Test
    i = 0
    for author in book['volumeInfo']['authors']:
        i += 1
        print "Author {i} : {name}".format(i=i, name=author)

    # Retrieve the interesting variables
    title = book['volumeInfo']['title']
    authors = book['volumeInfo']['authors']

