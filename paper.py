import matplotlib.pyplot as plt
import os
import numpy

root_dir = '/home/sqsq/Desktop/sat-ospf/inet/examples/ospfv2/sqsqtest/results/'
from command import arg_names
from resultAnalyze import getAvgDelay, getAvgLSUOverhead, getAvgPacketDeliveryRate


def drawEEDUnderLightLoad():
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    fig, ax = plt.subplots()

    overhead = []
    delay = []
    hops = [str(i) for i in range(0, 5)]
    for hop in hops:
        if hop.isnumeric():
            folder_name = root_dir + 'results_lightload_p2p/withDD-withLoopPrevention-withoutLoadBalance/' + hop + '/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            delay.append(getAvgDelay(folder_name) * 1e3)

    ax.plot(overhead, delay, label='with loop prevention', marker='o')
    for i in range(len(delay)):
        ax.text(overhead[i], delay[i] - 5, hops[i],
                ha='right', va='top', fontdict={'family': 'Times New Roman', 'size': 15})


    overhead = []
    delay = []
    hops = [str(i) for i in range(0, 5)]
    hops.append('OSPF-L')
    hops.append('OPSPF')
    for hop in hops:
        if hop.isnumeric():
            folder_name = root_dir + 'results_lightload_p2p/withDD-withoutLoopPrevention-withoutLoadBalance/' + hop + '/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            delay.append(getAvgDelay(folder_name) * 1e3)
        elif hop == 'OSPF-L':
            folder_name = root_dir + 'results_lightload_p2p/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6 / 2)
            delay.append(getAvgDelay(folder_name) * 1e3)
        elif hop == 'OPSPF':
            folder_name = root_dir + 'results_lightload_p2p/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            delay.append(getAvgDelay(folder_name) * 1e3)

    ax.plot(overhead, delay, 
            label='without loop prevention', marker='x', linestyle='--')
    for i in range(len(delay)):
        # print(parent_folder_name, experiment_names[i], "'s EED:", avg_delays[i])
        ax.text(overhead[i], delay[i], hops[i],
                  ha='left', va='bottom', fontdict={'family': 'Times New Roman', 'size': 15})
    
    ax.set_title('Avg. End to End Delay & Control Overhead under Light Load, Link Failure Rate = 10%')
    ax.set_xlabel('Avg. Control Overhead(MBps)')
    ax.set_ylabel('Avg. End to End Delay(ms)')
    ax.set_ylim(bottom=0, top=1000)
    ax.set_xlim(right=0.6)
    plt.legend()
    fig.savefig('./results/overhead and EED under light load.png', dpi=300)
    plt.close()


def drawDeliveryRatioUnderLightLoad():
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    fig, ax = plt.subplots()


    # light load, with loop prevention
    overhead = []
    ratio = []
    hops = [str(i) for i in range(0, 5)]
    for hop in hops:
        folder_name = root_dir + 'results_lightload_p2p/withDD-withLoopPrevention-withoutLoadBalance/' + hop + '/'
        overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
        ratio.append((1 - getAvgPacketDeliveryRate(folder_name)) * 100)

    ax.plot(overhead, ratio, label='with loop prevention', marker='o')
    for i in range(len(ratio)):
        ax.text(overhead[i], ratio[i], hops[i],
                ha='right', va='top', fontdict={'family': 'Times New Roman', 'size': 15})


    # light load, without loop prevention
    overhead = []
    ratio = []
    hops = [str(i) for i in range(0, 4)]
    hops.append('OSPF-L')
    hops.append('OPSPF')
    for hop in hops:
        if hop.isnumeric():
            folder_name = root_dir + 'results_lightload_p2p/withDD-withoutLoopPrevention-withoutLoadBalance/' + hop + '/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            ratio.append((1 - getAvgPacketDeliveryRate(folder_name)) * 100)
        elif hop == 'OSPF-L':
            folder_name = root_dir + 'results_lightload_p2p/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6 / 2)
            ratio.append((1 - getAvgPacketDeliveryRate(folder_name)) * 100)
        elif hop == 'OPSPF':
            folder_name = root_dir + 'results_lightload_p2p/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            ratio.append((1 - getAvgPacketDeliveryRate(folder_name)) * 100)

    ax.plot(overhead, ratio, 
            label='without loop prevention', marker='x', linestyle='--')
    for i in range(len(ratio)):
        ax.text(overhead[i], ratio[i], hops[i],
                  ha='left', va='bottom', fontdict={'family': 'Times New Roman', 'size': 15})
    

    ax.set_title('Avg. Packet Delivery Ratio & Control Overhead under Light Load, Link Failure Rate = 10%')
    ax.set_xlabel('Avg. Control Overhead(MBps)')
    ax.set_ylabel('Avg. packet Delivery Ratio(%)')
    ax.set_ylim(bottom=0, top=3)
    ax.set_xlim()
    plt.legend()
    fig.savefig('./results/overhead and PDR under light load.png', dpi=300)
    plt.close()


