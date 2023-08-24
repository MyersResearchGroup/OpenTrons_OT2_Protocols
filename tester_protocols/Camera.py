#selfnote, this code seems to be running, but the image is not being saved
# either it is a directory issue of OPT is terrible with images

#selfnote, something is up with this, not sure what

import subprocess
metadata = {
    'protocolName': 'camera2',
    'author': 'parke',
    'description':'protocol to run camera',
    'apiLevel':'2.10'
    }
 
 
def run(protocol): 
  if not protocol.is_simulating():

    subprocess.check_call(['ffmpeg', '-y', '-f', 'video4linux2', '-s',
                       '640x480', '-i', '/dev/video0', '-ss', '0:0:1', 
                       '-frames', '1', '/var/lib/jupyter/notebooks/image.jpg']) 

    contents = open('/var/lib/jupyter/notebooks/image.jpg', 'rb').read()
    protocol.comment('OPT took a picture!')