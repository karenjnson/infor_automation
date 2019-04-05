# -*- coding: utf-8 -*-
import re

DEBUG = False
DEBUG2 = False
DEBUG3 = False
DEBUG4 = False
DEBUG6 = False
DEBUG7 = True


############# FUNCTIONS ###############
def log(printComment):
    if DEBUG:
        print printComment

def log2(printComment):
    if DEBUG2:
        print printComment

def storeLinesInFileToArray(file):
    log('Function === storeLinesInFileToArray -------------------')
    theFileArray = []
    isFound = False
    lines = [line.rstrip('\n') for line in open(file)]
    if DEBUG2: print "The total lines in file before and after: {} {}".format(len(file), len(lines))
    for linenum, theLine in enumerate(lines):
        # Only save the lines starting at the Campaigns
        if "Campaign Types" in theLine[:14]:
            if DEBUG2: print "Found Campaign Types: {}".format(linenum)
            isFound = True
        if isFound and len(theLine) > 1 and theLine != "Comm Qualification Rule:":
            theFileArray.append(theLine)
    return (theFileArray)

def getObjectFromArray(theMopTextFileArray, objectType):
    log('Function  === getObjectFromArray -------------------')
    objectList = []
    for lineNum, line in enumerate(theMopTextFileArray):
        if objectType in line:
            objectList.append([str(lineNum), line.split('=')[1].split(']')[0]])
            #print 'The getObjectFromArray== {} {}'.format(objectList[0][0], objectList[0][1])
    return (objectList)

def printArrayList(theArray):
    log('Function  === printArrayList -------------------')
    for object in theArray:
        print "{}".format(object)

def removeMetaCharacters(line):
    theLine = line.strip();
    # remove all metacharacters
    theLine = theLine.replace(r'[','')
    theLine = theLine.replace(r']','')
    #theLine = theLine.replace(r'(','')
    #theLine = theLine.replace(r')','')
    theLine = theLine.replace(r':','')
    return theLine

def removeAttributeField(fieldName):
    fieldname = fieldName.replace(fieldName+"=","")
    return fieldName

def trimAttributeField(fieldName):
    if "=" in fieldName:
        fieldName = fieldName.split("=")[1]
    return fieldName

def trimColonAttributeField(fieldName):
    if ":" in fieldName:
        fieldName = fieldName.split(":")[1]
    return fieldName


def getCampaignAttributes(campaignList):
    campaignArrayList = []

    for campaign in campaignList:
        lineNum = int(campaign[0])
        campaignName = campaign[1]
        campaignDesc = ""
        campaignRule = ""
        campaignArbStrategy = ""
        campaignParent = ""
        campaignAnalyticGroup = ""

        isEndOfCampaign = False;

        #print 'Campaign = {}  =============='.format(campaignName)
        while not isEndOfCampaign and lineNum < len(theMopTextFileArray):
            line = theMopTextFileArray[lineNum]
            line = removeMetaCharacters(line)
            #print '          This line:{}'.format(line)
            if "Campaign Desc" in line:
                if line is not "Campaign Desc":
                    if campaignDesc == "":
                        campaignDesc = '"' + line[len("Campaign Desc"):] + '"'
                    else:
                        campaignDesc = campaignDesc+", char(10), "+ '"'+ line[len("Campaign Desc"):]+ '"'
                    if DEBUG2: print 'Campaign Description:  {}'.format(campaignDesc)

            if "Campaign Arbitration Strategy" in line:
                campaignArbStrategy = line[len("Campaign Arbitration Strategy"):]
                if DEBUG2: print 'Campaign Arbitraton Strategy:  {}'.format(campaignArbStrategy)

            if "Campaign Activation Rule" in line:
                line.rstrip()
                if line is not "Campaign Activation Rule":
                    if campaignRule == "":
                        campaignRule = '"'+line[len("Campaign Activation Rule"):]+'"'
                    else:
                        campaignRule = campaignRule+", char(10), "+ '"'+ line[len("Campaign Activation Rule"):]+'"'
                    if DEBUG2: print 'Campaign Rule:  {}'.format(campaignRule)

            if "Campaign Parent" in line:
                campaignParent =  line[len("Campaign Parent"):]
                if DEBUG2: print 'Campaign Parent  {}'.format(campaignParent)


            if "Campaign Arbitration Analytic Group" in line:
                campaignAnalyticGroup =  line[len("Campaign Arbitration Analytic Group"):]
                if DEBUG2: print 'Campaign AnalyticGroup  {}'.format(campaignAnalyticGroup)

            if "Campaign" is line or len(line) == 8 or "Communication" in line[:13]:
                isEndOfCampaign = True;
                if DEBUG2:  print 'The line is CAMPAIGN'
                campaignName = trimAttributeField(campaignName)
                campaignDesc = trimAttributeField(campaignDesc)
                campaignParent = trimAttributeField(campaignParent)

                #theCampaignString = campaignName + "," + campaignDesc+ "," + campaignRule+ "," + campaignParent+ "," + campaignArbStrategy+ "," + campaignAnalyticGroup
                #print 'THIS - Offer================:  {} {}'.format(lineNum,theCampaignString)

                campaignArrayList.append([campaignName, campaignDesc, campaignRule, campaignParent, campaignArbStrategy, campaignAnalyticGroup])

            lineNum = lineNum+1
    return (campaignArrayList)