def drawEEDUnderHeavyLoad():
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    fig, ax = plt.subplots()

    overhead = []
    delay = []
    hops = [str(i) for i in range(0, 5)]
    for hop in hops:
        folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withLoopPrevention-withLoadBalance-0.05/' + hop + '/'
        overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
        delay.append(getAvgDelay(folder_name) * 1e3)

    ax.plot(overhead, delay, 
            label='with load balance, scale=0.05', marker='o')
    for i in range(len(delay)):
        ax.text(overhead[i], delay[i] - 5, hops[i],
                ha='right', va='top', fontdict={'family': 'Times New Roman', 'size': 15})


    overhead = []
    delay = []
    hops = [str(i) for i in range(0, 5)]
    for hop in hops:
        folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withLoopPrevention-withLoadBalance-0.2/' + hop + '/'
        overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
        delay.append(getAvgDelay(folder_name) * 1e3)

    ax.plot(overhead, delay, 
            label='with load balance, scale=0.2', marker='x', linestyle='dotted')
    for i in range(len(delay)):
        # print(parent_folder_name, experiment_names[i], "'s EED:", avg_delays[i])
        ax.text(overhead[i], delay[i], hops[i],
                   ha='left', va='bottom', fontdict={'family': 'Times New Roman', 'size': 15})
    

    overhead = []
    delay = []
    hops = [str(i) for i in range(0, 5)]
    hops.append('OSPF-L')
    hops.append('OPSPF')
    for hop in hops:
        if hop.isnumeric():
            folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withoutLoopPrevention-withoutLoadBalance/' + hop + '/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            delay.append(getAvgDelay(folder_name) * 1e3)
        elif hop == 'OSPF-L':
            folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6 / 2)
            delay.append(getAvgDelay(folder_name) * 1e3)
        elif hop == 'OPSPF':
            folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            delay.append(getAvgDelay(folder_name) * 1e3)

    ax.plot(overhead, delay, 
            label='without load balance', marker='^', linestyle='--')
    for i in range(len(delay)):
        # print(parent_folder_name, experiment_names[i], "'s EED:", avg_delays[i])
        ax.text(overhead[i], delay[i], hops[i],
                   ha='left', va='bottom', fontdict={'family': 'Times New Roman', 'size': 15})
        
    
    ideal_x = numpy.linspace(-1, 1, 1000)
    ideal_y = numpy.full_like(ideal_x, 33.5)
    ax.plot(ideal_x, ideal_y, linestyle='-.', label='ideal delay')
        
    
    ax.set_title('Avg. End to End Delay & Control Overhead under Heavy Load, Link Failure Rate = 10%')
    ax.set_xlabel('Avg. Control Overhead(MBps)')
    ax.set_ylabel('Avg. End to End Delay(ms)')
    ax.set_ylim(bottom=0, top=1500)
    ax.set_xlim(left=-0.02, right=0.5)
    plt.legend(loc='center right')
    fig.savefig('./results/overhead and EED under heavy load.png', dpi=300)
    plt.close()

if __name__ == '__main__':
    
    drawEEDUnderLightLoad()
    drawDeliveryRatioUnderLightLoad()
    drawEEDUnderHeavyLoad()

    pass
