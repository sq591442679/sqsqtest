import matplotlib.pyplot as plt
import os
import numpy
import pandas
from typing import List

root_dir = '/home/sqsq/Desktop/sat-ospf/inet/examples/ospfv2/sqsqtest/results/'
from command import NUM_OF_TESTS, test_names
# from resultAnalyze import getAvgDelay, getAvgLSUOverhead, getAvgPacketDeliveryRate
from NEDGenerator import SIMULATION_DURATION_TIME


"""
returns the average delay of arg_names in corresponding folder_name
unit: ms
"""
def getAvgDelay(folder_name: str, arg_names: List[str]) -> float:
    df = pandas.DataFrame()
    for config_name in arg_names:
        if df.empty:
            df = pandas.read_csv(folder_name + config_name + '/successPacketCooked.csv')
        else:
            df = pandas.concat(
                [df, pandas.read_csv(folder_name + config_name + '/successPacketCooked.csv')],
                ignore_index=True
            )
    return df['avgDelay'].sum() / len(arg_names) * 1000


"""
unit: Mbps
"""
def getAvgControlOverhead(folder_name: str, arg_names: List[str], is_OSPFL: bool) -> float:
    overhead = 0
    df = pandas.DataFrame()
    for config_name in arg_names:
        if df.empty:
            df = pandas.read_csv(folder_name + config_name + '/controlOverhead.csv')
        else:
            df = pandas.concat(
                [df, pandas.read_csv(folder_name + config_name + '/controlOverhead.csv')],
                ignore_index=True
            )
    overhead += df['ELBOverhead'].sum()
    if is_OSPFL:
        overhead += (df['LSUOverhead'].sum() / 2)
    else:
        overhead += df['LSUOverhead'].sum()
    overhead /= len(arg_names)
    overhead /= SIMULATION_DURATION_TIME
    overhead /= 1e6
    
    return overhead


"""
unit: percentage
"""
def getAvgPacketLossRatio(folder_name: str, arg_names: List[str], expected_packet_number: int) -> float:
    df = pandas.DataFrame()
    for config_name in arg_names:
        if df.empty:
            df = pandas.read_csv(folder_name + config_name + '/successPacketCooked.csv')
        else:
            df = pandas.concat(
                [df, pandas.read_csv(folder_name + config_name + '/successPacketCooked.csv')],
                ignore_index=True
            )
    success_count = df['successCnt'].sum()
    return (1 - success_count / (len(arg_names) * expected_packet_number)) * 100


def drawEEDUnderLightLoad():
    # plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['axes.titlesize'] = 23
    plt.rcParams['axes.labelsize'] = 23
    plt.rcParams['xtick.labelsize'] = 23
    plt.rcParams['ytick.labelsize'] = 23
    plt.rcParams['legend.fontsize'] = 20
    fig, ax = plt.subplots()

    fr_names = ['05', '15']
    markers = ['X', 'o', '^', 's']
    linestyles = ['-', '--', ':', '-.']

    for i in range(len(fr_names)):
        fr = fr_names[i]
        arg_names = ['fail' + fr + '_test' + str(i) for i in range(1, NUM_OF_TESTS + 1)]

        overhead = []
        delay = []
        hops = [str(i) for i in range(1, 8)]
        # hops.append('OSPFL')
        # hops.append('OPSPF')

        for hop in hops:
            if hop.isnumeric():
                folder_name = root_dir + 'light_load/withDD-withLoopPrevention-withoutLoadBalance/' + hop + '/'
                overhead.append(getAvgControlOverhead(folder_name, arg_names, False))
                delay.append(getAvgDelay(folder_name, arg_names))
            elif hop == 'OSPFL':
                folder_name = root_dir + 'light_load/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
                overhead.append(getAvgControlOverhead(folder_name, arg_names, True))
                delay.append(getAvgDelay(folder_name, arg_names))
            elif hop == 'OPSPF':
                folder_name = root_dir + 'light_load/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
                overhead.append(getAvgControlOverhead(folder_name, arg_names, False))
                delay.append(getAvgDelay(folder_name, arg_names))
        if i == 0:
            ax.plot(overhead, delay, label='%d%%, LoFi(n, 1)' % int(fr), color='#ff7f0e', 
                    marker='o', linestyle='--', linewidth=1.5, markersize=10)
        else:
            ax.plot(overhead, delay, label='%d%%, LoFi(n, 1)' % int(fr), color='#ff7f0e', 
                    marker='o', markerfacecolor='white', linestyle='--', linewidth=1.5, markersize=10)
        
        print(overhead, delay)
        for j in range(len(delay)):
            if i == 0:
                if hops[j] == '1':
                    ax.text(overhead[j], delay[j] - 0.4, hops[j],
                        ha='right', va='top', fontdict={'size': 23})
                else:
                    ax.text(overhead[j], delay[j] - 0.4, hops[j],
                        ha='center', va='top', fontdict={'size': 23})
            else:
                ax.text(overhead[j], delay[j], hops[j],
                    ha='left', va='bottom', fontdict={'size': 23})


    for i in range(len(fr_names)):
        fr = fr_names[i]
        arg_names = ['fail' + fr + '_test' + str(i) for i in range(1, NUM_OF_TESTS + 1)]
        overhead = []
        delay = []
        folder_name = root_dir + 'light_load/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
        overhead.append(getAvgControlOverhead(folder_name, arg_names, False))
        delay.append(getAvgDelay(folder_name, arg_names))
        if i == 0:
            ax.plot(overhead, delay, color='#d62728', marker='^', linewidth=2.5, markersize=10)
            ax.text(overhead[0] + 0.02, delay[0], '%d%%, OPSPF' % int(fr),
                        ha='left', va='center', fontdict={'size': 23})
        else:
            ax.plot(overhead, delay, color='#d62728', marker='^', markerfacecolor='white', linewidth=2.5, markersize=10)
            ax.text(overhead[0], delay[0] - 1, '%d%%,\nOPSPF' % int(fr),
                        ha='center', va='top', fontdict={'size': 23})

    
    # ax.set_title('Avg. End-to-end delay & Control overhead \nunder Light Load, Link Failure Rate = 10%')
    ax.set_xlabel('Control overhead (MBps)')
    ax.set_ylabel('End-to-end delay (ms)')
    ax.set_ylim(bottom=65, top=89)
    ax.set_xlim(right=0.65)
    plt.legend(borderpad=0.1, labelspacing=0.02)
    plt.grid()
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], ['0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6'])
    plt.tight_layout()
    fig.savefig('./results/overhead and EED under light load.pdf', dpi=300, format='pdf')
    plt.close()


