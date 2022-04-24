# library-fetch-article

This simple program uses your public library credentials to access the full text of an article from the Wall Street Journal

To operate it, you need to do the following:
1. Create a mysecrets.py file with username and pin variables
2. Set the environment variable SEARCH_STRING

The program will log into the website, run the search, and export the first search result as a PDF file stored in a unique subfolder within the /tmp directory
