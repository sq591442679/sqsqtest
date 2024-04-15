import threading
import shutil
import subprocess
import os
import time
from multiprocessing import Process

from NEDGenerator import NUM_OF_TESTS, WARMUP_PERIOD, SIMULATION_END_TIME

# fr_names = ["00", "05", "10", "15", "20"]
fr_names=["10"]
test_names = [str(i) for i in range(1, NUM_OF_TESTS + 1)]
# test_names = [str(i) for i in range(1, 11)]
arg_names = ["fail" + i + "_test" + j for i in fr_names for j in test_names]

hops = [str(i) for i in range(0, 5)]
# hops = ['15']
experiment_names = ['ELB']  # test ELB
hops = []
# experiment_names = ['withDD-withoutLoopPrevention-withoutLoadBalance']  # test OSPF
# experiment_names = ['withDD-withLoopPrevention-withoutLoadBalance', 'withDD-withoutLoopPrevention-withoutLoadBalance']
# experiment_names = ['withDD-withLoopPrevention-withLoadBalance-0.05', 'withDD-withLoopPrevention-withLoadBalance-0.2', 'withDD-withLoopPrevention-withoutLoadBalance']
# experiment_names = ['withDD-withLoopPrevention-withoutLoadBalance', 'withDD-withoutLoopPrevention-withoutLoadBalance']
parent_folder_names = ['./results/' + experiment_name + '/' for experiment_name in experiment_names]


def getParameters(experiment_name: str):
    REQUEST_SHOULD_KNOWN_RANGE = 'false'
    LOOP_AVOIDANCE = 'false'
    LOAD_BALANCE = 'false'
    LOAD_SCALE = '1.0'
    ELB = 'false'

    if 'withDD' in experiment_name:
        REQUEST_SHOULD_KNOWN_RANGE = 'true'
    if 'withLoopPrevention' in experiment_name:
        LOOP_AVOIDANCE = 'true'
    if 'withLoadBalance' in experiment_name:
        LOAD_BALANCE = 'true'
        if (len(experiment_name.split('-')) == 4):
            LOAD_SCALE = experiment_name.split('-')[-1]
    if 'ELB' in experiment_name:
        REQUEST_SHOULD_KNOWN_RANGE = 'true'
        LOAD_BALANCE = 'false'
        ELB = 'true'

    return LOOP_AVOIDANCE, REQUEST_SHOULD_KNOWN_RANGE, LOAD_BALANCE, LOAD_SCALE, ELB


