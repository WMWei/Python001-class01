import time
from concurrent.futures import ProcessPoolExecutor as proc_exe
from concurrent.futures import ThreadPoolExecutor as thread_exe
from concurrent.futures import as_completed
from multiprocessing import cpu_count, Lock

from tools import command_parse, ip_port_parse, save_as_json
from scanner import ip_scanner, port_scanner


# 一些常量
THREAD_MODE = 'thread'
PROCESS_MODE = 'proc'
IP_SCANNER = 'ping'
PORT_SCANNER = 'tcp'
MAX_CUP_SIZE = cpu_count()


# 运行多线程|进程
def run_scanner(concurrent_mode: str,
                concurrent_num: int,
                scanner_type: str,
                host_ports: 'iterable',) -> list:

    # 选择并发模式
    pool_exe = thread_exe
    mode_str = '线程'
    if concurrent_mode == PROCESS_MODE:
        pool_exe = proc_exe
        concurrent_num = min(concurrent_num, MAX_CUP_SIZE)
        mode_str = '进程'

    # 选择扫描类型
    scanner = port_scanner
    scan_str = '端口'
    if scanner_type == IP_SCANNER:
        scanner = ip_scanner
        scan_str = 'ip'

    # 记录扫描结果
    result = []

    print(f'---执行多{mode_str}扫描{scan_str}---')
    # lock = Lock()
    with pool_exe(concurrent_num,
                #   initializer=init_lock,
                #   initargs=(lock,)
                  ) as pool:
        futures_to_hp = {pool.submit(scanner, hp): hp for hp in host_ports}
        for future in as_completed(futures_to_hp):
            try:
                res = future.result()
            except Exception as e:
                print(f'扫描{futures_to_hp[future]}出现异常：{e}')
            else:
                if res:
                    result.append(res)
        # for res in pool.map(scanner, host_ports):
        #     if res:
        #         result.append(res)
    print(f'---多{mode_str}扫描{scan_str}结束---')
    return result


# 主程序
def main():
    
    start = time.time()
    # 样例数据
    # 实际使用可以直接使用args = command_parse()从命令行获取
    temp = [
        # "-n", 
        # "16",
        "-f",
        "tcp",
        "-ip",
        "127.0.0.1-127.0.0.5",
        "-v",
        "-m",
        "proc",
        "-w",
        "port_by_proc.json",
        "-p",
        "100-150"
    ]
    args = command_parse(temp)
    host_ports = ip_port_parse(args.ip,
                              args.p,
                              is_port=(args.f==PORT_SCANNER))
    print('程序开始运行...')
    available_ip_ports = run_scanner(concurrent_mode=args.m,
                        concurrent_num=args.n,
                        scanner_type=args.f,
                        host_ports=host_ports,)
    if args.w:
        save_as_json(available_ip_ports, args.w)
    if args.v:
        print(f'程序消耗总时间：{time.time()-start}s')


if __name__ == '__main__':
    main()


