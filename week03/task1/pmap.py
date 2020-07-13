'''
基于多进程或多线程模型端口扫描器。

功能：
- 基于ping命令检测一个IP段是否可以ping通
- 探测目标IP是否开放了指定端口（1-1024），并在终端显示该主机全部开放的端口
- 扫描结果显示在终端，并使用json格式保存至文件
- 需考虑网络异常、超时等问题，增加必要的异常处理

命令行参数举例如下：
pmap.py -n 4 -f ping -ip 192.168.0.1-192.168.0.100
pmap.py -n 10 -f tcp -ip 192.168.0.1 -w result.json

-n：指定并发数量
-f ping：进行 ping 测试
-f tcp：进行 tcp 端口开放、关闭测试
-ip：连续 IP 地址支持 192.168.0.1-192.168.0.100 写法
-w：扫描结果进行保存
-m：proc|thread，指定扫描器使用多进程或多线程模型
-v：参数打印扫描器运行耗时

'''

# argparse用于解析命令行参数
import argparse
import time
import json
import multiprocessing
# 使用dummy创建多线程，可用和multiprocessing的多进程共用相同的api
import multiprocessing.dummy
# 处理ip_scanner
import subprocess
# 处理port_scanner
import socket
import re
from functools import wraps

# 第三方库，用于解析IP字符串
from netaddr import iprange_to_cidrs


# 对ip参数进行解析
def ip_parse(ips: list) -> set:
    ip_set = set()
    for ip_str in ips:
        # 对形如192.168.0.1-192.168.0.100的Ip段进行处理
        # 普通192.168.0.1也处理成IPNetwork对象，方便后续统一使用
        ip_list = ip_str.split('-')
        for ip in iprange_to_cidrs(ip_list[0], ip_list[-1]):
            # 去重
            ip_set.add(ip)
    return ip_set


# 解析命令行参数
def cmd_parser() -> 'argparse.Namespace':
    '''
    pmap.py -n 4 -f ping -ip 192.168.0.1-192.168.0.100 -m proc
    pmap.py -n 10 -f tcp -ip 192.168.0.1 -w result.json -m thread -v
    '''
    parser = argparse.ArgumentParser(
        description='端口扫描器，检查ip或端口是否开放')
    parser.add_argument(
        '-n',
        type=int,
        required=True,
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
    parser.add_argument(
        '-w',
        # type=,
        default=None,
        help='指定存储文档'
        )
    parser.add_argument(
        '-m',
        choices=('proc', 'thread'),
        default='proc',
        help='多进程/多线程模式'
        )
    parser.add_argument(
        '-v',
        action='store_true',
        help='参数打印扫描器运行耗时'
        )
    args = parser.parse_args()
    return args


class IpCheck:
    def __init__(self,
                concurrent: int,
                func: str,
                ips: 'set(netaddr.IPNetwork)',
                mode: str,
                file: str,):
        # 进程|线程数
        self.concurrent = concurrent
        # 功能 ping|tcp
        self.func = func
        # 待检测ip集合
        self.check_ips = ips
        # 存储文件
        # self.file = open(file, 'a')  #
        self.file = file
        # 运行模式 proc|thread
        self.mode = mode
        # 可用ip|port
        self.available_ip_ports = []
    
    # ping
    def ip_scanner(self, ip):
        reg = re.compile('100% 丢失')
        res = subprocess.Popen(['ping.exe', f'{ip}'],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True)
        # windows cmd默认输出编码cp936
        output = res.stdout.read().decode('cp936')
        if reg.findall(output):
            print(f'{ip} 不可用')
            return None
        else:
            print(f'{ip} 可用')
            return str(ip)
    
    # tcp
    def port_scanner(self, ip_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # sock.settimeout(10)
            # sock.connect(ip_port)
            result = sock.connect_ex((str(ip_port[0]), ip_port[1]))
            if result == 0:
                print(f'{ip_port[0]}:{ip_port[1]} 可用')
                return f'{ip_port[0]}:{ip_port[1]}'
            return None

    # 保存
    def save(self,):
        if self.file:
            with open(self.file, 'w') as f:
                try:
                    json.dump(self.available_ip_ports, f, indent=4)
                except Exception as _:
                    print(f'文件存储失败')

    def run(self,):
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
                    result = pool.imap_unordered(self.ip_scanner, ips)
                else:
                    ip_ports = ((ip, port) for ip in ips for port in range(1, 1025))
                    result = pool.imap_unordered(self.port_scanner, ip_ports)
                for res in result:
                    if res:
                        self.available_ip_ports.append(res)
        # 保存
        self.save()
        print(f'---主{print_str}结束---')


if __name__ == '__main__':
    start = time.time()
    args = cmd_parser()
    ip_check = IpCheck(
        concurrent=args.n,
        func=args.f,
        ips=ip_parse(args.ip),
        mode=args.m,
        file=args.w,
    )
    ip_check.run()
    elapsed = time.time() - start
    if args.v:
        print(f'总耗时{elapsed}s')