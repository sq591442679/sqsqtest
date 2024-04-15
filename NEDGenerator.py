import math
from xml.etree import ElementTree as et
import xml.dom.minidom
import numpy
import os
import shutil
from typing import List, Dict, Tuple, Set

X = 11  # 行 即每个轨道上的卫星数量
Y = 6  # 列 即轨道数
WARMUP_PERIOD = 20  # 热身期，要确保在此时间之前链路连接状况不变
SIMULATION_END_TIME = 120
SIMULATION_DURATION_TIME = SIMULATION_END_TIME - WARMUP_PERIOD
LINK_DOWN_DURATION = 5  # 链路故障的持续时间 单位秒
LINK_DISCONNECT_TYPE = 0
LINK_RECONNECT_TYPE = 1
NUM_OF_TESTS = 50  # for each link failure rate, run NUM_OF_TESTS times

H = 780000  # 轨道高度780千米
R = 6371004  # 地球半径6371.004千米
C = 3e8  # 光速
POLAR_RING = math.radians(66.34)  # 极圈纬度
ISLDelay = {}  # 轨间链路组号(0表示轨内链路) -> 时延(s)


class SatelliteID:
    """
    卫星的编号，由轨道号和轨内编号组成
    """

    def __init__(self, x: int, y: int):
        """
        :param x: 行号(轨内编号)  y: 列号(轨道号)
        """
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, SatelliteID) and self.x == other.x and self.y == other.y

    def __str__(self):
        return "satellite id: " + str((self.x, self.y))

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def getNeighborOnDirection(self, direction: int):
        """
        返回该编号在对应方向上"理论上的"的邻居编号，注意这时默认全连通
        """
        if direction == 0:
            return SatelliteID(rescale(self.x - 1, X), self.y)
        elif direction == 1:
            return SatelliteID(rescale(self.x + 1, X), self.y)
        elif direction == 2:
            return SatelliteID(self.x, rescale(self.y - 1, Y))
        elif direction == 3:
            return SatelliteID(self.x, rescale(self.y + 1, Y))
        else:
            raise Exception('invalid direction!')

    def getDirectionOfNeighbor(self, neighborSatelliteID) -> int:
        """
        返回自身到对应邻居之间的方向，注意这时默认全连通
        """
        if not isinstance(neighborSatelliteID, SatelliteID):
            raise Exception('parameter is not a SatelliteID!')
        else:
            if self.x == neighborSatelliteID.x:  # 相同纬度
                if neighborSatelliteID.y == rescale(self.y + 1, Y):  # neighbor在右侧
                    return 3
                elif neighborSatelliteID.y == rescale(self.y - 1, Y):  # neighbor在左侧
                    return 2
                else:
                    raise Exception("self and param are not neighbors!")
            elif self.y == neighborSatelliteID.y:  # 相同经度
                if neighborSatelliteID.x == rescale(self.x + 1, X):  # neighbor在下侧
                    return 1
                elif neighborSatelliteID.x == rescale(self.x - 1, X):  # neighbor在上侧
                    return 0
                else:
                    raise Exception("self and param are not neighbors!")
            else:
                raise Exception("self and param are not neighbors!")


class Ipv4Address:
    def __init__(self, ip1: int, ip2: int, ip3: int, ip4: int) -> None:
        self.ip1 = ip1
        self.ip2 = ip2
        self.ip3 = ip3
        self.ip4 = ip4

    def getNeighboringInterfaceIPAddress(self):
        if self.ip4 == 1:
            return Ipv4Address(self.ip1, self.ip2, self.ip3, 2)
        else:
            return Ipv4Address(self.ip1, self.ip2, self.ip3, 1)
        
    def __str__(self) -> str:
        return "%d.%d.%d.%d" % (self.ip1, self.ip2, self.ip3, self.ip4)
    
    def __hash__(self) -> int:
        return hash((self.ip1, self.ip2, self.ip3, self.ip4))
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Ipv4Address) and self.ip1 == other.ip1 \
            and self.ip2 == other.ip2 and self.ip3 == other.ip3 and self.ip4 == other.ip4
    
    def __lt__(self, other):
        return (self.ip1, self.ip2, self.ip3, self.ip4) < (other.ip1, other.ip2, other.ip3, other.ip4)
        


