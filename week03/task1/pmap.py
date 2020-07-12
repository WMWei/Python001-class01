'''
基于多进程或多线程模型端口扫描器，即通过一台主机发起向另一主机的常用端口发起连接，探测目标主机是否开放了指定端口（1-1024）。

功能：
- 基于ping命令检测一个IP段是否可以ping通
  - ping通返回主机IP
  - 否则忽略连接。
- 可以快速检测一个指定IP地址开放了哪些tcp端口，并在终端显示该主机全部开放的端口
- 扫描结果显示在终端，并使用 json 格式保存至文件

命令行参数举例如下：
pmap.py -n 4 -f ping -ip 192.168.0.1-192.168.0.100
pmap.py -n 10 -f tcp -ip 192.168.0.1 -w result.json

-n：指定并发数量。
-f ping：进行 ping 测试
-f tcp：进行 tcp 端口开放、关闭测试。
-ip：连续 IP 地址支持 192.168.0.1-192.168.0.100 写法。
-w：扫描结果进行保存

[-m proc|thread]：指定扫描器使用多进程或多线程模型
-v：参数打印扫描器运行耗时 (用于优化代码)

其他要求：
- 需考虑网络异常、超时等问题，增加必要的异常处理。
- 建立tcp连接的工具不限，可以使用telnet、nc或Python自带的socket套接字。

'''
# 用于解析命令行参数
import argparse
import time
import json
import multiprocessing
import multiprocessing.dummy
import subprocess
import socket
import re
from functools import wraps

# 用于解析IP字符串
from netaddr import IPNetwork, iprange_to_cidrs


# 对ip参数进行解析
def ip_parse(ips: list):
    ip_set = set()
    for ip_str in ips:
        # 对形如192.168.0.1-192.168.0.100的Ip段进行处理
        ip_list = ip_str.split('-')
        for ip in iprange_to_cidrs(ip_list[0], ip_list[-1]):
            # 去重
            ip_set.add(ip)
    return ip_set


# 解析命令行参数
def cmd_parser():
    '''
    pmap.py -n 4 -f ping -ip 192.168.0.1-192.168.0.100
    pmap.py -n 10 -f tcp -ip 192.168.0.1 -w result.json
    [-m proc|thread]：指定扫描器使用多进程或多线程模型
    -v：参数打印扫描器运行耗时 (用于优化代码)
    '''
    parser = argparse.ArgumentParser(description='端口扫描器，检查ip或端口是否开放')
    parser.add_argument(
        '-n',
        type=int,
        help='指定进程/线程数'
        )
    parser.add_argument(
        '-f',
        choices=('ping', 'tcp'),
        required=True,
        help='指定扫描ip还是扫描端口'
        )
    parser.add_argument(
        '-ip',
        nargs='+',
        required=True,
        help='指定ip列表',
        )
    parser.add_argument('-w', help='指定存储文档')
    parser.add_argument(
        '-m',
        choices=('proc', 'thread'),
        default='proc',
        help='多进程/多线程模式'
        )
    parser.add_argument('-v', action='store_true', help='参数打印扫描器运行耗时')
    args = parser.parse_args()
    return args




class IpCheck:
    def __init__(self,
                concurrent: int,
                func: str,
                ips: 'set(netaddr.IPNetwork)',
                mode: str,
                file: str,
                show_elapsed: bool,):
        # 进程|线程数
        self.concurrent = concurrent
        # 功能 ping|tcp
        self.func = func
        # 待检测ip集合
        self.check_ips = ips
        # 可用ip
        #self.available_ips = multiprocessing.Queue()
        # 存储文件
        self.file = open(file, 'a')  #
        # 总耗时
        # self.elapsed = None
        # 是否显示耗时
        self.show_elapsed = show_elapsed
        self.elapsed = None
        # 运行模式 proc|thread
        self.mode = mode
    
    # ping
    def ip_scanner(self, ip):
        # print(f'===检查 {ip} 是否可用===')
        # print('=' * 20)
        reg = re.compile('100% 丢失')
        res = subprocess.Popen(['ping.exe', f'{ip}'],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True)
        # windows cmd默认输出编码cp936
        output = res.stdout.read().decode('cp936')
        if reg.findall(output):
            print(f'{ip} 不可用')
        else:
            print(f'{ip} 可用')
            json.dump(f'{ip}', self.file)
            #self.available_ips.put(ip)
    
    # tcp
    def port_scanner(self, ip_port):
        # print(f'===检查 {ip_port[0]}:{ip_port[1]} 是否可用===')
        # try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # sock.settimeout(10)
            # sock.connect(ip_port)
            result = sock.connect_ex((str(ip_port[0]), ip_port[1]))
            if result == 0:
                print(f'{ip_port[0]}:{ip_port[1]} 可用')
                json.dump(f'{ip_port[0]}:{ip_port[1]}', self.file)

        # except Exception as _:
        #     # print(f'{ip_port[0]}:{ip_port[1]} 不可用')
        #     pass

    def run(self,):
        start = time.time()
        # multiprocessing.dummy.Pool提供多线程
        pool_func = multiprocessing.dummy.Pool
        print_str = '线程'
        concurrent = self.concurrent
        if self.mode == 'proc':
            # 进程
            pool_func = multiprocessing.Pool
            print_str = '进程'
            concurrent = min(self.concurrent, multiprocessing.cpu_count())
        print(f'---主{print_str}开始运行---')
        with pool_func(concurrent) as pool:
            for ips in self.check_ips:
                if self.func == 'ping':
                    pool.map(self.ip_scanner, ips)
                else:
                    ip_ports = ((ip, port) for ip in ips for port in range(1, 1025))
                    pool.map(self.port_scanner, ip_ports)
        self.file.close()
        print(f'---主{print_str}结束---')
        self.elapsed = time.time() - start
        if self.show_elapsed:
            print(f'总耗时{self.elapsed}s')


if __name__ == '__main__':
    args = cmd_parser()
    ip_check = IpCheck(
        concurrent=args.n,
        func=args.f,
        ips=ip_parse(args.ip),
        mode=args.m,
        file=args.w,
        show_elapsed=args.v
    )
    ip_check.run()