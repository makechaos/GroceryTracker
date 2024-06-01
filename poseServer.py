import glob, os
import json

dataDir = "/home/makechaos/PoseView/data/"
templateDir = "/home/makechaos/PoseView/templates/"
serverip = "http://makechaos.pythonanywhere.com/"

def upload(tempFile):
    with open(tempFile,'r') as f:
        l = f.readline()
    newName = '-'.join(l.split(',')[:2])+'.csv'
    os.rename(tempFile, os.path.join(dataDir,newName))
    return showAllEntries()

def saveTags(fname, tags):
    try:
        with open( os.path.join(dataDir,fname+'_tags.json'), 'w') as f:
            f.write(json.dumps(tags,indent=2))
    except:
        return str(sys.exc_info())
    return 'updated tags successfully '+fname

def getAllData():
    fils = glob.glob(dataDir+"/*.csv")
    fils.sort()
    return fils

def renderHtml(template, tags):
    html = ''
    with open(templateDir+'/'+template,'r') as f:
        html = '\n'.join(f.readlines())

    for tag in tags:
        html = html.replace(tag, tags[tag])

    return html

def showAllEntries():
    fils = [os.path.basename(x) for x in getAllData()]
    txt = '<table>'
    for nfil, fil in enumerate(fils):
        txt += '<tr><td><a href="%s">%s</a></td></tr>'%(serverip+'poses/view/%s'%fil,fil)
    txt += '</table>'
    return renderHtml('viewFiles.html',{'{{table}}':txt})

def showPose(nfile):
    # fils = getAllData()
    # file = fils[int(nfile)]
    file = nfile
    with open(os.path.join(dataDir,file),'r') as f:
        data = f.readlines()
    if data[0].find('(')>0:
        data = ['['+x.replace(')','').replace('(','')+']' for x in data]
        data = '['+ ','.join(data)+']'
    else:
        data = ''.join(data)

    fname = file.split('.csv')[0]
    tagsFile = os.path.join(dataDir,fname+'_tags.json')
    tags = [];
    if os.path.isfile(tagsFile):
        tags = json.load(open(tagsFile,'r'))

    kvs = {'{{posesData}}':data,'{{fname}}':fname,'{{tags}}':json.dumps(tags)}
    kvs['{{hostip}}']  = serverip
    return renderHtml('poseViewTemplate.html',kvs)