def drawPDRUnderLightLoad():
    # plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['axes.titlesize'] = 23
    plt.rcParams['axes.labelsize'] = 23
    plt.rcParams['xtick.labelsize'] = 23
    plt.rcParams['ytick.labelsize'] = 23
    plt.rcParams['legend.fontsize'] = 20
    fig, ax = plt.subplots()


    fr_names = ['05', '15']
    markers = ['X', 'o', '^', 's']
    linestyles = ['-', '--', ':', '-.']

    for i in range(len(fr_names)):
        fr = fr_names[i]
        arg_names = ['fail' + fr + '_test' + str(i) for i in range(1, NUM_OF_TESTS + 1)]
        overhead = []
        ratio = []
        hops = [str(i) for i in range(1, 8)]
        # hops.append('OSPFL')
        # hops.append('OPSPF')

        for hop in hops:
            if hop.isnumeric():
                folder_name = root_dir + 'light_load/withDD-withLoopPrevention-withoutLoadBalance/' + hop + '/'
                overhead.append(getAvgControlOverhead(folder_name, arg_names, False))
                ratio.append(getAvgPacketLossRatio(folder_name, arg_names, 10000))
            elif hop == 'OSPFL':
                folder_name = root_dir + 'light_load/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
                overhead.append(getAvgControlOverhead(folder_name, arg_names, True))
                ratio.append(getAvgPacketLossRatio(folder_name, arg_names, 10000))
            elif hop == 'OPSPF':
                folder_name = root_dir + 'light_load/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
                overhead.append(getAvgControlOverhead(folder_name, arg_names, False))
                ratio.append(getAvgPacketLossRatio(folder_name, arg_names, 10000))
        if i == 0:
            ax.plot(overhead, ratio, label='%d%%, LoFi(n, 1)' % int(fr), color='#ff7f0e', 
                    marker='o', linestyle='--', linewidth=1.5, markersize=10)
        else:
            ax.plot(overhead, ratio, label='%d%%, LoFi(n, 1)' % int(fr), color='#ff7f0e', 
                    marker='o', markerfacecolor='white', linestyle='--', linewidth=1.5, markersize=10)
        for j in range(len(ratio)):
            if i == 1 and hops[j] == '1':
                ax.text(overhead[j], ratio[j], hops[j],
                    ha='left', va='center', fontdict={'size': 23})
            else:
                ax.text(overhead[j], ratio[j], hops[j],
                    ha='left', va='bottom', fontdict={'size': 23})


    for i in range(len(fr_names)):
        fr = fr_names[i]
        arg_names = ['fail' + fr + '_test' + str(i) for i in range(1, NUM_OF_TESTS + 1)]
        overhead = []
        ratio = []
        folder_name = root_dir + 'light_load/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
        overhead.append(getAvgControlOverhead(folder_name, arg_names, False))
        ratio.append(getAvgPacketLossRatio(folder_name, arg_names, 10000))
        if i == 0:
            ax.plot(overhead, ratio, color='#d62728', marker='^', linewidth=2.5, markersize=10)
            ax.text(overhead[0] + 0.02, ratio[0], '%d%%, OPSPF' % int(fr),
                        ha='left', va='center', fontdict={'size': 23})
        else:
            ax.plot(overhead, ratio, color='#d62728', marker='^', markerfacecolor='white', linewidth=2.5, markersize=10)
            ax.text(overhead[0], ratio[0] + 0.02, '%d%%,\nOPSPF' % int(fr),
                        ha='center', va='bottom', fontdict={'size': 23})
    

    # ax.set_title('Avg. Packet Delivery Ratio & Control overhead \nunder Light Load, Link Failure Rate = 10%')
    ax.set_xlabel('Control overhead (MBps)')
    ax.set_ylabel('Packet loss ratio (%)')
    ax.set_ylim(bottom=0, top=2.1)
    ax.set_xlim(right=0.65)
    plt.legend(borderpad=0.1, labelspacing=0.02)
    plt.grid()
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], ['0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6'])
    plt.tight_layout()
    fig.savefig('./results/overhead and PDR under light load.pdf', dpi=300, format='pdf')
    plt.close()


