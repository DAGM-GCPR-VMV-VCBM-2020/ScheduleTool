"""
ScheduleTool to create a Time Table for a conference out of a Google Spreadsheet
Create by Jules Kreuer (@not_a_feature) for the GCPR VMV VCBM Conference 2020 
https://www.gcpr-vmv-vcbm-2020.uni-tuebingen.de/?page_id=886

OBACHT! READ THIS FIRST BEFORE YOU DO ANYTHING!
Before you run this program, you have to obtain an API key for Google Sheets!
See here: https://developers.google.com/sheets/api/quickstart/python
Place the file 'credentials.json' into ~/.config/gspread/credentials.json
AFTER THIS, install the needed requirements via pip (requirements.txt is included).
THEN, configure the file you want to get from Google Sheets below.
"""

import gspread
import time
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/XXXXXXXXXXXXXXX"

SHOW_TRACK = False
SHOW_CHAIR = True
SHOW_SPEAKER = True

# Defines the boundaries of which the label of the grids are printed
# You may need to adapt the style.css for
GRID_HOUR_START = 8
GRID_HOUR_END = 18


"""
This reads the contents of a Google Docs document that contains a row-based format.
Multiple sheets can be selected per document, i.e. for different parts of a conference.
"""
def get_sheets(scopes, url):
    gc = gspread.oauth(scopes)
    workbook = gc.open_by_url(url)
    timetable = workbook.worksheet("timetable")

    tt = timetable.get_all_records()
    return tt

"""
This creates a label for the timeslots from GRID_HOUR_START to GRID_HOUR_END in 30 minutes steps 
You may need to adapt the style.css for a 15 minutes grid or times prior/past 
"""
def createGrid():
    out = ''
    for i in range(GRID_HOUR_START , GRID_HOUR_END):
        out += '<h2 class="time-slot" style="grid-row: time-' + leadO(i) + '30;">' + leadO(i) + ':30</h2>\n'
        out += '<h2 class="time-slot" style="grid-row: time-' + leadO(i+1) + '00;">' + leadO(i+1) + ':00</h2>\n'
    return out

"""
This returns a string with a leading Zero if the length equals one
"""
def leadO(i):
    i = str(i)
    if len(i) == 1:
        i = "0" + i
    return i

"""
This takes a event dictionary and creates the html
"""
def create_event(event):
    if event['hidden'] == 'true':
        return ''
    # Customize this!
    if event['track'] == 'joint':
        grid = 'gcpr-start / vcbm-end'
        track = ""
    elif event['track'] == 'vmv-vcbm':
        grid = 'vmv-start / vcbm-end'
        track = "VMV & VCBM"
    else:
        grid = event['track']
        track = event['track'].upper()


    #adds a class for short sessions
    inline = ""
    if event["short"] == 'true':
        inline = 'shortSession'
    
    #Converts start and end time to string with leading zero
    event['start_time'] = str(event['start_time'])  
    event['end_time'] = str(event['end_time']) 
    if len(event['start_time']) == 3: 
        event['start_time'] = '0' + event['start_time']
    if len(event['end_time']) == 3: 
        event['end_time'] = '0' + event['end_time']  

    #Creates human readable time (example: 08:00 - 12:30)
    humanTime = event['start_time'][:2] + ":" + event['start_time'][2:] + " - " + event['end_time'][:2] + ":" + event['end_time'][2:]
    
    #Creates html for session
    """ Example:
        <a href="#vcbm_talks5" class="session session-vcbm_talks5 vcbm" style="grid-column: vcbm; grid-row: time-1100 / time-1230;">
                <h3 class="session-title ">Talks 5: Vascular and Flow</h3>
                <span class="session-time  ">11:00 – 12:30</span>
        </a>
    """
    out = '<a href="#' + event['id'] + '" class="session session-' + event['id'] + ' ' + event['class'] + '"\n'
    out += 'style = "grid-column: ' + grid + '; grid-row: time-' + event['start_time'] + ' / ' + 'time-' + event['end_time'] + ';">\n'
    out += '<h3 class="session-title ' + inline + '">' + event['title'] + '</h3>\n'
    out += '<span class="session-time  ' + inline + '">' + humanTime + '</span>\n'
    # Show / Hide Track information
    if SHOW_TRACK and track != "":
        out += '<span class="session-track  ' + inline + '">Track: ' + track + '</span>\n'

    # Show / Hide Speaker information
    if SHOW_SPEAKER and event['speaker'] != "":
        out += '<span class="session-speaker  ' + inline + '">Speaker: ' + event['speaker'] + '</span>\n'
    out += '</a>\n\n'
    return out

"""
This saves a string to a file. Overwrites existing file
"""
def saveFile(out):
    with open('schedule.html', 'w+') as f:
        f.write(out)

"""
This creates html placed on top of each day
"""
def mid(day):
    out = '<div class="' + day + ' weekday">\n'
    out += '<h2 id="schedule-heading">' + day + '</h2>'
    midFile = open("mid.html", "r") 
    mid = midFile.read()
    midFile.close()
    out += mid
    return out


if __name__ == '__main__':
    print("Fetching Google sheet...")
    tt = get_sheets(SCOPES, SPREADSHEET_URL)
    
    days = [tt[0]["day"]]
    for i in tt:
        if i["day"] not in days:
            days.append(i["day"])
    
    #Creating header and other information
    ts = time.gmtime()
    out = "<!--CSS Grid ScheduleTool by Jules Kreuer, Autogenerated on " + str(time.strftime("%Y-%m-%d %H:%M:%S", ts)) + ' -->\n\n'
    out += '<div class="weekdayContainer">'
    first = True
    for day in days:
        print("Creating: " + day)
        out += mid(day)
        if first:
            out += createGrid()
            first = False
        for i in tt:
            if i['day'] == day:
                    out += create_event(i)
        out += '</div></div>\n\n'

    out += '</div>\n'
    print("Writing file")
    saveFile(out)
    print("Done! Please check the file schedule.html")

