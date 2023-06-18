import matplotlib.pyplot as plt
import os
import numpy
import pandas

root_dir = '/home/sqsq/Desktop/sat-ospf/inet/examples/ospfv2/sqsqtest/results/'
from command import fr_names, NUM_OF_TESTS, test_names
from resultAnalyze import getAvgDelay, getAvgLSUOverhead, getAvgPacketDeliveryRate
from NEDGenerator import SIMULATION_DURATION_TIME


def drawEEDUnderLightLoad():
    # plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['axes.titlesize'] = 23
    plt.rcParams['axes.labelsize'] = 23
    plt.rcParams['xtick.labelsize'] = 23
    plt.rcParams['ytick.labelsize'] = 23
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

    ax.plot(overhead, delay, label='with loop prevention', marker='o', linewidth=3.0, markersize=10)
    for i in range(len(delay)):
        ax.text(overhead[i], delay[i] - 5, hops[i],
            ha='right', va='top', fontdict={'size': 23})


    overhead = []
    delay = []
    hops = [str(i) for i in range(0, 5)]
    hops.append('OSPFL')
    hops.append('OPSPF')
    for hop in hops:
        if hop.isnumeric():
            folder_name = root_dir + 'results_lightload_p2p/withDD-withoutLoopPrevention-withoutLoadBalance/' + hop + '/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            delay.append(getAvgDelay(folder_name) * 1e3)
        elif hop == 'OSPFL':
            folder_name = root_dir + 'results_lightload_p2p/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6 / 2)
            delay.append(getAvgDelay(folder_name) * 1e3)
        elif hop == 'OPSPF':
            folder_name = root_dir + 'results_lightload_p2p/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            delay.append(getAvgDelay(folder_name) * 1e3)

    ax.plot(overhead, delay, label='without loop prevention', marker='X', linestyle='--', linewidth=3.0, markersize=10)
    for i in range(len(delay)):
        if hops[i] == '0' or hops[i] == '1' or hops[i] == '2' or hops[i] == '3':
            ax.text(overhead[i], delay[i] - 5, hops[i],
                ha='left', va='bottom', fontdict={'size': 23})
        elif hops[i] == 'OPSPF':
            ax.text(overhead[i], delay[i] - 5, hops[i],
                ha='right', va='bottom', fontdict={'size': 23})
        else:
            ax.text(overhead[i], delay[i] - 5, hops[i],
                ha='center', va='bottom', fontdict={'size': 23})
    
    # ax.set_title('Avg. End-to-end delay & Control overhead \nunder Light Load, Link Failure Rate = 10%')
    ax.set_xlabel('Control overhead (MBps)')
    ax.set_ylabel('End-to-end delay (ms)')
    ax.set_ylim(bottom=-15, top=1050)
    ax.set_xlim(right=0.48)
    plt.legend(bbox_to_anchor=(0.0761, 0.9))
    plt.grid()
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4], ['0', '0.1', '0.2', '0.3', '0.4'])
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


    # light load, with loop prevention
    overhead = []
    ratio = []
    hops = [str(i) for i in range(0, 5)]
    for hop in hops:
        folder_name = root_dir + 'results_lightload_p2p/withDD-withLoopPrevention-withoutLoadBalance/' + hop + '/'
        overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
        ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 10000)) * 100)

    ax.plot(overhead, ratio, label='with loop prevention', marker='o', linewidth=3.0, markersize=10)
    for i in range(len(ratio)):
        ax.text(overhead[i], ratio[i], hops[i],
            ha='right', va='top', fontdict={'size': 23})


    # light load, without loop prevention
    overhead = []
    ratio = []
    hops = [str(i) for i in range(0, 5)]
    hops.append('OSPFL')
    hops.append('OPSPF')
    for hop in hops:
        if hop.isnumeric():
            folder_name = root_dir + 'results_lightload_p2p/withDD-withoutLoopPrevention-withoutLoadBalance/' + hop + '/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 10000)) * 100)
        elif hop == 'OSPFL':
            folder_name = root_dir + 'results_lightload_p2p/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6 / 2)
            ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 10000)) * 100)
        elif hop == 'OPSPF':
            folder_name = root_dir + 'results_lightload_p2p/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 10000)) * 100)

    ax.plot(overhead, ratio, label='without loop prevention', marker='X', linestyle='--', linewidth=3.0, markersize=10)
    for i in range(len(ratio)):
        if hops[i] == '0' or hops[i] == '1' or hops[i] == '2' or hops[i] == '3':
            ax.text(overhead[i], ratio[i], hops[i],
                ha='left', va='bottom', fontdict={'size': 23})
        elif hops[i] == 'OPSPF':
            ax.text(overhead[i], ratio[i], hops[i],
                ha='right', va='bottom', fontdict={'size': 23})
        else:
            ax.text(overhead[i], ratio[i], hops[i],
                ha='center', va='bottom', fontdict={'size': 23})
    

    # ax.set_title('Avg. Packet Delivery Ratio & Control overhead \nunder Light Load, Link Failure Rate = 10%')
    ax.set_xlabel('Control overhead (MBps)')
    ax.set_ylabel('Packet loss ratio (%)')
    ax.set_ylim(bottom=-0.15, top=3.15)
    ax.set_xlim(right=0.48)
    plt.legend()
    plt.grid()
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4], ['0', '0.1', '0.2', '0.3', '0.4'])
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

    overhead = []
    delay = []
    hops = [str(i) for i in range(0, 5)]
    for hop in hops:
        folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withLoopPrevention-withLoadBalance-0.05/' + hop + '/'
        overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
        delay.append(getAvgDelay(folder_name) * 1e3)

    ax.plot(overhead, delay, label='load balance, thr=0.05', marker='o', linewidth=3.0, markersize=10)
    for i in range(len(delay)):
        ax.text(overhead[i], delay[i] - 5, hops[i],
            ha='right', va='top', fontdict={'size': 23})


    overhead = []
    delay = []
    hops = [str(i) for i in range(0, 5)]
    for hop in hops:
        folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withLoopPrevention-withLoadBalance-0.2/' + hop + '/'
        overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
        delay.append(getAvgDelay(folder_name) * 1e3)

    ax.plot(overhead, delay, label='load balance, thr=0.2', marker='X', linestyle='--', linewidth=3.0, markersize=10)
    for i in range(len(delay)):
        ax.text(overhead[i], delay[i] - 5, hops[i],
            ha='left', va='bottom', fontdict={'size': 23})
    

    overhead = []
    delay = []
    hops = [str(i) for i in range(0, 5)]
    hops.append('OSPFL')
    hops.append('OPSPF')
    for hop in hops:
        if hop.isnumeric():
            folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withoutLoopPrevention-withoutLoadBalance/' + hop + '/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            delay.append(getAvgDelay(folder_name) * 1e3)
        elif hop == 'OSPFL':
            folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6 / 2)
            delay.append(getAvgDelay(folder_name) * 1e3)
        elif hop == 'OPSPF':
            folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            delay.append(getAvgDelay(folder_name) * 1e3)

    ax.plot(overhead, delay, label='without load balance', marker='^', linestyle='dotted', linewidth=3.0, markersize=10)
    for i in range(len(delay)):
        if hops[i] == '0' or hops[i] == '1' or hops[i] == '2':
            ax.text(overhead[i], delay[i] - 5, hops[i],
                ha='left', va='bottom', fontdict={'size': 23})
        elif hops[i] == 'OPSPF':
            ax.text(overhead[i], delay[i] - 5, hops[i],
                ha='right', va='bottom', fontdict={'size': 23})
        else:
            ax.text(overhead[i], delay[i] - 5, hops[i],
                ha='center', va='bottom', fontdict={'size': 23})
        
    
    ideal_x = numpy.linspace(-1, 1, 1000)
    ideal_y = numpy.full_like(ideal_x, 33.5)
    ax.plot(ideal_x, ideal_y, linestyle='-.', label='ideal delay', linewidth=3.0, markersize=10)
        
    
    # ax.set_title('Avg. End-to-end delay & Control overhead \nunder Heavy Load, Link Failure Rate = 10%')
    ax.set_xlabel('Control overhead (MBps)')
    ax.set_ylabel('End-to-end delay (ms)')
    ax.set_ylim(bottom=0, top=1560)
    ax.set_xlim(left=-0.02, right=0.48)
    plt.legend(bbox_to_anchor=(0.12, 0.7), borderpad=0.1, labelspacing=0.02)
    plt.grid()
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4], ['0', '0.1', '0.2', '0.3', '0.4'])
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

    overhead = []
    ratio = []
    hops = [str(i) for i in range(0, 5)]
    for hop in hops:
        folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withLoopPrevention-withLoadBalance-0.05/' + hop + '/'
        overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
        ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 200000)) * 100)

    ax.plot(overhead, ratio, label='load balance, thr=0.05', marker='o', linewidth=3.0, markersize=10)
    for i in range(len(ratio)):
        ax.text(overhead[i], ratio[i] - 0.1, hops[i],
            ha='right', va='top', fontdict={'size': 23})


    overhead = []
    ratio = []
    hops = [str(i) for i in range(0, 5)]
    for hop in hops:
        folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withLoopPrevention-withLoadBalance-0.2/' + hop + '/'
        overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
        ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 200000)) * 100)

    ax.plot(overhead, ratio, label='load balance, thr=0.2', marker='X', linestyle='--', linewidth=3.0, markersize=10)
    for i in range(len(ratio)):
        ax.text(overhead[i], ratio[i], hops[i],
            ha='left', va='bottom', fontdict={'size': 23})
    

    overhead = []
    ratio = []
    hops = [str(i) for i in range(0, 5)]
    hops.append('OSPFL')
    hops.append('OPSPF')
    for hop in hops:
        if hop.isnumeric():
            folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withoutLoopPrevention-withoutLoadBalance/' + hop + '/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 200000)) * 100)
        elif hop == 'OSPFL':
            folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6 / 2)
            ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 200000)) * 100)
        elif hop == 'OPSPF':
            folder_name = root_dir + 'results_heavyload_p2p-pseudoPFC/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/'
            overhead.append(getAvgLSUOverhead(folder_name) / 1e6)
            ratio.append((1 - getAvgPacketDeliveryRate(folder_name, 200000)) * 100)

    ax.plot(overhead, ratio, label='without load balance', marker='^', linestyle='dotted', linewidth=3.0, markersize=10)
    for i in range(len(ratio)):
        if hops[i].isnumeric():
            ax.text(overhead[i], ratio[i], hops[i],
                ha='left', va='bottom', fontdict={'size': 23})
        elif hops[i] == 'OPSPF':
            ax.text(overhead[i], ratio[i], hops[i],
                ha='right', va='bottom', fontdict={'size': 23})
        else:
            ax.text(overhead[i], ratio[i], hops[i],
                ha='center', va='bottom', fontdict={'size': 23})
        
    
    # ideal_x = numpy.linspace(-1, 1, 1000)
    # ideal_y = numpy.full_like(ideal_x, 0)
    # ax.plot(ideal_x, ideal_y, linestyle='-.', label='ideal packet loss')


    # ax.set_title('Avg. Packet Delivery Ratio & Control overhead \nunder Heavy Load, Link Failure Rate = 10%')
    ax.set_xlabel('Control overhead (MBps)')
    ax.set_ylabel('Packet loss ratio (%)')
    ax.set_ylim(bottom=-4, top=54)
    ax.set_xlim(left=-0.02, right=0.48)
    plt.legend(bbox_to_anchor=(1.0, 0.62))
    plt.grid()
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4], ['0', '0.1', '0.2', '0.3', '0.4'])
    plt.tight_layout()
    fig.savefig('./results/overhead and PDR under heavy load.pdf', dpi=300, format='pdf')
    plt.close()


