from dispatch import profiles


inherit = {
    "getters": [
        "GenericNetworkSwitch",
        "GenericNetworkRouter",
        "Cisco.ntp.client"
    ],
    "setters": []
}


arista = profiles.define_profile("Arista", includes=inherit)


@arista.gets("ntp.client.skew")
def ntp_client_skew(device):
    return -24


@arista.gets("network.interface.mac_address")
def mac_address_by_interface_name(device, interface):
    return "eth0"


@arista.identifies
def check_sys_descr(device):
    return True
