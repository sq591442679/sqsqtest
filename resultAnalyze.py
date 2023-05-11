import pandas
import matplotlib.pyplot
from NEDGenerator import deliverySrcID, deliveryDestID


folder_list = ['./results_n=1/', './results_n=2/', './results_n=3/', './results_n=4/', './results_n=5/', './results_OSPF/']
config_list = ['fail20_test%d' % i for i in range(1, 6)]


def cookDropPacketRaw():
    

def drawDropRatioPie():
    for folder in folder_list:
        df = pandas.read_csv(folder + 'dropPacket.csv')
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
            fig.savefig(folder + 'dropRatioPie.png')
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
    # drawDropRatioPie()
    for folder_name in folder_list:
        print(getAvgPacketDeliveryRate(folder_name))
        print(getAvgControlOverhead(folder_name))

            