def drawPDRUnderDifferentFailureRate():
    plt.rcParams['axes.titlesize'] = 23
    plt.rcParams['axes.labelsize'] = 23
    plt.rcParams['xtick.labelsize'] = 23
    plt.rcParams['ytick.labelsize'] = 23
    plt.rcParams['legend.fontsize'] = 20
    fig, ax = plt.subplots()

    folder_names = []
    folder_names.append(root_dir + 'results_different_fr/withDD-withLoopPrevention-withoutLoadBalance/3/')
    folder_names.append(root_dir + 'results_different_fr/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/')
    expected_total_num_packets = 10000

    experiment_names = ['n=3', 'OSPFL']

    markers = ['o', 'X', '^']
    linestyles = ['-', '--', 'dotted']

    for i in range(len(folder_names)):
        loss_ratio_list = []

        for fr in fr_names:
            arg_names = ["fail" + fr + "_test" + j for j in test_names]
            df = pandas.DataFrame()
            for config_name in arg_names:
                if df.empty:
                    df = pandas.read_csv(folder_names[i] + config_name + '/successPacketCooked.csv')
                else:
                    df = pandas.concat(
                        [df, pandas.read_csv(folder_names[i] + config_name + '/successPacketCooked.csv')],
                        ignore_index=True
                    )
            success_count = df['successCnt'].sum()
            loss_ratio_list.append((1 - success_count / (len(arg_names) * expected_total_num_packets)) * 100)

        x = [int(j) for j in fr_names]
        ax.plot(x, loss_ratio_list, label=experiment_names[i], marker=markers[i], linestyle=linestyles[i], linewidth=3, markersize=10)
    
    ax.set_xlabel('Link failure rate (%)')
    ax.set_ylabel('Packet loss rate (%)')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    fig.savefig('./results/PDR under different fr.pdf', dpi=300, format='pdf')
    plt.close()


