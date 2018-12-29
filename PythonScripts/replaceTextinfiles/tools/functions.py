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

def createPatternFromWordList(wordsList):
    pattern = r"\b(" + r"(?!(_|-))|".join(wordsList)+ r"(?!(_|-)))\b"
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
        logger.err(err)
        sys.exit()
    return data


def runReplacing(args):
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
            logger.info("Directory created successfully :" +
                        outputDirectoryPath)
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
        if not filename.startswith('.'):
            logger.info("Replace terms in file "  + filename)
            inputFilename = os.path.join(AbsInputDirectoryPath, filename)
            outputFile = os.path.join(AbsOutputDirectoryPath, filename)
            with open(inputFilename,"r",encoding="utf8") as fileIn, open(outputFile,"w",encoding="utf8") as fileOut:
                data = fileIn.read()
                dataOut = multipleReplace(data, vocabulary)
                fileOut.write(dataOut)
       
    logger.info("Replacements done")