class DirectionalInterSatelliteLink:
    """
    单向的星间链路
    """

    def __init__(self, srcSatelliteID: SatelliteID, destSatelliteID: SatelliteID, interfaceIPAddr: Ipv4Address):
        self.srcSatelliteID = srcSatelliteID
        self.destSatelliteID = destSatelliteID
        self.delay = 0x3f3f3f3f
        self.interfaceIPAddr = interfaceIPAddr
        self.failureTimeArray = []  # 记录该链路分别在哪些时间故障，每次故障的持续时间是LINK_DISCONNECT_DURATION
        if srcSatelliteID.getDirectionOfNeighbor(destSatelliteID) == 0 or \
                srcSatelliteID.getDirectionOfNeighbor(destSatelliteID) == 1:
            self.delay = ISLDelay[0]
        elif srcSatelliteID.getDirectionOfNeighbor(destSatelliteID) == 2 or \
                srcSatelliteID.getDirectionOfNeighbor(destSatelliteID) == 3:
            self.delay = ISLDelay[self.srcSatelliteID.x]

    def __str__(self):
        return self.srcSatelliteID.__str__() + ' --> ' + self.destSatelliteID.__str__()

    def __eq__(self, other):
        if not isinstance(other, DirectionalInterSatelliteLink):
            raise Exception('')
        return self.srcSatelliteID == other.srcSatelliteID and self.destSatelliteID == other.destSatelliteID
    
    def __lt__(self, other):
        if self.srcSatelliteID.__eq__(other.srcSatelliteID):
            return self.destSatelliteID.__lt__(other.destSatelliteID)
        else:
            return self.srcSatelliteID.__lt__(other.srcSatelliteID)

    def __hash__(self):
        return hash((self.srcSatelliteID.x, self.srcSatelliteID.y, self.destSatelliteID.x, self.destSatelliteID.y))

    def generateBackwardLink(self):
        return DirectionalInterSatelliteLink(self.destSatelliteID, self.srcSatelliteID, self.interfaceIPAddr.getNeighboringInterfaceIPAddress())


class ScenarioEvent:
    """
    描述链路断开或恢复事件，包含开始时间与结束时间
    """

    def __init__(self, link: DirectionalInterSatelliteLink, eventType: int, beginTime: float):
        """
        :param link: 该事件相关的单向链路
        :param eventType=1: 链路断开  eventType=2: 链路恢复
        """
        if eventType != LINK_DISCONNECT_TYPE and eventType != LINK_RECONNECT_TYPE:
            raise Exception('')
        self.link = link
        self.beginTime = beginTime
        self.eventType = eventType

    def __lt__(self, other):
        if not isinstance(other, ScenarioEvent):
            raise Exception('')
        else:
            return self.beginTime < other.beginTime

    def __str__(self):
        event = 'disconnect' if self.eventType == LINK_DISCONNECT_TYPE else 'reconnect'
        return 'link ' + self.link.__str__() + ' and its backward link ' + event + ' at ' + str(self.beginTime)

    def __eq__(self, other):
        if not isinstance(other, ScenarioEvent):
            raise Exception('')
        return self.link.__eq__(other.link) and self.eventType == other.eventType and self.beginTime == other.beginTime

    def __hash__(self):
        return hash({self.link, self.beginTime, self.eventType})


allISLSet: Set[DirectionalInterSatelliteLink] = set()

# send_interval = "0.002"
# deliverySrcIDs = [SatelliteID(6, 5), SatelliteID(7, 5), SatelliteID(8, 5), SatelliteID(9, 5)]

send_interval = "0.01"
deliverySrcIDs = [SatelliteID(9, 3)]

deliveryDestID = SatelliteID(5, 5)


# 其中的每个元素都是DirectionalInterSatelliteLink, 存储着卫星网络中所有的ISL  注意双向都保存


def rescale(num, NUM):
    if 0 < num <= NUM:
        return num
    elif num > NUM:
        return num % NUM
    else:
        return num + NUM