def drawEEDUnderHeavyLoad():
    # plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['axes.titlesize'] = 23
    plt.rcParams['axes.labelsize'] = 23
    plt.rcParams['xtick.labelsize'] = 23
    plt.rcParams['ytick.labelsize'] = 23
    plt.rcParams['legend.fontsize'] = 20
    fig, ax = plt.subplots()

    arg_names = ['fail10_test' + str(i) for i in range(1, NUM_OF_TESTS + 1)]

    overhead = []
    delay = []
    hops = [str(i) for i in range(1, 8)]
    # hops.append('ELB')
    for hop in hops:
        if hop.isnumeric():
            folder_name = root_dir + 'heavy_load/withDD-withLoopPrevention-withLoadBalance-0.05/' + hop + '/'
            overhead.append(getAvgControlOverhead(folder_name, arg_names, False))
            delay.append(getAvgDelay(folder_name, arg_names))
            
    ax.plot(overhead, delay, label="LoFi(n, 0.05)", color='#ff7f0e', 
            marker='o', linestyle='--', linewidth=1.5, markersize=10)
    for i in range(len(delay)):
        if hops[i].isnumeric():
            ax.text(overhead[i], delay[i] - 20, hops[i],
                ha='right', va='top', fontdict={'size': 23})
        else:
            ax.text(overhead[i], delay[i] - 20, hops[i],
                ha='right', va='bottom', fontdict={'size': 23})


    # overhead = []
    # delay = []
    # hops = [str(i) for i in range(0, 5)]
    # for hop in hops:
    #     folder_name = root_dir + 'heavy_load/withDD-withLoopPrevention-withLoadBalance-0.2/' + hop + '/'
    #     overhead.append(getAvgControlOverhead(folder_name, arg_names, False))
    #     delay.append(getAvgDelay(folder_name, arg_names))

    # ax.plot(overhead, delay, label="load balance, $\delta$=0.2", marker='X', linestyle='--', linewidth=2.5, markersize=10)
    # for i in range(len(delay)):
    #     ax.text(overhead[i], delay[i] - 5, hops[i],
    #         ha='left', va='bottom', fontdict={'size': 23})
    

    overhead = []
    delay = []
    hops = [str(i) for i in range(1, 8)]
    # hops.append('OSPFL')
    # hops.append('OPSPF')
    for hop in hops:
        if hop.isnumeric():
            folder_name = root_dir + 'heavy_load/withDD-withLoopPrevention-withoutLoadBalance/' + hop + '/'
            overhead.append(getAvgControlOverhead(folder_name, arg_names, False))
            delay.append(getAvgDelay(folder_name, arg_names))
        elif hop == 'OSPFL':
            folder_name = root_dir + 'heavy_load/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgControlOverhead(folder_name, arg_names, True))
            delay.append(getAvgDelay(folder_name, arg_names))
        elif hop == 'OPSPF':
            folder_name = root_dir + 'heavy_load/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgControlOverhead(folder_name, arg_names, False))
            delay.append(getAvgDelay(folder_name, arg_names))

    ax.plot(overhead, delay, label='LoFi(n, 1)', color='#ff7f0e', 
            marker='o', markerfacecolor='white', linestyle='--', linewidth=1.5, markersize=10)
    for i in range(len(delay)):
        if hops[i] == '2':
            ax.text(overhead[i], delay[i], hops[i],
                ha='left', va='bottom', fontdict={'size': 23})
        else:
            ax.text(overhead[i], delay[i], hops[i],
                ha='center', va='bottom', fontdict={'size': 23})

    
    overhead = []
    delay = []
    folder_name = root_dir + 'heavy_load/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
    overhead.append(getAvgControlOverhead(folder_name, arg_names, False))
    delay.append(getAvgDelay(folder_name, arg_names))
    ax.plot(overhead, delay, color='#2ca02c', marker='^', linewidth=2.5, markersize=10)
    ax.text(overhead[0], delay[0] - 5, 'OPSPF',
                ha='left', va='bottom', fontdict={'size': 23})


    overhead = []
    delay = []
    folder_name = root_dir + 'heavy_load/ELB/15/'

    overhead.append(getAvgControlOverhead(folder_name, arg_names, True))
    delay.append(getAvgDelay(folder_name, arg_names))   
    print(overhead, delay)
    ax2 = fig.add_axes([0.5, 0.43, 0.2, 0.23])
    ax2.plot(overhead, delay, color='#d62728', marker='s', markersize=10)
    ax2.text(overhead[0], delay[0] + 10, 'ELB',
                ha='center', va='bottom', fontdict={'size': 23})
    ax2.tick_params(axis='both', labelsize=20)
    
    # ideal_x = numpy.linspace(-1, 1, 1000)
    # ideal_y = numpy.full_like(ideal_x, 33.5)
    # ax.plot(ideal_x, ideal_y, linestyle='-.', label='ideal delay', linewidth=2.5, markersize=10)
        
    
    # ax.set_title('Avg. End-to-end delay & Control overhead \nunder Heavy Load, Link Failure Rate = 10%')
    ax.set_xlabel('Control overhead (MBps)')
    ax.set_ylabel('End-to-end delay (ms)')
    ax.set_ylim(bottom=0, top=1560)
    ax.set_xlim(left=-0.01)
    lines = []
    labels = []
    for _ax in fig.axes:
        axLine, axLabel = _ax.get_legend_handles_labels()
        lines.extend(axLine)
        labels.extend(axLabel)
    fig.legend(lines, labels, borderpad=0.1, labelspacing=0.02, loc=(0.55, 0.82))
    ax.grid(True)
    ax.set_xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
    ax.set_xticklabels(['0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7'])
    ax.set_yticks([0, 250, 500, 750, 1000, 1250, 1500])
    ax.set_yticklabels([str(i) for i in [0, 250, 500, 750, 1000, 1250, 1500]])

    ax2.grid(True)
    ax2.set_xlim(left=0.94, right=1.02)
    ax2.set_ylim(top=780)
    ax2.set_xticks([0.95, 1.00])
    ax2.set_xticklabels(['0.95', '1'])
    ax2.set_yticks([700, 750])
    ax2.set_yticklabels(['700', '750'])

    plt.tight_layout()
    fig.savefig('./results/overhead and EED under heavy load.pdf', dpi=300, format='pdf')
    plt.close()


