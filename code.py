import urllib.request
import shutil

# Downloads the txt files from the url`:
#with urllib.request.urlopen('https://s3.amazonaws.com/tcmg476/http_access_log') as response, open('Log.txt', 'wb') as out_file:
 #shutil.copyfileobj(response, out_file)
#indicates the name of the file which will be used to check the requets

URLPATH="https://s3.amazonaws.com/tcmg476/http_access_log"
LOCALPATH="Log.txt"

print("File will be saved {}".format(LOCALPATH))
urllib.request.urlretrieve(URLPATH, LOCALPATH)

total=0
badreq=0
redir=0

ALL_PATHS = {}

for line in open(LOCALPATH): 
	#print(line)
	total += 1
	# magic to parse the status code here
	status_code = ''
	req_date = ''
	req_path = ''

	if status_code[0] == '3':
		redir += 1

	# lokk for the bad requests
	if status_code[0] == '4':
		badreq += 1

	# store the url path in the dictionary
	if req_path in ALL_PATHS:
		ALL_PATHS[req_path] += 1
	else:
		ALL_PATHS[req_path] = 1


	#status_code = '302'
	
