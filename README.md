# Static Routing Implementation using SDN

This project demonstrates the manual installation of flow rules using an SDN controller to dictate specific network paths in a multi-switch environment.

## 🛠 Tech Stack
* **Controller:** POX (Python-based)
* **Emulator:** Mininet
* **Protocol:** OpenFlow 1.0
* **Environment:** Ubuntu (Linux)

## 🌐 Network Topology
The topology consists of three Open vSwitch (OVS) instances connected in a linear chain. Each switch is connected to a single host.


## 🚀 Execution Flow
1. **Controller:** Run `python2 pox.py ext.static_routing` to start the control plane logic.
2. **Mininet:** Run `sudo mn --custom topo.py --topo mystatictopo --controller remote` to instantiate the data plane.
3. **Verification:** Connectivity is validated using `h1 ping h3`.

## 📊 Results & Regression Testing
* **Static Paths:** Successfully hardcoded DPID-to-Port mappings.
* **ARP Logic:** Implemented ARP flooding to allow MAC discovery in a static environment.
* **Regression Test:** Verified that paths remain identical (consistent port mapping) after deleting and reinstalling flow rules. Observed packet counters resetting to 0 and resuming correctly.
