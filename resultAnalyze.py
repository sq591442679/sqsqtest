import pandas
import matplotlib.pyplot
import numpy
from NEDGenerator import  deliverySrcIDs,deliveryDestID, SIMULATION_DURATION_TIME, send_interval
from command import arg_names, hops, parent_folder_names


markers = ['.', '^', 's', 'x', 'o', 's', 'h']
expected_total_num_packets = 1 / float(send_interval) * len(deliverySrcIDs) * SIMULATION_DURATION_TIME


def cookDropPacketRaw(folder_name:str, hop):
    with open(folder_name + 'dropPacketCooked.csv', 'w') as f:
        print('config', 'hop', 'noEntryCnt', 'stubCnt', 'loopCnt', 'queueCnt', 'total', file=f, sep=',')
        df = pandas.read_csv(folder_name + 'dropPacketRaw.csv')
        df = pandas.concat([df, pandas.read_csv(folder_name + 'queueDropPacketRaw.csv')], ignore_index=True)
        # line_cnt1 = df.shape[0]
        df = df.drop_duplicates()
        # print('duplicate lines:', df.shape[0] - line_cnt1)

        no_entry_count = df['isNoEntry'].sum()
        stub_cnt = df['isStub'].sum()
        loop_cnt = df['isLoop'].sum()
        queue_cnt = df['isQueue'].sum()
        total = no_entry_count + stub_cnt + loop_cnt + queue_cnt

        print(config_name, hop, no_entry_count, stub_cnt, loop_cnt, queue_cnt, total, file=f, sep=',')

    return total


def cookSuccessPacketRaw(folder_name:str, hop):
    with open(folder_name + 'successPacketCooked.csv', 'w') as f:
        # print(folder_name)
        print('config', 'hop', 'successCnt', 'avgDelay', file=f, sep=',')
        df = pandas.read_csv(folder_name + 'successPacketRaw.csv')

        df_success = df[(df['module'] == 'Network.ospfRouter_%d_%d' % (deliveryDestID.x, deliveryDestID.y)) \
                    & (df['delay'] > 0)]
        success_count = df_success.shape[0]
        df_eed = df[(df['module'] == 'Network.ospfRouter_%d_%d' % (deliveryDestID.x, deliveryDestID.y)) \
                    & (df['delay'] > 0)]['delay']
        avg_eed = df_eed.sum() / df_eed.shape[0]
        print(config_name, hop, success_count, avg_eed, file=f, sep=',')

    return success_count


def drawDropRatioPie(folder_name: str):
    df = pandas.DataFrame()
    for config_name in arg_names:
        if df.empty:
            df = pandas.read_csv(folder_name+ config_name + '/dropPacketCooked.csv')
        else:
            df = pandas.concat(
                [df, pandas.read_csv(folder_name + config_name + '/dropPacketCooked.csv')],
                ignore_index=True
            )
    
    no_entry_sum = 0
    loop_sum = 0
    queue_sum = 0

    for config_name in arg_names:
        df_config = df[df['config'] == config_name]
        no_entry_sum += df_config['noEntryCnt'].sum()
        loop_sum += df_config['loopCnt'].sum()
        queue_sum += df_config['queueCnt'].sum()
    
    no_entry_sum /= len(arg_names)
    loop_sum /= len(arg_names)
    queue_sum /= len(arg_names)
    total_sum = no_entry_sum + loop_sum + queue_sum

    if total_sum != 0:
        no_entry_ratio = no_entry_sum / total_sum
        loop_ratio = loop_sum / total_sum
        queue_ratio = queue_sum / total_sum

        labels = ['avg no entry=%.2f%%' % (no_entry_ratio * 100), 'avg loop=%.2f%%' % (loop_ratio * 100), 'avg queue=%.2f%%' % (queue_ratio * 100)]
        sizes = [no_entry_ratio, loop_ratio, queue_ratio]
        colors = ['lightblue', 'lightgreen', '#FFC0CB']

        explodes = [0.1, 0.1, 0.1]

        fig, ax = matplotlib.pyplot.subplots()
        ax.pie(sizes, labels=labels, colors=colors, 
            explode=explodes, startangle=45, wedgeprops=dict(width=0.4, edgecolor='w'))
        ax.axis('equal')
        ax.set_title('no-entry failure vs. loop failure vs. queue failure in n = ' + folder_name.split('/')[-2])
        matplotlib.pyplot.text(0, 0, 'avg dropped packet:\n' + str(total_sum), ha='center')
        fig.savefig(folder_name + 'dropRatioPie.png')
        matplotlib.pyplot.close()
    else:
        fig, ax = matplotlib.pyplot.subplots()
        ax.set_title('no-entry failure vs. loop failure in n = ' + folder_name.split('/')[-2])
        matplotlib.pyplot.text(0, 0, 'avg dropped packet:\n' + str(total_sum), ha='center')
        fig.savefig(folder_name + 'dropRatioPie.png')
        matplotlib.pyplot.close()


