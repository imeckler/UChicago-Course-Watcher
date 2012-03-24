import urllib, smtplib
from BeautifulSoup import BeautifulSoup as BS
from time import sleep
from getpass import getpass

courses = []
ans = 'y'
while ans == 'y':
    course = raw_input("Course: ")
    courses.append(course)
    ans = raw_input("Do you want to continue? (y/n): ")

email_address = raw_input("Enter your email address: ")
password      = getpass()
server_name   = raw_input("Enter your SMTP server: ")

def is_available(course):
    url  = 'https://classes.uchicago.edu/courseDetail.php?courseName={0}'.format(course.replace(' ', '%20'))
    soup = BS(urllib.urlopen(url))
    for tag in soup.findAll('div', {'class':'enrolled'}):
        if eval(tag.text) == 0:
            return True
    return False

server = smtplib.SMTP(server_name)
server.ehlo()
server.starttls()
server.login(email_address, password)

while True:
    for course in courses[::]:
        if is_available(course):
            server.sendmail(email_address, [email_address],course)
            courses.remove(course)
    sleep(100)