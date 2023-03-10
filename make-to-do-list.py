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
            continue
            num = file.split("/")[-1]
            fileName = "/storage/jeremy/imf/exec-archives/html/other/request-rejected/" + num
            writeHTML(fileName, html)
            os.remove(file)
        elif "Simple search" in title:
            print(file)
            num = file.split("/")[-1]
            fileName = "/storage/jeremy/imf/exec-archives/html/other/temp/" + num
            writeHTML(fileName, html)
            os.remove(file)
            break
        # else:
        #     print(file)
        #     num = file.split("/")[-1]
        #     fileName = "/storage/jeremy/imf/exec-archives/html/other/unknown-error/" + num
        #     writeHTML(fileName, html)
        #     os.remove(file)
        #     break

        # if no record, save in special folder and continue to next iteration
        # if record == None:
        #     htmlName = "/storage/jeremy/imf/exec-archives/html/other/no-record/" + incToString(incremental) + ".html"
        #     writeHTML(htmlName, soup.prettify())
        #     brokenTracker += 1

        #     # if broken for 50 iterations, print debug statements and stop
        #     if brokenTracker >= 50:
        #         print("Broken for 50 iterations, stopping on " + incToString(incremental))
        #         print("Total reqs before stopping: " + str(totalReqs))
        #         break
        #     continue

        # from glob import glob
        # give it the path /storage/jeremy/imf/exec-archives/html/other/no-record/
        #python os module - delete a file
        # if no record try again 10 times before giving up

        # check for duplicate files due to multiple processes running