def drawPDRUnderHeavyLoad():
    # plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['axes.titlesize'] = 23
    plt.rcParams['axes.labelsize'] = 23
    plt.rcParams['xtick.labelsize'] = 23
    plt.rcParams['ytick.labelsize'] = 23
    plt.rcParams['legend.fontsize'] = 20
    fig, ax = plt.subplots()

    arg_names = ['fail10_test' + str(i) for i in range(1, NUM_OF_TESTS + 1)]


    overhead = []
    ratio = []
    hops = [str(i) for i in range(1, 8)]
    for hop in hops:
        folder_name = root_dir + 'heavy_load/withDD-withLoopPrevention-withLoadBalance-0.05/' + hop + '/'
        ratio.append(getAvgPacketLossRatio(folder_name, arg_names, 200000))
        overhead.append(getAvgControlOverhead(folder_name, arg_names, False))

    ax.plot(overhead, ratio, label="LoFi(n, 0.05)", color='#ff7f0e', 
            marker='o', linestyle='--', linewidth=1.5, markersize=10)
    for i in range(len(ratio)):
        if hops[i].isnumeric():
            ax.text(overhead[i], ratio[i] - 0.1, hops[i],
                ha='right', va='bottom', fontdict={'size': 23})
        else:
            ax.text(overhead[i], ratio[i] - 0.1, hops[i],
                ha='right', va='center', fontdict={'size': 23})


    # overhead = []
    # ratio = []
    # hops = [str(i) for i in range(0, 5)]
    # for hop in hops:
    #     folder_name = root_dir + 'heavy_load/withDD-withLoopPrevention-withLoadBalance-0.2/' + hop + '/'
    #     ratio.append(getAvgPacketLossRatio(folder_name, arg_names, 200000))
    #     overhead.append(getAvgControlOverhead(folder_name, arg_names, False))

    # ax.plot(overhead, ratio, label="load balance, $\delta$=0.2", marker='X', linestyle='--', linewidth=2.5, markersize=10)
    # for i in range(len(ratio)):
    #     ax.text(overhead[i], ratio[i], hops[i],
    #         ha='left', va='bottom', fontdict={'size': 23})
    

    overhead = []
    ratio = []
    hops = [str(i) for i in range(1, 8)]
    # hops.append('OSPFL')
    # hops.append('OPSPF')
    for hop in hops:
        if hop.isnumeric():
            folder_name = root_dir + 'heavy_load/withDD-withLoopPrevention-withoutLoadBalance/' + hop + '/'
            ratio.append(getAvgPacketLossRatio(folder_name, arg_names, 200000))
            overhead.append(getAvgControlOverhead(folder_name, arg_names, False))
        elif hop == 'OSPFL':
            folder_name = root_dir + 'heavy_load/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            ratio.append(getAvgPacketLossRatio(folder_name, arg_names, 200000))
            overhead.append(getAvgControlOverhead(folder_name, arg_names, True))
        elif hop == 'OPSPF':
            folder_name = root_dir + 'heavy_load/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            ratio.append(getAvgPacketLossRatio(folder_name, arg_names, 200000))
            overhead.append(getAvgControlOverhead(folder_name, arg_names, False))

    ax.plot(overhead, ratio, label='LoFi(n, 1)', color='#ff7f0e', 
            marker='o', markerfacecolor='white', linestyle='--', linewidth=1.5, markersize=10)
    for i in range(len(ratio)):
        if hops[i] == '2':
            ax.text(overhead[i], ratio[i], hops[i],
                ha='left', va='bottom', fontdict={'size': 23})
        else:
            ax.text(overhead[i], ratio[i], hops[i],
                ha='center', va='bottom', fontdict={'size': 23})
        
    overhead = []
    ratio = []
    folder_name = root_dir + 'heavy_load/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
    ratio.append(getAvgPacketLossRatio(folder_name, arg_names, 200000))
    overhead.append(getAvgControlOverhead(folder_name, arg_names, False))
    ax.plot(overhead, ratio, color='#2ca02c', marker='^', linewidth=2.5, markersize=10)
    ax.text(overhead[0], ratio[0], 'OPSPF',
                ha='left', va='bottom', fontdict={'size': 23})
    
    overhead = []
    ratio = []
    folder_name = root_dir + 'heavy_load/ELB/15/'

    overhead.append(getAvgControlOverhead(folder_name, arg_names, True))
    ratio.append(getAvgPacketLossRatio(folder_name, arg_names, 200000))   
    print(overhead, ratio)
    ax2 = fig.add_axes([0.5, 0.45, 0.2, 0.2])
    ax2.plot(overhead, ratio, color='#d62728', marker='s', markersize=10)
    ax2.text(overhead[0], ratio[0] + 0.1, 'ELB',
                ha='center', va='bottom', fontdict={'size': 23})
    ax2.tick_params(axis='both', labelsize=20)
    

    # ax.set_title('Avg. Packet Delivery Ratio & Control overhead \nunder Heavy Load, Link Failure Rate = 10%')
    ax.set_xlabel('Control overhead (MBps)')
    ax.set_ylabel('Packet loss ratio (%)')
    ax.set_ylim(bottom=-1, top=48)
    ax.set_xlim(left=-0.01)
    lines = []
    labels = []
    for _ax in fig.axes:
        axLine, axLabel = _ax.get_legend_handles_labels()
        lines.extend(axLine)
        labels.extend(axLabel)
    fig.legend(lines, labels, borderpad=0.1, labelspacing=0.02, loc=(0.55, 0.82))
    ax.grid(True)
    ax.set_xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
    ax.set_xticklabels(['0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7'])

    ax2.grid(True)
    ax2.set_xlim(left=0.94, right=1.02)
    # ax2.set_ylim(top=790)
    ax2.set_xticks([0.95, 1.00])
    ax2.set_xticklabels(['0.95', '1'])
    # ax2.set_yticks([700, 750])
    # ax2.set_yticklabels(['700', '750'])
    
    plt.tight_layout()
    fig.savefig('./results/overhead and PDR under heavy load.pdf', dpi=300, format='pdf')
    plt.close()


