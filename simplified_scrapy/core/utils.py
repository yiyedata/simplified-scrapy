#!/usr/bin/python
#coding=utf-8
import time, io, sys, hashlib, os, re, csv
from time import mktime
if sys.version_info.major == 2:
    from urlparse import urlparse, urljoin
else:
    from urllib.parse import urlparse, urljoin


def getTime(t):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))


def getTimeNow():
    return getTime(time.time())


def convertTime2Str(t, format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, t)


def convertStr2Time(st, format='%Y-%m-%d %H:%M:%S'):
    return mktime(time.strptime(st, format))


__lastMsg = None


def printInfo(*msgs):
    global __lastMsg
    if __lastMsg == msgs[0]:
        return
    __lastMsg = msgs[0]
    print(getTime(time.time()), msgs)


def save2csv(name, rows, encoding="utf-8", mode='w', **other):
    if 'b' in mode: encoding = None
    with io.open(name, mode=mode, encoding=encoding, **other) as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(rows)


def delLastEmptyRow(name):
    with open(name, "rb+") as f:
        f.seek(-1, os.SEEK_END)
        tmp = f.read()
        if tmp == b'\n':
            f.seek(-2, os.SEEK_END)
            tmp = f.read()
            if tmp == b'\r\n':
                f.seek(-2, os.SEEK_END)
            else:
                f.seek(-1, os.SEEK_END)
            f.truncate()


def delEmptyRows(name, encoding="utf-8", **other):
    lines = getFileLines(name, encoding=encoding, **other)
    lines = [line for line in lines if not line]
    saveFile(name, "".join(lines), encoding=encoding, **other)


def saveFile(name, text, encoding="utf-8", mode='w', **other):
    if 'b' in mode: encoding = None
    with io.open(name, mode=mode, encoding=encoding, **other) as file:
        file.write(u'{}\n'.format(text))


def appendFile(name, text, encoding="utf-8", **other):
    with io.open(name, 'a', encoding=encoding, **other) as file:
        file.write(u'{}\n'.format(text))


def getFileContent(name, encoding="utf-8", **other):
    with io.open(name, "r", encoding=encoding, **other) as file:
        return file.read()


def getFileLines(name, encoding="utf-8", **other):
    with io.open(name, "r", encoding=encoding, **other) as file:
        return file.readlines()


def getFileInfo(name):
    return os.stat(name)


def getFileModifyTime(name):
    return os.stat(name).st_mtime


def isExistsFile(name):
    return os.path.isfile(name)


def removeFile(name):
    if isExistsFile(name):
        os.remove(name)


def isExistsDir(name):
    return os.path.isdir(name)


def createDir(name, count=1):
    name = name.rstrip('/')
    if count > 1:
        paths = name.rsplit('/', count - 1)
    else:
        paths = [name.rstrip('/')]
    p = ''
    for i in range(0, count):
        p = p + paths[i] + '/'
        if (not os.path.exists(p)):
            os.mkdir(p)


def getSubDir(name, end=None, have=None, notHave=None):
    filelist = os.listdir(name)
    if have or notHave or end:
        filelist = [
            os.path.join(name, l) for l in filelist
            if _checkName(l, end, have, notHave)
        ]
    return filelist


def getSubFile(name, end=None, have=None, notHave=None):
    filelist = getSubDir(name, end, have, notHave)
    filelist = [l for l in filelist if isExistsFile(l)]
    return filelist


def getSubFolder(name, end=None, have=None, notHave=None):
    filelist = getSubDir(name, end, have, notHave)
    filelist = [l for l in filelist if isExistsDir(l)]
    return filelist


def _checkName(name, end, have, notHave):
    if end and not name.endswith(end):
        return False
    if have and have not in name:
        return False
    if notHave and notHave in name:
        return False
    return True


def saveResponseAsFile(res, path, fileType=None):
    try:
        if fileType:
            if sys.version_info.major == 2: maintype = res.headers.type
            else: maintype = res.info().get('Content-Type')
        if not fileType or (maintype and maintype.find(fileType) >= 0):
            name = ''
            if isExistsDir(path):
                if path[-1] == '/' or path[-1] == '\\': path = path[:-1]
                url = res.url
                name = url[url.rindex('/'):]
                index = name.find('?')
                if index > 0: name = name[:index]
                index = name.find('#')
                if index > 0: name = name[:index]
            file = io.open(path + name, "wb")
            file.write(res.read())
            file.close()
            return True
    except Exception as err:
        print(err)
    return False


def convertUrl2Int(url, count=10):
    value = urlparse(url).netloc
    value = value.split(":")[0]
    myint = 0
    for c in value:
        myint += ord(c)
    return myint % count


def md5(text, encoding="utf-8"):
    if sys.version_info.major == 2:
        return hashlib.md5(text).hexdigest()
    else:
        return hashlib.md5(text.encode(encoding)).hexdigest()


def absoluteUrl(baseUrl, url):
    if (not url or url[:7].lower() == "http://"
            or url[:8].lower() == "https://"):
        return url
    i = url.find('#')
    if (i >= 0):
        url = url[:i]
    if (not url):
        return baseUrl
    if (urljoin):
        return urljoin(baseUrl, url)
    return urlparse.urljoin(baseUrl, url)
