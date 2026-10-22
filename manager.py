from subprocess import Popen, PIPE

cmd_list = [['python', 'send_it.py', '10000'], ['python', 'dm.py'], ['python', 'wfs.py'], ['python', 'end_it.py']]
proc_list = [Popen(cmd, stdout=open('logs/' + cmd[1].replace('.py', '.txt'), 'w'), stderr=PIPE) for cmd in cmd_list]

N_ITERS = 1000
if __name__ == "__main__":
    
    for proc in proc_list:
        proc.wait()
    
