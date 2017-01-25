# -*- coding: utf-8 -*-
"""
Created on Tue Nov 01 22:04:06 2016

@author: Andrew Samuelson
"""

import Tkinter
import tkMessageBox
import operator
import numpy as np

from datetime import datetime
from time import sleep
from os import environ

from itertools import product as prod
from itertools import imap

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


#gui for user inputs
top = Tkinter.Tk()

#fullscreen the GUI
top.attributes('-fullscreen', True)

#simple label for a drop down menu
AlsoL = Tkinter.Label(top, text = "Please choose a term: \n")
AlsoL.pack()

#drop down menu for semesters available
var = Tkinter.StringVar(top)
var.set("Please select a term")

#create options for the terms
option = Tkinter.OptionMenu(top, var, "Please select a term", "Fall", "Winter", "Spring", "Summer I", "Summer II")
option.pack()

#label for user instructions
L = Tkinter.Label(top, text = "Please enter your classes (e.g., CS 2114) \n")
L.pack()

#allows the user to enter up to 10 classes
L1 = Tkinter.Label(top, text = "Class 1: ", justify = "left")
L1.pack()
E1 = Tkinter.Entry(top, bd = 5, justify = "right")
E1.pack()

L2 = Tkinter.Label(top, text = "Class 2: ", justify = "left")
L2.pack()
E2 = Tkinter.Entry(top, bd = 5, justify = "right")
E2.pack()

L3 = Tkinter.Label(top, text = "Class 3: ")
L3.pack()
E3 = Tkinter.Entry(top, bd = 5)
E3.pack()

L4 = Tkinter.Label(top, text = "Class 4: ")
L4.pack()
E4 = Tkinter.Entry(top, bd = 5)
E4.pack()

L5 = Tkinter.Label(top, text = "Class 5: ")
L5.pack()
E5 = Tkinter.Entry(top, bd = 5)
E5.pack()

L6 = Tkinter.Label(top, text = "Class 6: ")
L6.pack()
E6 = Tkinter.Entry(top, bd = 5)
E6.pack()

L7 = Tkinter.Label(top, text = "Class 7: ")
L7.pack()
E7 = Tkinter.Entry(top, bd = 5)
E7.pack()

L8 = Tkinter.Label(top, text = "Class 8: ")
L8.pack()
E8 = Tkinter.Entry(top, bd = 5)
E8.pack()

L9 = Tkinter.Label(top, text = "Class 9: ")
L9.pack()
E9 = Tkinter.Entry(top, bd = 5)
E9.pack()

L10 = Tkinter.Label(top, text = "Class 10: ")
L10.pack()
E10 = Tkinter.Entry(top, bd = 5)
E10.pack()

#initialize blank list for finalized class IDs
FinalClassIDs = []
#check class formatting (data validation) to make sure no data error has been made
def ValidateClassData(Class):
    SplitClass = Class.split()
    Valid = True
    
    Dept = SplitClass[0]    
    try:
        Course_Num = int(SplitClass[1])
    except ValueError:
        Valid = False
    Course_Num = str(Course_Num)
    
    if not Dept.isalpha():
        Valid = False
    if (2 > len(Dept)) or (len(Dept) > 4):
        Valid = False
    if len(Course_Num) != 4:
        Valid = False
    
    return Valid

#check to make sure a term has been selected
def TermCheck(Term):
    if Term == "Please select a term":
        return 0

#button function - checks to make sure all classes are in a recognizable format
#and that a term has been chosen. Sends the user back if error is found.
def SubmitClasses():
    Entries = [E1, E2, E3, E4, E5, E6, E7, E8, E9, E10]
    Term = var.get()
    
    ClassIDs = []
    Validate = []
    for user_input in Entries:
        ClassIDs.append(user_input.get())
    while "" in ClassIDs:
        ClassIDs.remove("")

    if len(ClassIDs) == 0:
        tkMessageBox.showinfo("No Entries Made", "Please input numbers.")
        return 0

    for Class in ClassIDs:
        Validate.append(ValidateClassData(Class))
    
    Validate.append(TermCheck(Term))
    if False in Validate:
        Index = Validate.index(False)
        Length = len(ClassIDs[Index])
        InvalidEntry = Entries[Index]
        InvalidEntry.delete(0,Length)
        tkMessageBox.showinfo("Class Error", "One of your entries was invalid. Please correct it.")
    elif 0 in Validate:
        tkMessageBox.showinfo("Term Error", "You did not select a term. Please select a term.")
    else:
        #if everything is correct, classes are appended to final list and the GUI is destroyed
        for Class in ClassIDs:
            FinalClassIDs.append(ClassIDs)
        FinalClassIDs.append(Term)
        top.destroy()
    
