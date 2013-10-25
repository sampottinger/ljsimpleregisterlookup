import subprocess

print 'Saving to Git repository...'
subprocess.check_call('git submodule update', shell=True)
subprocess.check_call('git commit -a -m "Incremental JSON update."', shell=True)
subprocess.check_call('git push', shell=True)
print 'Finished!'
