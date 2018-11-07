#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ******************************************************************************
#                                    prepareCSV.py
# SILEX-PHIS
# Copyright © INRA 2018
# Creation date:  07 November, 2018
# Contact: arnaud.charleroy@inra.fr, anne.tireau@inra.fr, pascal.neveu@inra.fr
# ******************************************************************************

import csv
from tools import utils
from tools import log
import dateparser

import os
import re
import os.path

replacedChars = {
    " ": "",
    "'": "",
    "/": "",
    "+": ""
}

DIRECTORY_PATH = ""
OUTPUT_DIRECTORY_PATH = ""
CSV_PATHS = []

for root, dirs, files in os.walk(OUTPUT_DIRECTORY_PATH):
    for file in files:
        os.remove(os.path.join(root, file))

filePaths = utils.getFileNameRecursively(DIRECTORY_PATH)
for filePath in filePaths:
    name = 0
    rows = []
    print(filePath)
    try:
        with open(filePath, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            firstline = True
            for row in spamreader:
                tmpRow = []
                if(firstline):
                    for element in row:
                        tmpRow.append(element)
                    rows.append(tmpRow)
                else:
                    for element in row:
                        element = utils.clean(element, replacedChars)
                        tmpRow.append(element)
                    rows.append(tmpRow)
                firstline = False
    except:
        with open(filePath, 'r', encoding="ISO-8859-1") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                tmpRow = []
                for element in row:
                    element = utils.clean(element, replacedChars)
                    tmpRow.append(element)
                rows.append(tmpRow)

    log.info("Writing")
    print(OUTPUT_DIRECTORY_PATH + utils.getFileNameFromFilePath(filePath))
    with open(OUTPUT_DIRECTORY_PATH + "/" + utils.getFileNameFromFilePath(filePath), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    name = + 1
