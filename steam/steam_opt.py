from lxml import etree
import requests
from tinydb import TinyDB, Query
fullpath = 'E:\\bakabot\\awesome\\plugins\\steam\\'

async def steam_list_add(steam_id,steam_belong_name,group_num):
    try:
        db = TinyDB(fullpath + f'{group_num}.json')
        db.insert({'steam_id':steam_id,'steam_belong_name':steam_belong_name})
    except:
        return False
    return True

async def steam_all(group_num):
    db = TinyDB(fullpath + f'{group_num}.json')
    return db.all()

async def steam_list_del(group_num,doc_id):
    try:
        db = TinyDB(fullpath + f'{group_num}.json')
        db.remove(doc_ids=[int(doc_id)])
    except:
        return False
    else:
        return True




async def steam_monitor(ID):
    import requests
    game_name = ''
    rich_presence = ''
    img_url = ''
    aim_url = f'https://steamcommunity.com/miniprofile/{ID}?appid=undefined'
    a = requests.get(aim_url)

    selector = etree.HTML(a.text)

    name = selector.xpath('//div[@class="player_content"]/span')[0].text

    try:
        state = selector.xpath('//div[@class="player_content"]/span')[1].text
        if state == 'Offline':
            img_url = selector.xpath('//div[@class="playersection_avatar border_color_offline"]//@src')[0]
            return [name,state,img_url]
        else:
            img_url = selector.xpath('//div[@class="playersection_avatar border_color_online"]//@src')[0]
    except:
        if len(selector.xpath('//div[@class="miniprofile_detailssection miniprofile_backdropblur not_in_game miniprofile_backdrop"]')) == 1:
            state = 'Online'
            img_url = selector.xpath('//div[@class="playersection_avatar border_color_online"]//@src')[0]
        else:
            # game_detail = ' '.join(selector.xpath('//div[@class="miniprofile_game_details"]//text()')).replace('\r\n', '').replace(
            #     '\t', '')
            # game_state
            state = selector.xpath('//span[@class="game_state"]/text()')[0]
            # miniprofile_game_name
            game_name = selector.xpath('//span[@class="miniprofile_game_name"]/text()')[0]
            # rich_presence
            try:
                rich_presence = selector.xpath('//span[@class="rich_presence"]/text()')[0]
            except:
                pass
            img_url = selector.xpath('//div[@class="playersection_avatar border_color_in-game"]//@src')[0]

    return [name,state,img_url,game_name,rich_presence]