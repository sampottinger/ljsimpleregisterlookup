import os
import subprocess

print 'Pulling from Git repository...'
subprocess.check_call('git reset --hard HEAD', shell=True, cwd='ljm_constants')
subprocess.check_call('git pull origin master', shell=True, cwd='ljm_constants')
subprocess.check_call('git pull', shell=True)
subprocess.call('git commit -a -m "Incremental JSON update."', shell=True)
subprocess.call('git push', shell=True)
print 'Finished!'
