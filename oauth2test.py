import pprint
import sys
from googleapiclient.discovery import build
import credentials
import dialog


# Get the search text
dialog_box = dialog.Dialog("Search book : ")
search_text = dialog_box.result

print "Searched text via dialog : {text}".format(text=search_text)

# Returns and instance of an API service object that can be used to make API calls
service = build("books", "v1", developerKey=credentials.api_key)

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