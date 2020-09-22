import os

working = os.environ['GITHUB_WORKSPACE']
print(os.environ['GITHUB_WORKSPACE'])

      
with open(working + "/proposedChanges") as f:
  c = f.read()
  
print(c)

#Check that zip files exist in the request
zips = filter(lambda x: x[-4:] == '.zip', c)