def getCampaignRules(campaignArrayList):
    rulesArrayList = []
    campaign = []
    for campaign in campaignArrayList:
        #print 'getCampaignRules: The campaign: {}'.format(campaign)
        #print '      {} {}\n\n'.format(campaign[0], campaign[2])
        rulesArrayList.append([campaign[0], campaign[2]])
    return (rulesArrayList)


def getAttribute(theArray, theObject, theField):
    isFound = False
    theAttributeValue = ""

    for offer in theArray:
        #print offer[0]
        if offer[0] == theObject:
            theAttributeValue = offer[theField]
            isFound = True
            break

    return theAttributeValue


def getCommunicationAttributes(communicationList):
    communicationArrayList = []
    communicationStringList = []

    for communication in communicationList:
        lineNum = int(communication[0])
        commName = communication[1]
        commDesc = ""
        commRule = ""
        commCapExt = ""
        commArbStrategy = ""
        commParent = ""
        commAnalyticGroup = ""
        commBusBenefit = ""

        isEndOfCommunication = False;

        if "=" in commName:
            commName = commName.split("=")[1]
        print 'Communication = {}  =============='.format(commName)
        while not isEndOfCommunication and lineNum < len(theMopTextFileArray):
            line = theMopTextFileArray[lineNum]
            line = removeMetaCharacters(line)
            #line = line.replace("'","")

            #print '          This line:{}'.format(line)
            if "Comm Desc" in line:
                #line = line.rstrip()
                #line = line.lstrip()
                line = line.replace("\n","")
                line = line.replace("\r","")

                if line is not "Comm Desc":
                    if commDesc == "":
                        commDesc = '"' + line[len("Comm Desc"):]+'"'
                    else:
                        commDesc = commDesc+" ,char(10), "+'"'+line[len("Comm Desc"):]+'"'
                    if DEBUG3: print 'Comm Description:  {}'.format(commDesc)

            if "Comm Qualification Rule" in line:
                line = line.rstrip()
                line = line.lstrip()
                line = line.replace("\n","")
                if line is not "Comm Qualification Rule":
                    if commRule == "":
                           commRule = '"'+line[len("Comm Qualification Rule"):]+'"'
                    else:
                        commRule = commRule + '"'+ line[len("Comm Qualification Rule"):]+'"'
                    if DEBUG2: print 'Comm Rule: {} -- {}'.format(line, commRule)

            if "Comm Qualification Cap Extensions" in line:
                commCapExt = line[len("Comm Qualification Cap Extensions"):]
                if DEBUG4: print 'Comm Qualification Cap Extensions {}'.format(commCapExt)


            if "Comm Campaigns List" in line:
                commParent =  line[len("Comm Campaigns List"):]
                commParent = line.split(",")[0]
                if DEBUG7: print 'Comm Campaigns List" {}'.format(commParent)

            if "Comm Likelihood Analytic Group" in line:
                commAnalyticGroup =  line[len("Comm Likelihood Analytic Group"):]
                if DEBUG2: print 'Comm AnalyticGroup  {}'.format(commAnalyticGroup)

            if "Comm Economics" in line:
                matchObj = re.match(r'(.*) B=([0-9]+) (.*)', line, re.M|re.I)
                if matchObj:
                    commBusBenefit = matchObj.group(2);

            if "Communication" == line[:13] or lineNum > len(theMopTextFileArray):
                #"Communication" is line or len(line) == 8 or
                isEndOfCommunication = True;
                #if DEBUG3:  print 'The line is COMMUNICATION'

                commName = trimAttributeField(commName)
                commParent = trimAttributeField(commParent)

               # Get Cascading
                cascadeRule = getCascadingRules(campaignFolderArray, commParent)
                commRule = cascadeRule.rstrip()  + commRule.rstrip()
                commRule = "=concatenate(" + commRule + ")"

                if commDesc is not "":
                    commDesc = "=concatenate(" + commDesc + ")"
                    commDesc = commDesc.replace("CommDesc=", "")



                theCommString = commName + "^" + commDesc+ "^" + commRule+ "^" + commParent+ "^" +commBusBenefit+"^"+ commCapExt+ "^" + commArbStrategy+ "^" + commAnalyticGroup
                #print 'THIS - Offer================:  {} {}'.format(lineNum,theCommString)

                communicationStringList.append(theCommString)
                communicationArrayList.append([commName, commDesc, commRule, commParent,commBusBenefit, commCapExt, commArbStrategy, commAnalyticGroup])

            lineNum = lineNum+1

    #writeToFile(communicationStringList)
    print "=================     Leaving the getCommunicationAttributes ============================================="
    return (communicationArrayList)