#create the submit button
B = Tkinter.Button(top, text = "Submit", command = SubmitClasses)
B.pack()

##this is to be used to create a new GUI for sorting preferences (in progress)
#Lunch = Tkinter.Tk()
#
#LLunch = Tkinter.Label(Lunch, text = "If you would like lunch, please select a time(s): \n")
#LLunch.pack()
#
#LLunch1 = Tkinter.Label(Lunch, text = "11-12")
#LLunch1.pack()
#
#def LunchBreak():
#
#    Lunch.destroy()
#
#BLunch = Tkinter.Button(Lunch, text = "Submit", command = LunchBreak)
#BLunch.pack()
#
#
#
#top.mainloop()

    



#initialize all relevant data. Determine the proper course year, the location
def GetTerm(TermSem):
    Today = datetime.today()
    Year = Today.year
    Month = Today.month
    if TermSem == "Fall":
        TermMonth = '09'
    if TermSem == "Spring":
        TermMonth = '01'
        Year = Year + 1
    elif TermSem == "Summer I":
        TermMonth = '05' #this may need to be fixed later
        if Month > 5:
            Year = Year + 1
    elif TermSem == "Summer II":
        TermMonth = '06'
        if Month > 6:
            Year = Year + 1
    elif TermSem == "Winter":
        TermMonth = '12'
    
    Term = str(Year) + str(TermMonth)
    
    return Term

#break up courses
def ParseCourses(CourseIDs):
    Courses = []
    for course in CourseIDs:
        Courses.append(course.split()) 
    
    return Courses

#directs the webpage to grab information on classes
def findCourses(subjVal, courseNumVal, courseTerm):    
    driver.get("https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_DispRequest")

    try:
        assert "Time Table" in driver.title
    except AssertionError:
        print(datetime.now().strftime('%Y-%m-%d\t%H:%M:%S') + "\tWebsite not loaded.")
        return False
   
    term = Select(driver.find_element_by_name("TERMYEAR"))
    term.select_by_value(courseTerm)

    campus = Select(driver.find_element_by_name("CAMPUS"))    
    campus.select_by_value("0")

    subj = Select(driver.find_element_by_name("subj_code"))
    subj.select_by_value(subjVal)

    courseNum = driver.find_element_by_name("CRSE_NUMBER")
    courseNum.clear()
    courseNum.send_keys(courseNumVal)

    butt = driver.find_element_by_class_name("formbutton")
    butt.click()

    return True
    
#generate list of list of unique classes (takes argument AllPossibleClassesInfo)
def UniqueClass(APCI):
    UniqueClasses = []
    i = 0    
    MaxLen = len(APCI)
    while i < MaxLen:
        if len(APCI) != 0:
            if isinstance(APCI[0], list):
                Class = APCI[0]
                if Class == 0:
                    break
                UClass = []
                ClassName = Class[2]
                LectureType = Class[3]
                for clas in APCI:
                    if isinstance(clas,list):
                        if (ClassName in clas) and (LectureType in clas):
                            UClass.append(clas)
                for clas in UClass:
                    APCI.remove(clas)
                    UniqueClasses.append(UClass)
        i += 1
    
    return UniqueClasses
        



#time is expected in the format of a string "##:##AM/PM" first number can be 1 or 2 digits
#input time to implement in to the time coverter
def TimeParser(Time):
    Colon = Time.find(":")
    Hour = int(Time[:Colon])
    if Hour < 8:
        Hour = Hour + 12
    Minutes = int(Time[Colon+1:Colon+3])
    Hour = Hour - 8
    
    return Hour, Minutes

