from scapy.all import srp


def scan_ip_net():
    with open('ip_net.lst', 'r', encoding='utf-8') as file:
        lines = file.readlines()  # Читаем всё содержимое
        print(lines[1].strip())  # Выводим на экран
        arp_request = ARP(pdst='192.168.1.255')
        srp_result = srp(arp_request, timeout=1)
        devices = [(ip, mac) for _, mac in srp_result if mac is not None]

def main():
    scan_ip_net()
    print('Start diploma')


main()
