#Copyright (c) 2004-2023 ltBerryshdo
from mcdreforged.api.all import *
from .config import *
import os.path
import re


serverDir: str
IPaddress: str


def on_load(server: PluginServerInterface, prev_module):
    with open('./config.yml', 'r') as configDir:
        for lines in configDir.readlines():
            if 'working_directory' in lines:
                global serverDir

                serverDir = lines.split(':')[1].strip().replace('\n', '')     #查找工作地址  ***尾部去除/
                serverDir = os.path.normpath(serverDir)
                serverDir = './{}'.format(serverDir)
                propertiesDir = '{}/server.properties'.format(serverDir)

    with open(propertiesDir, 'r') as server_properties:                    #检查是否为离线模式
        for lines in server_properties.readlines():
            if 'online-mode' in lines:
                modeValue = lines.split('=')[1].replace('\n', '')
                break
        if modeValue != 'true':                                         #---!!!false!!!---
            return

    init_config(server)
    get_global_value(serverDir)
    register_help_message(server)
    register_command(server)


def register_command(server: PluginServerInterface):
    server.register_command(
        Literal('!!offlineops').
            runs(lambda src: src.reply('为未开启在线模式（正版验证）的服务器提供了管理员账号保护的一种方法')).
        then(Literal('notOpsPlayerProtect').
            then(Literal('enable').
                runs(cmd_tree_protect_player_enable)).
            then(Literal('disable').
                runs(cmd_tree_protect_player_disable))).
                
        then(Literal('protectPlayer').
            then(Text('playerName').
                runs(lambda src, ctx: cmd_tree_protect_player(src, ctx['playerName'])))).
        then(Literal('allPlayerProtect').
            then(Literal('enable').
                runs(cmd_tree_all_player_protect_enable)).
            then(Literal('disable').
                runs(cmd_tree_all_player_protect_disable)))
    )

def register_help_message(server: PluginServerInterface):
    server.register_help_message("!!offlineops", {
        'en_us': '',
        'zh_cn': '为未开启在线模式（正版验证）的服务器提供了管理员账号保护的一种方法'
    })                                                                  #注册help内容


def on_player_joined(server: PluginServerInterface, player: str, info: Info):   #玩家进入检查
    playerJoin(server, player, IPaddress)

def on_info(server: PluginServerInterface, info: Info):
    if not info.is_user and re.search(r'logged in with entity id', info.content):
        logginInfo = re.search(r'(\w+)\[/(\d+.\d+.\d+.\d+):(\d+)\] logged in with entity id', info.content)
        if logginInfo:
            global IPaddress
            #playerName = logginInfo.group(1)
            IPaddress = logginInfo.group(2)
            #port = logginInfo.group(3)
