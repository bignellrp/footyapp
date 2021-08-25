from os import popen

def cmdline(command):
    process = popen(
        command
    )
    return process.read()

##Get current branch
GITBRANCH = cmdline('git rev-parse --abbrev-ref HEAD')
IFBRANCH = "botpre"
print(f"Git branch is:{GITBRANCH}")
print(f"Required branch is:{IFBRANCH}")