def getAvgPacketDeliveryRate(folder_name: str, expected_total_num_packets: int) -> float:
    df = pandas.DataFrame()

    for config_name in arg_names:
        if df.empty:
            df = pandas.read_csv(folder_name+ config_name + '/successPacketCooked.csv')
        else:
            df = pandas.concat(
                [df, pandas.read_csv(folder_name + config_name + '/successPacketCooked.csv')],
                ignore_index=True
            )
    success_count = df['successCnt'].sum()
    return success_count / (len(arg_names) * expected_total_num_packets)


def getAvgLSUOverhead(folder_name:str) -> float:
    df = pandas.DataFrame()
    for config_name in arg_names:
        if df.empty:
            df = pandas.read_csv(folder_name + config_name + '/controlOverhead.csv')
        else:
            df = pandas.concat(
                [df, pandas.read_csv(folder_name + config_name + '/controlOverhead.csv')],
                ignore_index=True
            )
    
    overhead = df['LSUOverhead'].sum()
    overhead /= len(arg_names)
    overhead /= SIMULATION_DURATION_TIME
    return overhead


def getAvgDelay(folder_name:str) -> float:
    df = pandas.DataFrame()
    for config_name in arg_names:
        if df.empty:
            df = pandas.read_csv(folder_name + config_name + '/successPacketCooked.csv')
        else:
            df = pandas.concat(
                [df, pandas.read_csv(folder_name + config_name + '/successPacketCooked.csv')],
                ignore_index=True
            )
    return df['avgDelay'].sum() / len(arg_names)


