from glob import glob
import os
from bs4 import BeautifulSoup

# helper function to write html to file
def writeHTML(fileName, html):
    f = open(fileName, "w+")
    f.write(html)
    f.close()

if __name__ == '__main__':
    # get list of files in no-record folder
    noRecordFiles = glob("/storage/jeremy/imf/exec-archives/html/other/no-record/*.html")
    # print(noRecordFiles)

    # for each file in no-record folder
    for file in noRecordFiles:
        # print(file)
        # open file
        f = open(file, "r")
        # read file
        html = f.read()
        # print(html)
        # parse for record and hierarchy
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find("title").text.strip()
        # if (title != "Request Rejected" and title.count("Simple search") == 0):
        #     print("\n", file)
        #     print("TITLE:", title)

        if title == "Request Rejected":
            num = file.split("/")[-1]
            fileName = "/storage/jeremy/imf/exec-archives/html/other/request-rejected/" + num
            writeHTML(fileName, html)
            os.remove(file)
        elif "Simple search" in title:
            num = file.split("/")[-1]
            fileName = "/storage/jeremy/imf/exec-archives/html/other/temp/" + num
            writeHTML(fileName, html)
            os.remove(file)
        else:
            num = file.split("/")[-1]
            fileName = "/storage/jeremy/imf/exec-archives/html/other/unknown-error/" + num
            writeHTML(fileName, html)
            os.remove(file)

        # if no record try again 10 times before giving up
        # check for duplicate files due to multiple processes running