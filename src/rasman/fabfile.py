
from fabric.api import run, sudo, env, local, cd, lcd, put 
from fabric.operations import prompt

# fabric is written poorly, it needs __init__.py which it doesn't have

env.user = 'pi'
env.hosts = ['rasman.local']


# Folder in remote host where the Rasman software will be copied to
APPROOT = '/home/' + env.user

def listSource():
    """Show all files/folders in the workspace where the job is deployed"""
    run('ls -lt %s' % APPROOT)

def cleanSource():
    """Clean up your local folder in preparation for zipping up the source tree"""
    local("rm -f *.pyc .DS_Store */.DS_Store")
          
def zipSource():
    """Package the source tree"""
    ans = prompt("Include rasman database (y/n)?", default='n').lower()
    if ans == 'y':
        cmd = "tar cvfz rasman.tgz rasman/"
    else:
        cmd = "tar cvfz rasman.tgz --exclude rasman.db rasman/"
    cleanSource()
    with lcd(".."):
        local(cmd)

def deploySource():
    """Install and deploy on the Raspberry Pi"""
    zipfile = "%s/rasman.tgz" % APPROOT
    with cd(APPROOT):
        sudo('rm -rf rasman')
        put('../rasman.tgz', zipfile, use_sudo=False)
        sudo('tar xvfz %s' % zipfile)
        run('ls -lt .')
    