#small function to help the program jump to the correct position in the time array
def DayBase(Day):
    if Day == "M":
        return 0
    elif Day == "T":
        return 130
    elif Day == "W":
        return 260
    elif Day == "R":
        return 390
    elif Day == "F":
        return 520

        
#input on the days and times to get the array of times
def ConvertTime(Begin, End, Days):
    TimeArray = [0]*650
    Days = Days.split()
    
    for Day in Days:
        Base = DayBase(Day)
        
        begin_Hour, begin_Minute = TimeParser(Begin)
        end_Hour, end_Minute = TimeParser(End)
        
        TimeFrameStart = (begin_Hour * 12) + (begin_Minute/5)
        TimeFrameEnd = (end_Hour * 12) + (end_Minute/5) + 1
        
        i = range(Base+TimeFrameStart,Base+TimeFrameEnd)
        for n in i:
            TimeArray[n] = 1
        
    return TimeArray
    

    
#takes the class times and additional times (recitation) and generates an array of 1s and 0s representing 5 minute intervals
#when a classes are in session
def CreateTimeArray(AllPossibleClassesInfo, AdditionalTimes):
    TimeArray = []
    AddTimesCRN = []
    for Class in AdditionalTimes:
        AddTimesCRN.append(Class[0])
    for Class in AllPossibleClassesInfo:
        CRN = Class[0]
        Day = Class[6]
        Begin = Class[7]
        End = Class[8]
        CurrentArray = ConvertTime(Begin, End, Day)
        
        if CRN in AddTimesCRN:
            FinalArray = []
            Index = AddTimesCRN.index(CRN)
            ExtraClass = AdditionalTimes[Index]
            Day = ExtraClass[6]
            Begin = ExtraClass[7]
            End = ExtraClass[8]
            
            AdditionalArray = ConvertTime(Begin, End, Day)          
            
            i = 0
            while i < len(CurrentArray):
                FinalArray.append(CurrentArray[i] + AdditionalArray[i])
                i += 1
        
        else:
            FinalArray = CurrentArray
        
        TimeArray.append(FinalArray)
    
    return TimeArray

#cleans up redundancies left by the uniqueclasses function
def RedundancyRemover(UniquewRed):
    NewUnique = []
    for row in UniquewRed:
        NewUnique.append(row)
        Start = UniquewRed.index(row) + 1
        Sublist = UniquewRed[Start:]
        while row in Sublist:
            Sublist.remove(row)
            UniquewRed.remove(row)
    return NewUnique    

#returns binary translation of specific class within set of a single class
def DecisionsPerClass(test):
    PossibleDecisions = []
    for uniqueClass in test:
        Index = len(uniqueClass)
        i = 0
        UniqueDecision = []
        UTest = []
        while i < Index:
            NewString = ""
            j = 0
            while j < Index:
                if j == i:
                    NewString += "1"
                else:
                    NewString += "0"
                j += 1
            UniqueDecision.append(NewString)
            i += 1
        PossibleDecisions.append(UniqueDecision)
    return PossibleDecisions

#converts the decisions back to a list (previously a string)
def ConvertDecision(RawDecisions):
    AllDecisions = []
    Concatenate = []
    for decision in RawDecisions:
        Concatenate.append(''.join(decision))
    for string in Concatenate:
        List = []
        for element in string:
            List.append(int(element))
        AllDecisions.append(List)
    
    return AllDecisions


#creates a matrix based on class times and sums the rows. Checks to make sure all rows are less than 2 (no two classes overlap)
def TimeFeasabilityCheck(AllDecisions, TimeMatrix, NumofClasses):
    FeasibleOption = []
    ClassTimes = []
    n = range(2,NumofClasses)
    Time = np.asmatrix(TimeMatrix)
    for Option in AllDecisions:
        Option = np.asarray(Option)
        OptionClassTimes = Option * Time
        Good = 1
        for element in n:
            if element in OptionClassTimes:
                Good = 0
        if Good == 1:
            FeasibleOption.append(Option.tolist())
            ClassTimes.append(OptionClassTimes.tolist())
    return FeasibleOption, ClassTimes

