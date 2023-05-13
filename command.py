import threading
import shutil
import subprocess
import os

fr_names = ["10"]
test_names = ["1", "2", "3", "4", "5"]
arg_names = ["fail" + i + "_test" + j for i in fr_names for j in test_names]
SQSQ_HOP = 10

def execute(command: str) -> None:
    try:
        os.system("gnome-terminal -e 'bash -c \" source ~/omnetpp-6.0/setenv; " + command + "; exit; exec bash \"'")
        # print(command)
        # subprocess.run("bash -c \" source ~/omnetpp-6.0/setenv; " + command + "; exit;\"", shell=True)
        # os.system(command)
        # print("running: " + command)
        # print(results.stdout)
    except:
        print('fail to execute %s' % command)

if __name__ == '__main__':
    """
    README
    before running this script:
        1. change the SQSQ_HOP in Ospfv2Common.h and SQSQ_HOP in this script, then build the omnet++ project
        2. make sure there is no ./results/$SQSQHOP repository
    when the simulation ends, there will be:
        1. a dropPacketRaw.csv, which contains the information about the dropped packet
            header: 'config', 'hop', 'module', 'simtime', 'isNoEntry', 'isStub', 'isLoop'
            REMEMBER: this csv may contains repeated lines
        2. a controlOverhead.csv
            header: config, hop, module, helloOverhead, DDOverhead, LSROverhead, LSUOverhead, LSACKOverhead, total
        3. a successPacketRaw.csv
            header: 'config', 'hop', 'module', 'simtime', 'delay'
    """
    
    cmds = ["opp_run -m -u Cmdenv -c " + i + " --cmdenv-express-mode=true -n " + 
            "../..:../../../showcases:../../../src:../../../tests/validation:../../../tests/networks:../../../tutorials  " + 
            "--image-path=../../../images -l ../../../src/INET omnetpp.ini" 
            for i in arg_names]
    # print(arg_names)
    threads = []

    os.mkdir('./results/' + str(SQSQ_HOP))
    for config in arg_names:
        parent_dir = './results/' + str(SQSQ_HOP) + '/' + config 
        os.mkdir(parent_dir)
        with open(parent_dir + '/dropPacketRaw.csv', 'w') as f:
            print('config', 'hop', 'module', 'simtime', 'isNoEntry', 'isStub', 'isLoop', file=f, sep=',')
        with open(parent_dir + '/controlOverhead.csv', 'w') as f:
            print('config', 'hop', 'module', 'helloOverhead', 'DDOverhead', 'LSROverhead', 'LSUOverhead', 'LSACKOverhead', 'total', file=f, sep=',')
        with open(parent_dir + '/successPacketRaw.csv', 'w') as f:
            print('config', 'hop', 'module', 'simtime', 'delay', file=f, sep=',')
    
    for cmd in cmds:
        th = threading.Thread(target=execute, args=(cmd,))
        threads.append(th)
        
    for th in threads:
        th.start()
        th.join()

    print('-------------------END----------------------')
