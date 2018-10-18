# Import the necessary resources
from datetime import datetime, date, time, timedelta
import urllib.request
import re
import os

# Define the URL to download from, and the filename to save to
logurl = "https://s3.amazonaws.com/tcmg476/http_access_log" 
logfile = "locallog.txt"

# Define funtion to download the file if it is not already downloaded
def getFile():
    if not os.path.exists(logfile):
        print("Downloading log file. Please wait.")
        urllib.request.urlretrieve(logurl, "locallog.txt")

# Define function to parse through the file
def parseFile():
    print("File is downloaded. Parsing now.")
    openlog = open("locallog.txt")
    
    # Create and set all counters to zero
    totalrequests = 0
    errorcount = 0
    errors = []    
    monthcount = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0} # A dictionary with the months of the year, starting with January at one
    daycount = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}  # A dictionary with the days of the week, starting with Monday at zero
    failcount = 0
    redirectcount = 0
    successcount = 0
    filecount = {"index.html": 0}

    # Create and name a dictionary of month file names
    monthfile = {1: "Jan.txt", 2: "Feb.txt", 3: "Mar.txt", 4: "Apr.txt", 5: "May.txt", 6: "Jun.txt", 7: "Jul.txt", 8: "Aug.txt", 9: "Sep.txt", 10: "Oct.txt", 11: "Nov.txt", 12: "Dec.txt"}

    # Split the next read line into usable parts
    for line in openlog:
        totalrequests += 1
        
        # Define the columns to be parsed
        lineparts = re.split(".*\[([^:]*):(.*) \-[0-9]{4}\] \"([A-Z]+) (.+?)( HTTP.*\"|\") ([2-5]0[0-9]) .*", line)
        
        # Determine if regex worked
        if len(lineparts) >= 7:
            
            # Append the day and month counters as necessary
            dt = datetime.strptime(lineparts[1], "%d/%b/%Y")
            daycount[dt.weekday()] += 1
            monthcount[dt.month] += 1
            
            # Write the line to the appropriate month file
            if not os.path.exists(monthfile[dt.month]):
                file = open(monthfile[dt.month], "w")
                file.write(line)
                file.close()
            else:
                file = open(monthfile[dt.month], "a")
                file.write(line)
                file.close()

            # Append the status code counters as necessary
            if lineparts[6] == '200':
                successcount += 1
            elif lineparts[6] == '302' or lineparts[6] == '304' or  lineparts[6] == '306':
                redirectcount += 1
            else:
                failcount += 1

            # Append the most called file counter as necessary
            if lineparts[4] in filecount:
                filecount[lineparts[4]] += 1
            else:
                filecount[lineparts[4]] = 1

        # Determine if regex did not work
        else:
            errorcount += 1
            errors.append(line)
    
    # Print the results of the parsing to the screen
    
    # Print the total number of requests and the percentage of faulty requests
    print("There were ", totalrequests, "total requests- ", round(((errorcount/totalrequests)*100),2),"percent of which were faulty over the time period represented.")
    
    # Print the total number of successful, failed, and redirected requests.
    print(round(((successcount/totalrequests)*100),2)," percent of requests were successful, ", round(((failcount/totalrequests)*100),2), " percent of requests failed, and ", round(((redirectcount/totalrequests)*100),2), " percent of requests were redirected over the time period represented.")

    # Print the number of logs for each day
    for d in daycount:
        print("There were ", daycount[d], " requests during weekday ", d, " over the time period represented.")

    # Print the number of logs for each month
    for m in monthcount:
        print("There were ", monthcount[m], " requests during month ", m, " over the time period represented.")

    # Find the most request file
    mostrequested = "index.html"
    mostcount = filecount["index.html"]
    for filer, count in filecount.items():
        if count > mostcount:
            mostrequested = filer
            mostcount = filecount[filer]
            
    # Print the most requested file
    print("The most requested file was ", mostrequested, "with a total of", mostcount, "request(s).")

    # Find the least requested file
    leastrequested = "index.html"
    leastcount = filecount["index.html"]
    for filer, count in filecount.items():
        if count < leastcount:
            leastrequested = filer
            leastcount = filecount[filer]
            
    # Print the least requested file
    print("The least requested file was ", leastrequested, "with a total of", leastcount, "request(s).")

    # Close the file
    openlog.close()

# Define main function
def main():
    getFile()
    parseFile()

# Call main function
if __name__ == "__main__":
    main()