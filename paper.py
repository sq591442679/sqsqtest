import matplotlib.pyplot as plt
import os
import numpy

root_dir = '/home/sqsq/Desktop/sat-ospf/inet/examples/ospfv2/sqsqtest/results/'
from command import arg_names
from resultAnalyze import getAvgDelay, getAvgLSUOverhead, getAvgPacketDeliveryRate


def drawEEDUnderLightLoad():
    # plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['axes.titlesize'] = 22
    plt.rcParams['axes.labelsize'] = 22
    plt.rcParams['xtick.labelsize'] = 18
    plt.rcParams['ytick.labelsize'] = 18
    plt.rcParams['legend.fontsize'] = 20
    fig, ax = plt.subplots()

    overhead = []
    delay = []
    hops = [str(i) for i in range(0, 5)]
    for hop in hops:
        if hop.isnumeric():
            folder_name = root_dir + 'results_lightload_p2p/withDD-withLoopPrevention-withoutLoadBalance/' + hop + '/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            delay.append(getAvgDelay(folder_name) * 1e3)

    ax.plot(overhead, delay, label='with loop prevention', marker='o', linewidth=4.0, markersize=10)
    for i in range(len(delay)):
        if hops[i].isnumeric():
            ax.text(overhead[i], delay[i] - 5, hops[i],
                ha='right', va='top', fontdict={'size': 22})
        else:
            ax.text(overhead[i], delay[i] - 5, hops[i],
                ha='center', va='top', fontdict={'size': 22})


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

    ax.plot(overhead, delay, label='without loop prevention', marker='X', linestyle='--', linewidth=4.0, markersize=10)
    for i in range(len(delay)):
        if hops[i].isnumeric():
            ax.text(overhead[i], delay[i] - 5, hops[i],
                ha='left', va='bottom', fontdict={'size': 22})
        else:
            ax.text(overhead[i], delay[i] - 5, hops[i],
                ha='center', va='bottom', fontdict={'size': 22})
    
    # ax.set_title('Avg. End to End Delay & Control Overhead \nunder Light Load, Link Failure Rate = 10%')
    ax.set_xlabel('Control Overhead (MBps)')
    ax.set_ylabel('End to End Delay (ms)')
    ax.set_ylim(bottom=0, top=1000)
    ax.set_xlim(right=0.48)
    plt.legend(loc='upper right')
    plt.grid()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4], ['0', '0.1', '0.2', '0.3', '0.4'])
    plt.tight_layout()
    fig.savefig('./results/overhead and EED under light load.pdf', dpi=300, format='pdf')
    plt.close()


