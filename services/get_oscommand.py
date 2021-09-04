from os import popen
from services.lookup import lookup

def cmdline(command):
    process = popen(command)
    return process.read()

##Get current branch
GITBRANCH = cmdline('git rev-parse --abbrev-ref HEAD')
IFBRANCH = lookup("git_branch")
GITBRANCH = str(GITBRANCH)
IFBRANCH = str(IFBRANCH)
print(f"IF branch is:{IFBRANCH}")
print(f"Git branch is:{GITBRANCH}")