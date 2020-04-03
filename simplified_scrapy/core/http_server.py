from http.server import BaseHTTPRequestHandler, HTTPServer
import json
class WebApplication(object):
  _data=None
  def setData(self,data):
    if not self._data: return
    self._data['count10s'] = data[5]
    self._data['last_tm'] =data[-1]
    urlDic = {}
    if not self._data.get(data[2]):
      urlDic['success']=0
      urlDic['fail']=0
      urlDic['max_tm']=0
      urlDic['min_tm']=0
      urlDic['total_tm']=0
      self._data[data[2]]=urlDic
    else: urlDic = self._data[data[2]]
    if data[6]:
      urlDic['success']+=1
      self._data['success']+=1
    else:
      urlDic['fail']+=1
      self._data['fail']+=1
    if data[3]>urlDic['max_tm']:
      urlDic['max_tm']=data[3]
    if urlDic['min_tm']==0 or data[3]<urlDic['min_tm']:
      urlDic['min_tm']=data[3]
    urlDic['total_tm']+=data[3]

  def start(self,port=8787):
    self._data={'success':0,'fail':0,'last_tm':0}
    serverAddress = ('', port)
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
webAppState = WebApplication()
class RequestHandler(BaseHTTPRequestHandler):
  superclass = webAppState
  def do_GET(self):
    data = json.dumps(self.superclass._data)
    self.send_response(200)
    self.send_header("Content-Type", "application/json") # text/plain
    self.send_header("Content-Length", str(len(data)))
    self.end_headers()
    self.wfile.write(data.encode('utf-8'))
if __name__ == '__main__':
  webAppState._data={"test":1}
  webAppState.start(8080)