if __name__ == '__main__':
    for parent_folder_name in parent_folder_names:
        if 'withDD-withoutLoopPrevention-withoutLoadBalance' in parent_folder_name:
            hops.append('OSPF')
        else:
            if 'OSPF' in hops:
                hops.remove('OSPF')
        
        for hop in hops:
            total = 0
            for config_name in arg_names:
                folder_name = parent_folder_name + hop + '/' + config_name + '/'
                total_drop = cookDropPacketRaw(folder_name, hop)
                total_success = cookSuccessPacketRaw(folder_name, hop)
                total += total_success
                if total_drop + total_success < 0.85 * expected_total_num_packets:
                    print('----------drop & success not match in', folder_name, 'drop:', total_drop, 'success:', total_success, '----------')
            print(parent_folder_name + hop, "\'s loss ratio:", (1 - total / (expected_total_num_packets * len(arg_names))) * 100, '\%')

    # marker_index = 0
    # fig, ax = matplotlib.pyplot.subplots()
    # # ax2 = fig.add_axes([0.3, 0.3, 0.5, 0.3])
    # for parent_folder_name in parent_folder_names:

    #     if 'withDD-withoutLoopPrevention-withoutLoadBalance' in parent_folder_name:
    #         hops.append('OSPF')
    #     else:
    #         if 'OSPF' in hops:
    #             hops.remove('OSPF')

    #     avg_packet_delivery_failure_rates = []
    #     avg_control_overheads = []
    #     experiment_names = []      

    #     for hop in hops:
    #         folder_name = parent_folder_name + hop + '/'
    #         drawDropRatioPie(folder_name)
    #         experiment_name = hop
    #         experiment_names.append(experiment_name)
    #         avg_packet_delivery_failure_rates.append((1 - getAvgPacketDeliveryRate(folder_name, expected_total_num_packets)) * 100)
    #         avg_control_overheads.append(getAvgLSUOverhead(folder_name) / 1e6)

    #     # ax2.plot(avg_control_overheads, avg_packet_delivery_failure_rates, marker=markers[marker_index])
    #     # for i in range(len(avg_packet_delivery_failure_rates)):
    #     #     ax2.annotate(experiment_names[i], (avg_control_overheads[i], avg_packet_delivery_failure_rates[i]))
        
    #     # ax2.set_ylim([0.00, 0.4])
    #     # ax2.set_xlim(right=0.3)
    #     # ax2.set_xlabel('Avg. Control Overhead(MBps)')
    #     # ax2.set_ylabel('Avg. Packet Loss Rate(%)') 

    #     ax.plot(avg_control_overheads, avg_packet_delivery_failure_rates, 
    #             marker=markers[marker_index], label=parent_folder_name.split('/')[-2])
    #     marker_index += 1

    #     for i in range(len(avg_packet_delivery_failure_rates)):
    #         print(parent_folder_name, experiment_names[i], "'s packet loss: %.2f%%" % avg_packet_delivery_failure_rates[i])
    #         ax.annotate(experiment_names[i], (avg_control_overheads[i], avg_packet_delivery_failure_rates[i]))

    # ax.set_title('Avg. Packet Loss Rate & Control Overhead, link failure rate = 0.1')
    # ax.set_xlabel('Avg. Control Overhead(MBps)')
    # ax.set_ylabel('Avg. Packet Loss Rate(%)')
    # ax.set_ylim(bottom=0)
    # ax.legend(prop={'size': 8})
    # fig.savefig('./results/overhead and PDR.png', dpi=300)
    # matplotlib.pyplot.close()

    # marker_index = 0
    # fig, ax = matplotlib.pyplot.subplots()
    # for parent_folder_name in parent_folder_names:

    #     if 'withDD-withoutLoopPrevention-withoutLoadBalance' in parent_folder_name:
    #         hops.append('OSPF')
    #     else:
    #         if 'OSPF' in hops:
    #             hops.remove('OSPF')
        
    #     avg_control_overheads = []
    #     avg_delays = []
    #     experiment_names = []       

    #     for hop in hops:
    #         folder_name = parent_folder_name + hop + '/'
    #         drawDropRatioPie(folder_name)
    #         experiment_name = hop
    #         experiment_names.append(experiment_name)
    #         avg_control_overheads.append(getAvgLSUOverhead(folder_name) / 1e6)
    #         avg_delays.append(getAvgDelay(folder_name) * 1e3)
        
    #     # if parent_folder_name == './results/results_dis=6_fr=10_withDD-withoutLoopPrevention/':
    #     #     experiment_names.append('OSPF')
    #     #     avg_delays.append(getAvgDelay('./results/OSPF/') * 1e3)
    #     #     avg_control_overheads.append(getAvgLSUOverhead('./results/OSPF/') / 1e6)

    #     ax.plot(avg_control_overheads, avg_delays, 
    #             marker=markers[marker_index], label=parent_folder_name.split('/')[-2])
    #     marker_index += 1
        
    #     for i in range(len(avg_delays)):
    #         print(parent_folder_name, experiment_names[i], "'s EED:", avg_delays[i])
    #         ax.annotate(experiment_names[i], (avg_control_overheads[i], avg_delays[i]))
    
    # ideal_x = numpy.linspace(0, 1, 100)
    # ideal_y = numpy.full_like(ideal_x, 33.5)
    # ax.plot(ideal_x, ideal_y, linestyle='--')
    # ax.set_title('Avg. End to End Delay & Control Overhead, link failure rate = 0.1')
    # ax.set_xlabel('Avg. Control Overhead(MBps)')
    # ax.set_ylabel('Avg. End to End Delay(ms)')
    # ax.set_ylim(bottom=0)
    # ax.set_xlim(right=0.6)
    # matplotlib.pyplot.legend(prop={'size': 8})
    # fig.savefig('./results/overhead and EED.png', dpi=300)
    # matplotlib.pyplot.close()

    # for parent_folder_name in parent_folder_names:    

    #     if 'withDD-withoutLoopPrevention-withoutLoadBalance' in parent_folder_name:
    #         hops.append('OSPF')
    #     else:
    #         if 'OSPF' in hops:
    #             hops.remove('OSPF')

    #     avg_control_overheads = []
    #     experiment_names = []
    #     for hop in hops:
    #         folder_name = parent_folder_name + hop + '/'
    #         experiment_name = 'n=' + hop
    #         experiment_names.append(experiment_name)
    #         avg_control_overheads.append(getAvgLSUOverhead(folder_name))
    #     fig, ax = matplotlib.pyplot.subplots()
    #     ax.plot(hops, avg_control_overheads, marker='.')
    #     for i in range(len(experiment_names)):
    #         print(parent_folder_name, experiment_names[i], "'s LSU overhead:", avg_control_overheads[i])
    #         ax.annotate(experiment_names[i], (hops[i], avg_control_overheads[i]))
    #     fig.savefig(parent_folder_name + 'overhead on different hops', dpi=300)
    #     matplotlib.pyplot.close()
            