def generateISLDelay():
    # 假设ospfRouter_1_1, ..., ospfRouter_1_6都在80.N
    pi = math.pi
    latitude = math.radians(10)  # 以地心为原点，北极轴为正方向的角度
    delta_latitude = 2 * pi / X
    delta_altitude = 2 * pi / Y

    ISLDelay[0] = 2 * (H + R) * math.sin(delta_latitude / 2) / C  # 轨内链路
    for x in range(1, X + 1):
        # if abs(latitude - 0) <= pi / 2 - POLAR_RING or abs(latitude - pi) <= pi / 2 - POLAR_RING \
        #         or abs(latitude - 2 * pi) <= pi / 2 - POLAR_RING:  # 在极区内
        #     ISLDelay[x] = 0x3f3f3f3f
        # else:
        #     ISLDelay[x] = (H + R) * abs(math.sin(latitude)) * math.sin(delta_altitude / 2) / C
        ISLDelay[x] = 2 * (H + R) * abs(math.sin(latitude)) * math.sin(delta_altitude / 2) / C
        latitude += delta_latitude


def generateLinks():
    # 生成连接
    cnt = 0
    for x in range(1, X + 1):
        for y in range(1, Y + 1):
            # ethg[0~3]分别对应上下左右
            if ISLDelay[x] < 1:  # 轨间链路存在
                allISLSet.add(DirectionalInterSatelliteLink(SatelliteID(x, y), SatelliteID(x, rescale(y + 1, Y)), Ipv4Address(192, 168, cnt, 1)))
                allISLSet.add(DirectionalInterSatelliteLink(SatelliteID(x, rescale(y + 1, Y)), SatelliteID(x, y), Ipv4Address(192, 168, cnt, 2)))
                # 与其右边的建立双向连接
            cnt += 1
            allISLSet.add(DirectionalInterSatelliteLink(SatelliteID(x, y), SatelliteID(rescale(x + 1, X), y), Ipv4Address(192, 168, cnt, 1)))
            allISLSet.add(DirectionalInterSatelliteLink(SatelliteID(rescale(x + 1, X), y), SatelliteID(x, y), Ipv4Address(192, 168, cnt, 2)))
            cnt += 1
            # 与其下边的建立双向连接


