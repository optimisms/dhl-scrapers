from glob import glob
import os
from bs4 import BeautifulSoup

def writeHTML(fileName, html):
    f = open(fileName, "w+")
    f.write(html)
    f.close()

if __name__ == '__main__':
    noRecordFiles = glob("/storage/jeremy/imf/exec-archives/html/other/no-record/*.html")

    for file in noRecordFiles:        
        f = open(file, "r")
        html = f.read()
        f.close()

        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find("title").text.strip()
        num = file.split("/")[-1]
        fileName = "/storage/jeremy/imf/exec-archives/html/other/"

        if title == "Request Rejected":
            fileName += "request-rejected/"
        elif "Simple search" in title:
            fileName += "temp/"
        else:
            fileName += "unknown-error/"
            
        fileName += num
        writeHTML(fileName, html)
        os.remove(file)

        # if no record try again 10 times before giving up
        # check for duplicate files due to multiple processes running