def drawLightLoadPDRUnderDifferentFailureRate():
    plt.rcParams['axes.titlesize'] = 23
    plt.rcParams['axes.labelsize'] = 23
    plt.rcParams['xtick.labelsize'] = 23
    plt.rcParams['ytick.labelsize'] = 23
    plt.rcParams['legend.fontsize'] = 20
    fig, ax = plt.subplots()

    fr_names = ["00", "05", "10", "15", "20"]
    folder_names = []
    folder_names.append(root_dir + 'light_load/withDD-withLoopPrevention-withoutLoadBalance/3/')
    folder_names.append(root_dir + 'light_load/withDD-withLoopPrevention-withoutLoadBalance/4/')
    folder_names.append(root_dir + 'light_load/withDD-withLoopPrevention-withoutLoadBalance/5/')
    folder_names.append(root_dir + 'light_load/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/')

    experiment_names = ['n=3', 'n=4', 'n=5', 'OSPFL']

    markers = ['X', 'o', '^', 's']
    linestyles = ['-', '--', ':', '-.']

    for i in range(len(folder_names)):
        loss_ratio_list = []

        for fr in fr_names:
            arg_names = ["fail" + fr + "_test" + j for j in test_names]
            loss_ratio_list.append(getAvgPacketLossRatio(folder_names[i], arg_names, 10000))

        x = [int(j) for j in fr_names]
        ax.plot(x, loss_ratio_list, label=experiment_names[i], marker=markers[i], linestyle=linestyles[i], linewidth=3, markersize=10)
    
    ax.set_xlabel('Link failure rate (%)')
    ax.set_ylabel('Packet loss rate (%)')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    fig.savefig('./results/PDR on different fr under light load.pdf', dpi=300, format='pdf')
    plt.close()


