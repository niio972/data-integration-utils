#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ******************************************************************************
#                                    functions.py
# BigDataGrapes
# Copyright © INRA 2018
# Creation date:  20 December, 2018
# Contact: arnaud.charleroy@inra.fr, anne.tireau@inra.fr, pascal.neveu@inra.fr
# ******************************************************************************


import os
import sys
import yaml
import re
from subprocess import call

from tools import log as logger


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

def isValidDirOrFile(path):
   return isValidDir(path) or isValidFile(path)        

def createPatternFromWordList(wordsList):
    pattern = r"\b(?!(_|-))(" + r"|".join(wordsList)+ r")(?!(_|-))\b"
    return pattern

def multipleReplace(data, vocabulary):
    """
    take a text and replace words that match the key in a dictionary
    with the associated value, return the changed text
    """
    # data = data.replace("_","").replace("-","")
    try:
        for uniqTerm in vocabulary:
            pattern = createPatternFromWordList(vocabulary[uniqTerm])
            pattern = re.compile(pattern)
            data = pattern.sub(uniqTerm, data)
    except TypeError as err:
        print(vocabulary[uniqTerm])
        logger.err(err)
        sys.exit()
    return data


def runReplacing(args):
    inputDirectoryOrFilePath = args.i
    outputDirectoryPath = args.o

    vocabularyPath = args.c

    # valid directory
    validInputFile = isValidDirOrFile(inputDirectoryOrFilePath)
    validOutputDirectory = isValidDir(outputDirectoryPath)
    validVocabularyFile = isValidFile(vocabularyPath)

    if(not validInputFile):
        logger.err(inputDirectoryOrFilePath + " is not a valid directory or file")
    if(not validOutputDirectory):
        try:
            logger.info("Creating output directory :" + outputDirectoryPath)
            os.makedirs(outputDirectoryPath, exist_ok=True)
            validOutputDirectory = True
            logger.info("Directory created successfully :" +
                        outputDirectoryPath)
        except OSError as exc:  # Guard against race condition
            logger.err(outputDirectoryPath + " is not a valid directory")

    if(not validVocabularyFile):
        logger.err(vocabularyPath + " is not a valid file path")

    if(not validInputFile or not validOutputDirectory or not validVocabularyFile):
        sys.exit()

    absInputFileOrDirectoryPath = os.path.abspath(inputDirectoryOrFilePath)
    absOutputDirectoryPath = os.path.abspath(outputDirectoryPath)
    vocabulary = loadVocabularyFile(vocabularyPath)

    if(isValidDir(absInputFileOrDirectoryPath)):
        # if it is a directory 
        filenameList = os.listdir(os.path.abspath(absInputFileOrDirectoryPath))
    if(isValidFile(absInputFileOrDirectoryPath)):
        # if it is a directory 
        filenameList= [os.path.abspath(absInputFileOrDirectoryPath)]

    for filename in filenameList:
        if not filename.startswith('.'):
            logger.info("Replace terms in file "  + filename)
            inputFilename = os.path.join(absInputFileOrDirectoryPath, filename)
            outputFile = os.path.join(absOutputDirectoryPath, filename)
            with open(inputFilename,"r",encoding="utf8") as fileIn, open(outputFile,"w",encoding="utf8") as fileOut:
                data = fileIn.read()
                dataOut = multipleReplace(data, vocabulary)
                fileOut.write(dataOut)
    # if it is a file
    #    
    logger.info("Replacements done")
