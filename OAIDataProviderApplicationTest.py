# Alex Priscu
# Program that takes in OAI-PMH Request verbs and provides Responses.
# OAI Data Provider Application
# 11 August 2020

# !/usr/bin/python3

# Imports
import os
import xmltodict
from dicttoxml import dicttoxml
from dict2xml import dict2xml

import pprint
from lxml import etree
from xmlutils import Rules, dump_etree_helper, etree_to_string
import simpledc
import cgi
from datetime import datetime
import xml.etree.ElementTree as ET

form = cgi.FieldStorage()

#query = form.getvalue("verb","")
query = form["verb"].value

#query = 'ListRecords'
baseURL = "www.heriport.com"
print ("Content-type: text/html\n")

if (query == 'GetRecord'):
    """Get a record for a metadataPrefix and identifier.

    metadataPrefix - identifies metadata set to retrieve
    identifier - repository-unique identifier of record

    Should raise error.CannotDisseminateFormatError if
    metadataPrefix is unknown or not supported by identifier.

    Should raise error.IdDoesNotExistError if identifier is
    unknown or illegal.

    Returns a header, metadata, about tuple describing the record.
    """

    #metadataPrefix = form["metadataPrefix"].value
    #identifier = form.["identifier"].value

    #metadataPrefix = "oai_dc"
    #identifier = "1"
    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
    verbResponseDate = "<responseDate>"
    verbResponseDate += str(datetime.now())
    verbResponseDate += "</responseDate>"

    verbRequest = "<request verb=\"GetRecord\" identifier=\""
    verbRequest += identifier+"\"\n         metadataPrefix=\""
    verbRequest += metadataPrefix+"\""+baseURL+"</request>\n<GetRecord>"

    response = []
    response.append(verbResponseHeader)
    response.append(verbResponseDate)
    response.append(verbRequest)

    fileName = "stories-dc/metadata-"+identifier+"-dc.xml"
    try:
        with open(fileName) as file:
            data = file.read()
            #print(data)
    except:
        print(" Content-type: text/html\n Error")

    splitString = "<dc:identifiers>"+identifier+"</dc:identifiers>"
    split = data.split(splitString)

    if len(split) == 2:
        part1 = split[0]
        part1 = part1[0:len(part1)-3]
        part2 = split[1]
        data = part1+part2

    data = "<metadata>"+data+"</metadata>"
    headerIdentifier = "<header>\n  <identifier>"+identifier+"</identifier>"
    headerDatestamp = "\n  <datestamp>"+str(datetime.now())+"</datestamp>\n</header>"

    header = []
    header.append(headerIdentifier)
    header.append(headerDatestamp)
    strHead = ' '.join([str(elem) for elem in header])

    record = []
    record.append(strHead)
    record.append(data)
    strRec = ' '.join([str(elem) for elem in record])

    responseEnd = "</GetRecord> \n</OAI-PMH>"

    response.append(strRec)
    response.append(responseEnd)

    strResp = ' '.join([str(elem) for elem in response])
    print("Content-type: text/html\n"+strResp)

else:
# Error handling
    print ("Content-type: text/html\n Error")
