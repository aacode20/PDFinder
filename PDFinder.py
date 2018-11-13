from googlesearch import search
import os
import requests
import easygui as egui
import tkinter
import queue


def displayMsg(msgid):
    msgid = int(msgid)
    if(msgid == 0):
        egui.msgbox("Welcome to PDFinder", "PDFinder", image = "pdf-icon.png")
    elif(msgid == 1):
        egui.msgbox("No inputs detected, closing program..", "PDFinder")
    elif(msgid == 2):
        egui.msgbox("No PDFs found", "PDFinder")
    elif(msgid == 3):
        egui.msgbox("Thank you for using PDFinder!")
    else: return None

def getURLs(searchterm,pageno):
    URLs = []
    for url in search(searchterm, stop=(pageno*10)):
        i = len(url)
        url = str(url)
        if(url[(i-4):].lower() == '.pdf'):
            URLs.append(url)
    return URLs


def savePDFs(URLs, directory):
    egui.msgbox("Beginning process...","PDFinder")
    if(len(URLs) == 0): return None
    for url in URLs:
        fname = url.rsplit('/',1)[1]
        filename = os.path.join(directory, fname)
        file = requests.get(url)
        with open(filename,'wb') as fd:
            fd.write(file.content)
            fd.close()
        egui.msgbox("Finished! Press OK to Exit", "PDFinder")

def getInputs():
    msg = "Enter the details of your search"
    title = "PDFinder"
    fieldNames = ["Search Term: ", "# Pages: "]
    fieldValues = egui.multenterbox(msg, title, fieldNames)
    if(fieldValues is None): return None
    directory = egui.diropenbox("Select the directory in which you would like the files to be saved", "PDFinder")
    fieldValues.append(directory)
    return fieldValues

def tryAgain():
    tryagain = egui.ynbox("Would you like to try again?")
    if(tryagain == True):
        PDFSaver()


def PDFSaver():
    searchterms = getInputs()
    if(not(searchterms == None)):
        URLs = getURLs(searchterms[0],int(searchterms[1]))
        directory = searchterms[2]
        sv = savePDFs(URLs,directory)
        if(sv == None):
            displayMsg(2)
            tryAgain()

    else: displayMsg(1)

def main():
    displayMsg(0)
    PDFSaver()
    displayMsg(3)


main()