def buildNEDFile():
    with open('./sqsqtest.ned', 'w') as f:
        dependency = [
            'package inet.examples.ospfv2.sqsqtest;',
            'import inet.common.misc.ThruputMeteringChannel;',
            'import inet.common.scenario.ScenarioManager;',
            'import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;'
        ]
        for _ in dependency:
            print(_, file=f)

        print('', file=f)

        for i in ISLDelay.keys():
            if ISLDelay[i] < 1:
                print('channel ISL%d extends ThruputMeteringChannel' % i, file=f)
                print('{', file=f)
                print('\tdelay = %fs;' % ISLDelay[i], file=f)
                print('\tdatarate = 10Mbps;', file=f)
                print('\tthruputDisplayFormat = \"#N\";', file=f)
                print('}', file=f)

        print('network Network', file=f)
        print('{', file=f)
        print('\t@display("bgb=1024,1400");', file=f)

        print('', file=f)

        print('\tsubmodules:', file=f)
        print('\t\tconfigurator: Ipv4NetworkConfigurator {', file=f)
        print('\t\t\tparameters:', file=f)
        print('\t\t\t\tconfig = xmldoc(\"sqsqNetworkConfig.xml\");', file=f)
        print('\t\t\t\taddStaticRoutes = false;', file=f)
        print('\t\t\t\taddDefaultRoutes = false;', file=f)
        print('\t\t\t\t@display("p=50,100;is=s");', file=f)
        print('\t\t}', file=f)
        print('\t\tscenarioManager: ScenarioManager {', file=f)
        print('\t\t\t@display("p=50,200;is=s");', file=f)
        print('\t\t}', file=f)

        # 生成路由器名单
        for x in range(1, X + 1):
            for y in range(1, Y + 1):
                print("\t\tospfRouter_%d_%d: SqsqRouter {" % (x, y), file=f)
                print("\t\t\t@display(\"p=%d,%d\");" % (100 + 120 * y, 120 * x), file=f)
                print("\t\t\thasStatus = true;", file=f)
                print("\t\t\tipv4.routingTable.routerId = \"0.0.%d.%d\";" % (x, y), file=f)
                print("\t\t\tgates:", file=f)
                print("\t\t\t\tethg[4];", file=f)
                print("\t\t}", file=f)

        # 生成连接
        print('\tconnections:', file=f)
        f2 = open('channel.xml', 'a')
        for x in range(1, X + 1):
            for y in range(1, Y + 1):
                # ethg[0~3]分别对应上下左右
                if ISLDelay[x] < 1:  # 轨间链路存在
                    print("\t\tospfRouter_%d_%d.ethg[%d] <--> ISL%d <--> ospfRouter_%d_%d.ethg[%d];" % (
                        x, y, 3, x, x, rescale(y + 1, Y), 2), file=f)
                    src_module = f"ospfRouter_{x}_{y}"
                    dest_module = f"ospfRouter_{x}_{rescale(y + 1, Y)}"
                    src_gate = "ethg[3]"
                    dest_gate = "ethg[2]"
                    print(f"<SatToSat src-module='{src_module}' src-gate='{src_gate}' dest-module='{dest_module}' dest-gate='{dest_gate}' "
                          f"channel-type='masterNodes.OsgEarthNet.SatToSat_10Mbps' link-info='inter-orbit' />",
                          file=f2)
                    # 与其右边的建立双向连接
                print("\t\tospfRouter_%d_%d.ethg[%d] <--> ISL0 <--> ospfRouter_%d_%d.ethg[%d];" % (
                    x, y, 1, rescale(x + 1, X), y, 0), file=f)
                src_module = f"ospfRouter_{x}_{y}"
                dest_module = f"ospfRouter_{rescale(x + 1, X)}_{y}"
                src_gate = "ethg[1]"
                dest_gate = "ethg[0]"
                print(f"<SatToSat src-module='{src_module}' src-gate='{src_gate}' dest-module='{dest_module}' dest-gate='{dest_gate}' "
                      f"channel-type='masterNodes.OsgEarthNet.SatToSat_10Mbps' link-info='intra-orbit' />",
                      file=f2)
                # 与其下边的建立双向连接

        print('}', file=f)


