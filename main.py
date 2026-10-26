import nmap
import pexpect


USER = 'admin'
PASSWORD = 'admin123'
TFTP_SERVER ='192.168.1.5'
FILE_CONFIG = 'vrpcfg.cfg'

def load_sw_config(ip_sw, user_sw, password_sw, ip_tftp_server, file_sw_config):
    string_ip_sw = '_'.join(ip_sw.split('.'))
    # sw_expect = pexpect.spawn(f'telnet {ip_sw}')
    sw_expect = pexpect.spawn(f"telnet {ip_sw}")
    sw_expect.expect('Password:')
    sw_expect.sendline(f'f{password_sw}')
    sw_expect.expect('>')
    sw_expect.sendline(f'tftp {ip_tftp_server} put {file_sw_config} {string_ip_sw}.cfg')
    sw_expect.expect('>')
    '''
    command copy config to file: 
    tftp 192.168.1.5 put vrpcfg.cfg 10_10_10_23.cfg
    copy startup-config tftp://192.168.1.5/10_10_10.25.cfg
    and
    server tftp-hpa need to edit file /etc/default/tftpd-hpa - change line:
    TFTP_OPTIONS="--secure --create" 
    '''

    

def scan_all_net():
    with open('ip_net.lst', 'r', encoding='utf-8') as file:
        ip_net_list = file.readlines()  # Читаем файла с ip адресами сетей

        for ip_net in ip_net_list: # Передор Ip адресов сетей
            # ip_net_and_mask = f'{ip_net.strip()}/24'
            print(f"\nДоступные хосты сети {ip_net.strip()}")
            hosts = scan_one_net(ip_net.strip()) # Выполняем сканирование выбранной сети
            # print(hosts)
            for h in hosts:
                print(f"IP: {h['ip']}, Hostname: {h['hostname']}") # Выводим ip доступных адресов
                load_sw_config(h['ip'], USER, PASSWORD, TFTP_SERVER, FILE_CONFIG)




def scan_one_net(ip_range):
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
    scan_all_net()


main()
