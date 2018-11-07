#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#******************************************************************************
#                                    utils.py
# SILEX-PHIS
# Copyright © INRA 2018
# Creation date:  13 September, 2018
# Contact: arnaud.charleroy@inra.fr, anne.tireau@inra.fr, pascal.neveu@inra.fr
#******************************************************************************

import os
import json
import sys
import csv
import unidecode
import log as log
import datetime

def serializeDate(self,date):
    """Date object is not serializable by JsonSerializer by default"""
    # Test if the date is serializable
    if type(date) is datetime.date or type(date) is datetime.datetime:
        return date.isoformat()
    else:
        return date

def getExtensionFromFilename(filename):
    extensionWithPoint = os.path.splitext(filename)[1]
    return extensionWithPoint.replace(".", "")

def getNameFromFilename(filename):
    extensionWithPoint = os.path.splitext(filename)[0]
    return extensionWithPoint

# @link https://stackoverflow.com/questions/2212643/python-recursive-folder-read
# walk recursively in directory
def getFileNameRecursively(walk_dir):
    """ Description
    :type walk_dir:
    :param walk_dir:

    :raises:

    :rtype:
    """
    filePaths = []
    for root,directory_names,file_names in os.walk(walk_dir):
        for filename in file_names:
            filePath = os.path.join(root, filename)
            if(os.path.isfile(filePath)):
                filePaths.append(filePath)
    log.info(str(len(filePaths)) + " files found" )
    return filePaths

def getFileNameFromFilePath(filePath):
    """ Description
    :type filePath:
    :param filePath:

    :raises:

    :rtype:
    """
    head, tail = os.path.split(filePath)
    return tail

def removeNewLine(line):
    if(isinstance(line, str)):
        return line.rstrip()
    else:
        return line

def readCSV(filePath):
    with open(filePath, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        return spamreader

def clean(element):
        element = removeNewLine(unidecode.unidecode(element))
        element = element.replace(" ", "")
        element = element.replace("'", "")
        element = element.replace("/", "")
        element = element.replace("+", "")
        return element