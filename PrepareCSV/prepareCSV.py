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
    dateColumn = []
    print(filePath)
    try:
        with open(filePath, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            firstline = True
            for row in spamreader:
                tmpRow = []
                if(firstline):
                    for element in row:
                        if(element.find('date') != -1):
                            print(element)
                            dateColumn.append(True)
                        else:
                            dateColumn.append(False)
                        tmpRow.append(element)
                    rows.append(tmpRow)
                else:
                    i = 0
                    while i < len(row):
                        element = row[i]
                        element = utils.clean(
                            element, replacedChars, dateColumn[i]
                            )
                        tmpRow.append(element)
                        i += 1

                    rows.append(tmpRow)
                firstline = False
    except:
        pass
        # with open(filePath, 'r', encoding="ISO-8859-1") as csvfile:
        #     spamreader = csv.reader(csvfile, delimiter=',')
        #     for row in spamreader:
        #         tmpRow = []
        #         for element in row:
        #             element = utils.clean(element, replacedChars)
        #             tmpRow.append(element)
        #         rows.append(tmpRow)

    log.info("Writing")
    with open(OUTPUT_DIRECTORY_PATH + "/" + utils.getFileNameFromFilePath(filePath), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    log.success(OUTPUT_DIRECTORY_PATH + utils.getFileNameFromFilePath(filePath))
    name = + 1