def drawLightLoadEEDUnderDifferentFailureRate():
    plt.rcParams['axes.titlesize'] = 23
    plt.rcParams['axes.labelsize'] = 23
    plt.rcParams['xtick.labelsize'] = 23
    plt.rcParams['ytick.labelsize'] = 23
    plt.rcParams['legend.fontsize'] = 20
    fig, ax = plt.subplots()

    fr_names = ["00", "05", "10", "15", "20"]
    folder_names = []
    folder_names.append(root_dir + 'light_load/withDD-withLoopPrevention-withoutLoadBalance/3/')
    folder_names.append(root_dir + 'light_load/withDD-withLoopPrevention-withoutLoadBalance/4/')
    folder_names.append(root_dir + 'light_load/withDD-withLoopPrevention-withoutLoadBalance/5/')
    folder_names.append(root_dir + 'light_load/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/')

    experiment_names = ['n=3', 'n=4', 'n=5', 'OSPFL']

    markers = ['X', 'o', '^', 's']
    linestyles = ['-', '--', ':', '-.']

    for i in range(len(folder_names)):
        delay_list = []

        for fr in fr_names:
            arg_names = ["fail" + fr + "_test" + j for j in test_names]
            delay_list.append(getAvgDelay(folder_names[i], arg_names)) 

        x = [int(j) for j in fr_names]
        ax.plot(x, delay_list, label=experiment_names[i], marker=markers[i], linestyle=linestyles[i], linewidth=3, markersize=10)
    
    ax.set_xlabel('Link failure rate (%)')
    ax.set_ylabel('End-to-end delay (ms)')
    ax.set_ylim(bottom=0)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    fig.savefig('./results/EED on different fr under light load.pdf', dpi=300, format='pdf')
    plt.close()