def drawPDRUnderLightLoad():
    # plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['axes.titlesize'] = 22
    plt.rcParams['axes.labelsize'] = 22
    plt.rcParams['xtick.labelsize'] = 18
    plt.rcParams['ytick.labelsize'] = 18
    plt.rcParams['legend.fontsize'] = 20
    fig, ax = plt.subplots()


    # light load, with loop prevention
    overhead = []
    ratio = []
    hops = [str(i) for i in range(0, 5)]
    for hop in hops:
        folder_name = root_dir + 'results_lightload_p2p/withDD-withLoopPrevention-withoutLoadBalance/' + hop + '/'
        overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
        ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 10000)) * 100)

    ax.plot(overhead, ratio, label='with loop prevention', marker='o', linewidth=4.0, markersize=10)
    for i in range(len(ratio)):
        ax.text(overhead[i], ratio[i], hops[i],
            ha='right', va='top', fontdict={'size': 22})


    # light load, without loop prevention
    overhead = []
    ratio = []
    hops = [str(i) for i in range(0, 5)]
    hops.append('OSPF-L')
    hops.append('OPSPF')
    for hop in hops:
        if hop.isnumeric():
            folder_name = root_dir + 'results_lightload_p2p/withDD-withoutLoopPrevention-withoutLoadBalance/' + hop + '/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 10000)) * 100)
        elif hop == 'OSPF-L':
            folder_name = root_dir + 'results_lightload_p2p/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6 / 2)
            ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 10000)) * 100)
        elif hop == 'OPSPF':
            folder_name = root_dir + 'results_lightload_p2p/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 10000)) * 100)

    ax.plot(overhead, ratio, label='without loop prevention', marker='X', linestyle='--', linewidth=4.0, markersize=10)
    for i in range(len(ratio)):
        if hops[i].isnumeric():
            ax.text(overhead[i], ratio[i], hops[i],
                ha='left', va='bottom', fontdict={'size': 22})
        else:
            ax.text(overhead[i], ratio[i], hops[i],
                ha='center', va='bottom', fontdict={'size': 22})
    

    # ax.set_title('Avg. Packet Delivery Ratio & Control Overhead \nunder Light Load, Link Failure Rate = 10%')
    ax.set_xlabel('Control Overhead (MBps)')
    ax.set_ylabel('Packet Loss Ratio (%)')
    ax.set_ylim(bottom=0, top=3)
    ax.set_xlim(right=0.48)
    plt.legend()
    plt.grid()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4], ['0', '0.1', '0.2', '0.3', '0.4'])
    plt.tight_layout()
    fig.savefig('./results/overhead and PDR under light load.pdf', dpi=300, format='pdf')
    plt.close()


def drawEEDUnderHeavyLoad():
    # plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['axes.titlesize'] = 22
    plt.rcParams['axes.labelsize'] = 22
    plt.rcParams['xtick.labelsize'] = 18
    plt.rcParams['ytick.labelsize'] = 18
    plt.rcParams['legend.fontsize'] = 19
    fig, ax = plt.subplots()

    overhead = []
    delay = []
    hops = [str(i) for i in range(0, 5)]
    for hop in hops:
        folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withLoopPrevention-withLoadBalance-0.05/' + hop + '/'
        overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
        delay.append(getAvgDelay(folder_name) * 1e3)

    ax.plot(overhead, delay, label='load balance, thr=0.05', marker='o', linewidth=4.0, markersize=10)
    for i in range(len(delay)):
        ax.text(overhead[i], delay[i] - 5, hops[i],
            ha='right', va='top', fontdict={'size': 22})


    overhead = []
    delay = []
    hops = [str(i) for i in range(0, 5)]
    for hop in hops:
        folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withLoopPrevention-withLoadBalance-0.2/' + hop + '/'
        overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
        delay.append(getAvgDelay(folder_name) * 1e3)

    ax.plot(overhead, delay, label='load balance, thr=0.2', marker='X', linestyle='dotted', linewidth=4.0, markersize=10)
    for i in range(len(delay)):
        ax.text(overhead[i], delay[i] - 5, hops[i],
            ha='left', va='bottom', fontdict={'size': 22})
    

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

    ax.plot(overhead, delay, label='without load balance', marker='^', linestyle='--', linewidth=4.0, markersize=10)
    for i in range(len(delay)):
        if hops[i].isnumeric():
            ax.text(overhead[i], delay[i] - 5, hops[i],
                ha='left', va='bottom', fontdict={'size': 22})
        else:
            ax.text(overhead[i], delay[i] - 5, hops[i],
                ha='center', va='bottom', fontdict={'size': 22})
        
    
    ideal_x = numpy.linspace(-1, 1, 1000)
    ideal_y = numpy.full_like(ideal_x, 33.5)
    ax.plot(ideal_x, ideal_y, linestyle='-.', label='ideal delay', linewidth=4.0, markersize=10)
        
    
    # ax.set_title('Avg. End to End Delay & Control Overhead \nunder Heavy Load, Link Failure Rate = 10%')
    ax.set_xlabel('Control Overhead (MBps)')
    ax.set_ylabel('End to End Delay (ms)')
    ax.set_ylim(bottom=0, top=1500)
    ax.set_xlim(left=-0.02, right=0.48)
    plt.legend(bbox_to_anchor=(0.31, 0.7))
    plt.legend(labelspacing=0.05)
    plt.grid()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4], ['0', '0.1', '0.2', '0.3', '0.4'])
    plt.tight_layout()
    fig.savefig('./results/overhead and EED under heavy load.pdf', dpi=300, format='pdf')
    plt.close()


