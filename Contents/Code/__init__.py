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
  for item in RSS.FeedFromURL(RSS_FEED).entries:
    entry = HTML.ElementFromString(item.content[0].value)
    imgs = entry.xpath('//img')
    if len(imgs) >= 1:
      thumb = ''
      for img in imgs:
        if img.get('src').find('http://braedonsblog.com/wp-content/uploads') != -1:
          thumb = img.get('src')
          
      dir.Append(Function(DirectoryItem(PictureMenu, title=item.title, thumb=thumb, summary=item.description), url=item.link))
  return dir

def PictureMenu(sender, url):
  dir = MediaContainer(viewGroup="Pictures", title2=sender.itemTitle)
  count = 1
  for img in HTML.ElementFromURL(url).xpath('//img'):
    if img.get('src').find('/wp-content/uploads') != -1:
      url = img.get('src')
      dir.Append(PhotoItem(url, title='Photo %d' % count, thumb=url))
      count += 1
    
  return dir
