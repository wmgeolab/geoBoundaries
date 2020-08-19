import subprocess
from os.path import expanduser
home = expanduser("~")
if(os.environ["manualRun"] == "True"):
  version = "manual"
else:
  version = os.environ["manualRun"]

if(version != "development"):


  #geoBoundaries High Precision Single Country:
  rcloneCallHPSCU = "rclone sync " + home + "/gbRelease/gbReleaseData/HPSCU/ web:/geoboundaries.org/data/geoBoundaries-" + version + "/"

  dlProcessHPSCU = subprocess.Popen([rcloneCallHPSCU], shell=True)
  dlProcessHPSCU.wait()

  rcloneCallHPSCGS = "rclone sync " + home + "/gbRelease/gbReleaseData/HPSCGS/ web:/geoboundaries.org/data/geoBoundariesHPSCGS-" + version + "/"

  dlProcessHPSCGS = subprocess.Popen([rcloneCallHPSCGS], shell=True)
  dlProcessHPSCGS.wait()

  rcloneCallSSCGS = "rclone sync " + home + "/gbRelease/gbReleaseData/SSCGS/ web:/geoboundaries.org/data/geoBoundariesSSCGS-" + version + "/"

  dlProcessSSCGS = subprocess.Popen([rcloneCallSSCGS], shell=True)
  dlProcessSSCGS.wait()

  rcloneCallSSCU = "rclone sync " + home + "/gbRelease/gbReleaseData/SSCU/ web:/geoboundaries.org/data/geoBoundariesSSCU-" + version + "/"

  dlProcessSSCU = subprocess.Popen([rcloneCallSSCU], shell=True)
  dlProcessSSCU.wait()

  rcloneCallSSCU = "rclone sync " + home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ web:/geoboundaries.org/data/geoBoundariesCGAZ-" + version + "/"

  dlProcessSSCU = subprocess.Popen([rcloneCallSSCU], shell=True)
  dlProcessSSCU.wait()
else:
  #geoBoundaries High Precision Single Country:
  rcloneCallHPSCU = "rclone sync " + home + "/gbRelease/gbReleaseData/HPSCU/ web:/geoboundaries.org/data/dev/geoBoundaries-" + version + "/"

  dlProcessHPSCU = subprocess.Popen([rcloneCallHPSCU], shell=True)
  dlProcessHPSCU.wait()

  rcloneCallHPSCGS = "rclone sync " + home + "/gbRelease/gbReleaseData/HPSCGS/ web:/geoboundaries.org/data/dev/geoBoundariesHPSCGS-" + version + "/"

  dlProcessHPSCGS = subprocess.Popen([rcloneCallHPSCGS], shell=True)
  dlProcessHPSCGS.wait()

  rcloneCallSSCGS = "rclone sync " + home + "/gbRelease/gbReleaseData/SSCGS/ web:/geoboundaries.org/data/dev/geoBoundariesSSCGS-" + version + "/"

  dlProcessSSCGS = subprocess.Popen([rcloneCallSSCGS], shell=True)
  dlProcessSSCGS.wait()

  rcloneCallSSCU = "rclone sync " + home + "/gbRelease/gbReleaseData/SSCU/ web:/geoboundaries.org/data/dev/geoBoundariesSSCU-" + version + "/"

  dlProcessSSCU = subprocess.Popen([rcloneCallSSCU], shell=True)
  dlProcessSSCU.wait()

  rcloneCallCGAZ = "rclone sync " + home + "/gbRelease/gbReleaseData/CGAZ/!CGAZ/ web:/geoboundaries.org/data/dev/geoBoundariesCGAZ-" + version + "/"

  dlProcessCGAZ = subprocess.Popen([rcloneCallCGAZ], shell=True)
  dlProcessCGAZ.wait()
  
