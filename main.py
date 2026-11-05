import nmap
import pexpect


USER = 'user'
PASSWORD = 'password'
TFTP_SERVER_IP = '192.168.1.5'
CONFIG_FILE_NMAE = 'vrpcfg.cfg'

def load_sw_config(ip, user, password, tftp_server_ip,config_file_name):
    string_ip_sw = '_'.join(ip.split('.'))
    sw_expect = pexpect.spawn(f'telnet {ip}')
    sw_expect.expect(['Username:','User Name',],timeout=5)
    sw_expect.sendline(f'{user}')
    sw_expect.expect('Password:')
    sw_expect.sendline(f'{password}')
    name = sw_expect.expect(['*Q2309','*Q2326','*Q2328','*Q2352','*MES2308','*MES2408','*MES1124', pexpect.TIMEOUT],timeout=5)
    if name in [0,1,2,3]:
        sw_expect.sendline(f'tftp {tftp_server_ip} put {config_file_name} {string_ip_sw}.cfg')
        sw_expect.expect('*>')
        sw_expect.sendline('quit')
    elif name in [4,5,6]:
        sw_expect.sendline(f'copy startup-config tftp://{tftp_server_ip}/{string_ip_sw}.cfg')
        sw_expect.expect('*>')
        sw_expect.sendline('exit')
    elif name == 7:
        print(f'****** TELNET {ip} TIME_OUT! *********')
    sw_expect.close()
    return 0


    '''
    command copy config to file: 
    Huawei s2326 s2328 s2309 (192.168.1.250 admin admin123)
    tftp 192.168.1.5 put vrpcfg.cfg 10_10_10_23.cfg
    Eltex mes2308 mes2328 mes2408 mes2428 (192.168.1.251 admin admin)
    copy startup-config tftp://192.168.1.5/10_10_10.25.cfg
    Qtech qsw2850 qsw2870 qsw3470 qsw3750
    copy running-config tftp://192.168.1.5/10_10_10.25.cfg 
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
                # load_sw_config(h['ip'], USER, PASSWORD, TFTP_SERVER, FILE_CONFIG)




def scan_one_net(ip_range):
    # For runing programm in windows
    # Need also install nmap in windows
    # nmap_path = [r"C:\Program Files (x86)\Nmap\nmap.exe"]
    # nm = nmap.PortScanner(nmap_search_path=nmap_path)
    nm = nmap.PortScanner()
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
load_sw_config('192.168.1.250', USER, PASSWORD, TFTP_SERVER_IP, CONFIG_FILE_NMAE, )


