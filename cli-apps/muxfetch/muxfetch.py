import os
import platform
import getpass
import distro
import subprocess
import math

def hardware():
    distro_inf =  f'{distro.name()} {distro.version()}'
    cpu_info = subprocess.check_output("cat /proc/cpuinfo | grep 'model name' | head -1", shell=True).strip().decode()
    # Extract the CPU name from the outputcpu_name
    cpu_name = cpu_info.split(":")[1].strip()
    return distro_inf, cpu_name
def packages():
    package_managers = {
        "apt": "dpkg-query --help",
        "yum": "yum --version",
        "dnf": "dnf --version",
        "pacman": "pacman --version",
        "brew": "brew --version",
        "zypper": "zypper --version",
        "port": "port version"
    }

    for manager, command in package_managers.items():
        try:
            subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return manager
        except subprocess.CalledProcessError:
            continue
        except FileNotFoundError:
            continue
    return None

def get_total_memory_mib():
    try:
        output = subprocess.check_output("grep MemTotal /proc/meminfo", shell=True).decode()
        total_memory_kb = int(output.split()[1])
        # Convert KB to MiB
        total_memory_mib = total_memory_kb / 1024
        # Round up to the nearest whole number
        return math.ceil(total_memory_mib)
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

def main():
    distro_inf, cpu_inf = hardware()
    package_inf = packages()
    info_string = f"{getpass.getuser()}@{platform.node()}"
    under_string = len(info_string) * "-"
    mem_inf = get_total_memory_mib()
    shell = os.getenv('SHELL', 'Unknown shell')
    shell_name = shell.split('/')[-1]

    print(f"""
    .--.       \033[91m█\033[0m  {info_string}
   |o_o |      \033[92m█\033[0m  {under_string}
   |;_/ |      \033[93m█\033[0m    {distro_inf}
  //   \ \\     \033[94m█\033[0m    {cpu_inf}
 (|     | )    \033[95m█\033[0m    {package_inf}
 /'\_   _/`\\   \033[96m█\033[0m    {shell_name}
 \___)=(___/   \033[97m█\033[0m  󰍛  {mem_inf} MiB
    """)

if __name__ == "__main__":
    main()
