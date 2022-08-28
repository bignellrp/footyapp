from os import popen
from services.lookup import lookup

def cmdline(command):
    process = popen(command)
    return process.read()

##Main branch is written into the tokens json
##If they match then PRO tokens are used
##Otherwise they pull the dev tokens
##Note the 'in' syntax was because equals
##was not matching.
GITBRANCH = cmdline('git rev-parse --abbrev-ref HEAD')
IFBRANCH = lookup("git_branch")
GITBRANCH = str(GITBRANCH)
IFBRANCH = str(IFBRANCH)
print(f"IF branch is:{IFBRANCH}")
print(f"Git branch is:{GITBRANCH}")