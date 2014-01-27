import subprocess

print 'Pulling from Git repository...'
subprocess.check_call('git submodule foreach git pull origin master', shell=True)
subprocess.check_call('git pull --recurse-submodules', shell=True)
subprocess.check_call('git submodule update --recursive', shell=True)
subprocess.check_call('git pull', shell=True)
subprocess.call('git commit -a -m "Incremental JSON update."', shell=True)
subprocess.call('git push', shell=True)
print 'Finished!'
