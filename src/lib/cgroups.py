
import os
import time
import subprocess
import syslog


syslog.openlog('reaperd', syslog.LOG_PID, syslog.LOG_SYSLOG)

controllers = ['cpuset', 'memory']

cfile = '/etc/cgconfig.conf'
rfile = '/etc/cgrules.conf'

def _mount():
    f = open(cfile, 'w')
    f.write('mount {\n')
    for controller in controllers:
        f.write('\t%s = /cgroup/%s;\n' % (controller, controller))
    f.write('}\n\n')
    f.close()
    syslog.syslog(syslog.LOG_INFO, 'Updated mount points con cgconfig configuration file')

def _update_memory(users, memory):
    """ Generate memory related cgroup rules
    """
    f = open(cfile, 'a')
    for user in users:
        f.write('group user.%s {\n' % user)
        f.write('\tmemory {\n')
        f.write('\t\tmemory.limit_in_bytes = %sM;\n' % memory)
        f.write('\t\tmemory.swappiness = 0;\n')
        f.write('\t}\n')
        f.write('}\n\n')
    f.close()
    syslog.syslog(syslog.LOG_INFO, 'Updated memory groups on cgconfig configuration file')

def _update_cpuset(cores):
    """ Generate processor core groups
    """
    f = open(cfile, 'a')
    for core in cores.split(','):
        f.write('group cpu%s {\n' % core)
        f.write('\tcpuset {\n')
        f.write('\t\tcpuset.mems = 0;\n')
        f.write('\t\tcpuset.cpus = %s;\n' % core)
        f.write('\t}\n')
        f.write('}\n\n')
    f.close()
    syslog.syslog(syslog.LOG_INFO, 'Updated cpusets on cgconfig configuration file')

def cgapply():
    syslog.syslog(syslog.LOG_INFO, 'Stopping cgconfig daemon')
    subprocess.call(['/sbin/service', 'cgconfig', 'stop'])
    syslog.syslog(syslog.LOG_INFO, 'Stopping cgred daemon')
    subprocess.call(['/sbin/service', 'cgred', 'stop'])
    time.sleep(2)
    syslog.syslog(syslog.LOG_INFO, 'Starting cgconfig daemon')
    subprocess.call(['/sbin/service', 'cgconfig', 'start'])
    time.sleep(2)
    syslog.syslog(syslog.LOG_INFO, 'Starting cgred daemon')
    subprocess.call(['/sbin/service', 'cgred', 'start'])
    
def update_rules(allusers, cores, memory, ememory):
    """ Update control groups rules on server
    """
    unlimited = set(allusers['unlimited'])
    extended = set(allusers['extended'])
    users = set(allusers['users'])
    users.difference_update(unlimited)

    ## Setting up rules
    corelist = cores.split(',')
    corenumber = len(corelist)
    counter = 0
    f = open(rfile, 'w')
    for user in users:
        f.write('%s\t\tcpuset\tcpu%s\n' % (user, corelist[counter]))
        if counter < (corenumber - 1):
            counter = counter + 1
        else:
            counter = 0
        f.write('%s\t\tmemory\tuser.%s\n' % (user, user))
    f.close()
    syslog.syslog(syslog.LOG_INFO, 'Updated cgroup rules engine daemon (cgred) configuration file')

    ## Setting up groups
    _mount()
    _update_cpuset(cores)
    _update_memory(extended, ememory)
    _update_memory(users, memory)

    ## Apply rules on system services
    cgapply()
