#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#******************************************************************************
#                                    log.py
# SILEX-PHIS
# Copyright © INRA 2018
# Creation date:  12 September, 2018
# Contact: arnaud.charleroy@inra.fr, anne.tireau@inra.fr, pascal.neveu@inra.fr
#******************************************************************************

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = "\033[1m"
SEP = "\n"

def disable():
    HEADER = ''
    OKBLUE = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''

def success( msg):
    print(OKGREEN + str(msg) + ENDC + SEP)

def info( msg):
    print(OKBLUE + str(msg) + ENDC + SEP)

def warn( msg):
    print(WARNING + str(msg) + ENDC + SEP)

def err( msg):
    print(FAIL + str(msg) + ENDC + SEP)