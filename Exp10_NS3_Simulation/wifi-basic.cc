/*
 * Experiment 10: Introduction to the NS-3 network simulator, basic Wi-Fi experiment.
 *
 * Topology: one access point at the origin and nSta stations on a circle of
 * radius `distance` around it (802.11n, 2.4 GHz). Each station sends a constant
 * bit rate UDP stream to the AP. FlowMonitor reports per-flow throughput, mean
 * delay and packet loss, and a pcap trace of the AP is written for Wireshark.
 *
 * Build & run (from the ns-3 root directory):
 *   cp wifi-basic.cc scratch/
 *   ./ns3 run "scratch/wifi-basic --nSta=3 --distance=10 --dataRate=5Mbps"
 */
#include "ns3/applications-module.h"
#include "ns3/core-module.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/internet-module.h"
#include "ns3/mobility-module.h"
#include "ns3/network-module.h"
#include "ns3/wifi-module.h"

#include <cmath>
#include <iomanip>
#include <iostream>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("WifiBasic");

int
main(int argc, char* argv[])
{
    uint32_t nSta = 3;
    double distance = 10.0;
    double simTime = 10.0;
    std::string dataRate = "5Mbps";
    uint32_t packetSize = 1024;

    CommandLine cmd(__FILE__);
    cmd.AddValue("nSta", "Number of Wi-Fi stations", nSta);
    cmd.AddValue("distance", "Distance of stations from the AP (m)", distance);
    cmd.AddValue("dataRate", "Offered load per station", dataRate);
    cmd.AddValue("simTime", "Simulation time (s)", simTime);
    cmd.Parse(argc, argv);

    NodeContainer apNode;
    apNode.Create(1);
    NodeContainer staNodes;
    staNodes.Create(nSta);

    // PHY and channel: log-distance propagation loss by default
    YansWifiChannelHelper channel = YansWifiChannelHelper::Default();
    YansWifiPhyHelper phy;
    phy.SetChannel(channel.Create());

    WifiHelper wifi;
    wifi.SetStandard(WIFI_STANDARD_80211n);
    wifi.SetRemoteStationManager("ns3::MinstrelHtWifiManager");

    WifiMacHelper mac;
    Ssid ssid = Ssid("mdl501-lab");
    mac.SetType("ns3::StaWifiMac", "Ssid", SsidValue(ssid));
    NetDeviceContainer staDevices = wifi.Install(phy, mac, staNodes);
    mac.SetType("ns3::ApWifiMac", "Ssid", SsidValue(ssid));
    NetDeviceContainer apDevice = wifi.Install(phy, mac, apNode);

    // Mobility: AP at origin, stations on a circle
    MobilityHelper mobility;
    Ptr<ListPositionAllocator> positions = CreateObject<ListPositionAllocator>();
    positions->Add(Vector(0.0, 0.0, 0.0));
    for (uint32_t i = 0; i < nSta; ++i)
    {
        double angle = 2 * M_PI * i / nSta;
        positions->Add(Vector(distance * std::cos(angle), distance * std::sin(angle), 0.0));
    }
    mobility.SetPositionAllocator(positions);
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
    mobility.Install(apNode);
    mobility.Install(staNodes);

    InternetStackHelper stack;
    stack.Install(apNode);
    stack.Install(staNodes);

    Ipv4AddressHelper address;
    address.SetBase("192.168.1.0", "255.255.255.0");
    Ipv4InterfaceContainer apInterface = address.Assign(apDevice);
    address.Assign(staDevices);

    // Applications: UDP sink on the AP, CBR sources on each station
    uint16_t port = 9;
    PacketSinkHelper sink("ns3::UdpSocketFactory", InetSocketAddress(Ipv4Address::GetAny(), port));
    ApplicationContainer sinkApp = sink.Install(apNode.Get(0));
    sinkApp.Start(Seconds(0.0));
    sinkApp.Stop(Seconds(simTime));

    OnOffHelper onoff("ns3::UdpSocketFactory", InetSocketAddress(apInterface.GetAddress(0), port));
    onoff.SetConstantRate(DataRate(dataRate), packetSize);
    ApplicationContainer clientApps = onoff.Install(staNodes);
    clientApps.Start(Seconds(1.0));
    clientApps.Stop(Seconds(simTime));

    FlowMonitorHelper flowHelper;
    Ptr<FlowMonitor> monitor = flowHelper.InstallAll();
    phy.EnablePcap("wifi-basic-ap", apDevice.Get(0));

    Simulator::Stop(Seconds(simTime));
    Simulator::Run();

    monitor->CheckForLostPackets();
    Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier>(flowHelper.GetClassifier());
    double totalThroughput = 0;

    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Flow  Source -> Destination        Tx pkts  Rx pkts  Throughput(Mbps)  Delay(ms)  Loss(%)\n";
    for (const auto& [flowId, st] : monitor->GetFlowStats())
    {
        Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow(flowId);
        double duration = st.timeLastRxPacket.GetSeconds() - st.timeFirstTxPacket.GetSeconds();
        double throughput = duration > 0 ? st.rxBytes * 8.0 / duration / 1e6 : 0;
        double delay = st.rxPackets > 0 ? st.delaySum.GetSeconds() / st.rxPackets * 1000 : 0;
        double loss = st.txPackets > 0 ? 100.0 * (st.txPackets - st.rxPackets) / st.txPackets : 0;
        totalThroughput += throughput;
        std::cout << std::setw(4) << flowId << "  " << t.sourceAddress << " -> " << t.destinationAddress
                  << std::setw(10) << st.txPackets << std::setw(9) << st.rxPackets << std::setw(18)
                  << throughput << std::setw(11) << delay << std::setw(9) << loss << "\n";
    }
    std::cout << "Aggregate throughput: " << totalThroughput << " Mbps\n";

    monitor->SerializeToXmlFile("wifi-basic-flowmon.xml", true, true);
    Simulator::Destroy();
    return 0;
}