def drawEEDUnderDifferentFailureRate():
    plt.rcParams['axes.titlesize'] = 23
    plt.rcParams['axes.labelsize'] = 23
    plt.rcParams['xtick.labelsize'] = 23
    plt.rcParams['ytick.labelsize'] = 23
    plt.rcParams['legend.fontsize'] = 20
    fig, ax = plt.subplots()

    folder_names = []
    folder_names.append(root_dir + 'results_different_fr/withDD-withLoopPrevention-withoutLoadBalance/3/')
    # folder_names.append(root_dir + 'results_different_fr/withDD-withoutLoopPrevention-withoutLoadBalance/3/')
    folder_names.append(root_dir + 'results_different_fr/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/')

    experiment_names = ['n=3', 'OSPFL']

    markers = ['o', 'X', '^']
    linestyles = ['-', '--', 'dotted']

    for i in range(len(folder_names)):
        delay_list = []

        for fr in fr_names:
            arg_names = ["fail" + fr + "_test" + j for j in test_names]
            df = pandas.DataFrame()
            for config_name in arg_names:
                if df.empty:
                    df = pandas.read_csv(folder_names[i] + config_name + '/successPacketCooked.csv')
                else:
                    df = pandas.concat(
                        [df, pandas.read_csv(folder_names[i] + config_name + '/successPacketCooked.csv')],
                        ignore_index=True
                    )
            delay_list.append(df['avgDelay'].sum() / len(arg_names) * 1000) 

        x = [int(j) for j in fr_names]
        ax.plot(x, delay_list, label=experiment_names[i], marker=markers[i], linestyle=linestyles[i], linewidth=3, markersize=10)
    
    ax.set_xlabel('Link failure rate (%)')
    ax.set_ylabel('End-to-end delay (ms)')
    ax.set_ylim(bottom=0)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    fig.savefig('./results/EED under different fr.pdf', dpi=300, format='pdf')
    plt.close()


