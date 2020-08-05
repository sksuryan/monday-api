import requests
import json
import datetime
import os
from bs4 import BeautifulSoup
from datetime import datetime

#initializing session object
session = requests.Session()

#Subject dictionaries
subjects = {}

#main url of the site
formURL = 'https://student.amizone.net/'
#post request login url
url = 'https://student.amizone.net/Login/Login'

def login():
  #initial get request to site to get required cookies
  try:
    data = session.get(formURL, timeout = 30)
  except:
    return 'Session timeout or Amizone is down'
  else:
    soup = BeautifulSoup(data.text, 'html.parser')
    #scraping the verification token required for login
    vToken = soup.find('input',attrs = {'name': '__RequestVerificationToken'})
    
    #data for login post request
    payload = {
        "__RequestVerificationToken": vToken['value'],
        "_UserName": os.environ.get('USERNAME'), #your username here
        "_QString": "",
        "_Password": os.environ.get('PASSWORD') #your password here
    }

    #post request for login
    res = session.post(url,data = payload,headers=
        {
            'Referer': formURL, 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
        }
    )
    return res.status_code

def getAttendance():
    #post request url of showing courses
    requestURL = 'https://student.amizone.net/Academics/MyCourses/CourseListSemWise'
    message = ''
    #post request for getting data
    try: 
        newData = session.post(requestURL,data = {'sem': '5'},headers=
            {
                'Referer': formURL, 
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
            },
            timeout = (20,60)
        )
        if newData.history:
            res = login()
            if res == 200:
                return getAttendance()
            else:
                return res
    except:
        return 'Session timeout.'
    else:
        #parsing the loaded page
        soup = BeautifulSoup(newData.text, 'html.parser')
        for elt in soup.findAll('tr'):

            subjectName = elt.find('td', attrs={'data-title': 'Course Name'})
            subjectCode = elt.find('td', attrs={'data-title': 'Course Code'})
            subjectAttendance = elt.find('td', attrs={'data-title': 'Attendance'})
            lastUpdated = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            totalClasses = 0
            totalAttended = 0

            if subjectName is not None:
                subjectName = subjectName.text.strip()
                subjectCode = subjectCode.text.strip()

                if subjectAttendance.button is not None:
                    subjectAttendance = subjectAttendance.button.text.strip()
                    message += f'{subjectName} - {subjectAttendance}\n'
                    pos = None
                    for i in range(len(subjectAttendance)):
                        if subjectAttendance[i] == ' ':
                            pos = i
                            break
                    numbers = subjectAttendance[:pos].split('/')
                    totalClasses = int(numbers[1])
                    totalAttended = int(numbers[0])
                    subject = {}
                    for var in ['subjectName', 'subjectCode', 'totalClasses', 'totalAttended', 'lastUpdated']:
                        subject[var] = eval(var)

                    subjects[subjectCode] = subject
    return message

def loadClasses():
    #post request url of showing courses
    today = datetime.now().strftime('%Y-%m-%d')
    requestURL = f'https://student.amizone.net/Calendar/home/GetDiaryEvents?start={today}&end={today}'
    #post request for getting data
    try: 
        newData = session.get(requestURL,headers=
            {
                'Referer': formURL, 
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
            },
            timeout = (20,60)
        )
        if newData.history:
            res = login()
            if res == 200:
                return loadClasses()
            else:
                return []
    except:
        print('Session timeout.')
        return []
    else:
        return json.loads(newData.text)

def getToday():
    classes = loadClasses()
    message = ''
    if not len(classes):
        message = 'Server timeout.'
    else:
        for Class in classes:
            attendance = ''
            AttndColor = Class["AttndColor"]
            if AttndColor == '#3a87ad':
                attendance = '⏰ Not marked'
            elif AttndColor == '#4FCC4F':
                attendance = '✅ Present'
            else:
                attendance = '❌ Absent'
            message += f'Subject: {Class["title"]}\nStarts at: {Class["start"]}\nEnds at: {Class["end"]}\nFaculty: {Class["FacultyName"]}\nRoom No.: {Class["RoomNo"]}\nAttendance: {attendance}\n\n'
    return message

def getAttendanceForToday():
    classes = loadClasses()
    message = ''
    if not len(classes):
        message = 'Server timeout.'
    else:
        for Class in classes:
            attendance = ''
            AttndColor = Class["AttndColor"]
            if AttndColor == '#3a87ad':
                attendance = '⏰ Not marked'
            elif AttndColor == '#4FCC4F':
                attendance = '✅ Present'
            else:
                attendance = '❌ Absent'
            message += f'Subject: {Class["title"]}\nStarts at: {Class["start"]}\nAttendance: {attendance}\n\n'
    return message