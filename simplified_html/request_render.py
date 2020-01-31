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
    pass
    # if res.request.resourceType in ['xhr']:
    #   print(res.request.url)
  async def afterNewPage(self,page):
    pass
  async def _get(self,url,js=None,delay=0):
    browser = await self.browser()
    page = await browser.newPage()
    await self.afterNewPage(page)
    await page.setRequestInterception(True)
    page.on('request', self.inject_request)
    page.on('response',self.inject_response)
    await page.goto(url)
    if(js):
      await page.evaluate(js)
    else:
      await page.evaluate(
          '''() =>{Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    if delay:
      await page.waitFor(delay)
    doc = await page.content()
    cookies = await page.cookies()
    await page.close()
    return (doc,cookies)
  
  async def _close(self):
    if hasattr(self, "_browser"):
      await self._browser.close()

class RequestRender():
  def __init__(self, options={}, verify : bool = False, headless : bool = True,
                browser_args : list = ['--disable-infobars','--no-sandbox']):
                #--proxy-server="https=proxy1:80;http=socks4://baz:1080"
    if(not options): options={}
    self.options = options
    self.verify = verify
    self.headless = headless
    self.__browser_args = browser_args
    if(options.get('headless') != None):
      self.headless=options.get('headless')
    if(options.get('verify') != None):
      self.verify=options.get('verify')
  async def __browser(self):
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
    pass
    # if res.request.resourceType in ['xhr']:
    #   print(res.request.url)
  async def afterNewPage(self,page):
    await page.setRequestInterception(True)
    page.on('request', self.inject_request)
    page.on('response',self.inject_response)
    
  async def afterGoto(self,page,js):
    if(js):
      await page.evaluate(js)
    else:
      await page.evaluate(
          '''() =>{Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
  async def _get(self,url,options=None,js=None,delay=0):
    browser = await self.__browser()
    page = await browser.newPage()
    await self.afterNewPage(page)
    await page.goto(url,options)
    if( options and options.get('waitForNavigation')):
      del options['waitForNavigation']
      await page.waitForNavigation(options)
    await self.afterGoto(page,js)
    if delay:
      await page.waitFor(delay)
    doc = await page.content()
    cookies = await page.cookies()
    # print (cookies)
    await page.close()
    return (doc,cookies)
  
  async def _close(self):
    if hasattr(self, "_browser"):
      await self._browser.close()

  def get(self,url,callback,options=None,extr_data=None,js=None,selectorOrFunctionOrTimeout=0):
    # try:
     asyncio.get_event_loop().run_until_complete(self._getContent(url,callback,options,extr_data,js,selectorOrFunctionOrTimeout))
    # except Exception as err:
    #   print (err)
  def getCookies(self,url,callback,options=None,extr_data=None,js=None,selectorOrFunctionOrTimeout=0):
    try:
      asyncio.get_event_loop().run_until_complete(self._getCookies(url,callback,options,extr_data,js,selectorOrFunctionOrTimeout))
    except Exception as err:
      print (err)

  async def _getAsync(self,url,options=None,js=None,delay=0):
    u=url
    if(isinstance(url,dict)):
      u=url.get('url')
    await self.__browser()
    res = await self._get(u,options,js,delay)
    return res
  async def _getContent(self,url,callback,options=None,extr_data=None,js=None,delay=0):
    res = await self._getAsync(url,options,js,delay)
    if(callback):
      callback(res[0],url,extr_data)
    return res[0]
  async def _getCookies(self,url,callback,options=None,extr_data=None,js=None,delay=0):
    res = await self._getAsync(url,options,js,delay)
    cookies = []
    for cookie in res[1]:
      cookies.append(cookie['name']+'='+cookie['value'])
    if(callback):
      callback(cookies,url,extr_data)
    return cookies

  def close(self):
    asyncio.get_event_loop().run_until_complete(self._close())
      
