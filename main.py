import nmap
import pexpect


def telnet_kd_and_put_config():
    telnet_kd=pexpect.spawn('telnet 192.168.1.250')
    telnet_kd.expect('Password:')
    telnet_kd.sendline('admin123')
    telnet_kd.expect('>')
    '''
    command copy config to file: 
    tftp 192.168.1.5 put vrpcfg.cfg 10_10_10_23.cfg
    copy startup-config tftp://192.168.1.5/10_10_10.25.cfg
    and
    server tftp-hpa need to edit file /etc/default/tftpd-hpa - change line:
    TFTP_OPTIONS="--secure --create" 
    '''

    

def scan_ip_net():
    with open('ip_net.lst', 'r', encoding='utf-8') as file:
        ip_net_list = file.readlines()  # Читаем файла с ip адресами сетей

        for ip_net in ip_net_list: # Передор Ip адресов сетей
            ip_net_mask = f'{ip_net.strip()}/24'
            print(f"\nДоступные хосты сети {ip_net_mask.strip()}")
            hosts = scan_with_nmap(ip_net_mask) # Выполняем сканирование выбранной сети
            # print(hosts)
            for h in hosts:
                print(f"IP: {h['ip']}, Hostname: {h['hostname']}") # Выводим ip доступных адресов





def scan_with_nmap(ip_range):
    nmap_path = [r"C:\Program Files (x86)\Nmap\nmap.exe"]
    nm = nmap.PortScanner(nmap_search_path=nmap_path)
    # Аргументы: -sn означает "Ping Scan" (без сканирования портов)
    nm.scan(hosts=ip_range, arguments='-sn', timeout=0)

    live_hosts = []
    for host in nm.all_hosts():
        if nm[host].state() == 'up':
            hostname = nm[host].hostname()
            live_hosts.append({'ip': host, 'hostname': hostname})

    return live_hosts


def main():
    scan_ip_net()


main()
