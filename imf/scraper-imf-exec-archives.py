from time import sleep
import requests
from bs4 import BeautifulSoup

# helper function to write html to file
def writeHTML(fileName, html):
    f = open(fileName, "w+")
    f.write(html)
    f.close()

# helper function to convert incremental to string including leading zeroes
def incToString(incremental):
    incString = str(incremental)
    while len(incString) < 6:
        incString = "0" + incString
    return incString

if __name__ == '__main__':
    rootPath = "/storage/jeremy/imf/exec-archives/"
    rootHtmlName = "/storage/jeremy/imf/exec-archives/html/"
    permURL = 'https://archivescatalog.imf.org/Details/ArchiveExecutive/'
    brokenTracker = 0
    totalReqs = 0

    # URL is incrementable - starting with last accessed page (.../125065838.html)
    for incremental in range(90483, 322149):
        totalReqs += 1
        if (incremental % 100 == 0):
            print("Made it to " + incToString(incremental))

        #create OG request
        iterURL = permURL + str(incremental + 125000000)
        headers = {
            'User-Agent': 'Haile Terry: hailedterry@gmail.com'
        }
        # response = requests.get(iterURL)
        response = requests.get(iterURL, headers=headers)

        # parse for record and hierarchy
        soup = BeautifulSoup(response.content, 'html.parser')
        record = soup.find(class_='record')
        hierarchy = soup.find(class_='hierarchy')

        # if no record, save in special folder and continue to next iteration
        if record == None:
            title = soup.find("title").text.strip()
            fileName = rootPath + "other/"

            # for requests rejected by server failure
            if title == "Request Rejected":
                fileName += "request-rejected/"
            # for records that do not exist & returned search home page
            elif "Simple search" in title:
                fileName += "temp/"
            # catch-all for any others
            else:
                fileName += "unknown-error/"
                
            fileName += incToString(incremental) + ".html"
            writeHTML(fileName, soup.prettify())
            brokenTracker += 1

            # if broken for 50 iterations, print debug statements and stop
            if brokenTracker >= 50:
                print("Broken for 50 iterations, stopping on " + incToString(incremental))
                print("Total reqs before stopping: " + str(totalReqs))
                break
            continue

        # parse for file type
        fileType = record.find(class_="label", string="Level of description").parent.find(class_="value").text
        
        # set file path based on file type
        htmlName = rootHtmlName
        if fileType == "item" or fileType == "collection" or fileType == "series" or fileType == "sub-series":
            htmlName += fileType + "/"
        else:
            htmlName += "other/other-file-type/"
        htmlName += incToString(incremental) + ".html"

        # save html to new file
        writeHTML(htmlName, record.prettify()+"\n\n"+hierarchy.prettify())

        # create second request for PDF
        if fileType == "item":
            linkContainer = record.find(class_='ais-image-container')

            # if link container does not exist, save in special folder and continue to next iteration
            if (linkContainer == None):
                htmlName = rootHtmlName + "other/no-link-container/" + incToString(incremental) + ".html"
                writeHTML(htmlName, soup.prettify())
                continue

            pdfURL = linkContainer.find('a')['href']

            # if no href found, save in special folder and continue to next iteration
            if (pdfURL == None):
                htmlName = rootHtmlName + "other/no-url/" + incToString(incremental) + ".html"
                writeHTML(htmlName, soup.prettify())
                continue
            pdfResp = requests.get(pdfURL)

            # save PDF to new text file
            pdfName = rootPath + "pdfs/" + incToString(incremental) + ".pdf"
            f2 = open(pdfName, "wb")
            f2.write(pdfResp.content)
            f2.close()

        brokenTracker = 0
        sleep (1)

        # less file, inside 'F'
        # come back to 125061624 - 125065837

        # if no record try again 10 times before giving up

        # check for duplicate files due to multiple processes running