import os, sys
import datetime, json

dateTimeEnts = {}

sudokuDir = '/home/makechaos/letsSudoku/'

def loadDateEnts(force=False):
    global dateTimeEnts

    if len(dateTimeEnts)==0 or force:
        dateTimeEnts = json.load(open(sudokuDir+'sudoku.json','r'))

def fresh():
    global dateTimeEnts
    with open(sudokuDir + 'sudokuMain.html','r') as f:
        r = f.read()
    loadDateEnts(True)
    optxt = ''
    for a in dateTimeEnts:
        optxt += '<option value="%s">%s</option>'%(a,a)
    r= r.replace('dateOptions',optxt);
    return r

def update(jsonStr):
    global dateTimeEnts

    jsonData = json.loads(jsonStr)
    curDate = jsonData['date']

    curDate = getDate(curDate)
    # if curDate=='today':
    #     curDate = datetime.datetime.now().strftime('%Y-%m-%d')

    dateTimeEnts[curDate] = jsonStr
    json.dump(dateTimeEnts, open(sudokuDir+'sudoku.json','w'), indent=2)
    return dateTimeEnts[curDate]

def getDate(curDate):
    if curDate=="today":
        curDate = datetime.datetime.now().strftime('%Y-%m-%d')
    return curDate

def clear(dt):
    global dateTimeEnts
    dt = getDate(dt)
    dateTimeEnts[dt] = ""
    json.dump(dateTimeEnts, open(sudokuDir+'sudoku.json','w'), indent=2)
    return "cl-"+dt

def poll(curDate):
    global dateTimeEnts

    loadDateEnts()
    curDate = getDate(curDate)
    if curDate in dateTimeEnts:
        return dateTimeEnts[curDate]
    else:
        return "no-data"