def buildNetworkConfigFile():
    """
    生成网络配置文件，配置各个网络的地址
    :return: void
    """
    interface_address_by_router_id: Dict[Tuple[int, int], List[Ipv4Address]] = {}  # router id -> ip addresses of its interfaces, order by up 
    for x in range(1, X + 1):
        for y in range(1, Y + 1):
            interface_address_by_router_id[(x, y)] = []
    router_id_by_interface_address: Dict[Ipv4Address, Tuple[int, int]] = {}

    root = et.Element('config')
    for x in range(1, X + 1):
        for y in range(1, Y + 1):
            link_list = [
                DirectionalInterSatelliteLink(SatelliteID(x, y), SatelliteID(rescale(x - 1, X), y), Ipv4Address(0, 0, 0, 0)),  # upper neighbor
                DirectionalInterSatelliteLink(SatelliteID(x, y), SatelliteID(rescale(x + 1, X), y), Ipv4Address(0, 0, 0, 0)),  # lower neighbor
                DirectionalInterSatelliteLink(SatelliteID(x, y), SatelliteID(x, rescale(y - 1, Y)), Ipv4Address(0, 0, 0, 0)),  # left neighbor
                DirectionalInterSatelliteLink(SatelliteID(x, y), SatelliteID(x, rescale(y + 1, Y)), Ipv4Address(0, 0, 0, 0))  # right neighbor
            ]
            for link in link_list:
                from_x, from_y, to_x, to_y = link.srcSatelliteID.x, link.srcSatelliteID.y, link.destSatelliteID.x, link.destSatelliteID.y
                
                if link in allISLSet:
                    interfaceAddr = Ipv4Address(0, 0, 0, 0)
                    for tmp_link in allISLSet:
                        if tmp_link.__eq__(link):
                            interfaceAddr = tmp_link.interfaceIPAddr
                    et.SubElement(root, 'interface', attrib={
                        'hosts': 'ospfRouter_%d_%d' % (from_x, from_y),
                        'towards': 'ospfRouter_%d_%d' % (to_x, to_y),
                        'address': interfaceAddr.__str__(),
                        'netmask': '255.255.255.0'
                    })
                    interface_address_by_router_id[(x, y)].append(interfaceAddr)
                    router_id_by_interface_address[interfaceAddr] = (x, y)
                
            
    xml_str = et.tostring(root, encoding='utf-8')
    xml_pretty_str = xml.dom.minidom.parseString(xml_str).toprettyxml()
    with open('./sqsqNetworkConfig.xml', 'w') as f:
        f.write(xml_pretty_str)


    print('--------------------------------')
    for x in range(1, X + 1):
        for y in range(1, Y + 1):
            print(
                '{Ipv4Address(0, 0, %d, %d), {Ipv4Address(%d, %d, %d, %d), Ipv4Address(%d, '
                '%d, %d, %d), Ipv4Address(%d, %d, %d, %d), Ipv4Address(%d, %d, %d, %d)}},'
                % (x, y, 
                    interface_address_by_router_id[(x, y)][0].ip1, 
                    interface_address_by_router_id[(x, y)][0].ip2,
                    interface_address_by_router_id[(x, y)][0].ip3,
                    interface_address_by_router_id[(x, y)][0].ip4,
                    interface_address_by_router_id[(x, y)][1].ip1, 
                    interface_address_by_router_id[(x, y)][1].ip2,
                    interface_address_by_router_id[(x, y)][1].ip3,
                    interface_address_by_router_id[(x, y)][1].ip4,
                    interface_address_by_router_id[(x, y)][2].ip1, 
                    interface_address_by_router_id[(x, y)][2].ip2,
                    interface_address_by_router_id[(x, y)][2].ip3,
                    interface_address_by_router_id[(x, y)][2].ip4,
                    interface_address_by_router_id[(x, y)][3].ip1, 
                    interface_address_by_router_id[(x, y)][3].ip2,
                    interface_address_by_router_id[(x, y)][3].ip3,
                    interface_address_by_router_id[(x, y)][3].ip4))


    print('--------------------------------')
    sorted_router_id_by_interface_address = sorted(router_id_by_interface_address)
    for key in sorted_router_id_by_interface_address:
        print('{Ipv4Address(%d, %d, %d, %d), Ipv4Address(0, 0, %d, %d)},' % 
              (key.ip1, key.ip2, key.ip3, key.ip4, router_id_by_interface_address[key][0], router_id_by_interface_address[key][1]))


def buildASConfigFile(by_hop=False):
    """
    生成AS配置文件  主要是配置区域和路由器的接口以及ospf cost
    :return: void
    """
    root = et.Element('OSPFASConfig', attrib={
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsi:schemaLocation': 'OSPF.xsd'
    })
    area = et.SubElement(root, 'Area', attrib={
        'id': '0.0.0.0'
    })
    for x in range(1, X + 1):
        for y in range(1, Y + 1):
            for i in range(0, 4):
                if (i == 2 or i == 3) and ISLDelay[x] > 1:
                    continue
                et.SubElement(area, 'AddressRange', attrib={
                    'address': 'ospfRouter_%d_%d%%eth%d' % (x, y, i),
                    'mask': 'ospfRouter_%d_%d%%eth%d' % (x, y, i)
                })
    for x in range(1, X + 1):
        for y in range(1, Y + 1):
            router = et.SubElement(root, 'Router', attrib={
                'name': 'ospfRouter_%d_%d' % (x, y),
                'RFC1583Compatible': 'true'
            })
            if not by_hop:
                for i in range(0, 4):
                    if i == 0 or i == 1:  # 上 下
                        et.SubElement(router, 'PointToPointInterface', attrib={
                            'ifName': 'eth%d' % i,
                            'areaID': '0.0.0.0',
                            'interfaceOutputCost': str(round(ISLDelay[0] * 10000))  # 注意ospfcost应为整数
                        })
                    elif ISLDelay[x] < 1:
                        et.SubElement(router, 'PointToPointInterface', attrib={
                            'ifName': 'eth%d' % i,
                            'areaID': '0.0.0.0',
                            'interfaceOutputCost': str(round(ISLDelay[x] * 10000))
                        })
            if (by_hop):
                for i in range(0, 4):
                    if i == 0 or i == 1:  # 上 下
                        et.SubElement(router, 'PointToPointInterface', attrib={
                            'ifName': 'eth%d' % i,
                            'areaID': '0.0.0.0',
                            'interfaceOutputCost': '1' 
                        })
                    elif ISLDelay[x] < 1:
                        et.SubElement(router, 'PointToPointInterface', attrib={
                            'ifName': 'eth%d' % i,
                            'areaID': '0.0.0.0',
                            'interfaceOutputCost': '1'
                        })
            

    xml_str = et.tostring(root, encoding='utf-8')
    xml_pretty_str = xml.dom.minidom.parseString(xml_str).toprettyxml()
    with open('./sqsqASConfig.xml', 'w') as f:
        f.write(xml_pretty_str)


