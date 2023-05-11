import pandas
import matplotlib.pyplot

folder_list = ['./results_n=1', './results_n=2', './results_n=3', './results_n=4', './results_n=5', './results_OSPF']
config_list = ['fail20_test%d' % i for i in range(1, 6)]

if __name__ == '__main__':
    print(config_list)
    for folder in folder_list:
        df = pandas.read_csv(folder + '/dropPacket.csv')
        for config_name in config_list:
            df_config = df[df['config'] == config_name]
            no_entry_sum = df_config['noEntryCnt'].sum()
            loop_sum = df_config['loopCnt'].sum()
            total_sum = no_entry_sum + loop_sum
            no_entry_ratio = no_entry_sum / total_sum
            loop_ratio = loop_sum / total_sum

            labels = ['no entry', 'loop']
            sizes = [no_entry_ratio, loop_ratio]
            colors = ['lightblue', 'lightgreen']
            explode = [0.1, 0]
            fig, ax = matplotlib.pyplot.subplots()
            ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            matplotlib.pyplot.show()