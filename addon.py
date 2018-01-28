import os
import urllib2
import sys
import time
from urllib import urlencode
import xbmcaddon
import xbmcgui
import xbmcvfs
import json as simplejson
dialog     = xbmcgui.Dialog()
dialpro    = xbmcgui.DialogProgress()
addon      = xbmcaddon.Addon()
addon_dir  = xbmc.translatePath('special://userdata/addon_data/script.libraryhelper/')
addon_set  = xbmc.translatePath('special://userdata/addon_data/script.libraryhelper/results.txt')
addon_old  = xbmc.translatePath('special://userdata/addon_data/script.libraryhelper/old_results.txt')


class movieset_artwork:
    def __init__(self):
        if not xbmcvfs.exists(addon_dir):
            xbmcvfs.mkdir(addon_dir)
        if xbmcvfs.exists(addon_old):
            xbmcvfs.delete(addon_old)
        if xbmcvfs.exists(addon_set):
            xbmcvfs.rename(addon_set,addon_old)
        self.encoding()
        self.json = self.executeJSON('VideoLibrary.GetMovieSets',{"properties":["title","fanart","thumbnail","art","plot"],"sort":{ "method": "label" }})
        if self.json.has_key('result') and self.json['result'].has_key('sets'):
            self.sets       = []
            self.totals     = []
            self.complete   = []
            self.pc = 1
            for self.item in self.json['result']['sets']:
                self.m_title = self.item.get('title', '')
                self.totals.append(self.m_title)
            self.total_m = len(self.totals)
            for self.item in self.json['result']['sets']:
                self.percent = float(self.pc)/float(self.total_m)*100
                dialpro.create(addon.getLocalizedString(30000),addon.getLocalizedString(30001)+str(self.pc)+addon.getLocalizedString(30002)+str(self.total_m))
                if dialpro.iscanceled():
                        return
                try:
                    self.testpoint=self.executeJSON('VideoLibrary.SetMovieSetDetails', {'setid': self.item.get('setid',''), "art":{'poster': self.item.get('art','').get('set',''), 'fanart': self.item.get('art','').get('setfanart','')}})
                    # dialog.textviewer("",str(self.testpoint))
                    self.complete.append(self.item.get('title',''))
                    self.save_results(self.item.get('title',''))
                except:
                    pass
                dialpro.update(int(self.percent),addon.getLocalizedString(30001)+str(self.pc)+addon.getLocalizedString(30002)+str(self.total_m) ,str(self.item.get('title','')))
                self.pc+=1
                # time.sleep(.75)
            self.completed = len(self.complete) 
            # self.save_results(str(self.complete))

            xbmc.executebuiltin("Dialog.Close(all)")
            if self.completed == self.totals:
                dialog.ok(addon.getLocalizedString(30000),addon.getLocalizedString(30004))
            else:
                dialog.ok(addon.getLocalizedString(30000),str(self.completed)+addon.getLocalizedString(30006)+addon.getLocalizedString(30002)+str(self.total_m)+addon.getLocalizedString(30005))

    def executeJSON(self,method, params):
        self.json = simplejson.dumps({'jsonrpc':'2.0', 'method':method, 'params':params, 'id':1})
        self.result = simplejson.loads(xbmc.executeJSONRPC(self.json))
        return self.result
    def save_results(self,title):
        self.file=open(addon_set, "a")
        self.file.write(title+"\n")
        return
    def encoding(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        return


if __name__ == '__main__':
    movieset_artwork()