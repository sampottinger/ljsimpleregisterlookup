import subprocess

print 'Saving to Git repository...'
subprocess.check_call('git submodule update', shell=True)
subprocess.call('git commit -a -m "Incremental JSON update."', shell=True)
subprocess.call('git push', shell=True)
print 'Finished!'