def buildScenarioFile(link_failure_rate: float, file_name: str):
    """
    生成剧本文件
    :param link_failure_rate: 对任一链路，其故障时间占总时间的比例的期望
    """
    events: list[ScenarioEvent] = []

    if link_failure_rate > 1e-6:
        poisson_lambda = link_failure_rate / (LINK_DOWN_DURATION * (1 - link_failure_rate))
        # 链路故障次数的期望，假设其服从泊松分布，则两次故障之间的时间间隔服从指数分布
        exponential_lambda = 1 / poisson_lambda
        link: DirectionalInterSatelliteLink
        for link in allISLSet:
            if link.__lt__(link.generateBackwardLink()):

                isKeyLink = False
                for deliverySrcID in deliverySrcIDs:
                    if (
                            (link.srcSatelliteID.__eq__(deliverySrcID) and link.destSatelliteID.__eq__(deliverySrcID.getNeighborOnDirection(0))) \
                        or  (link.destSatelliteID.__eq__(deliverySrcID) and link.srcSatelliteID.__eq__(deliverySrcID.getNeighborOnDirection(0))) \
                        or  (link.srcSatelliteID.__eq__(deliveryDestID) and link.destSatelliteID.__eq__(deliveryDestID.getNeighborOnDirection(0))) \
                        or  (link.destSatelliteID.__eq__(deliveryDestID) and link.srcSatelliteID.__eq__(deliveryDestID.getNeighborOnDirection(0)))
                    ):
                        isKeyLink = True
                if isKeyLink == True:
                    continue

                event_time: float = WARMUP_PERIOD
                while event_time <= SIMULATION_END_TIME:
                    event_time_interval = numpy.random.exponential(scale=exponential_lambda, size=1)[0]
                    event_time += event_time_interval
                    if event_time <= SIMULATION_END_TIME:
                        events.append(ScenarioEvent(link, LINK_DISCONNECT_TYPE, event_time))
                        event_time += LINK_DOWN_DURATION
                        if event_time <= SIMULATION_END_TIME:
                            events.append(ScenarioEvent(link, LINK_RECONNECT_TYPE, event_time))
    events.sort()

    # check_time_list = []
    # for i in range(100):
    #     check_time_list.append(random.uniform(WARMUP_PERIOD, SIMULATION_END_TIME))
    # # print(check_time_list)
    # avg = 0.0
    # for check_time in check_time_list:
    #     cnt = 0
    #     for event in events:
    #         if event.eventType == LINK_DISCONNECT_TYPE and \
    #                 event.beginTime <= check_time <= event.beginTime + LINK_DOWN_DURATION:
    #             cnt += 1
    #     avg += cnt
    #     # print(cnt)
    # if len(check_time_list) != 0:
    #     avg /= len(check_time_list)
    # print("avg number of disconnected links at any time: ", avg)
    # time_map = {}
    # for event in events:
    #     if event.link not in time_map.keys() and event.link.generateBackwardLink() not in time_map.keys():
    #         time_map[event.link] = 0
    # for event in events:
    #     if event.eventType == LINK_DISCONNECT_TYPE:
    #         if event.link in time_map.keys():
    #             time_map[event.link] += LINK_DOWN_DURATION
    #         else:
    #             time_map[event.link.generateBackwardLink()] += LINK_DOWN_DURATION
    # avg = 0.0
    # for key in time_map.keys():
    #     avg += time_map[key]
    # if len(time_map) != 0:
    #     avg /= len(time_map)
    # print("avg duration of link-down-time for a single link: ", avg)

    # for event in events:
    #     if event.eventType == LINK_DISCONNECT_TYPE:
    #         if (event.link.srcSatelliteID.__eq__(deliverySrcID) and event.link.destSatelliteID.__eq__(deliveryDestID.getNeighborOnDirection(0))) \
    #             or (event.link.srcSatelliteID.__eq__(deliveryDestID) or event.link.destSatelliteID.__eq__(deliverySrcID)):
    #             print(event.link.__str__())

    root = et.Element('scenario')
    for event in events:
        # if link_failure_rate == 0.16:
        #     print(event.__str__())
        at = et.SubElement(root, 'at', attrib={
            't': ('%.3f' % event.beginTime) + 's'
        })
        if event.eventType == LINK_DISCONNECT_TYPE:
            et.SubElement(at, 'disconnect', attrib={
                'src-module': 'ospfRouter_%d_%d' % (event.link.srcSatelliteID.x, event.link.srcSatelliteID.y),
                'src-gate': 'ethg[%d]' % event.link.srcSatelliteID.getDirectionOfNeighbor(event.link.destSatelliteID)
            })
        elif event.eventType == LINK_RECONNECT_TYPE:
            src_gate = event.link.srcSatelliteID.getDirectionOfNeighbor(event.link.destSatelliteID)
            dest_gate = event.link.destSatelliteID.getDirectionOfNeighbor(event.link.srcSatelliteID)
            if src_gate == 0 or src_gate == 1:
                channel_type = 'inet.examples.ospfv2.sqsqtest.ISL0'
            else:
                channel_type = 'inet.examples.ospfv2.sqsqtest.ISL%d' % event.link.srcSatelliteID.x
            et.SubElement(at, 'connect', attrib={
                'src-module': 'ospfRouter_%d_%d' % (event.link.srcSatelliteID.x, event.link.srcSatelliteID.y),
                'src-gate': 'ethg[%d]' % src_gate,
                'dest-module': 'ospfRouter_%d_%d' % (event.link.destSatelliteID.x, event.link.destSatelliteID.y),
                'dest-gate': 'ethg[%d]' % dest_gate,
                'channel-type': channel_type
            })
        else:
            raise Exception('')

    xml_str = et.tostring(root, encoding='utf-8')
    xml_pretty_str = xml.dom.minidom.parseString(xml_str).toprettyxml()
    with open(file_name, 'w') as f:
        f.write(xml_pretty_str)


