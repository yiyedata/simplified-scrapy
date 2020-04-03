import gzip
import zlib
import sys,io

def decodeZip (page):
  if sys.version_info.major == 2:
    encoding = page.headers.get('Content-Encoding')
  else: 
    encoding = page.info().get('Content-Encoding')
  if encoding in ('gzip', 'x-gzip', 'deflate'):
      content = page.read()
      if encoding == 'deflate':
        page = _deflate(content)
      else:
        buf = io.BytesIO(content)
        data = gzip.GzipFile(fileobj=buf)
        page = data.read()
        data.close()
  return page
def _deflate(data):
  try:
    return zlib.decompress(data, -zlib.MAX_WBITS)
  except zlib.error:
    return zlib.decompress(data)