def drawOverheadunderDifferentFailureRate():
    plt.rcParams['axes.titlesize'] = 23
    plt.rcParams['axes.labelsize'] = 23
    plt.rcParams['xtick.labelsize'] = 23
    plt.rcParams['ytick.labelsize'] = 23
    plt.rcParams['legend.fontsize'] = 20
    fig, ax = plt.subplots()

    folder_names = []
    folder_names.append(root_dir + 'results_different_fr/withDD-withLoopPrevention-withoutLoadBalance/3/')
    # folder_names.append(root_dir + 'results_different_fr/withDD-withoutLoopPrevention-withoutLoadBalance/3/')
    folder_names.append(root_dir + 'results_different_fr/withDD-withoutLoopPrevention-withoutLoadBalance/OSPF/')

    experiment_names = ['n=3', 'OSPFL']

    markers = ['o', 'X', '^']
    linestyles = ['-', '--', 'dotted']

    for i in range(len(folder_names)):
        overhead_list = []

        for fr in fr_names:
            arg_names = ["fail" + fr + "_test" + j for j in test_names]
            df = pandas.DataFrame()
            for config_name in arg_names:
                if df.empty:
                    df = pandas.read_csv(folder_names[i] + config_name + '/controlOverhead.csv')
                else:
                    df = pandas.concat(
                        [df, pandas.read_csv(folder_names[i] + config_name + '/controlOverhead.csv')],
                        ignore_index=True
                    )
            overhead = df['LSUOverhead'].sum()
            overhead /= len(arg_names)
            overhead /= SIMULATION_DURATION_TIME
            overhead /= 1e6
            overhead /= 2
            overhead_list.append(overhead)

        x = [int(j) for j in fr_names]
        ax.plot(x, overhead_list, label=experiment_names[i], marker=markers[i], linestyle=linestyles[i], linewidth=3, markersize=10)
    
    ax.set_xlabel('Link failure rate (%)')
    ax.set_ylabel('Control Overhead (MBps)')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    fig.savefig('./results/Overhead under different fr.pdf', dpi=300, format='pdf')
    plt.close()


if __name__ == '__main__':
    
    # drawEEDUnderLightLoad()
    # drawPDRUnderLightLoad()
    # drawEEDUnderHeavyLoad()
    # drawPDRUnderHeavyLoad()
    drawPDRUnderDifferentFailureRate()
    drawEEDUnderDifferentFailureRate()
    drawOverheadunderDifferentFailureRate()

    pass
