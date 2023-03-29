import re

from tinydb import TinyDB, Query
import requests
import time
from nonebot import on_command, CommandSession
from awesome.plugins.steam.steam_opt import *
from nonebot.experimental.permission import simple_allow_list



@on_command('steamaddid', patterns=('ADDSTID (.*)'), only_to_me=False)
async def steam3(session: CommandSession,):
    choicess = str(session.current_arg).split(' ')
    if len(choicess) == 2:
        await session.send(f'请为该账号添加一个别名哦 例如 ADDSTID 1234568 狗群主', at_sender=True)
        return
    elif len(choicess) != 3:
        await session.send(f'输入格式有误！', at_sender=True)
        return
    choicess = choicess[1:]

    steam_id = choicess[0] # steamid
    steam_belong_name = choicess[1] # 所属人

    try:
        message = []
        result_list = await steam_monitor(steam_id)
        message.append({"type": "image", "data": {"file": result_list[2], }})
        message.append({"type": "text", "data": {"text": result_list[0] + '\n' + result_list[1] + '\n' + result_list[3] + '\n' + result_list[4] }})
        message.append({"type": "text", "data": {"text": '\n------------------------------\n'}})
        await session.send(message=message, at_sender=True)

        answer = (await session.aget( prompt=f'即将向本群steam状态列表添加以下账号\n账号所属: {steam_belong_name} ,\n输入y确认添加, 输入其他内容取消添加。')).strip()
    except:
        await session.send('获取该账号时发生错误，该steam账号可能不存在。')
        return

    if str(answer).lower() == 'y':
        if await steam_list_add(steam_id=steam_id,steam_belong_name=steam_belong_name,group_num=session.event['group_id']):
            await session.send('添加成功。')
        else:
            await session.send('数据库错误，添加失败。')
    else:
        await session.send('添加已取消。')
        return

@on_command('steamaddidel', aliases=('DELSTID'), only_to_me=False)
async def steam4(session: CommandSession,):

    def check_id_inlist_or_not( m ,alist): # m in alist or not
        for j in alist:
            if m == j:
                return True
        else:
            return False

    all_list = await steam_all(session.event['group_id'])

    if len(all_list) == 0:
        await session.send('当前未绑定任何steam信息！')
        return

    message = []
    i_list = []
    for i in range(0,len(all_list)):
        i_list.append(f'{all_list[i].doc_id}')
        message.append({"type": "text", "data": {"text": '序号 ' + f' {all_list[i].doc_id}\n' + f'STEAMID : {all_list[i]["steam_id"]}\n' + f'该账户所属:{all_list[i]["steam_belong_name"]}\n-----------------------\n' }})
    await session.send(message=message, at_sender=True)
    answer = (await session.aget(prompt=f'请输入序号,bot将删除该条steam信息,输入其他内容取消删除流程。')).strip()



    if check_id_inlist_or_not(answer,i_list):
        if await steam_list_del(session.event['group_id'],answer):
            await session.send('删除成功。')
        else:
            await session.send('数据库错误，删除失败。')
    else:
        await session.send('已经取消删除流程。')

@on_command('steamaddiall', aliases=('ALLSTID'), only_to_me=False)
async def steam5(session: CommandSession,):
    all_list = await steam_all(session.event['group_id'])

    if len(all_list) == 0:
        await session.send('当前群聊未绑定任何steam信息！')
        return
    message = []

    for i in all_list:
        message.append({"type": "text", "data": {"text": '\n序号 ' + f' {i.doc_id}\n' + f'STEAMID : {i["steam_id"]}\n' + f'该账户所属:{i["steam_belong_name"]}\n-----------------------\n' }})

    await session.send(message=message, at_sender=True)