def drawLightLoadOverheadunderDifferentFailureRate():
    plt.rcParams['axes.titlesize'] = 23
    plt.rcParams['axes.labelsize'] = 23
    plt.rcParams['xtick.labelsize'] = 23
    plt.rcParams['ytick.labelsize'] = 23
    plt.rcParams['legend.fontsize'] = 20
    fig, ax = plt.subplots()

    fr_names = ["00", "05", "10", "15", "20"]
    folder_names = []
    folder_names.append(root_dir + 'light_load/withDD-withLoopPrevention-withoutLoadBalance/3/')
    folder_names.append(root_dir + 'light_load/withDD-withLoopPrevention-withoutLoadBalance/4/')
    folder_names.append(root_dir + 'light_load/withDD-withLoopPrevention-withoutLoadBalance/5/')
    folder_names.append(root_dir + 'light_load/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/')

    experiment_names = ['n=3', 'n=4', 'n=5', 'OSPFL']

    markers = ['X', 'o', '^', 's']
    linestyles = ['-', '--', ':', '-.']

    for i in range(len(folder_names)):
        overhead_list = []

        for fr in fr_names:
            arg_names = ["fail" + fr + "_test" + j for j in test_names]
            overhead_list.append(getAvgControlOverhead(folder_names[i], arg_names, False))

        x = [int(j) for j in fr_names]
        ax.plot(x, overhead_list, label=experiment_names[i], marker=markers[i], linestyle=linestyles[i], linewidth=3, markersize=10)
    
    ax.set_xlabel('Link failure rate (%)')
    ax.set_ylabel('Control Overhead (MBps)')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    fig.savefig('./results/Overhead on different fr under light load.pdf', dpi=300, format='pdf')
    plt.close()


def drawHeavyLoadPDRUnderDifferentFailureRate():
    plt.rcParams['axes.titlesize'] = 42
    plt.rcParams['axes.labelsize'] = 42
    plt.rcParams['xtick.labelsize'] = 42
    plt.rcParams['ytick.labelsize'] = 42
    plt.rcParams['legend.fontsize'] = 40
    fig, ax = plt.subplots()

    fr_names = ["00", "05", "10", "15", "20"]
    folder_names = []
    folder_names.append(root_dir + 'heavy_load/withDD-withLoopPrevention-withLoadBalance-0.05/2/')
    # folder_names.append(root_dir + 'heavy_load/withDD-withLoopPrevention-withLoadBalance-0.05/3/')
    folder_names.append(root_dir + 'heavy_load/withDD-withLoopPrevention-withLoadBalance-0.05/4/')
    folder_names.append(root_dir + 'heavy_load/ELB/15/')

    experiment_names = ['LoFi(2, 0.05)', 'LoFi(4, 0.05)', 'ELB']
    hatches = ['++', '///', '\\\\\\', '']

    total_width, num = 0.7, 3
    width = total_width / num
    x = [int(i) / 5 for i in fr_names]
    x = numpy.array(x)
    x = x - (total_width - width) / 2

    for i in range(len(experiment_names)):
        ratio = []
        for fr in fr_names:
            arg_names = ['fail' + fr + '_test' + str(j) for j in range(1, NUM_OF_TESTS + 1)]
            ratio.append(getAvgPacketLossRatio(folder_names[i], arg_names, 200000))
        plt.bar(x + i * (width + 0.05), ratio, width=width, label=experiment_names[i], hatch=hatches[i], linewidth=4,
                color='white', edgecolor=plt.rcParams['axes.prop_cycle'].by_key()['color'][i])
    
    ax.set_xlabel('Link failure rate (%)')
    ax.set_ylabel('Packet loss rate (%)')
    ax.set_ylim(top=25)
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_xticklabels([str(i * 5) for i in [0, 1, 2, 3, 4]])
    legend = ax.legend(borderpad=0.1, labelspacing=0.02, ncol=3, columnspacing=1, handletextpad=0.2)
    plt.grid()

    width, height = 16, 9
    fig.set_size_inches(width, height)
    plt.tight_layout()
    fig.savefig('./results/PDR on different fr under heavy load.pdf', dpi=300, format='pdf')
    plt.close()