def changeOspfv2Common(experiment_name: str, hop: str):
    LOOP_AVOIDANCE, REQUEST_SHOULD_KNOWN_RANGE, LOAD_BALANCE, LOAD_SCALE, ELB = getParameters(experiment_name)

    file_read = open("/home/sqsq/Desktop/sat-ospf/inet/src/inet/routing/ospfv2/router/Ospfv2Common.h", "r")
    lines = file_read.readlines()
    print('-------reading .h file -------')
    file_read.close()
    time.sleep(10)

    if hop == 'OSPF':
        if "SQSQ_CONVERGENCY_TIME" in lines[46]:
            lines[46] = "#define SQSQ_CONVERGENCY_TIME                  %f\n" % float(SIMULATION_END_TIME + 50)
        else:
            raise Exception('')   
        if "SQSQ_HOP" in lines[47]:
            lines[47] = "#define SQSQ_HOP                               0\n"
        else:
            raise Exception('')  
        if "IS_OSPF" in lines[64]:
            lines[64] = "#define IS_OSPF                                true\n"  
        else:
            raise Exception('')                   
    else:
        if "SQSQ_CONVERGENCY_TIME" in lines[46]:
            lines[46] = "#define SQSQ_CONVERGENCY_TIME                  %f\n" % float(WARMUP_PERIOD)
        else:
            raise Exception('')
        if "SQSQ_HOP" in lines[47]:
            lines[47] = "#define SQSQ_HOP                               %s\n" % hop
        else:
            raise Exception('') 
        if "IS_OSPF" in lines[64]:
            lines[64] = "#define IS_OSPF                                false\n"  
        else:
            raise Exception('')   

    if "EXPERIMENT_NAME" in lines[48]:
        lines[48] = "#define EXPERIMENT_NAME                        \"%s\"\n" % experiment_name
    else:
        raise Exception('')           
    if "LOOP_AVOIDANCE" in lines[56]:
        lines[56] = "#define LOOP_AVOIDANCE                         %s\n" % LOOP_AVOIDANCE
    else:
        raise Exception('')
    if "REQUEST_SHOULD_KNOWN_RANGE" in lines[59]:
        lines[59] = "#define REQUEST_SHOULD_KNOWN_RANGE             %s\n" % REQUEST_SHOULD_KNOWN_RANGE
    else:
        raise Exception('')   
    if "LSR_RANGE" in lines[60]:
        lines[60] = "#define LSR_RANGE                              SQSQ_HOP\n"
    else:
        raise Exception('')   
    if "LOAD_BALANCE" in lines[62]:
        lines[62] = "#define LOAD_BALANCE                           %s\n" % LOAD_BALANCE
    else:
        raise Exception('')        
    if "RECORD_CSV" in lines[66]:
        lines[66] = "#define RECORD_CSV                             true\n"
    else:
        raise Exception('')
    if "LOAD_SCALE" in lines[69]:
        lines[69] = "#define LOAD_SCALE                             %s\n" % LOAD_SCALE
    else:
        raise Exception('')
    if "ELB" in lines[72]:
        lines[72] = "#define ELB                                    %s\n" % ELB
    else:
        raise Exception('')
    
    print('-------writing .h file-------')
    file_write = open("/home/sqsq/Desktop/sat-ospf/inet/src/inet/routing/ospfv2/router/Ospfv2Common.h", "w")
    file_write.writelines(lines)
    file_write.close()
    time.sleep(10)
    


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
                a dropPacketRaw.csv and queueDropPacketRaw.csv, which contains the information about the dropped packet
                    header: 'config', 'hop', 'module', 'simtime', 'isNoEntry', 'isStub', 'isLoop', 'isQueue'
                    REMEMBER: this csv may contains repeated lines
                a controlOverhead.csv
                    header: config, hop, module, helloOverhead, DDOverhead, LSROverhead, LSUOverhead, LSACKOverhead, total
                a successPacketRaw.csv
                    header: 'config', 'hop', 'module', 'simtime', 'delay'
    before running, check:
        SEND_ICMP, PRINT_IVP4_DROP_PACKET and RECORD_CSV in Ospfv2Common.h
        configs in omnetpp.ini, send_interval and deliverySrcIDs in NEDGenerator.py
        experiment_names and hops in this file
    """


    # for parent_folder_name in parent_folder_names:
    #     for hop in hops
    for experiment_name in experiment_names:
        if not os.path.exists('./results/' + experiment_name):
            os.mkdir('./results/' + experiment_name)

        if 'withDD-withoutLoopPrevention-withoutLoadBalance' in experiment_name:
            hops.append('OSPF')
        else:
            if 'OSPF' in hops:
                hops.remove('OSPF')
        
        processes = []
        for hop in hops:

            if not os.path.exists('./results/' + experiment_name + '/' + hop):
                os.mkdir('./results/' + experiment_name + '/' + hop)
            changeOspfv2Common(experiment_name, hop)
            time.sleep(0.5)

            result = subprocess.run("make -C /home/sqsq/Desktop/sat-ospf/inet MODE=release -j64 all", shell=True)
            if result.returncode != 0:
                raise Exception('')

            for fr in fr_names:
                for config in ['fail' + fr + '_test' + j for j in test_names]:
                    parent_dir = './results/' + experiment_name + '/' + hop + '/' + config 
                    os.mkdir(parent_dir)
                    with open(parent_dir + '/dropPacketRaw.csv', 'w') as f:
                        print('config', 'hop', 'module', 'simtime', 'isNoEntry', 'isStub', 'isLoop', 'isQueue', file=f, sep=',')
                    with open(parent_dir + '/queueDropPacketRaw.csv', 'w') as f:
                        print('config', 'hop', 'module', 'simtime', 'isNoEntry', 'isStub', 'isLoop', 'isQueue', file=f, sep=',')
                    with open(parent_dir + '/controlOverhead.csv', 'w') as f:
                        print('config', 'hop', 'module', 'helloOverhead', 'DDOverhead', 'LSROverhead', 'LSUOverhead', 'LSACKOverhead', 'ELBOverhead', 'total', file=f, sep=',')
                    with open(parent_dir + '/successPacketRaw.csv', 'w') as f:
                        print('config', 'hop', 'module', 'simtime', 'delay', file=f, sep=',')

                cmds = ["opp_run -m -u Cmdenv -c " + i + " --cmdenv-express-mode=true -n " + 
                "../..:../../../showcases:../../../src:../../../tests/validation:../../../tests/networks:../../../tutorials  " + 
                "--image-path=../../../images -l ../../../src/INET omnetpp.ini" 
                for i in ['fail' + fr + '_test' + j for j in test_names]]
    
                for cmd in cmds:
                    process = Process(target=execute, args=(cmd,))
                    process.start()
                    processes.append(process)

                for process in processes:
                    process.join()

    print('-------------------END----------------------')
