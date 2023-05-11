package inet.examples.ospfv2.sqsqtest;
import inet.common.misc.ThruputMeteringChannel;
import inet.common.scenario.ScenarioManager;
import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;

channel ISL0 extends ThruputMeteringChannel
{
    delay = 0.013431s;
    datarate = 100Mbps;
    thruputDisplayFormat = "#N";
}
channel ISL1 extends ThruputMeteringChannel
{
    delay = 0.004139s;
    datarate = 100Mbps;
    thruputDisplayFormat = "#N";
}
channel ISL2 extends ThruputMeteringChannel
{
    delay = 0.016173s;
    datarate = 100Mbps;
    thruputDisplayFormat = "#N";
}
channel ISL3 extends ThruputMeteringChannel
{
    delay = 0.023073s;
    datarate = 100Mbps;
    thruputDisplayFormat = "#N";
}
channel ISL4 extends ThruputMeteringChannel
{
    delay = 0.022647s;
    datarate = 100Mbps;
    thruputDisplayFormat = "#N";
}
channel ISL5 extends ThruputMeteringChannel
{
    delay = 0.015030s;
    datarate = 100Mbps;
    thruputDisplayFormat = "#N";
}
channel ISL6 extends ThruputMeteringChannel
{
    delay = 0.002642s;
    datarate = 100Mbps;
    thruputDisplayFormat = "#N";
}
channel ISL7 extends ThruputMeteringChannel
{
    delay = 0.010585s;
    datarate = 100Mbps;
    thruputDisplayFormat = "#N";
}
channel ISL8 extends ThruputMeteringChannel
{
    delay = 0.020451s;
    datarate = 100Mbps;
    thruputDisplayFormat = "#N";
}
channel ISL9 extends ThruputMeteringChannel
{
    delay = 0.023825s;
    datarate = 100Mbps;
    thruputDisplayFormat = "#N";
}
channel ISL10 extends ThruputMeteringChannel
{
    delay = 0.019634s;
    datarate = 100Mbps;
    thruputDisplayFormat = "#N";
}
channel ISL11 extends ThruputMeteringChannel
{
    delay = 0.009209s;
    datarate = 100Mbps;
    thruputDisplayFormat = "#N";
}
network Network
{
    @display("bgb=1024,1400");

    submodules:
        configurator: Ipv4NetworkConfigurator {
            parameters:
                config = xmldoc("sqsqNetworkConfig.xml");
                addStaticRoutes = false;
                addDefaultRoutes = false;
                @display("p=50,100;is=s");
        }
        scenarioManager: ScenarioManager {
            @display("p=50,200;is=s");
        }
        ospfRouter_1_1: SqsqRouter {
            @display("p=220,96");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.1.1";
            gates:
                ethg[4];
        }
        ospfRouter_1_2: SqsqRouter {
            @display("p=340,120");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.1.2";
            gates:
                ethg[4];
        }
        ospfRouter_1_3: SqsqRouter {
            @display("p=460,120");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.1.3";
            gates:
                ethg[4];
        }
        ospfRouter_1_4: SqsqRouter {
            @display("p=580,120");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.1.4";
            gates:
                ethg[4];
        }
        ospfRouter_1_5: SqsqRouter {
            @display("p=700,120");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.1.5";
            gates:
                ethg[4];
        }
        ospfRouter_1_6: SqsqRouter {
            @display("p=820,89");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.1.6";
            gates:
                ethg[4];
        }
        ospfRouter_2_1: SqsqRouter {
            @display("p=169,193.7");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.2.1";
            gates:
                ethg[4];
        }
        ospfRouter_2_2: SqsqRouter {
            @display("p=288.6,234");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.2.2";
            gates:
                ethg[4];
        }
        ospfRouter_2_3: SqsqRouter {
            @display("p=408.19998,234");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.2.3";
            gates:
                ethg[4];
        }
        ospfRouter_2_4: SqsqRouter {
            @display("p=529.1,234");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.2.4";
            gates:
                ethg[4];
        }
        ospfRouter_2_5: SqsqRouter {
            @display("p=648.7,234");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.2.5";
            gates:
                ethg[4];
        }
        ospfRouter_2_6: SqsqRouter {
            @display("p=768.3,193.7");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.2.6";
            gates:
                ethg[4];
        }
        ospfRouter_3_1: SqsqRouter {
            @display("p=169,315.9");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.3.1";
            gates:
                ethg[4];
        }
        ospfRouter_3_2: SqsqRouter {
            @display("p=288.6,356.19998");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.3.2";
            gates:
                ethg[4];
        }
        ospfRouter_3_3: SqsqRouter {
            @display("p=408.19998,356.19998");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.3.3";
            gates:
                ethg[4];
        }
        ospfRouter_3_4: SqsqRouter {
            @display("p=529.1,356.19998");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.3.4";
            gates:
                ethg[4];
        }
        ospfRouter_3_5: SqsqRouter {
            @display("p=648.7,356.19998");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.3.5";
            gates:
                ethg[4];
        }
        ospfRouter_3_6: SqsqRouter {
            @display("p=768.3,315.9");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.3.6";
            gates:
                ethg[4];
        }
        ospfRouter_4_1: SqsqRouter {
            @display("p=169,436.8");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.4.1";
            gates:
                ethg[4];
        }
        ospfRouter_4_2: SqsqRouter {
            @display("p=288.6,477.1");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.4.2";
            gates:
                ethg[4];
        }
        ospfRouter_4_3: SqsqRouter {
            @display("p=408.19998,477.1");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.4.3";
            gates:
                ethg[4];
        }
        ospfRouter_4_4: SqsqRouter {
            @display("p=529.1,477.1");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.4.4";
            gates:
                ethg[4];
        }
        ospfRouter_4_5: SqsqRouter {
            @display("p=648.7,477.1");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.4.5";
            gates:
                ethg[4];
        }
        ospfRouter_4_6: SqsqRouter {
            @display("p=768.3,436.8");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.4.6";
            gates:
                ethg[4];
        }
        ospfRouter_5_1: SqsqRouter {
            @display("p=169,556.39996");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.5.1";
            gates:
                ethg[4];
        }
        ospfRouter_5_2: SqsqRouter {
            @display("p=288.6,596.7");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.5.2";
            gates:
                ethg[4];
        }
        ospfRouter_5_3: SqsqRouter {
            @display("p=408.19998,596.7");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.5.3";
            gates:
                ethg[4];
        }
        ospfRouter_5_4: SqsqRouter {
            @display("p=529.1,596.7");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.5.4";
            gates:
                ethg[4];
        }
        ospfRouter_5_5: SqsqRouter {
            @display("p=648.7,596.7");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.5.5";
            gates:
                ethg[4];
        }
        ospfRouter_5_6: SqsqRouter {
            @display("p=768.3,556.39996");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.5.6";
            gates:
                ethg[4];
        }
        ospfRouter_6_1: SqsqRouter {
            @display("p=169,676");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.6.1";
            gates:
                ethg[4];
        }
        ospfRouter_6_2: SqsqRouter {
            @display("p=288.6,716.3");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.6.2";
            gates:
                ethg[4];
        }
        ospfRouter_6_3: SqsqRouter {
            @display("p=408.19998,716.3");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.6.3";
            gates:
                ethg[4];
        }
        ospfRouter_6_4: SqsqRouter {
            @display("p=529.1,716.3");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.6.4";
            gates:
                ethg[4];
        }
        ospfRouter_6_5: SqsqRouter {
            @display("p=648.7,716.3");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.6.5";
            gates:
                ethg[4];
        }
        ospfRouter_6_6: SqsqRouter {
            @display("p=768.3,676");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.6.6";
            gates:
                ethg[4];
        }
        ospfRouter_7_1: SqsqRouter {
            @display("p=169,796.89996");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.7.1";
            gates:
                ethg[4];
        }
        ospfRouter_7_2: SqsqRouter {
            @display("p=288.6,837.2");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.7.2";
            gates:
                ethg[4];
        }
        ospfRouter_7_3: SqsqRouter {
            @display("p=408.19998,837.2");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.7.3";
            gates:
                ethg[4];
        }
        ospfRouter_7_4: SqsqRouter {
            @display("p=529.1,837.2");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.7.4";
            gates:
                ethg[4];
        }
        ospfRouter_7_5: SqsqRouter {
            @display("p=648.7,837.2");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.7.5";
            gates:
                ethg[4];
        }
        ospfRouter_7_6: SqsqRouter {
            @display("p=768.3,796.89996");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.7.6";
            gates:
                ethg[4];
        }
        ospfRouter_8_1: SqsqRouter {
            @display("p=169,916.5");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.8.1";
            gates:
                ethg[4];
        }
        ospfRouter_8_2: SqsqRouter {
            @display("p=288.6,956.8");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.8.2";
            gates:
                ethg[4];
        }
        ospfRouter_8_3: SqsqRouter {
            @display("p=408.19998,956.8");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.8.3";
            gates:
                ethg[4];
        }
        ospfRouter_8_4: SqsqRouter {
            @display("p=529.1,956.8");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.8.4";
            gates:
                ethg[4];
        }
        ospfRouter_8_5: SqsqRouter {
            @display("p=648.7,956.8");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.8.5";
            gates:
                ethg[4];
        }
        ospfRouter_8_6: SqsqRouter {
            @display("p=768.3,916.5");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.8.6";
            gates:
                ethg[4];
        }
        ospfRouter_9_1: SqsqRouter {
            @display("p=169,1038.7");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.9.1";
            gates:
                ethg[4];
        }
        ospfRouter_9_2: SqsqRouter {
            @display("p=288.6,1079");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.9.2";
            gates:
                ethg[4];
        }
        ospfRouter_9_3: SqsqRouter {
            @display("p=408.19998,1079");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.9.3";
            gates:
                ethg[4];
        }
        ospfRouter_9_4: SqsqRouter {
            @display("p=529.1,1079");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.9.4";
            gates:
                ethg[4];
        }
        ospfRouter_9_5: SqsqRouter {
            @display("p=648.7,1079");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.9.5";
            gates:
                ethg[4];
        }
        ospfRouter_9_6: SqsqRouter {
            @display("p=768.3,1038.7");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.9.6";
            gates:
                ethg[4];
        }
        ospfRouter_10_1: SqsqRouter {
            @display("p=169,1159.6");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.10.1";
            gates:
                ethg[4];
        }
        ospfRouter_10_2: SqsqRouter {
            @display("p=288.6,1199.9");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.10.2";
            gates:
                ethg[4];
        }
        ospfRouter_10_3: SqsqRouter {
            @display("p=408.19998,1199.9");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.10.3";
            gates:
                ethg[4];
        }
        ospfRouter_10_4: SqsqRouter {
            @display("p=529.1,1199.9");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.10.4";
            gates:
                ethg[4];
        }
        ospfRouter_10_5: SqsqRouter {
            @display("p=648.7,1199.9");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.10.5";
            gates:
                ethg[4];
        }
        ospfRouter_10_6: SqsqRouter {
            @display("p=768.3,1159.6");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.10.6";
            gates:
                ethg[4];
        }
        ospfRouter_11_1: SqsqRouter {
            @display("p=219.7,1279.2");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.11.1";
            gates:
                ethg[4];
        }
        ospfRouter_11_2: SqsqRouter {
            @display("p=340,1320");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.11.2";
            gates:
                ethg[4];
        }
        ospfRouter_11_3: SqsqRouter {
            @display("p=460,1320");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.11.3";
            gates:
                ethg[4];
        }
        ospfRouter_11_4: SqsqRouter {
            @display("p=580,1320");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.11.4";
            gates:
                ethg[4];
        }
        ospfRouter_11_5: SqsqRouter {
            @display("p=700,1320");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.11.5";
            gates:
                ethg[4];
        }
        ospfRouter_11_6: SqsqRouter {
            @display("p=819,1279.2");
            hasStatus = true;
            ipv4.routingTable.routerId = "0.0.11.6";
            gates:
                ethg[4];
        }
    connections:
        ospfRouter_1_1.ethg[3] <--> ISL1 <--> ospfRouter_1_2.ethg[2];
        ospfRouter_1_1.ethg[1] <--> ISL0 <--> ospfRouter_2_1.ethg[0];
        ospfRouter_1_2.ethg[3] <--> ISL1 <--> ospfRouter_1_3.ethg[2];
        ospfRouter_1_2.ethg[1] <--> ISL0 <--> ospfRouter_2_2.ethg[0];
        ospfRouter_1_3.ethg[3] <--> ISL1 <--> ospfRouter_1_4.ethg[2];
        ospfRouter_1_3.ethg[1] <--> ISL0 <--> ospfRouter_2_3.ethg[0];
        ospfRouter_1_4.ethg[3] <--> ISL1 <--> ospfRouter_1_5.ethg[2];
        ospfRouter_1_4.ethg[1] <--> ISL0 <--> ospfRouter_2_4.ethg[0];
        ospfRouter_1_5.ethg[3] <--> ISL1 <--> ospfRouter_1_6.ethg[2];
        ospfRouter_1_5.ethg[1] <--> ISL0 <--> ospfRouter_2_5.ethg[0];
        ospfRouter_1_6.ethg[3] <--> ISL1 <--> ospfRouter_1_1.ethg[2];
        ospfRouter_1_6.ethg[1] <--> ISL0 <--> ospfRouter_2_6.ethg[0];
        ospfRouter_2_1.ethg[3] <--> ISL2 <--> ospfRouter_2_2.ethg[2];
        ospfRouter_2_1.ethg[1] <--> ISL0 <--> ospfRouter_3_1.ethg[0];
        ospfRouter_2_2.ethg[3] <--> ISL2 <--> ospfRouter_2_3.ethg[2];
        ospfRouter_2_2.ethg[1] <--> ISL0 <--> ospfRouter_3_2.ethg[0];
        ospfRouter_2_3.ethg[3] <--> ISL2 <--> ospfRouter_2_4.ethg[2];
        ospfRouter_2_3.ethg[1] <--> ISL0 <--> ospfRouter_3_3.ethg[0];
        ospfRouter_2_4.ethg[3] <--> ISL2 <--> ospfRouter_2_5.ethg[2];
        ospfRouter_2_4.ethg[1] <--> ISL0 <--> ospfRouter_3_4.ethg[0];
        ospfRouter_2_5.ethg[3] <--> ISL2 <--> ospfRouter_2_6.ethg[2];
        ospfRouter_2_5.ethg[1] <--> ISL0 <--> ospfRouter_3_5.ethg[0];
        ospfRouter_2_6.ethg[3] <--> ISL2 <--> ospfRouter_2_1.ethg[2];
        ospfRouter_2_6.ethg[1] <--> ISL0 <--> ospfRouter_3_6.ethg[0];
        ospfRouter_3_1.ethg[3] <--> ISL3 <--> ospfRouter_3_2.ethg[2];
        ospfRouter_3_1.ethg[1] <--> ISL0 <--> ospfRouter_4_1.ethg[0];
        ospfRouter_3_2.ethg[3] <--> ISL3 <--> ospfRouter_3_3.ethg[2];
        ospfRouter_3_2.ethg[1] <--> ISL0 <--> ospfRouter_4_2.ethg[0];
        ospfRouter_3_3.ethg[3] <--> ISL3 <--> ospfRouter_3_4.ethg[2];
        ospfRouter_3_3.ethg[1] <--> ISL0 <--> ospfRouter_4_3.ethg[0];
        ospfRouter_3_4.ethg[3] <--> ISL3 <--> ospfRouter_3_5.ethg[2];
        ospfRouter_3_4.ethg[1] <--> ISL0 <--> ospfRouter_4_4.ethg[0];
        ospfRouter_3_5.ethg[3] <--> ISL3 <--> ospfRouter_3_6.ethg[2];
        ospfRouter_3_5.ethg[1] <--> ISL0 <--> ospfRouter_4_5.ethg[0];
        ospfRouter_3_6.ethg[3] <--> ISL3 <--> ospfRouter_3_1.ethg[2];
        ospfRouter_3_6.ethg[1] <--> ISL0 <--> ospfRouter_4_6.ethg[0];
        ospfRouter_4_1.ethg[3] <--> ISL4 <--> ospfRouter_4_2.ethg[2];
        ospfRouter_4_1.ethg[1] <--> ISL0 <--> ospfRouter_5_1.ethg[0];
        ospfRouter_4_2.ethg[3] <--> ISL4 <--> ospfRouter_4_3.ethg[2];
        ospfRouter_4_2.ethg[1] <--> ISL0 <--> ospfRouter_5_2.ethg[0];
        ospfRouter_4_3.ethg[3] <--> ISL4 <--> ospfRouter_4_4.ethg[2];
        ospfRouter_4_3.ethg[1] <--> ISL0 <--> ospfRouter_5_3.ethg[0];
        ospfRouter_4_4.ethg[3] <--> ISL4 <--> ospfRouter_4_5.ethg[2];
        ospfRouter_4_4.ethg[1] <--> ISL0 <--> ospfRouter_5_4.ethg[0];
        ospfRouter_4_5.ethg[3] <--> ISL4 <--> ospfRouter_4_6.ethg[2];
        ospfRouter_4_5.ethg[1] <--> ISL0 <--> ospfRouter_5_5.ethg[0];
        ospfRouter_4_6.ethg[3] <--> ISL4 <--> ospfRouter_4_1.ethg[2];
        ospfRouter_4_6.ethg[1] <--> ISL0 <--> ospfRouter_5_6.ethg[0];
        ospfRouter_5_1.ethg[3] <--> ISL5 <--> ospfRouter_5_2.ethg[2];
        ospfRouter_5_1.ethg[1] <--> ISL0 <--> ospfRouter_6_1.ethg[0];
        ospfRouter_5_2.ethg[3] <--> ISL5 <--> ospfRouter_5_3.ethg[2];
        ospfRouter_5_2.ethg[1] <--> ISL0 <--> ospfRouter_6_2.ethg[0];
        ospfRouter_5_3.ethg[3] <--> ISL5 <--> ospfRouter_5_4.ethg[2];
        ospfRouter_5_3.ethg[1] <--> ISL0 <--> ospfRouter_6_3.ethg[0];
        ospfRouter_5_4.ethg[3] <--> ISL5 <--> ospfRouter_5_5.ethg[2];
        ospfRouter_5_4.ethg[1] <--> ISL0 <--> ospfRouter_6_4.ethg[0];
        ospfRouter_5_5.ethg[3] <--> ISL5 <--> ospfRouter_5_6.ethg[2];
        ospfRouter_5_5.ethg[1] <--> ISL0 <--> ospfRouter_6_5.ethg[0];
        ospfRouter_5_6.ethg[3] <--> ISL5 <--> ospfRouter_5_1.ethg[2];
        ospfRouter_5_6.ethg[1] <--> ISL0 <--> ospfRouter_6_6.ethg[0];
        ospfRouter_6_1.ethg[3] <--> ISL6 <--> ospfRouter_6_2.ethg[2];
        ospfRouter_6_1.ethg[1] <--> ISL0 <--> ospfRouter_7_1.ethg[0];
        ospfRouter_6_2.ethg[3] <--> ISL6 <--> ospfRouter_6_3.ethg[2];
        ospfRouter_6_2.ethg[1] <--> ISL0 <--> ospfRouter_7_2.ethg[0];
        ospfRouter_6_3.ethg[3] <--> ISL6 <--> ospfRouter_6_4.ethg[2];
        ospfRouter_6_3.ethg[1] <--> ISL0 <--> ospfRouter_7_3.ethg[0];
        ospfRouter_6_4.ethg[3] <--> ISL6 <--> ospfRouter_6_5.ethg[2];
        ospfRouter_6_4.ethg[1] <--> ISL0 <--> ospfRouter_7_4.ethg[0];
        ospfRouter_6_5.ethg[3] <--> ISL6 <--> ospfRouter_6_6.ethg[2];
        ospfRouter_6_5.ethg[1] <--> ISL0 <--> ospfRouter_7_5.ethg[0];
        ospfRouter_6_6.ethg[3] <--> ISL6 <--> ospfRouter_6_1.ethg[2];
        ospfRouter_6_6.ethg[1] <--> ISL0 <--> ospfRouter_7_6.ethg[0];
        ospfRouter_7_1.ethg[3] <--> ISL7 <--> ospfRouter_7_2.ethg[2];
        ospfRouter_7_1.ethg[1] <--> ISL0 <--> ospfRouter_8_1.ethg[0];
        ospfRouter_7_2.ethg[3] <--> ISL7 <--> ospfRouter_7_3.ethg[2];
        ospfRouter_7_2.ethg[1] <--> ISL0 <--> ospfRouter_8_2.ethg[0];
        ospfRouter_7_3.ethg[3] <--> ISL7 <--> ospfRouter_7_4.ethg[2];
        ospfRouter_7_3.ethg[1] <--> ISL0 <--> ospfRouter_8_3.ethg[0];
        ospfRouter_7_4.ethg[3] <--> ISL7 <--> ospfRouter_7_5.ethg[2];
        ospfRouter_7_4.ethg[1] <--> ISL0 <--> ospfRouter_8_4.ethg[0];
        ospfRouter_7_5.ethg[3] <--> ISL7 <--> ospfRouter_7_6.ethg[2];
        ospfRouter_7_5.ethg[1] <--> ISL0 <--> ospfRouter_8_5.ethg[0];
        ospfRouter_7_6.ethg[3] <--> ISL7 <--> ospfRouter_7_1.ethg[2];
        ospfRouter_7_6.ethg[1] <--> ISL0 <--> ospfRouter_8_6.ethg[0];
        ospfRouter_8_1.ethg[3] <--> ISL8 <--> ospfRouter_8_2.ethg[2];
        ospfRouter_8_1.ethg[1] <--> ISL0 <--> ospfRouter_9_1.ethg[0];
        ospfRouter_8_2.ethg[3] <--> ISL8 <--> ospfRouter_8_3.ethg[2];
        ospfRouter_8_2.ethg[1] <--> ISL0 <--> ospfRouter_9_2.ethg[0];
        ospfRouter_8_3.ethg[3] <--> ISL8 <--> ospfRouter_8_4.ethg[2];
        ospfRouter_8_3.ethg[1] <--> ISL0 <--> ospfRouter_9_3.ethg[0];
        ospfRouter_8_4.ethg[3] <--> ISL8 <--> ospfRouter_8_5.ethg[2];
        ospfRouter_8_4.ethg[1] <--> ISL0 <--> ospfRouter_9_4.ethg[0];
        ospfRouter_8_5.ethg[3] <--> ISL8 <--> ospfRouter_8_6.ethg[2];
        ospfRouter_8_5.ethg[1] <--> ISL0 <--> ospfRouter_9_5.ethg[0];
        ospfRouter_8_6.ethg[3] <--> ISL8 <--> ospfRouter_8_1.ethg[2];
        ospfRouter_8_6.ethg[1] <--> ISL0 <--> ospfRouter_9_6.ethg[0];
        ospfRouter_9_1.ethg[3] <--> ISL9 <--> ospfRouter_9_2.ethg[2];
        ospfRouter_9_1.ethg[1] <--> ISL0 <--> ospfRouter_10_1.ethg[0];
        ospfRouter_9_2.ethg[3] <--> ISL9 <--> ospfRouter_9_3.ethg[2];
        ospfRouter_9_2.ethg[1] <--> ISL0 <--> ospfRouter_10_2.ethg[0];
        ospfRouter_9_3.ethg[3] <--> ISL9 <--> ospfRouter_9_4.ethg[2];
        ospfRouter_9_3.ethg[1] <--> ISL0 <--> ospfRouter_10_3.ethg[0];
        ospfRouter_9_4.ethg[3] <--> ISL9 <--> ospfRouter_9_5.ethg[2];
        ospfRouter_9_4.ethg[1] <--> ISL0 <--> ospfRouter_10_4.ethg[0];
        ospfRouter_9_5.ethg[3] <--> ISL9 <--> ospfRouter_9_6.ethg[2];
        ospfRouter_9_5.ethg[1] <--> ISL0 <--> ospfRouter_10_5.ethg[0];
        ospfRouter_9_6.ethg[3] <--> ISL9 <--> ospfRouter_9_1.ethg[2];
        ospfRouter_9_6.ethg[1] <--> ISL0 <--> ospfRouter_10_6.ethg[0];
        ospfRouter_10_1.ethg[3] <--> ISL10 <--> ospfRouter_10_2.ethg[2];
        ospfRouter_10_1.ethg[1] <--> ISL0 <--> ospfRouter_11_1.ethg[0];
        ospfRouter_10_2.ethg[3] <--> ISL10 <--> ospfRouter_10_3.ethg[2];
        ospfRouter_10_2.ethg[1] <--> ISL0 <--> ospfRouter_11_2.ethg[0];
        ospfRouter_10_3.ethg[3] <--> ISL10 <--> ospfRouter_10_4.ethg[2];
        ospfRouter_10_3.ethg[1] <--> ISL0 <--> ospfRouter_11_3.ethg[0];
        ospfRouter_10_4.ethg[3] <--> ISL10 <--> ospfRouter_10_5.ethg[2];
        ospfRouter_10_4.ethg[1] <--> ISL0 <--> ospfRouter_11_4.ethg[0];
        ospfRouter_10_5.ethg[3] <--> ISL10 <--> ospfRouter_10_6.ethg[2];
        ospfRouter_10_5.ethg[1] <--> ISL0 <--> ospfRouter_11_5.ethg[0];
        ospfRouter_10_6.ethg[3] <--> ISL10 <--> ospfRouter_10_1.ethg[2];
        ospfRouter_10_6.ethg[1] <--> ISL0 <--> ospfRouter_11_6.ethg[0];
        ospfRouter_11_1.ethg[3] <--> ISL11 <--> ospfRouter_11_2.ethg[2];
        ospfRouter_11_1.ethg[1] <--> ISL0 <--> ospfRouter_1_1.ethg[0];
        ospfRouter_11_2.ethg[3] <--> ISL11 <--> ospfRouter_11_3.ethg[2];
        ospfRouter_11_2.ethg[1] <--> ISL0 <--> ospfRouter_1_2.ethg[0];
        ospfRouter_11_3.ethg[3] <--> ISL11 <--> ospfRouter_11_4.ethg[2];
        ospfRouter_11_3.ethg[1] <--> ISL0 <--> ospfRouter_1_3.ethg[0];
        ospfRouter_11_4.ethg[3] <--> ISL11 <--> ospfRouter_11_5.ethg[2];
        ospfRouter_11_4.ethg[1] <--> ISL0 <--> ospfRouter_1_4.ethg[0];
        ospfRouter_11_5.ethg[3] <--> ISL11 <--> ospfRouter_11_6.ethg[2];
        ospfRouter_11_5.ethg[1] <--> ISL0 <--> ospfRouter_1_5.ethg[0];
        ospfRouter_11_6.ethg[3] <--> ISL11 <--> ospfRouter_11_1.ethg[2];
        ospfRouter_11_6.ethg[1] <--> ISL0 <--> ospfRouter_1_6.ethg[0];
}