def drawHeavyLoadEEDUnderDifferentFailureRate():
    plt.rcParams['axes.titlesize'] = 42
    plt.rcParams['axes.labelsize'] = 42
    plt.rcParams['xtick.labelsize'] = 42
    plt.rcParams['ytick.labelsize'] = 42
    plt.rcParams['legend.fontsize'] = 40
    fig, ax = plt.subplots()

    fr_names = ["00", "05", "10", "15", "20"]
    folder_names = []
    folder_names.append(root_dir + 'heavy_load/withDD-withLoopPrevention-withLoadBalance-0.05/2/')
    # folder_names.append(root_dir + 'heavy_load/withDD-withLoopPrevention-withLoadBalance-0.05/3/')
    folder_names.append(root_dir + 'heavy_load/withDD-withLoopPrevention-withLoadBalance-0.05/4/')
    folder_names.append(root_dir + 'heavy_load/ELB/15/')

    experiment_names = ['LoFi(2, 0.05)', 'LoFi(4, 0.05)', 'ELB']
    hatches = ['++', '///', '\\\\\\', '']

    total_width, num = 0.7, 3
    width = total_width / num
    x = [int(i) / 5 for i in fr_names]
    x = numpy.array(x)
    x = x - (total_width - width) / 2

    for i in range(len(experiment_names)):
        delay = []
        for fr in fr_names:
            arg_names = ['fail' + fr + '_test' + str(j) for j in range(1, NUM_OF_TESTS + 1)]
            delay.append(getAvgDelay(folder_names[i], arg_names))
        plt.bar(x + i * (width + 0.05), delay, width=width, label=experiment_names[i], hatch=hatches[i], linewidth=4,
                color='white', edgecolor=plt.rcParams['axes.prop_cycle'].by_key()['color'][i])
    
    ax.set_xlabel('Link failure rate (%)')
    ax.set_ylabel('End-to-end delay (ms)')
    ax.set_ylim(bottom=0, top=1070)
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_xticklabels([str(i * 5) for i in [0, 1, 2, 3, 4]])
    legend = ax.legend(borderpad=0.1, labelspacing=0.02, ncol=3, columnspacing=1, handletextpad=0.2)
    plt.grid()

    width, height = 16, 9
    fig.set_size_inches(width, height)

    plt.tight_layout()
    fig.savefig('./results/EED on different fr under heavy load.pdf', dpi=300, format='pdf')
    plt.close()


def drawHeavyLoadOverheadunderDifferentFailureRate():
    plt.rcParams['axes.titlesize'] = 42
    plt.rcParams['axes.labelsize'] = 42
    plt.rcParams['xtick.labelsize'] = 42
    plt.rcParams['ytick.labelsize'] = 42
    plt.rcParams['legend.fontsize'] = 40
    fig, ax = plt.subplots()

    fr_names = ["00", "05", "10", "15", "20"]
    folder_names = []
    folder_names.append(root_dir + 'heavy_load/withDD-withLoopPrevention-withLoadBalance-0.05/2/')
    # folder_names.append(root_dir + 'heavy_load/withDD-withLoopPrevention-withLoadBalance-0.05/3/')
    folder_names.append(root_dir + 'heavy_load/withDD-withLoopPrevention-withLoadBalance-0.05/4/')
    folder_names.append(root_dir + 'heavy_load/ELB/15/')

    experiment_names = ['LoFi(2, 0.05)', 'LoFi(4, 0.05)', 'ELB']
    hatches = ['++', '///', '\\\\\\', '']

    total_width, num = 0.7, 3
    width = total_width / num
    x = [int(i) / 5 for i in fr_names]
    x = numpy.array(x)
    x = x - (total_width - width) / 2

    for i in range(len(experiment_names)):
        overhead = []
        for fr in fr_names:
            arg_names = ['fail' + fr + '_test' + str(j) for j in range(1, NUM_OF_TESTS + 1)]
            overhead.append(getAvgControlOverhead(folder_names[i], arg_names, False))
        plt.bar(x + i * (width + 0.05), overhead, width=width, label=experiment_names[i], hatch=hatches[i], linewidth=4,
                color='white', edgecolor=plt.rcParams['axes.prop_cycle'].by_key()['color'][i])
    
    ax.set_xlabel('Link failure rate (%)')
    ax.set_ylabel('Control Overhead (MBps)')
    ax.set_ylim(top=1.6)
    ax.set_yticks([0, 0.5, 1.0, 1.5])
    ax.set_yticklabels([str(i) for i in [0, 0.5, 1.0, 1.5]])
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_xticklabels([str(i * 5) for i in [0, 1, 2, 3, 4]])
    legend = ax.legend(borderpad=0.1, labelspacing=0.02, ncol=3, columnspacing=1, handletextpad=0.2)
    plt.grid()

    width, height = 16, 9
    fig.set_size_inches(width, height)
    plt.tight_layout()
    fig.savefig('./results/Overhead on different fr under heavy load.pdf', dpi=300, format='pdf')
    plt.close()

if __name__ == '__main__':
    
    # drawEEDUnderLightLoad()
    # drawPDRUnderLightLoad()

    # drawEEDUnderHeavyLoad()
    # drawPDRUnderHeavyLoad()

    # drawLightLoadPDRUnderDifferentFailureRate()
    # drawLightLoadEEDUnderDifferentFailureRate()
    # drawLightLoadOverheadunderDifferentFailureRate()

    drawHeavyLoadPDRUnderDifferentFailureRate()
    drawHeavyLoadEEDUnderDifferentFailureRate()
    drawHeavyLoadOverheadunderDifferentFailureRate()

    pass
