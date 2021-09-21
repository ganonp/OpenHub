import os
import socket
import multiprocessing
import subprocess
import os
import logging

logger = logging.getLogger(__name__)


def pinger(job_q, results_q):
    """
    Do Ping
    :param job_q:
    :param results_q:
    :return:
    """
    while True:

        ip = job_q.get()

        if ip is None:
            break

        try:
            logger.debug('Pinging: ' + str(ip))
            subprocess.check_call(['/usr/bin/ping', '-c', '1', '-W', '0.5', '-w', '0.5', str(ip)], timeout=0.5,
                                  shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.debug('added: ' + str(ip))
            results_q.put(ip)
        except Exception as e:
            logger.debug(str(e))
            logger.debug(str(e.with_traceback(e.__traceback__)))
            pass


def get_my_ip():
    """
    Find my IP address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    logger.debug('My IP: ' + str(ip))

    return ip


def map_network(pool_size=4):
    """
    Maps the network
    :param pool_size: amount of parallel ping processes
    :return: list of valid ip addresses
    """

    ip_list = list()

    # get my IP and compose a base like 192.168.1.xxx
    ip_parts = get_my_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

    # prepare the jobs queue
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]

    for p in pool:
        p.start()

    # cue hte ping processes
    for i in range(1, 255):
        jobs.put(base_ip + '{0}'.format(i))

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    # collect he results
    while not results.empty():
        ip = results.get()
        ip_list.append(ip)

    return ip_list


import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
        logger.debug('My IP: ' + str(IP))

    return IP


def non_multiprocessing():
    ip_parts = get_my_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

    ips = []
    for i in range(1, 255):
        ip = base_ip + '{0}'.format(i)
        print(str(ip))

        try:
            subprocess.check_call(['/usr/bin/ping', '-c', '1', '-W', '0.3', '-w', '0.3', str(ip)], timeout=0.3,
                                  shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.debug('adding ' + str(ip))
            ips.append(ip)
        except Exception as a:
            logger.debug(a)
    logger.debug(str(ips))
    return ips


if __name__ == '__main__':
    print('Mapping...')
    lst = map_network()
    print(lst)
