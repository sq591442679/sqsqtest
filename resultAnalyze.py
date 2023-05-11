import pandas
import matplotlib.pyplot
from NEDGenerator import deliverySrcID, deliveryDestID


folder_list = ['./results_n=1/', './results_n=2/', './results_n=3/', './results_n=4/', './results_n=5/', './results_OSPF/']
config_list = ['fail20_test%d' % i for i in range(1, 6)]


def cookDropPacketRaw(folder_name:str):
    with open(folder_name + 'dropPacketCooked.csv', 'w') as f:
        print('config', 'hop', 'noEntryCnt', 'stubCnt', 'loopCnt', 'total', file=f, sep=',')
        df = pandas.read_csv(folder_name + 'dropPacketRaw.csv')
        line_cnt1 = df.shape[0]
        df = df.drop_duplicates()
        print('duplicate lines:', df.shape[0] - line_cnt1)

        for config_name in config_list:
            no_entry_count = df[df['config'] == config_name]['isNoEntry'].sum()
            stub_cnt = df[df['config'] == config_name]['isStub'].sum()
            loop_cnt = df[df['config'] == config_name]['isLoop'].sum()
            total = no_entry_count + stub_cnt + loop_cnt
            hop = df['hop'].to_list()[0]

            print(config_name, hop, no_entry_count, stub_cnt, loop_cnt, total, file=f, sep=',')



def drawDropRatioPie(folder_name: str):
    df = pandas.read_csv(folder_name + 'dropPacketCooked.csv')
    no_entry_sum = 0
    loop_sum = 0

    for config_name in config_list:
        df_config = df[df['config'] == config_name]
        no_entry_sum += df_config['noEntryCnt'].sum()
        loop_sum += df_config['loopCnt'].sum()
    
    no_entry_sum /= len(config_list)
    loop_sum /= len(config_list)
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
            startangle=90, wedgeprops=dict(width=0.4, edgecolor='w'))
        ax.axis('equal')
        matplotlib.pyplot.text(0, 0, 'avg dropped packet=' + str(total_sum), ha='center')
        fig.savefig(folder_name + 'dropRatioPie.png')
        matplotlib.pyplot.close()


def getAvgPacketDeliveryRate(folder_name: str) -> float:
    df = pandas.read_csv(folder_name + 'successPacket.csv')
    success_count = 0
    for config_name in config_list:
        success_count += df[(df['module'] == 'Network.ospfRouter_%d_%d' % (deliveryDestID.x, deliveryDestID.y)) \
                        & (df['config'] == config_name) \
                        & (df['avgDelay'] > 0)]['packetCnt'].to_list()[0]
    success_count /= (len(config_list) * 1000)
    return success_count


def getAvgControlOverhead(folder_name:str) -> float:
    df = pandas.read_csv(folder_name + 'controlOverhead.csv')
    overhead = 0
    for config_name in config_list:
        overhead += df[df['config'] == config_name]['total'].sum()
    overhead /= len(config_list)
    return overhead


if __name__ == '__main__':
    avg_packet_delivery_failure_rates = []
    avg_control_overheads = []
    experiment_names = []
    # drawDropRatioPie()
    # cookDropPacketRaw('./results/')
    # drawDropRatioPie('./results/')
    for folder_name in folder_list:
        experiment_name = folder_name.split('_')[-1][:-1]
        experiment_names.append(experiment_name)
        avg_packet_delivery_failure_rates.append(1 - getAvgPacketDeliveryRate(folder_name))
        avg_control_overheads.append(getAvgControlOverhead(folder_name))

    fig, ax = matplotlib.pyplot.subplots()
    ax.plot(avg_control_overheads, avg_packet_delivery_failure_rates, 
            marker='.', label='with loop avoidance, link failure rate = 0.2')
    for i in range(len(avg_packet_delivery_failure_rates)):
        ax.annotate(experiment_names[i], (avg_control_overheads[i], avg_packet_delivery_failure_rates[i]))
    ax.set_title('Avg. Packet Delivery Failure Rate & Control Overhead \n on Different Mechanisms, End-to-end Hop = 3')
    ax.set_xlabel('Avg. Control Overhead(Bytes)')
    ax.set_ylabel('Avg. Packet Delivery Failure Rate')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.show()
            