import subprocess
from os.path import expanduser

version = "3_0_0"

home = expanduser("~")

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