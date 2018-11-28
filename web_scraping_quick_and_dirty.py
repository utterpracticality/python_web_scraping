#! /usr/bin/python

'''
This program collects content from a web page.
PREREQ: pip install requests
'''


import requests #module for web requests
import sys 	#module for sys.exit() to terminate program on-demand


def get_web_page(URL):
    """get_web_page() ingests a URL and requests that web page, returning the text of the web page"""

    webrequest = "" #declare the string in the function. We'll use it to store the web page.
    error = False
    try:
        webrequest = requests.get(URL)
    except Exception as e: #this will trigger if the web page URL doesn't resolve
        #can also utilize webrequest.status_code to return the status code and check if that is 200 OK
        print e  #print the exception if the web page fails to resolve
        error = True

    if not error:
        page_text = webrequest.text #this gets the text of the request
        return page_text
    else:
        print "Web request failed. Exiting..."
        sys.exit() #web request failed so let's quit the program


def parse_page_content(page_content):
    """parse_page_content() takes in the text of a web page and parses it looking for the cost of the couch, returning the cost"""

    couch_index = page_content.find("price\" content=") #this finds the index of the string we're looking for
    value = page_content[couch_index:couch_index + 30]

    if value:
        #print value #value right now is: price" content="1799.99">
        value = value.split("=")[1].replace(">","").replace('\"',"").rstrip()
        #value.split("=") returns list of two items. 0th element is [price" content] and 1st element is ["1799.99">].
        #[1].replace(">","") returns the first element and replaces > with nothing (basically deletes that character) so we now have "1799.99".
        #.replace('\"',"") replaces the " characters with nothing (deletes them), so we're now left with 1799.99.
        #.rstrip() deletes any trailing spaces or newline characters.
        return value
    else:
        print "Empty value. Exiting..."
        sys.exit()


if __name__ == "__main__":
    URL = 'https://www.rcwilley.com/Furniture/Living-Room/Sectionals/Fabric/110950208/Beige-2-Piece-Sectional-Sofa-with-RAF-Chaise---Baltic-View.jsp'
    page_content = get_web_page(URL)
    couch_value = parse_page_content(page_content)
    print "Couch costs $%s" % (couch_value)
