#! /usr/bin/python
#pip install beautifulsoup4
#https://www.digitalocean.com/community/tutorials/how-to-work-with-web-data-using-requests-and-beautiful-soup-with-python-3
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/

from bs4 import BeautifulSoup
import requests #module for web requests
import sys 	#module for sys.exit() to terminate program on-demand
import smtplib #sending email
from email.mime.text import MIMEText #formulating email text
from email.mime.multipart import MIMEMultipart #formulating email
import datetime #getting timestamp


"""
This program collects content from a web page.
PREREQ: pip install requests
"""


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
    soup = BeautifulSoup(page_content, "html.parser")
    #print soup.prettify()
    data = soup.find("meta", itemprop="price")
    print data.get("content")
    return data.get("content")

def send_email(price):
    """send_email() takes in the the price as a string and sends an email. Does not return anything."""

    from_gmail_user = "myspecialemailsender@gmail.com" #DON'T USE YOUR NORMAL EMAIL FOR THIS!
    to_gmail_user = "myspecialemailsender@gmail.com" #DON'T USE YOUR NORMAL EMAIL FOR THIS!
    gmail_password = "mytestpass123*"
    
    #create the message
    msg = MIMEMultipart()
    body = MIMEText("Couch costs: $" + price, "plain")
    msg["Subject"] = "Couch Price Update"
    msg["From"] = from_gmail_user
    msg["To"] = to_gmail_user
    msg.attach(body)

    #send the message
    try:  
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(from_gmail_user, gmail_password)
        server.sendmail(from_gmail_user, to_gmail_user, msg.as_string())
        server.close()

        print "Email sent!"
    except Exception as e: #handle exception 
        print "Email not sent..."
        print e


def write_to_file(price):
    """write_to_file() takes in the price and writes it to a file along with the timestamp"""

    now = datetime.datetime.now() # get the current time
    date_formatted = now.strftime("%Y-%m-%d %H:%M:%S") #format the time into Year-Month-Day Hour:Minute:Second

    #write to the file
    try:
        with open("historical_price.txt", "a+") as myfile: #open historical_price.txt for appending. '+' means create the file if it doesn't exist. 
            myfile.write("Couch Costs: $" + price + " (" + date_formatted + ")" + "\n--------\n") #write price and timestamp to file
            print "Date: " + date_formatted
            print "Wrote to file."
    except Exception as e: #handle exception
        print "File not written..."
        print e


if __name__ == "__main__":
    URL = "https://www.rcwilley.com/Furniture/Living-Room/Sectionals/Fabric/110950208/Beige-2-Piece-Sectional-Sofa-with-RAF-Chaise---Baltic-View.jsp"
    page_content = get_web_page(URL)
    couch_value = parse_page_content(page_content)
    #write_to_file(couch_value)
    print "Couch costs $%s" % (couch_value)
    #if float(couch_value) < 1800: #make couch_value a number and compare and conditionally send email. 
        #send_email(couch_value)
