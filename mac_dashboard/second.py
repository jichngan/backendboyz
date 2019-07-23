import subprocess

child = subprocess.Popen(['python', 'plotpoisontest.py'], stdin=subprocess.PIPE)
try:  
  child.communicate('192.168.0.168')
except KeyboardInterrupt:
  child.terminate()