def buildIniFile(link_failure_rate_array):
    """
    print the config setting into config.txt
    """
    with open('./config.txt', 'w') as f:
        for link_failure_rate in link_failure_rate_array:
            for test in range(1, NUM_OF_TESTS + 1):
                print('[Config fail%s_test%d]' % (str(int(link_failure_rate * 100)).zfill(2), test), file=f)
                print('**.scenarioManager.script = xmldoc(\"./scenarios/test%d/sqsqScenario%s.xml\")' %
                      (test, "{:.3f}".format(link_failure_rate)), file=f)

                print('**.app[0].sendInterval = %ss' % send_interval, file=f)
                print('**.app[0].messageLength = 1024 bytes', file=f)      
                for deliverySrcID in deliverySrcIDs:
                    print('**.ospfRouter_%d_%d.app[0].destAddresses = "ospfRouter_%d_%d"' 
                        % (deliverySrcID.x, deliverySrcID.y, deliveryDestID.x, deliveryDestID.y), 
                        file=f)    
            print('', file=f)


def run():
    generateISLDelay()
    generateLinks()
    buildNEDFile()
    buildNetworkConfigFile()
    # buildASConfigFile()

    link_failure_rate_array = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
    
    # for i in range(1, NUM_OF_TESTS + 1):
        # os.mkdir('./scenarios/test%d' % i)
        # for fr in link_failure_rate_array:
            # buildScenarioFile(fr, './scenarios/test%d/sqsqScenario%s.xml' % (i, "{:.3f}".format(fr)))

    buildIniFile(link_failure_rate_array)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    run()