def drawPDRUnderHeavyLoad():
    # plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['axes.titlesize'] = 22
    plt.rcParams['axes.labelsize'] = 22
    plt.rcParams['xtick.labelsize'] = 18
    plt.rcParams['ytick.labelsize'] = 18
    plt.rcParams['legend.fontsize'] = 20
    fig, ax = plt.subplots()

    overhead = []
    ratio = []
    hops = [str(i) for i in range(0, 5)]
    for hop in hops:
        folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withLoopPrevention-withLoadBalance-0.05/' + hop + '/'
        overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
        ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 200000)) * 100)

    ax.plot(overhead, ratio, label='with load balance, thr=0.05', marker='o', linewidth=4.0, markersize=10)
    for i in range(len(ratio)):
        ax.text(overhead[i], ratio[i] - 0.1, hops[i],
            ha='right', va='top', fontdict={'size': 22})


    overhead = []
    ratio = []
    hops = [str(i) for i in range(0, 5)]
    for hop in hops:
        folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withLoopPrevention-withLoadBalance-0.2/' + hop + '/'
        overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
        ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 200000)) * 100)

    ax.plot(overhead, ratio, label='with load balance, thr=0.2', marker='X', linestyle='--', linewidth=4.0, markersize=10)
    for i in range(len(ratio)):
        ax.text(overhead[i], ratio[i], hops[i],
            ha='left', va='bottom', fontdict={'size': 22})
    

    overhead = []
    ratio = []
    hops = [str(i) for i in range(0, 5)]
    hops.append('OSPF-L')
    hops.append('OPSPF')
    for hop in hops:
        if hop.isnumeric():
            folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withoutLoopPrevention-withoutLoadBalance/' + hop + '/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 200000)) * 100)
        elif hop == 'OSPF-L':
            folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6 / 2)
            ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 200000)) * 100)
        elif hop == 'OPSPF':
            folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 200000)) * 100)

    ax.plot(overhead, ratio, label='without load balance', marker='^', linestyle='dotted', linewidth=4.0, markersize=10)
    for i in range(len(ratio)):
        if hops[i].isnumeric():
            ax.text(overhead[i], ratio[i], hops[i],
                ha='left', va='bottom', fontdict={'size': 22})
        else:
            ax.text(overhead[i], ratio[i], hops[i],
                ha='center', va='bottom', fontdict={'size': 22})
        
    
    # ideal_x = numpy.linspace(-1, 1, 1000)
    # ideal_y = numpy.full_like(ideal_x, 0)
    # ax.plot(ideal_x, ideal_y, linestyle='-.', label='ideal packet loss')


    # ax.set_title('Avg. Packet Delivery Ratio & Control Overhead \nunder Heavy Load, Link Failure Rate = 10%')
    ax.set_xlabel('Control Overhead (MBps)')
    ax.set_ylabel('Packet Loss Ratio (%)')
    ax.set_ylim(top=52)
    ax.set_xlim(left=-0.02, right=0.48)
    plt.legend(bbox_to_anchor=(1.0, 0.6))
    plt.grid()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4], ['0', '0.1', '0.2', '0.3', '0.4'])
    plt.tight_layout()
    fig.savefig('./results/overhead and PDR under heavy load.pdf', dpi=300, format='pdf')
    plt.close()


if __name__ == '__main__':
    
    drawEEDUnderLightLoad()
    drawPDRUnderLightLoad()
    drawEEDUnderHeavyLoad()
    drawPDRUnderHeavyLoad()

    pass
