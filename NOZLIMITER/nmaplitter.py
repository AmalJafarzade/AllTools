import nmap
import subprocess
from tqdm import tqdm
import netifaces as ni
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

devices_info = []

def print_banner():
    banner = f"""
{Fore.RED}.__   __.   ______    ________   __       __  .___  ___.  __  .___________. _______ .______      
{Fore.RED}|  \ |  |  /  __  \  |       /  |  |     |  | |   \/   | |  | |           ||   ____||   _  \     
{Fore.RED}|   \|  | |  |  |  | `---/  /   |  |     |  | |  \  /  | |  | `---|  |----`|  |__   |  |_)  |    
{Fore.RED}|  . `  | |  |  |  |    /  /    |  |     |  | |  |\/|  | |  |     |  |     |   __|  |      /     
{Fore.RED}|  |\   | |  `--'  |   /  /----.|  `----.|  | |  |  |  | |  |     |  |     |  |____ |  |\  \----.
{Fore.RED}|__| \__|  \______/   /________||_______||__| |__|  |__| |__|     |__|     |_______|| _| `._____|
{Style.RESET_ALL}                                                                                              
    """
    print(banner)

def get_network_range():
    gateways = ni.gateways()
    default_gateway = gateways['default'][ni.AF_INET][0]
    interface = gateways['default'][ni.AF_INET][1]
    
    addr = ni.ifaddresses(interface)
    netmask = addr[ni.AF_INET][0]['netmask']
    
    ip = addr[ni.AF_INET][0]['addr']
    network_prefix = sum(bin(int(x)).count('1') for x in netmask.split('.'))
    
    network_range = f"{default_gateway.rsplit('.', 1)[0]}.0/{network_prefix}"
    return network_range

def scan_network():
    global devices_info
    network_range = get_network_range()
    print(f"Scanning network in range: {network_range}")
    nm = nmap.PortScanner()
    nm.scan(hosts=network_range, arguments='-sP')
    devices = []

    for host in nm.all_hosts():
        devices.append(nm[host]['addresses']['ipv4'])

    devices_info = scan_ports_and_os(devices)
    print("Scan completed.")

def scan_ports_and_os(devices):
    nm = nmap.PortScanner()
    results = []

    print("Scanning ports and OS...")
    for device in tqdm(devices, desc="Scanning devices"):
        try:
            nm.scan(device, arguments='-O -p 1-1024')
            device_info = nm[device] if device in nm.all_hosts() else {}
            open_ports = list(device_info['tcp'].keys()) if 'tcp' in device_info else []
            os_info = 'Unknown'

            if 'osclass' in device_info:
                os_info = f"{device_info['osclass'][0]['osfamily']} {device_info['osclass'][0]['osgen']}"

            results.append({
                'ip': device,
                'open_ports': open_ports,
                'os': os_info
            })
        except Exception as e:
            print(f"Error scanning device {device}: {e}")
            results.append({
                'ip': device,
                'open_ports': [],
                'os': 'Unknown'
            })

    return results

def display_hosts():
    global devices_info
    print("{:<5} {:<15} {:<20} {:<20}".format("Index", "IP Address", "Open Ports", "OS"))
    print("="*60)
    for i, result in enumerate(devices_info, 1):
        print("{:<5} {:<15} {:<20} {:<20}".format(i, result['ip'], ', '.join(map(str, result['open_ports'])), result['os']))

def block_device(index):
    global devices_info
    try:
        device = devices_info[index - 1]
        ip = device['ip']
        subprocess.call(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
        subprocess.call(["iptables", "-A", "OUTPUT", "-d", ip, "-j", "DROP"])
        print(f"Blocked device with IP: {ip}")
    except IndexError:
        print("Invalid index.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to block the device. Error: {e}. Please run the script with sudo.")

def main():
    print_banner()
    while True:
        command = input("evillimiter> ").strip()
        if command == "scan":
            scan_network()
        elif command == "hosts":
            display_hosts()
        elif command.startswith("block"):
            try:
                _, index = command.split()
                index = int(index)
                block_device(index)
            except ValueError:
                print("Usage: block <index>")
        elif command == "exit":
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
