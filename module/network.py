import requests
from utils.common import is_using_proxy


url_override_map = {
    'https://github.com': 'https://ghproxy.com/https://github.com',
    'https://archive.org': 'https://archive.e6ex.com',
}


def get_global_options():
    if is_using_proxy():
        import urllib.request
        proxies = urllib.request.getproxies()
        global_options = {
            'split': '16',
            'max-connection-per-server': '16',
            'min-split-size': '1M',
            'all-proxy': iter(proxies.values()).__next__()
        }
    else:
        global_options = {
            'split': '16',
            'max-connection-per-server': '16',
            'min-split-size': '4M',
        }
    return global_options


def get_finial_url(origin_url: str):
    if is_using_proxy():
        return origin_url
    for k in url_override_map:
        if origin_url.startswith(k):
            return origin_url.replace(k, url_override_map[k])
    return origin_url


def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def get_available_port() -> int:
    import random
    while True:
        port = random.randint(20000, 60000)
        if not is_port_in_use(port):
            break
    return port