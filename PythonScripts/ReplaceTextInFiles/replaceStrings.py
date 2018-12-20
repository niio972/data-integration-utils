#!/usr/bin/env python
# -*- coding:utf-8 -*-
# ******************************************************************************
#                                    replaceStrings.py
# SILEX-PHIS
# Copyright © INRA 2018
# Creation date:  19 December, 2018
# Contact: arnaud.charleroy@inra.fr, anne.tireau@inra.fr, pascal.neveu@inra.fr
# ******************************************************************************
import argparse
import os
import yaml
import sys
from subprocess import call
from shlex import quote

from tools import log as logger

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

parser = argparse.ArgumentParser()
parser.add_argument("-i", type=str,
                    help="The path of the directory which contains the files to Format",
                    required=True)
parser.add_argument("-o", type=str,
                    help="The path of the directory which will contains the formatted files",
                    required=True)
parser.add_argument("-c", type=str,
                    help="The path of yml vocabulary file",
                    required=True)
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()


def loadVocabularyFile(filePath):
    """ Load config file """
    try:
        with open(filePath, 'r', encoding='utf-8') as config:
            configData = yaml.load(config)
    except Exception as e:
        logger.err("Parsing error \n" + str(e))
        sys.exit()
    return configData


def isValidDir(directoryPath):
    absoluteDirectoryPath = os.path.abspath(directoryPath)
    if(os.path.isdir(absoluteDirectoryPath) and os.path.exists(absoluteDirectoryPath)):
        return True
    else:
        return False


def isValidFile(filePath):
    absoluteFilePath = os.path.abspath(filePath)
    if(os.path.exists(absoluteFilePath)):
        return True
    else:
        return False


def multipleReplace(text, vocabulary):
    """
    take a text and replace words that match the key in a dictionary
    with the associated value, return the changed text
    """
    for uniqTerm in vocabulary:
        for termSearched in vocabulary[uniqTerm]:
            text = text.replace(termSearched, uniqTerm)
    return text


inputDirectoryPath = args.i
outputDirectoryPath = args.o
vocabularyPath = args.c
# valid directory
ValidInputDirectory = isValidDir(inputDirectoryPath)
ValidOutputDirectory = isValidDir(outputDirectoryPath)
ValidVocabularyFile = isValidFile(vocabularyPath)

if(not ValidInputDirectory):
    logger.err(inputDirectoryPath + " is not a valid directory")
if(not ValidOutputDirectory):
    try:
        logger.info("Creating output directory :" + outputDirectoryPath)
        os.makedirs(outputDirectoryPath, exist_ok=True)
        ValidOutputDirectory = True
        logger.info("Directory created successfully :" + outputDirectoryPath)
    except OSError as exc:  # Guard against race condition
        logger.err(outputDirectoryPath + " is not a valid directory")

if(not ValidVocabularyFile):
    logger.err(vocabularyPath + " is not a valid file path")

if(not ValidInputDirectory or not ValidOutputDirectory or not ValidVocabularyFile):
    sys.exit()


AbsInputDirectoryPath = os.path.abspath(inputDirectoryPath)
AbsOutputDirectoryPath = os.path.abspath(outputDirectoryPath)
filenameList = os.listdir(os.path.abspath(AbsInputDirectoryPath))
vocabulary = loadVocabularyFile(vocabularyPath)

for filename in filenameList:
    inputFilename = os.path.join(AbsInputDirectoryPath, filename)
    outputFile = os.path.join(AbsOutputDirectoryPath, filename)

    # Read in the file
    with open(inputFilename, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = multipleReplace(filedata, vocabulary)

    # Write the file out again
    with open(outputFile, 'w') as file:
        file.write(filedata)
