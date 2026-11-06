import nmap
import threading
import os

# Файл со списком сетей (по одной в строке, например 192.168.1.0/24)
INPUT_FILE = "nets.lst"
# Файл для записи доступных IP-адресов
OUTPUT_FILE = "hosts.lst"

# Блокировка для безопасной записи в файл из разных потоков
write_lock = threading.Lock()


def scan_network(network, results):
    """
    Сканирует указанную сеть и добавляет найденные IP в список results.
    Использует аргумент -sn для ping-сканирования (только обнаружение хостов).
    """
    nm = nmap.PortScanner()
    try:
        # -sn: Ping scan - отключает сканирование портов, только обнаружение хостов
        nm.scan(hosts=network, arguments='-sn')
        for host in nm.all_hosts():
            if nm[host].state() == 'up':
                results.append(host)
                print(f"[+] {host} доступен (сеть {network})")
    except Exception as e:
        print(f"[!] Ошибка при сканировании сети {network}: {e}")


def main():
    # Проверка наличия входного файла
    if not os.path.exists(INPUT_FILE):
        print(f"Файл {INPUT_FILE} не найден.")
        return

    # Чтение списка сетей
    with open(INPUT_FILE, "r") as f:
        networks = [line.strip() for line in f if line.strip()]

    if not networks:
        print(f"Файл {INPUT_FILE} пуст.")
        return

    print(f"Загружено сетей для сканирования: {len(networks)}")

    # Общий список для сбора результатов из всех потоков
    all_hosts = []

    # Создание и запуск потоков
    threads = []
    for net in networks:
        t = threading.Thread(target=scan_network, args=(net, all_hosts))
        t.start()
        threads.append(t)

    # Ожидание завершения всех потоков
    for t in threads:
        t.join()

    # Запись результатов в файл
    with write_lock:
        with open(OUTPUT_FILE, "w") as f:
            for ip in all_hosts:
                f.write(ip + "\n")

    print(f"Сканирование завершено. Найдено хостов: {len(all_hosts)}")
    print(f"Результаты сохранены в {OUTPUT_FILE}")


if __name__ == "__main__":
    main()