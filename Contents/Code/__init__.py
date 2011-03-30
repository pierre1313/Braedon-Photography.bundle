import re

PLUGIN_PREFIX   = "/photos/BraedonPhotography"
ROOT_URL        = "http://braedonsblog.com"
RSS_FEED        = ROOT_URL + "/feed/"

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, "Braedon Photography", "icon-default.png", "art-default.jpg")
  Plugin.AddViewGroup("Pictures", viewMode="Pictures", mediaType="photos")
  Plugin.AddViewGroup("Info", viewMode="InfoList", mediaType="items")
  MediaContainer.art = "art-default.jpg"
  DirectoryItem.thumb = "icon-default.png"

####################################################################################################
def MainMenu():
  dir = MediaContainer(viewGroup="Info", title1="Braedon Photography")
  for item in XML.ElementFromURL(RSS_FEED).xpath("//item"):
    title = item.xpath('.//title')[0].text
    url = item.xpath('.//link')[0].text
    raw_summary = HTML.StringFromElement(item.xpath('.//description')[0]).replace(']]','').replace('<![CDATA[','').replace('&gt;','>').replace('&lt;','<').replace('&nbsp;','')#.text
    summary = HTML.ElementFromString(raw_summary).text_content()
    try:
      thumb = HTML.ElementFromString(raw_summary).xpath('.//img')[0].get('src')
    except:
      thumb = None
   
    dir.Append(Function(DirectoryItem(PictureMenu, title=title, thumb=thumb, summary=summary), url=url))
  return dir

def PictureMenu(sender, url):
  dir = MediaContainer(viewGroup="Pictures", title2=sender.itemTitle)
  count = 1
  for img in HTML.ElementFromURL(url).xpath('//img'):
    if img.get('src').find('osmek') != -1:
      url = img.get('src')
      dir.Append(PhotoItem(url, title='Photo %d' % count, thumb=url))
      count += 1
    
  return dir
