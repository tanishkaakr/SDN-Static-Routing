from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class StaticRouter (object):
  def __init__ (self, connection):
    self.connection = connection
    connection.addListeners(self)

  def _handle_ConnectionUp (self, event):
    dpid = event.dpid
    log.info("Switch %s has connected", dpid)

    # --- HELPER FUNCTIONS ---

    def install_path(dst_ip, out_port):
      """Installs a flow rule for specific IPv4 traffic."""
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0800 # Match IPv4
      msg.match.nw_dst = dst_ip
      msg.actions.append(of.ofp_action_output(port = out_port))
      self.connection.send(msg)

    def allow_arp():
      """Installs a flow rule to allow ARP (Address Resolution Protocol)."""
      msg = of.ofp_flow_mod()
      msg.match.dl_type = 0x0806 # Match ARP
      msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      self.connection.send(msg)

    # --- EXECUTE RULES ---

    # 1. Always allow ARP so hosts can find each other
    allow_arp()

    # 2. Install Static IP Routes based on Switch ID
    if dpid == 1:
        # Route to H1 (Local port 1)
        install_path("10.0.0.1", 1)
        # Route to H2 and H3 (Go out via Switch 2 on port 2)
        install_path("10.0.0.2", 2)
        install_path("10.0.0.3", 2)

    elif dpid == 2:
        # Route to H2 (Local port 1)
        install_path("10.0.0.2", 1)
        # Route to H1 (Go out via Switch 1 on port 2)
        install_path("10.0.0.1", 2)
        # Route to H3 (Go out via Switch 3 on port 3)
        install_path("10.0.0.3", 3)

    elif dpid == 3:
        # Route to H3 (Local port 1)
        install_path("10.0.0.3", 1)
        # Route to H1 and H2 (Go out via Switch 2 on port 2)
        install_path("10.0.0.1", 2)
        install_path("10.0.0.2", 2)

def launch ():
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    StaticRouter(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)