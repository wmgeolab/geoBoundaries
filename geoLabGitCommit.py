import datetime
import subprocess
import os

def pyGitUpdate(repository_name):
  first = 0
  access_token = os.environ['access_token'] 
  
  commit_message = str(datetime.date.today()) + " daily commit for repo " + repository_name + ". (" + str(datetime.datetime.timestamp(datetime.datetime.now())) + ")"
  
  #You can update these to your own user if you want:
  subprocess.check_output('git config --global user.email "geogdan@gmail.com"', shell=True)
  subprocess.check_output('git config --global user.name "DanRunfola"', shell=True)
    
  
  
  git_init = subprocess.check_output('git init', shell=True)
  print(str(git_init.decode('UTF-8')))
  
  git_validate = subprocess.check_output("git remote -v", shell=True)
  print(str(git_validate.decode('UTF-8')))
  if(len(str(git_validate.decode('UTF-8'))) > 10):
    repoURL = "https://DanRunfola:" + access_token + "@github.com/wmgeolab/" + repository_name 
    print("Repository URL is already set, adding files...")
  else:
    print("Setting repo URL...")
    repoURL = "https://DanRunfola:" + access_token + "@github.com/wmgeolab/" + repository_name 
    git_remote = subprocess.check_output(str('git remote add origin ' + repoURL), shell=True)
    print(str(git_remote.decode('UTF-8')))
    git_validate = subprocess.check_output("git remote -v", shell=True)
    print(str(git_validate.decode('UTF-8')))
    
  for (dirpath, dirnames, filenames) in os.walk('.'):
      for f in filenames:
          if(os.stat(os.path.join(dirpath, f)).st_size >= 1e+6):
            print("File " + str(os.path.join(dirpath,f)) + " is too large to commit to github (>10 MB).  It will NOT be backed up via git!")
              
            if os.path.exists(".gitignore"):
              append_write = 'a' # append if already exists
            else:
              append_write = 'w' # make a new file if not

            gIgnore = open(".gitignore",append_write)
            if(first == 0):
              first = 1
              gIgnore.write("releaseCandidateRaw \n")
              gIgnore.write("releaseCandidateInit \n")
              gIgnore.write("releaseCandidateZips \n")
              gIgnore.write("release \n")
              gIgnore.write("tmp \n")
            gIgnore.write(os.path.join(dirpath, f) + '\n')
            gIgnore.close()

  git_add = subprocess.check_output('git add .', shell=True)
  print(str(git_add.decode('UTF-8')))

  git_status = subprocess.check_output("git status", shell = True)
  print(str(git_status.decode('UTF-8')))
  
  if(len(str(git_status.decode('UTF-8'))) > 65):
    print("There are new files to commit - committing them now.")
    git_commit = subprocess.check_output(str('git commit -m "' + str(commit_message)) + '"', shell=True)
    print(str(git_commit.decode('UTF-8')))
  
  else:
    print("No new files to commit.")
  

  git_push = subprocess.check_output('git push ' + repoURL + ' master', shell=True)
  

pyGitUpdate(os.environ['repository_name'])