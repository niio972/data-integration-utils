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
    if(os.path.isfile(absoluteFilePath) and os.path.exists(absoluteFilePath)):
        return True
    else:
        return False

def isValidDirOrFile(path):
   return isValidDir(path) or isValidFile(path)        

def createPatternFromWordList(wordsList,strictPattern):
    wordsList_escaped = [re.escape(x) for x in wordsList]
  
    if(strictPattern == True) :
        pattern = r"\b(?!(_|-))(" + r"|".join(wordsList_escaped)+ r")(?!(_|-))\b"
    else: 
        pattern =  r"|".join(wordsList_escaped)
    print(pattern)
    return pattern

def multipleReplace(data, vocabulary,strictPattern):
    """
    take a text and replace words that match the key in a dictionary
    with the associated value, return the changed text
    """
    # data = data.replace("_","").replace("-","")
    try:
        for uniqTerm in vocabulary:
            pattern = createPatternFromWordList(vocabulary[uniqTerm],strictPattern)
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

    vocabulariesFilesPath = args.c # list

    strictPattern = args.nostrictpattern
    # valid directory
    validInputFileOrDir = isValidDirOrFile(inputDirectoryOrFilePath)
    validOutputDirectory = isValidDir(outputDirectoryPath)
    

    if(not validInputFileOrDir):
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

    
    for vocabularyFilePath in vocabulariesFilesPath:
        validVocabularyFile = isValidFile(vocabularyFilePath)
        if(not validVocabularyFile):
            logger.err(vocabularyFilePath + " is not a valid file path")
            sys.exit()
    
    if(not validInputFileOrDir or not validOutputDirectory or not validVocabularyFile):
        sys.exit()

    
    absOutputDirectoryPath = os.path.abspath(outputDirectoryPath)
   

    if(isValidDir(inputDirectoryOrFilePath)):
        absInputDirectoryPath = os.path.abspath(inputDirectoryOrFilePath)
        # if it is a directory 
        filenameList = os.listdir(os.path.abspath(absInputDirectoryPath))
    if(isValidFile(inputDirectoryOrFilePath)):
        # if it is a file
        absInputDirectoryPath = os.path.dirname(inputDirectoryOrFilePath)
        filenameList= [os.path.basename(inputDirectoryOrFilePath)]

    for filename in filenameList:
        if not filename.startswith('.'):
            logger.info("Replace terms in file "  + filename)
            inputFilename = os.path.join(absInputDirectoryPath, filename)
            outputFile = os.path.join(absOutputDirectoryPath, filename)
            with open(inputFilename,"r",encoding="utf8") as fileIn, open(outputFile,"w",encoding="utf8") as fileOut:
                data = fileIn.read()
                for vocabularyFilePath in vocabulariesFilesPath:
                    vocabulary = loadVocabularyFile(vocabularyFilePath)
                    data = multipleReplace(data, vocabulary,strictPattern)
                fileOut.write(data)
    # if it is a file
    #    
    logger.info("Replacements done")
