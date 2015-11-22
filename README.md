# TvShowTimeChecker

## Check your progress on downloaded Tv Shows

This app scans a specific folder to look for tv shows and then compares the last episode present in the directory
with the last aired episode. Optionally also indicate the TvShowTime progress in the Tv Show if available

The information is retrived from the Tv Show Time api so Oauth2 is used to connect to the user's account.
For the app to work, the files need to have the standard file naming convention. eg. "The.Walking.Dead.S06E06.1080p.WEB-DL.DD5.1.H264.mkv"

It uses the libraries :
 * Guessit
 * Prettytable
