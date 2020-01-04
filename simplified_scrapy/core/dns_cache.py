import socket,time
_dnscache = {}
def _getaddrinfo(*args, **kwargs):
  if args[0] in _dnscache:
    return _dnscache[args[0]]
  else:
    _dnscache[args[0]] = socket._getaddrinfo(*args, **kwargs)
    return _dnscache[args[0]]
if not hasattr(socket, '_getaddrinfo'):
  socket._getaddrinfo = socket.getaddrinfo
  socket.getaddrinfo = _getaddrinfo
def resetCache(domain):
  _dnscache[domain]=None