def writeToFile(theArray):
    theFile = newFile
    file = open(theFile, "w")

    for eachOffer in theArray:
        file.write(eachOffer)
    file.close()



def getCascadingRules(campaignFolderArray, folderName):
    #print "FUNCTION:  getCascadingRules: {} - END".format(folderName)
    theNewRule = ""
    theObject = folderName
    if folderName is not "":
        while theObject is not "":
            for offer in campaignFolderArray:
                if offer[0] == theObject:
                    # Get the Parent and the Rule
                    theObject = getAttribute(campaignFolderArray, offer[0], 3)
                    theObjectRule = getAttribute(campaignFolderArray, offer[0], 2)
                    theObjectRule = theObjectRule.lstrip()
                    theObjectRule = theObjectRule.rstrip()
                    theObjectRule = theObjectRule.replace("\n"," char(10) ")
                    if theObjectRule != "" or len(theObjectRule) > 2:
                        #print "Found a new offer:  {} -- {}".format(theObject, theObjectRule)
                        theNewRule = theObjectRule + theNewRule
                    break

        #print "The cascade rule for {}".format(folderName)
        #print "     {}".format(theNewRule)
    return theNewRule



############# FUNCTIONS END ###############

############# VARIABLES ###############
filename = "/Users/karenjnson/Downloads/AOL_V1_20190404_223437.txt"
newFile = "/Users/karenjnson/Downloads/inforAutoResults.txt"


lines = []
offerList = []
offerLineNum = []
channelListStr = "Channel: [ChanName"
campaignListStr = "Campaign Object: [CampName="
communicationListStr = "Comm Object: [CommName=webmail_lb"




# Parsing Offers from the Text File
offerArray = [];
offerCapExtension = "No CapExtension";
offerQualRules = "";
offerParent = "No OfferParent";
offerBB = "No BusinessBenefit";
offerActive = "No Active";
offerAnalyticG = "No AnalyticsGroup";
offerArbMethod = "No ArbitrationStrategy"
campaignDesc = ""
campaignRule = ""


############# VARIABLES END ###############

# 1) Open File for Reading
# 2) Get/Print the total number of lines
# 3) Store contents in an array
theMopTextFileArray = storeLinesInFileToArray(filename)
print "The total number of items in theFileArray: {}".format(len(theMopTextFileArray))

# 1) Get Names of Channels, Campaigns, & Communications
# ChannelList will be 0 - the lines above "Campaigns" are deleted prior to parsing file
##channelList = getObjectFromArray(theMopTextFileArray, channelListStr)
##if DEBUG2:   printArrayList(channelList)

campaignList = getObjectFromArray(theMopTextFileArray, campaignListStr)
if DEBUG2:   printArrayList(campaignList)

communicationList = getObjectFromArray(theMopTextFileArray, communicationListStr)
if DEBUG2:   printArrayList(communicationList)


# 2) Print the number of Channels, Campaigns, & Communications
#print 'The total Channels: {}'.format(len(channelList))
print 'The total Campaigns(ParentFolders): {}'.format(len(campaignList))
print 'The total Communications(Offers): {}'.format(len(communicationList))

# 3) Get Attributes of Campaigns & Communications
campaignFolderArray = getCampaignAttributes(campaignList)
print 'The total number of Folders in the campaignFolderArray:  {}'.format(len(campaignFolderArray))

communicationOfferArray = getCommunicationAttributes(communicationList)
print 'The total number of Offers in the communicationOfferArray:  {}'.format(len(communicationOfferArray))

# 4) Get Campaign Rules
campaignRulesArray = getCampaignRules(campaignFolderArray)
print 'The total number of Rules in the Array:  {}'.format(len(campaignRulesArray))

# 5) Write the offers to a file
newFile = "/Users/karenjnson/Downloads/inforAutoResults.txt"

file = open(newFile, "w")

for offer in communicationOfferArray:
    if DEBUG6:  print "The offer to write: {}".format(offer)
##    newOffer = offer
##    for item in range(len(offer)):
##        if item % 2 == 0:
##            newOffer.append("^")
##        newOffer.append(offer[item])
##
##
##
##    file.write("{}".format("{}".format(newOffer)))
##    file.write("\n")

    for item in offer:
        #print "ITEM: {} --END".format(item)
        item.rstrip()
        #item.lstrip()
        #item.replace("\r\n", "char(10)")
        file.write(item+" ^ ")
    file.write("\n")
file.close()
