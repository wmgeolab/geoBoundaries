#Upload release to geoboundaries.org
import os
import ftputil
import ftputil.session
import importlib
import pandas as pd


def tracker(path, obj):
  if(obj == "reset"):
    tracker = open("./tmp/tracking.txt", "w")
    tracker.write("Paths\n")
    tracker.close()
  
  if(obj == "update"):
    tracker = open("./tmp/tracking.txt", "a")
    tracker.write(path + "\n")
    tracker.close()
  
  if(obj == "check"):
    with open("./tmp/tracking.txt") as f:
      lines = f.read().splitlines()
    
    if(path in lines):
      return True
    else:
      return False

def uploadGB(buildID):  
  
  
  sf = ftputil.session.session_factory(use_passive_mode=True)
  
  version = buildID.split('_', 1)[1]
  
  with ftputil.FTPHost(host=os.getenv('ftp'), 
                       user=os.getenv('user'), 
                       password=os.getenv('pass'), 
                       session_factory=sf) as ftp_host:
    
    root = './release/geoBoundaries-' + version
    
    ftp_host.chdir("/geoboundaries.org/data/")
    for dir_name, _, dir_files in os.walk(root):
      local = os.path.join(os.curdir, dir_name)
      #remove release from path
      dir_name = dir_name.split('/', 2)[2]
      remote = ftp_host.path.join(ftp_host.curdir, dir_name)
      if not ftp_host.path.exists(remote):
          print ('mkdir:' + local + '->' + remote)
          ftp_host.mkdir(remote)

      for f in dir_files:
          local_f = os.path.join(local, f)
          remote_f = ftp_host.path.join(remote, f)
          if(tracker(remote_f, "check") == False):
            print ('upload:' + local_f + '->' + remote_f)
            ftp_host.upload(local_f, remote_f)
            tracker(remote_f, "update")
          else:
            pass
          

    


if __name__ == "__main__": 
  import buildMain
  importlib.reload(buildMain)
  buildMain.geoBoundaries_build("gbReleaseCandidate_2_0_0")