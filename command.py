import threading
import shutil
import subprocess

def execute(command: str) -> None:
    try:
        # os.system("gnome-terminal -e 'bash -c \" source ~/omnetpp-6.0/setenv; " + command + "; exit; exec bash \"'")
        print(command)
        subprocess.run("bash -c \" source ~/omnetpp-6.0/setenv; " + command + "; exit;\"", shell=True)
        # os.system(command)
        # print("running: " + command)
        # print(results.stdout)
    except:
        print('fail to execute %s' % command)

if __name__ == '__main__':
    """
    README
    before running this script, change the SQSQ_HOP in Ospfv2Common.h, then build the omnet++ project
    when the simulation ends, there will be:
        1. a dropPacket.csv, which contains the information about the dropped packet
            dropPacket.csv header:  config name in ini, SQSQ_HOP, module name, no entry number, loop number, total
            it is Ipv4.cc who prints into thr dropPacket.csv
        2. a controlOverhead.csv
            header: config, hop, module, helloOverhead, DDOverhead, LSROverhead, LSUOverhead, LSACKOverhead, total

    after running this script, remember to rename the "results" folder, or it will be covered the next time this script is run
    """

    with open('dropPacket.csv', 'w') as f:
        print('config', 'hop', 'module', 'noEntryCnt', 'loopCnt', 'total', file=f, sep=',')
    with open('controlOverhead.csv', 'w') as f:
        print('config', 'hop', 'module', 'helloOverhead', 'DDOverhead', 'LSROverhead', 'LSUOverhead', 'LSACKOverhead', 'total', file=f, sep=',')
    with open('successPacket.csv', 'w') as f:
        print('config', 'hop', 'module', 'packetCnt', 'avgDelay', file=f, sep=',')
    
    fr_names = ["20"]
    test_names = ["1", "2", "3", "4", "5"]
    arg_names = ["fail" + i + "_test" + j for i in fr_names for j in test_names]
    cmds = ["opp_run -m -u Cmdenv -c " + i + " --cmdenv-express-mode=true -n " + 
            "../..:../../../showcases:../../../src:../../../tests/validation:../../../tests/networks:../../../tutorials  " + 
            "--image-path=../../../images -l ../../../src/INET omnetpp.ini" 
            for i in arg_names]
    # print(arg_names)
    threads = []
    
    for cmd in cmds:
        th = threading.Thread(target=execute, args=(cmd,))
        threads.append(th)
        
    for th in threads:
        th.start()
        th.join()

    shutil.move('./dropPacket.csv', './results')
    shutil.move('./controlOverhead.csv', './results')
    shutil.move('./successPacket.csv', './results')
    print('-------------------END----------------------')