#converts the feasible classes back to class data, creating a list of feasible classes to sign up for            
def ConvertDecisionstoClassData(FeasibleDecisions, APCI):
    FeasibleClassInfo = []
    for Decision in FeasibleDecisions:
        Classes = []
        FeasibleClassInfo.append(OneCheck(Decision, APCI, Classes))
    return FeasibleClassInfo

#recursive method to grab all the class positions
def OneCheck(Decision, APCI, Classes):
    ClassPlace = Decision.index(1)
    Classes.append(APCI[ClassPlace])
    Decision.pop(ClassPlace)
    Decision.insert(0,0)
    if 1 in Decision:
        Classes = OneCheck(Decision, APCI, Classes)
    return Classes



#for unit testing purposes
#ClassIDs = ['ISE 3214', 'ISE 3424', 'ISE 4404', 'ISE 3624', 'STAT 4214', 'PHIL 1204']

#grab the term for classes from the end of the GUI, remove it from the rest of the classes, and load the classes in to a new list
TermSem = FinalClassIDs[-1] 
FinalClassIDs.pop(-1)
ClassIDs = FinalClassIDs[0]

#initialize the Chrome webdriver   
driver = webdriver.Chrome()

#convert the term selected in to a format recognized by the time table of classes
Term = GetTerm(TermSem)
Courses = ParseCourses(ClassIDs)
AllPossibleClassesInfo = []
TempAllClasses = []
AdditionalTimes = []
DoubleHit = 1
for course in Courses:
    findCourses(course[0], course[1], Term)
    Num = range(2,3000)
    for i in Num:
        try:
            FirstElement = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i) + "]/td[1]").text
            TimesCheck = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i) + "]/td[5]").text
            if "* Additional Times *" in str(TimesCheck):
                CRN = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i-1) + "]/td[1]").text
                CourseID = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i-1) + "]/td[2]").text
                ClassName = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i-1) + "]/td[3]").text
                Type = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i-1) + "]/td[4]").text
                CrHr = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i-1) + "]/td[5]").text
                Instructor = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i-1) + "]/td[7]").text
                Days = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i) + "]/td[6]").text
                Begins = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i) + "]/td[7]").text
                Ends = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i) + "]/td[8]").text
                AdditionalTimes.append([str(CRN), str(CourseID), str(ClassName), str(Type), str(CrHr), str(Instructor), str(Days), str(Begins), str(Ends)])
            else:
                CRN = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i) + "]/td[1]").text
                CourseID = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i) + "]/td[2]").text
                ClassName = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i) + "]/td[3]").text
                Type = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i) + "]/td[4]").text
                CrHr = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i) + "]/td[5]").text
                Instructor = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i) + "]/td[7]").text
                Days = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i) + "]/td[8]").text
                Begins = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i) + "]/td[9]").text
                Ends = driver.find_element_by_xpath("//table[@class='dataentrytable']/tbody/tr[" + str(i) + "]/td[10]").text
                TempAllClasses.append([str(CRN), str(CourseID), str(ClassName), str(Type), str(CrHr), str(Instructor), str(Days), str(Begins), str(Ends)])
                AllPossibleClassesInfo.append([str(CRN), str(CourseID), str(ClassName), str(Type), str(CrHr), str(Instructor), str(Days), str(Begins), str(Ends)])
                
            DoubleHit = 1
        except NoSuchElementException:
            if "Comments for CRN" in str(FirstElement):
                DoubleHit += 1
                if DoubleHit == 3:
                    break
                pass
            else:
                break

driver.close()
TimeMatrix = CreateTimeArray(AllPossibleClassesInfo, AdditionalTimes)
UniqueClasses = UniqueClass(TempAllClasses)
UniqueClasses = RedundancyRemover(UniqueClasses)
PossibleClassDecisions = DecisionsPerClass(UniqueClasses)
#create a list of all possible class combinations
RawDecisions = list(prod(*PossibleClassDecisions))
AllDecisions = ConvertDecision(RawDecisions)
FeasibleDecisions, ClassTimes= TimeFeasabilityCheck(AllDecisions, TimeMatrix, len(UniqueClasses))
ClassData = ConvertDecisionstoClassData(FeasibleDecisions, AllPossibleClassesInfo)





