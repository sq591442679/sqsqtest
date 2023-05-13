import pandas
import matplotlib.pyplot
from NEDGenerator import deliveryDestID
from command import arg_names

hops = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
# folder_list = ['./results_n=1/', './results_n=2/','./results_n=3/', './results_n=5/', './results_OSPF/']


def cookDropPacketRaw(folder_name:str):
    with open(folder_name + 'dropPacketCooked.csv', 'w') as f:
        print('config', 'hop', 'noEntryCnt', 'stubCnt', 'loopCnt', 'total', file=f, sep=',')
        df = pandas.read_csv(folder_name + 'dropPacketRaw.csv')
        line_cnt1 = df.shape[0]
        df = df.drop_duplicates()
        print('duplicate lines:', df.shape[0] - line_cnt1)

        no_entry_count = df['isNoEntry'].sum()
        stub_cnt = df['isStub'].sum()
        loop_cnt = df['isLoop'].sum()
        total = no_entry_count + stub_cnt + loop_cnt
        hop = folder_name.split('/')[2]

        print(config_name, hop, no_entry_count, stub_cnt, loop_cnt, total, file=f, sep=',')


def cookSuccessPacketRaw(folder_name:str):
    with open(folder_name + 'successPacketCooked.csv', 'w') as f:
        print('config', 'hop', 'successCnt', 'avgDelay', file=f, sep=',')
        df = pandas.read_csv(folder_name + 'successPacketRaw.csv')

        df_success = df[(df['module'] == 'Network.ospfRouter_%d_%d' % (deliveryDestID.x, deliveryDestID.y)) \
                    & (df['delay'] > 0)]
        success_count = df_success.shape[0]
        df_eed = df[(df['module'] == 'Network.ospfRouter_%d_%d' % (deliveryDestID.x, deliveryDestID.y)) \
                    & (df['delay'] > 0)]['delay']
        avg_eed = df_eed.sum() / df_eed.shape[0]
        hop = folder_name.split('/')[2]
        print(config_name, hop, success_count, avg_eed, file=f, sep=',')


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

    for config_name in arg_names:
        df_config = df[df['config'] == config_name]
        no_entry_sum += df_config['noEntryCnt'].sum()
        loop_sum += df_config['loopCnt'].sum()
    
    no_entry_sum /= len(arg_names)
    loop_sum /= len(arg_names)
    total_sum = no_entry_sum + loop_sum

    if total_sum != 0:
        no_entry_ratio = no_entry_sum / total_sum
        loop_ratio = loop_sum / total_sum
        labels = ['avg no entry=' + str(no_entry_sum), 'avg loop=' + str(loop_sum)]
        sizes = [no_entry_ratio, loop_ratio]
        colors = ['lightblue', 'lightgreen']
        explode = [0.1, 0]
        fig, ax = matplotlib.pyplot.subplots()
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', 
            startangle=45, wedgeprops=dict(width=0.4, edgecolor='w'))
        ax.axis('equal')
        ax.set_title('no-entry failure vs. loop failure in n = ' + folder_name.split('/')[-2])
        matplotlib.pyplot.text(0, 0, 'avg dropped packet:\n' + str(total_sum), ha='center')
        fig.savefig(folder_name + 'dropRatioPie.png')
        matplotlib.pyplot.close()
    else:
        fig, ax = matplotlib.pyplot.subplots()
        ax.set_title('no-entry failure vs. loop failure in n = ' + folder_name.split('/')[-2])
        matplotlib.pyplot.text(0, 0, 'avg dropped packet:\n' + str(total_sum), ha='center')
        fig.savefig(folder_name + 'dropRatioPie.png')
        matplotlib.pyplot.close()


def getAvgPacketDeliveryRate(folder_name: str) -> float:
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

    return success_count / (len(arg_names) * 1000)


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
    return overhead


if __name__ == '__main__':
    avg_packet_delivery_failure_rates = []
    avg_control_overheads = []
    experiment_names = []

    for hop in hops:
        for config_name in arg_names:
            folder_name = './results/' + hop + '/' + config_name + '/'
            cookDropPacketRaw(folder_name)
            cookSuccessPacketRaw(folder_name)
            
    
    for hop in hops:
        folder_name = './results/' + hop + '/'
        drawDropRatioPie(folder_name)
        experiment_name = 'n=' + hop
        experiment_names.append(experiment_name)
        avg_packet_delivery_failure_rates.append(1 - getAvgPacketDeliveryRate(folder_name))
        avg_control_overheads.append(getAvgLSUOverhead(folder_name))

    fig, ax = matplotlib.pyplot.subplots()
    ax.plot(avg_control_overheads, avg_packet_delivery_failure_rates, 
            marker='.', label='with loop avoidance, link failure rate = 0.1')
    for i in range(len(avg_packet_delivery_failure_rates)):
        print(experiment_names[i], "'s PDR:", 1 - avg_packet_delivery_failure_rates[i])
        ax.annotate(experiment_names[i], (avg_control_overheads[i], avg_packet_delivery_failure_rates[i]))
    ax.set_title('Avg. Packet Delivery Failure Rate & Control Overhead \n on Different Mechanisms, End-to-end Hop = 5')
    ax.set_xlabel('Avg. Control Overhead(Bytes)')
    ax.set_ylabel('Avg. Packet Delivery Failure Rate')
    ax.set_ylim([0.0, 0.02])
    matplotlib.pyplot.legend()
    fig.savefig('./results/overhead and PDR.png')
    matplotlib.pyplot.close()

    fig, ax = matplotlib.pyplot.subplots()
    ax.plot(hops, avg_control_overheads, marker='.')
    for i in range(len(avg_packet_delivery_failure_rates)):
        print(experiment_names[i], "'s LSU overhead:", avg_control_overheads[i])
        ax.annotate(experiment_names[i], (hops[i], avg_control_overheads[i]))
    fig.savefig('./results/overhead on different hops')
    matplotlib.pyplot.close()
            