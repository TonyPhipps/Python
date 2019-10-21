# Processes
## CPU and RAM Percentages
    top

## Process tree
    ps -auxwf

## Open network ports or raw sockets
    netstat -nalp
    netstat -plant
    ss -a -e -i
    lsof [many options]

## Running Processes with Deleted Binaries
    ls -alR /proc/*/exe 2> /dev/null |  grep deleted

### Recover Deleted Binary
    cp /proc/<PID>/exe /tmp/recovered_bin

### Hash of Deleted binary
    sha1sum /tmp/recovered_bin

## Process command name/cmdline
    strings /proc/<PID>/comm
    strings /proc/<PID>/cmdline

## Real process path
    ls -al /proc/<PID>/exe

## Process environment variables
    strings /proc/<PID>/environ

## Process working directory
    ls -alR /proc/*/cwd

## Process running from tmp or dev
    ls -alR /proc/*/cwd 2> /dev/null | grep tmp
    ls -alR /proc/*/cwd 2> /dev/null | grep dev

## Open file descriptors
     ls -al /proc/<PID>/fd

## Process maps
    cat /proc/<PID>/maps

## process stack
    cat /proc/<PID>/stack




# Users
## SSH authorized_keys files:
    find / -name authorized_keys

# User History files:
    find / -name .*history

# History files linked to /dev/null:
    ls -alR / 2> /dev/null | grep .*history |  grep null

# Look for UID 0/GID 0:
    grep ":0:" /etc/passwd

# Check sudoers file:
    cat /etc/sudoers and /etc/group

# Check scheduled tasks:
    crontab -latqsystemctl list-timers  --all