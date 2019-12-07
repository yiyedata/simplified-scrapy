import asyncio
import pyppeteer
class _RequestRenderAsync():
  def __init__(self, options, verify, headless, browser_args):
    self.options = options
    self.verify = verify
    self.headless = headless
    self.__browser_args = browser_args
    if(options.get('headless') != None):
      self.headless=options.get('headless')
    if(options.get('verify') != None):
      self.verify=options.get('verify')
  async def browser(self):
    if not hasattr(self, "_browser"):
      self._browser = await pyppeteer.launch(self.options,
        ignoreHTTPSErrors=not(self.verify), headless=self.headless, args=self.__browser_args)
    return self._browser

  async def inject_request(self,req):
    """
    resourceType:
        document, stylesheet, image, media, font, script, texttrack, 
        xhr, fetch, eventsource, websocket, manifest, other
    """
    if req.resourceType in ['media','image']:
      await req.abort()
    else:
      await req.continue_()

  async def inject_response(self,res):
    if res.request.resourceType in ['xhr']:
      print(res.request.url)

  async def get(self,url,js=None):
    browser = await self.browser()
    page = await browser.newPage()
    await page.setRequestInterception(True)
    page.on('request', self.inject_request)
    page.on('response',self.inject_response)
    await page.goto(url)
    if(js):
      await page.evaluate(js)
    else:
      await page.evaluate(
          '''() =>{Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    doc = await page.content()
    cookies = page.cookies
    await page.close()
    return (doc,cookies)
  
  async def close(self):
    if hasattr(self, "_browser"):
      await self._browser.close()

class RequestRender():
  def __init__(self, options={}, verify : bool = False, headless : bool = True,
                 browser_args : list = ['--disable-infobars','--no-sandbox']):
    # self._options = options
    # self._verify = verify
    # self._headless = headless
    # self.__browser_args = browser_args
    self._request = _RequestRenderAsync(options,verify,headless,browser_args)
  def get(self,url,callback,extr_data=None,js=None):
    asyncio.get_event_loop().run_until_complete(self._getContent(url,callback,extr_data,js))
  def getCookies(self,url,callback,extr_data=None):
    asyncio.get_event_loop().run_until_complete(self._getCookies(url,callback,extr_data))

  async def getAsync(self,url,js=None):
    u=url
    if(not isinstance(url,str)):
      u=url.get('url')
    await self._request.browser()
    res = await self._request.get(u,js)
    return res
  async def _getContent(self,url,callback,extr_data=None,js=None):
    res = await self.getAsync(url,js)
    if(callback):
      callback(res[0],url,extr_data)
    return res[0]
  async def _getCookies(self,url,callback,extr_data=None):
    res = await self.getAsync(url)
    if(callback):
      callback(res[1],url,extr_data)
    return res[1]

  def close(self):
    asyncio.get_event_loop().run_until_complete(self._request.close())
      
