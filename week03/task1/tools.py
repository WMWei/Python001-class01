import argparse
import json
import os.path
import os

import netaddr



# 命令行解析
def command_parse(*args, **kwargs) -> 'argparse.Namespace':
    '''
    功能：解析命令行命令
    命令示例：
    pmap.py -n 4 -f ping -ip 192.168.0.1-192.168.0.100 -m proc
    pmap.py -n 10 -f tcp -ip 192.168.0.1 -w result.json -m thread -v
    
    -n: int;
    -f: str; ping | tcp
    -ip: str; 192.168.0.1-192.168.0.100 | 192.168.0.1, 192.168.0.2, ...
    -p: str; 1-1024 | 443, 27017, ...
    -m: str; proc | thread
    -w: str; path/to/xxx.json
    -v: bool;
    '''
    parser = argparse.ArgumentParser(description='端口扫描器，检查ip或端口是否开放')
    parser.add_argument('-ip',
                        required=True,
                        type=str,
                        nargs='+',
                        help='-ip <a.a.a.a-b> | <b.b.b.b, c.c.c.c>, 指定ip列表')
    parser.add_argument('-p',
                        type=str,
                        nargs='*',
                        default='1-1024',
                        help='-p <port1, port2, ...> | <port1-port2>, 指定port列表')
    parser.add_argument('-n',
                        type=int,
                        default=4,
                        help='-n <concurrence>, 指定进程/线程数')
    parser.add_argument('-f',
                        type=str,
                        choices=('ping', 'tcp'),
                        default='ping',
                        help='-f ping | tcp, 指定扫描ip还是扫描端口')
    parser.add_argument('-m',
                        type=str,
                        choices=('proc', 'thread'),
                        default='thread',
                        help='-m proc | thread, 多进程/多线程模式')
    parser.add_argument('-w',
                        type=str,
                        # action='store_const',
                        # const='result.json',
                        default=None,
                        help='-w <path/to/json.json>, 指定存储文档路径')
    parser.add_argument('-v',
                        action='store_true',
                        default=False,
                        help='-v, 指定是否显示消耗时间')
    return parser.parse_args(*args, **kwargs)

# ip地址解析
def ip_parse(ips: list):
    '''
    解析形如['192.18.0.1-100', '192.168.101.1']这样的ip字符串列表
    返回解析后的ip字符串生成器

    >>> list(ip_parse(['192.168.0.1']))
    ['192.168.0.1']
    >>> list(ip_parse(['192.168.0.1-192.168.0.3']))
    ['192.168.0.1', '192.168.0.2', '192.168.0.3']
    >>> list(ip_parse(['192.168.0.1-192.168.0.3', '127.0.0.1']))
    ['192.168.0.1', '192.168.0.2', '192.168.0.3', '127.0.0.1']
    '''
    for ip_str in ips:
        ip_list = ip_str.split('-')
        if len(ip_list) > 1:
            for ipnetwork in netaddr.iprange_to_cidrs(*ip_list):
                yield from map(str, ipnetwork)
        else:
            yield from ip_list

# port解析
def port_parse(ports: list):
    '''
    解析形如['1-1024', '443']这样的port字符串列表
    返回解析后的port数值生成器

    >>> list(port_parse(['1-3']))
    [1, 2, 3]
    >>> list(port_parse(['1-3', '443']))
    [1, 2, 3, 443]
    '''
    for port_str in ports:
        port_list = port_str.split('-')
        if not all(s.isdigit() for s in port_list):
            raise ValueError('port must be int')
        if len(port_list) > 1:
            start = int(port_list[0])
            end = int(port_list[1])
            while start <= end:
                yield start
                start += 1
        else:
            yield int(port_list[0])

# 将ip与port组合
def ip_port_parse(ips: list, ports: list, is_port: bool=False):
    parse_ips = ip_parse(ips)
    if is_port:
        parse_ports = port_parse(ports)
        return ((ip, port) for ip in parse_ips for port in parse_ports)
    return parse_ips

# 检查保存路径
# 得到 path/to/file.json 的路径
def check_path(fp: str) -> str:
    dir_path, file = os.path.split(fp)
    file_name, ext = os.path.splitext(file)
    if dir_path:
        try:
            os.makedirs(dir_path)
        except Exception as _:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            print(f'提供的文件存储目录存在问题，将修改为当前目录{dir_path}')
    else:
        dir_path = os.path.dirname(os.path.abspath(__file__))
    if ext != '.json':
        file = file_name + '.json'
    return os.path.join(dir_path, file)

# 保存内容至json文件
def save_as_json(obj: 'Any', fp: str):
    checked_fp = check_path(fp)
    with open(checked_fp, 'w', encoding='utf-8') as f:
        try:
            json.dump(obj, f, indent=4)
            print(f'保存文件至{checked_fp}成功')
        except Exception as e:
            print(f'保存文件至{checked_fp}失败，失败原因：{e}')
    


if __name__ == '__main__':
    s = port_parse(None)
    print(s)