@on_command('steam1', patterns=('(?<=查steam状态 )(.*)'), only_to_me=False, )
async def steam_test_1(session: CommandSession,):
    try:
        ID_list = re.findall(r'(?<=查steam状态 )(.*)', session.current_arg)[0]
        ID_list = str(ID_list).split(' ')

        message = []

        message.append({"type": "text", "data": {"text": '群友Steam状态\n'}})
        message.append({"type": "text", "data": {"text": '获取时间:' + time.strftime('%Y-%m-%d %H:%M:%S') }}) # 格式化时间
        message.append({"type": "text", "data": {"text": '\n------------------------------\n'}})

        for ID in ID_list:

            result_list = await steam_monitor(ID)

            if len(result_list) == 3:
                    message.append({"type": "image", "data": { "file": result_list[2], }})
                    message.append({"type": "text", "data": {"text": result_list[0] + '\n' + result_list[1]  }})
                    message.append({"type": "text", "data": {"text": '\n------------------------------\n' }})

            else:
                if result_list[3] == '':
                    message.append({"type": "image", "data": {"file": result_list[2], }})
                    message.append({"type": "text", "data": {"text": result_list[0] + '\n' + result_list[1]}})
                    message.append({"type": "text", "data": {"text": '\n------------------------------\n'}})
                else:
                    message.append({"type": "image", "data": {"file": result_list[2], }})
                    message.append({"type": "text", "data": {"text": result_list[0] + '\n' + result_list[1] + '\n' + result_list[3] + '\n' + result_list[4] }})
                    message.append({"type": "text", "data": {"text": '\n------------------------------\n'}})
    except:
        message = [{"type": "text", "data": {"text": '输入有误或者网络原因获取失败了>_<'}},]

    await session.send(message=message)

@on_command('steam2', aliases=('查水表','查水表！','查水表!'), only_to_me=False, shell_like=False, permission = simple_allow_list(group_ids={ 194731458 }, reverse=False))
async def steam_test_2(session: CommandSession,):
    try:
        # ['117011705', '880840172', '188204018', '1012463710']
        message = []
        message.append({"type": "text", "data": {"text": '群友Steam状态\n'}})
        message.append({"type": "text", "data": {"text": '获取时间:' + time.strftime('%Y-%m-%d %H:%M:%S') }}) # 格式化时间
        message.append({"type": "text", "data": {"text": '\n------------------------------\n'}})


        ID_list_all = await steam_all(session.event['group_id'])
        ID_list = []
        belong_list = []

        for i in ID_list_all:
            ID_list.append(i['steam_id'])
            belong_list.append(i['steam_belong_name'])


        if len(ID_list ) == 0:
            message.append({"type": "text", "data": {"text": '本群还未绑定steam信息！\n'}})
            message.append({"type": "text", "data": {"text": '\n------------------------------\n'}})

        #
        c = 0
        for ID in ID_list:
            result_list = await steam_monitor(ID)
            message.append({"type": "text", "data": {"text": f'群友名称 : {belong_list[c]}'}})
            if len(result_list) == 3:

                message.append({"type": "image", "data": { "file": result_list[2], }})
                message.append({"type": "text", "data": {"text": result_list[0] + '\n' + result_list[1]  }})
                message.append({"type": "text", "data": {"text": '\n------------------------------\n' }})

            else:
                if result_list[3] == '':
                    message.append({"type": "image", "data": {"file": result_list[2], }})
                    message.append({"type": "text", "data": {"text": result_list[0] + '\n' + result_list[1]}})
                    message.append({"type": "text", "data": {"text": '\n------------------------------\n'}})
                else:
                    message.append({"type": "image", "data": {"file": result_list[2], }})
                    message.append({"type": "text", "data": {"text": result_list[0] + '\n' + result_list[1] + '\n' + result_list[3] + '\n' + result_list[4] }})
                    message.append({"type": "text", "data": {"text": '\n------------------------------\n'}})
                c += 1

    except:
        message = [{"type": "text", "data": {"text": '获取失败了>_<'}},]

    message.append({"type": "text", "data": {"text": '\n如何管理名单？输入"steam帮助"查看详情\n'}})

    await session.send(message=message)

@on_command('steamhelp', aliases=('steam帮助','/steam帮助','Steam帮助','/Steam帮助'), only_to_me=False)
async def steam6(session: CommandSession,):
    message = []
    message.append({"type": "text", "data": {"text": '\n绑定steam号 ADDSTID steam好友代码 群友名称 \n'}})
    message.append({"type": "text", "data": {"text": '\n例:ADDSTID 123456 狗群主 \n'}})
    message.append({"type": "text", "data": {"text": '\n查看所有绑定账号 ALLSTID\n'}})
    message.append({"type": "text", "data": {"text": '\n删除绑定账号 DELSTID\n'}})
    await session.send(message=message, at_sender=True)