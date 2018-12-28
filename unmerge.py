#!/usr/bin/python
#
# merge.py
#
# created by Timberwoof 2018-12-28
# copyright (c) 2018 by Timberwoof
#
try:
    import argparse
    import os
    import shutil
    import time
    import sys
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

def unmerge(templateFileName, contentFileName, mergedFileName):
    tempContentFileName = contentFileName + '.t'
    tempTemplateFileName = templateFileName + '.t'

    log('merged file: '+mergedFileName)
    try:
        mf = open(mergedFileName,'r')
        mergedFile = mf.read()
    except:
        log('Error: could not read merged file: '+mergedFileName)
        return;
            
    log('content file: '+contentFileName)
    try:
        cf = open(tempContentFileName,'w')
    except:
        log('Error: could not open content file: '+tempContentFileName)
        return;

    log('template file: '+templateFileName)
    try:
        tfi = open(templateFileName,'i')
        templateFile = tfi.read()
    except:
        log('Error: could not read template file: '+templateFileName)
        return;
    try:
        tfo = open(tempTemplateFileName,'w')
    except:
        log('Error: could not open template file: '+tempTemplateFileName)
        return;

mergeLogFileName = 'mergeLog.log'
mergeLogFile = open(mergeLogFileName,'w');
log('unmerge: Log Begins')


templateFileName = 'template.txt'
contentFileName = 'content.txt'
mergedFileName = 'merged.txt'

parser = argparse.ArgumentParser(description='Separate a merged file into Template and Content.')
parser.add_argument('--template', dest='templateFileName', type=str, default=templateFileName, help='output template file name')
parser.add_argument('--content', dest='contentFileName', type=str, default=contentFileName, help='output content file name')
parser.add_argument('--merged', dest='mergedFileName', type=str, default=mergedFileName, help='output merged file name')
args = parser.parse_args()
unmerge(args.templateFileName, args.contentFileName, args.mergedFileName)

