import threading
import shutil
import subprocess
import os
import time
from multiprocessing import Process

from NEDGenerator import NUM_OF_TESTS, WARMUP_PERIOD, SIMULATION_END_TIME

fr_names = ["10"]
test_names = [str(i) for i in range(1, NUM_OF_TESTS + 1)]
# test_names = [str(i) for i in range(1, 11)]
arg_names = ["fail" + i + "_test" + j for i in fr_names for j in test_names]

hops = ['0', '1', '2', '3', '4', '5']
# hops = ['1']
# experiment_names = ['withDD-withLoopPrevention', 'withDD-withoutLoopPrevention', 'withoutDD-withLoopPrevention', 'withoutDD-withoutLoopPrevention']
experiment_names = ['withDD-withLoopPrevention-withLoadBalance', 'withDD-withLoopPrevention-withoutLoadBalance', 'withDD-withoutLoopPrevention-withoutLoadBalance']
# experiment_names = ['withDD-withLoopPrevention-withLoadBalance']
parent_folder_names = ['./results/' + experiment_name + '/' for experiment_name in experiment_names]


def getParameters(experiment_name: str):
    REQUEST_SHOULD_KNOWN_RANGE = 'false'
    LOOP_AVOIDANCE = 'false'
    LOAD_BALANCE = 'false'

    if 'withDD' in experiment_name:
        REQUEST_SHOULD_KNOWN_RANGE = 'true'
    if 'withLoopPrevention' in experiment_name:
        LOOP_AVOIDANCE = 'true'
    if 'withLoadBalance' in experiment_name:
        LOAD_BALANCE = 'true'

    return LOOP_AVOIDANCE, REQUEST_SHOULD_KNOWN_RANGE, LOAD_BALANCE


def changeOspfv2Common(experiment_name: str, hop: str):
    # TODO OSPF
    if hop == 'OSPF':
        with open("/home/sqsq/Desktop/sat-ospf/inet/src/inet/routing/ospfv2/router/Ospfv2Common.h", "r+") as f:
            lines = f.readlines()
            if "SQSQ_CONVERGENCY_TIME" in lines[46]:
                lines[46] = "#define SQSQ_CONVERGENCY_TIME                  %f\n" % float(SIMULATION_END_TIME + 50)
                f.seek(0)
            f.writelines(lines)
        f.close()
        return
    else:
        with open("/home/sqsq/Desktop/sat-ospf/inet/src/inet/routing/ospfv2/router/Ospfv2Common.h", "r+") as f:
            lines = f.readlines()
            if "SQSQ_CONVERGENCY_TIME" in lines[46]:
                lines[46] = "#define SQSQ_CONVERGENCY_TIME                  %f\n" % float(WARMUP_PERIOD)
                f.seek(0)
            f.writelines(lines)
        f.close()

    LOOP_AVOIDANCE, REQUEST_SHOULD_KNOWN_RANGE, LOAD_BALANCE = getParameters(experiment_name)

    with open("/home/sqsq/Desktop/sat-ospf/inet/src/inet/routing/ospfv2/router/Ospfv2Common.h", "r+") as f:
        lines = f.readlines()
        # print(lines[50])
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
        if "LOAD_BALANCE" in lines[62]:
            lines[62] = "#define LOAD_BALANCE                           %s\n" % LOAD_BALANCE
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
    what this script does:
        1. change the SQSQ_HOP, LOOP_AVOIDANCE...... in Ospfv2Common.h according to expriment name 
        2. then build the omnet++ project
        3. init csv files, which will be written by inet during the simulation
            csv files are:
                a dropPacketRaw.csv, which contains the information about the dropped packet
                    header: 'config', 'hop', 'module', 'simtime', 'isNoEntry', 'isStub', 'isLoop', 'isQueue'
                    REMEMBER: this csv may contains repeated lines
                a controlOverhead.csv
                    header: config, hop, module, helloOverhead, DDOverhead, LSROverhead, LSUOverhead, LSACKOverhead, total
                a successPacketRaw.csv
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
        if not os.path.exists('./results/' + experiment_name):
            os.mkdir('./results/' + experiment_name)
        if experiment_name == 'withDD-withoutLoopPrevention':
            hops.append('OSPF')
        else:
            if 'OSPF' in hops:
                hops.remove('OSPF')
        
        for hop in hops:
            if not os.path.exists('./results/' + experiment_name + '/' + hop):
                os.mkdir('./results/' + experiment_name + '/' + hop)
            changeOspfv2Common(experiment_name, hop)
            result = subprocess.run("make -C /home/sqsq/Desktop/sat-ospf/inet MODE=release -j64 all", shell=True)
            if result.returncode != 0:
                raise Exception('')

            for config in arg_names:
                parent_dir = './results/' + experiment_name + '/' + hop + '/' + config 
                os.mkdir(parent_dir)
                with open(parent_dir + '/dropPacketRaw.csv', 'w') as f:
                    print('config', 'hop', 'module', 'simtime', 'isNoEntry', 'isStub', 'isLoop', 'isQueue', file=f, sep=',')
                with open(parent_dir + '/queueDropPacketRaw.csv', 'w') as f:
                    print('config', 'hop', 'module', 'simtime', 'isNoEntry', 'isStub', 'isLoop', 'isQueue', file=f, sep=',')
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
