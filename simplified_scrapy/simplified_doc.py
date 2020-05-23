#!/usr/bin/python
#coding=utf-8
from simplified_scrapy.core.regex_helper import *
from simplified_scrapy.core.request_helper import extractHtml, _getResponseStr
from simplified_scrapy.extracter import ExtractModel
from simplified_scrapy.core.utils import absoluteUrl
from simplified_scrapy.core.regex_dic import RegexDict, RegexDictNew
from simplified_scrapy.core.listex import List


class SimplifiedDoc(RegexDict):
    def __init__(self, html=None, start=None, end=None, before=None, edit=True):
        # self._rootNode=self
        self._editFlag = edit
        self._elements = []
        self['html'] = None
        self.last = None
        if (not html): return
        html = _getResponseStr(html)
        sec = getSection(html, start, end, before)
        if (sec): html = html[sec[0]:sec[1]]
        html = preDealHtml(html)
        self['html'] = html

    def loadHtml(self, html, start=None, end=None, before=None):
        if (not html): return
        html = _getResponseStr(html)
        sec = getSection(html, start, end, before)
        if (sec): html = html[sec[0]:sec[1]]
        html = preDealHtml(html)
        self['html'] = html

    def listA(self, html=None, url=None, start=None, end=None, before=None):
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        return List(listA(html, url, start, end, before))

    def listImg(self, html=None, url=None, start=None, end=None, before=None):
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        return List(listImg(html, url, start, end, before))

    def getElementByID(self, id, html=None, start=None, end=None, before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        self.last = getElementByID(id, html, start, end, before)
        self.last = RegexDictNew(self.last, root=self)
        return self.last

    def getElementByText(self,
                         text,
                         tag=None,
                         html=None,
                         start=None,
                         end=None,
                         before=None):
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        self.last = getElementByText(text, tag, html, start, end, before)
        self.last = RegexDictNew(self.last, root=self)
        return self.last

    def getElementByReg(self,
                        regex,
                        tag=None,
                        html=None,
                        start=None,
                        end=None,
                        before=None):
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        self.last = getElementByReg(regex, tag, html, start, end, before)
        self.last = RegexDictNew(self.last, root=self)
        return self.last

    def getElementsByReg(self,
                         regex,
                         tag=None,
                         html=None,
                         start=None,
                         end=None,
                         before=None):
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        lst = List()
        ele = getElementByReg(regex, tag, html, start, end, before)
        ele = RegexDictNew(ele, root=self)
        while ele:
            lst.append(ele)
            s = ele._end
            ele = getElementByReg(regex, tag, html, s, end)
            if not ele: break
            ele = RegexDictNew(ele, root=self, s=s)
            if ele._end >= len(html):
                break

        return lst

    def getElementByTag(self,
                        tag,
                        html=None,
                        start=None,
                        end=None,
                        before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        self.last = getElementByTag(tag, html, start, end, before)
        self.last = RegexDictNew(self.last, root=self)
        return self.last

    def getElementByClass(self,
                          className,
                          html=None,
                          start=None,
                          end=None,
                          before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        self.last = getElementByClass(className, html, start, end, before)
        self.last = RegexDictNew(self.last, root=self)
        return self.last

    def _convert2lst(self, eles):
        lst = List()
        if (eles):
            for e in eles:
                dic = RegexDictNew(e, root=self)
                lst.append(dic)
        return lst

    def getElementsByTag(self,
                         tag,
                         html=None,
                         start=None,
                         end=None,
                         before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        eles = getElementsByTag(tag, html, start, end, before)
        return self._convert2lst(eles)

    def getElementsByClass(self,
                           className,
                           html=None,
                           start=None,
                           end=None,
                           before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        eles = getElementsByClass(className, html, start, end, before)
        return self._convert2lst(eles)

    def getElementByAttr(self,
                         attr,
                         value,
                         html=None,
                         start=None,
                         end=None,
                         before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        self.last = getElementByAttr(attr, value, html, start, end, before)
        self.last = RegexDictNew(self.last, root=self)
        return self.last

    def getElement(self,
                   tag,
                   attr='class',
                   value=None,
                   html=None,
                   start=None,
                   end=None,
                   before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        self.last = getElement(tag, attr, value, html, start, end, before)
        self.last = RegexDictNew(self.last, root=self)
        return self.last

    def removeElement(self,
                      tag,
                      attr='class',
                      value=None,
                      html=None,
                      start=None,
                      end=None,
                      before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        self['html'] = removeElement(tag, attr, value, html, start, end,
                                     before)
        return self['html']

    def removeElements(self,
                       tag,
                       attr='class',
                       value=None,
                       html=None,
                       start=None,
                       end=None,
                       before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        while True:
            tmp = removeElement(tag, attr, value, html, start, end, before)
            if tmp != html:
                html = tmp
            else:
                break
        self['html'] = html
        return self['html']

    def getElements(self,
                    tag,
                    attr='class',
                    value=None,
                    html=None,
                    start=None,
                    end=None,
                    before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        eles = getElements(tag, attr, value, html, start, end, before)
        return self._convert2lst(eles)

    def getParent(self,
                  tag=None,
                  attr=None,
                  value=None,
                  html=None,
                  start=None,
                  end=None,
                  before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        self.last = getParent(tag, attr, value, html, start, end, before)
        self.last = RegexDictNew(self.last, root=self)
        return self.last

    def getChildren(self,
                    html=None,
                    tag=None,
                    start=None,
                    end=None,
                    before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        eles = getChildren(html, tag, start, end, before)
        return self._convert2lst(eles)

    def getNexts(self,
                 attr,
                 value,
                 html,
                 tag=None,
                 start=None,
                 end=None,
                 before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        eles = getNexts(attr, value, html, tag, start, end, before)
        return self._convert2lst(eles)

    def getElementByStr(self, html=None, start=None, end=None, before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        s, e = getSection(html, start, end, before)
        if s < 0 or e < 0:
            return Dict()
        if end: e += len(end)
        ele = Dict()
        ele.html = html[s:e]
        ele._start = s
        ele._end = e
        return ele

    def getElementsByStr(self, html=None, start=None, end=None, before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        lst = List()
        ele = None
        while True:
            s = 0
            if ele: s = ele._end
            h = html[s:]
            ele = self.getElementByStr(h, start, end, before)
            if (not ele): break
            ele._start += s
            ele._end += s
            lst.append(ele)
        return lst

    def getSection(self, html=None, start=None, end=None, before=None):
        return self._getSection(html, start, end, before)[0]

    def getSectionByReg(self,
                        regex,
                        html=None,
                        group=0,
                        start=None,
                        end=None,
                        before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        return getOneByReg(html, regex, group, start, end, before)

    def getSectionsByReg(self,
                         regex,
                         html=None,
                         group=0,
                         start=None,
                         end=None,
                         before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        return getListByReg(html, regex, group, start, end, before)

    def _getSection(self, html=None, start=None, end=None, before=None):
        if html: html = preDealHtml(html)
        if (not html): html = self.html
        if (not html and self.last): html = self.last.html
        s, e = getSection(html, start, end, before)
        l = 0
        if before: l = len(before)
        elif start: l = len(start)
        el = 0
        if end: el = len(end)
        if s < 0:
            s = 0
            l = 0
        if e < 0:
            e = len(html)
            el = 0
        return (html[s + l:e], s, e + el)

    def removeHtml(self, html, separator='', tags=None):
        return removeHtml(html, separator, tags)

    def trimHtml(self, html):
        return trimHtml(html)

    def replaceReg(self, html, regex, new):
        if html:
            return replaceReg(html, regex, new)
        elif self.html:
            self['html'] = replaceReg(self.html, regex, new)
            return self.html
        elif self.last:
            self.last['html'] = replaceReg(self.last.html, regex, new)
            return self.last.html
        return html

    def absoluteUrl(self, baseUrl, url):
        return absoluteUrl(baseUrl, url)

    def getObjByModel(self, html, url=None, models=[{"Type": 3}], title=None):
        if (not isinstance(models, dict) and not isinstance(models, list)):
            models = json.loads(models)
        if (isinstance(models, dict)):
            models = [models]
        return extractHtml(url, html, models, None, title)
