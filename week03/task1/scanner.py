import subprocess
import socket
import re
import locale
from multiprocessing import Lock


print_lock = Lock()
# Lock初始化
# 由于在进程池不能pickle序列化普通的multiprocessing.Lock()
# 因此不能直接将lock对象当作参数传入进程执行的函数，需要在创建Pool时初始化
# def init_lock(lock: Lock):
#     global print_lock
#     print_lock = lock


def ip_scanner(ip: str,) -> str:
    reg = re.compile('100% 丢失')
    res = subprocess.Popen(['ping', ip],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True)

    output = res.stdout.read().decode(locale.getpreferredencoding(False))
    if not reg.findall(output,):
        with print_lock:
            print(f'#{ip} 可用')
        return ip
    return None

# port 扫描
def port_scanner(ip_port: tuple,) -> tuple:
    ip, port = ip_port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        conn = sock.connect_ex((ip, port))
        if conn == 0:
            with print_lock:
                print(f'#{ip}:{port} 可用')
            return (ip, port)
        return None


