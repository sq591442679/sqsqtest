import threading
import shutil
import subprocess
import os
import time
from multiprocessing import Process

fr_names = ["10"]
test_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
arg_names = ["fail" + i + "_test" + j for i in fr_names for j in test_names]

hops = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
experiment_names = ['withDD-withLoopPrevention', 'withDD-withoutLoopPrevention', 'withoutDD-withLoopPrevention', 'withoutDD-withoutLoopPrevention']
parent_folder_names = ['./results/' + experiment_name + '/' for experiment_name in experiment_names]


def getParameters(experiment_name: str):
    if experiment_name == 'withDD-withLoopPrevention':
        LOOP_AVOIDANCE = 'true'
        REQUEST_SHOULD_KNOWN_RANGE = 'true'
    elif experiment_name == 'withDD-withoutLoopPrevention':
        LOOP_AVOIDANCE = 'false'
        REQUEST_SHOULD_KNOWN_RANGE = 'true'    
    elif experiment_name == 'withoutDD-withLoopPrevention':
        LOOP_AVOIDANCE = 'true'
        REQUEST_SHOULD_KNOWN_RANGE = 'false'
    elif experiment_name == 'withoutDD-withoutLoopPrevention':
        LOOP_AVOIDANCE = 'false'
        REQUEST_SHOULD_KNOWN_RANGE = 'false'
    return LOOP_AVOIDANCE, REQUEST_SHOULD_KNOWN_RANGE


def changeOspfv2Common(experiment_name: str, hop: str):
    LOOP_AVOIDANCE, REQUEST_SHOULD_KNOWN_RANGE = getParameters(experiment_name)

    with open("/home/sqsq/Desktop/sat-ospf/inet/src/inet/routing/ospfv2/router/Ospfv2Common.h", "r+") as f:
        lines = f.readlines()
        print(lines[50])
        if "SQSQ_HOP" in lines[47]:
            lines[47] = "#define SQSQ_HOP                               %s\n" % hop
        else:
            raise Exception('')
        if "EXPERIMENT_NAME" in lines[48]:
            lines[48] = "#define EXPERIMENT_NAME                        \"%s\"\n" % experiment_name
            
        if "LOOP_AVOIDANCE" in lines[56]:
            lines[56] = "#define LOOP_AVOIDANCE                         %s\n" % LOOP_AVOIDANCE
        else:
            raise Exception('')
        if "REQUEST_SHOULD_KNOWN_RANGE" in lines[59]:
            lines[59] = "#define REQUEST_SHOULD_KNOWN_RANGE             %s\n" % REQUEST_SHOULD_KNOWN_RANGE
        else:
            raise Exception('')
        
        f.seek(0)
        f.writelines(lines)
    f.close()


def execute(command: str) -> None:
    subprocess.run("source ~/omnetpp-6.0/setenv; " + command + "; ", shell=True)


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
    processes = []

    # for parent_folder_name in parent_folder_names:
    #     for hop in hops
    for experiment_name in experiment_names:
        os.mkdir('./results/' + experiment_name)
        for hop in hops:
            os.mkdir('./results/' + experiment_name + '/' + hop)
            changeOspfv2Common(experiment_name, hop)
            subprocess.run("make -C /home/sqsq/Desktop/sat-ospf/inet MODE=release -j64 all", shell=True)

            for config in arg_names:
                parent_dir = './results/' + experiment_name + '/' + hop + '/' + config 
                os.mkdir(parent_dir)
                with open(parent_dir + '/dropPacketRaw.csv', 'w') as f:
                    print('config', 'hop', 'module', 'simtime', 'isNoEntry', 'isStub', 'isLoop', file=f, sep=',')
                with open(parent_dir + '/controlOverhead.csv', 'w') as f:
                    print('config', 'hop', 'module', 'helloOverhead', 'DDOverhead', 'LSROverhead', 'LSUOverhead', 'LSACKOverhead', 'total', file=f, sep=',')
                with open(parent_dir + '/successPacketRaw.csv', 'w') as f:
                    print('config', 'hop', 'module', 'simtime', 'delay', file=f, sep=',')
    
            for cmd in cmds:
                process = Process(target=execute, args=(cmd,))
                process.start()
                processes.append(process)

            for process in processes:
                process.join()

    print('-------------------END----------------------')
