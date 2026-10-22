from subprocess import Popen, PIPE

turb_viewer = ['shmImshow.py', 'turbulence', '--fr=20']
wfs_viewer = ['shmImshow.py', 'wfs', '--fr=20']
dm_viewer = ['shmImshow.py', 'dm', '--fr=20']
cmd_list = [turb_viewer, wfs_viewer, dm_viewer]

proc_list = [Popen(cmd, stdout=PIPE, stderr=PIPE) for cmd in cmd_list]
if __name__ == "__main__":

    for proc in proc_list:
        proc.wait()


