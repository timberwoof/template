#!/usr/bin/python
#
# unmerge.py
#
# created by Timberwoof 2019-04-13
# copyright (c) 2019 by Timberwoof
try:
    import argparse
    import os
    import io
    import shutil
    import time
    import sys
    import json
    import collections
    sys.path.append('../xmltodict')
    import xmltodict
except ImportError:
    print 'Error: buildMonitor.py failed to import a needed library.'

def formattedTime():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def log(message):
    # write a message to the console and to the current monitor log
    timestring = formattedTime()
    print timestring,message
    try:
        mergeLogFile.write (timestring + ' ' + message + '\n')
    except:
        # fail silently
        pass

def merge (templateFileName, contentFileName, mergedFileName):
    mergeSections = collections.OrderedDict()
    
    log('-------------')
    log('open template file '+templateFileName)
    templateFile = open(templateFileName,'r')
    log('xmltodict.parse')
    templateDict = xmltodict.parse(templateFile)
    log('json.dumps')
    templateJson = json.dumps(templateDict)
    log('json.loads')
    templateObject = json.loads(templateJson)
    commentMarker = templateObject['body']['commentMarker']
    log('commentMarker:'+commentMarker)
    count = len(templateObject['body']['sections']['section'])
    log('count:'+str(count))
    for i in range(0,count):
        #log('i:'+str(i))
        key = templateObject['body']['sections']['section'][i]['@id']
        log('key:'+key)
        value = templateObject['body']['sections']['section'][i]['#text']
        #log('value:'+value)
        mergeSections[key] = value

    log('-------------')
    log('open content file '+contentFileName)
    contentFile = open(contentFileName,'r')
    log('xmltodict.parse')
    contentDict = xmltodict.parse(contentFile)
    log('json.dumps')
    contentJson = json.dumps(contentDict)
    log('json.loads')
    contentObject = json.loads(contentJson)
    count = len(contentObject['body']['sections']['section'])
    for i in range(0,count):
        #log('i:'+str(i))
        key = contentObject['body']['sections']['section'][i]['@id']
        log('key:'+key)
        value = contentObject['body']['sections']['section'][i]['#text']
        #log('value:'+value)
        mergeSections[key] = value

    log('===============')
    log('open output file '+mergedFileName)
    templateFile = io.open(mergedFileName, 'w', encoding='utf-8')
    templateFile.write (commentMarker + ' ---- merge --template '+templateFileName+' --content '+contentFileName+' --merged '+mergedFileName+'\n')
    for key in mergeSections:
        templateFile.write (commentMarker + ' ---- merge section: ' + key + '\n')
        value = mergeSections[key].replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        templateFile.write (value + '\n')
    templateFile.close()

mergeLogFileName = 'mergeLog.log'
mergeLogFile = open(mergeLogFileName,'w');

templateFileName = 'template.xml'
contentFileName = 'content.xml'
mergedFileName = 'merged.txt'

parser = argparse.ArgumentParser(description='Separate a merged file into Template and Content.')
parser.add_argument('--template', dest='templateFileName', type=str, default=templateFileName, help='output template file name')
parser.add_argument('--content', dest='contentFileName', type=str, default=contentFileName, help='output content file name')
parser.add_argument('--merged', dest='mergedFileName', type=str, default=mergedFileName, help='output merged file name')
parser.add_argument('-t', dest='templateFileName', type=str, default=templateFileName, help='output template file name')
parser.add_argument('-c', dest='contentFileName', type=str, default=contentFileName, help='output content file name')
parser.add_argument('-m', dest='mergedFileName', type=str, default=mergedFileName, help='output merged file name')
args = parser.parse_args()
merge(args.templateFileName, args.contentFileName, args.mergedFileName)
log('merge finished')
