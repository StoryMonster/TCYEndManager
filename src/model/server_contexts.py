from .server_names import *

serverContexts = {
    CHUNK_SERVER: {
        "name": "chunk server",
        "workdir": "D:\DGT_Server\gamechunksvr\Debug",
        "exefile": "gamechunksvr.exe",
        "configfile": "LaGpChunkSvr.ini",
        "logfile": "ChunkServer.log",
		"comments": ["启动chunk服务器之前，需要先将其配置文件中的clientid改为自己的clientid",
		             "务必确保防火墙已经关闭"]
    },
    ASSIST_SERVER: {
        "name": "assist server",
        "workdir": "D:\DGT_Server\gameassitsvr\Debug",
        "exefile": "gameassitsvr.exe",
        "configfile": "LaGpAssitSvr.ini",
        "logfile": "AssistServer.log",
    },
    ASSIST_PROXY_SERVER: {
        "name": "assist proxy server",
        "workdir": "D:/DGT_Server/mpsvr/debug/",
        "exefile": "assistmpsvr.exe",
        "configfile": "assistmpsvr.ini",
        "logfile": "AssistProxyServer.log",
    },
    GAME_SERVER: {
        "name": "game server",
        "workdir": "D:/DGT_Server/gamesvr/Debug/",
        "exefile": "lagpsvr.exe",
        "configfile": "lagpsvr.ini",
        "logfile": "GameServer.log",
    },
    GAME_PROXY_SERVER: {
        "name": "game proxy server",
        "workdir": "D:/DGT_Server/mpsvr/debug/",
        "exefile": "gamempsvr.exe",
        "configfile": "gamempsvr.ini",
        "logfile": "GameProxyServer.log",
    },
    ROOM_SERVER: {
        "name": "room server",
        "workdir": "D:/DGT_Server/roomsvrlagp/Debug",
        "exefile": "roomsvrlagpD.exe",
        "configfile": "RoomSvr.ini",
        "logfile": "RoomServer.log",
        "comments": ["启动房间服务器，必须要有license.dat处于同级目录",]
    },
    ROOM_PROXY_SERVER: {
        "name": "room proxy server",
        "workdir": "D:/roommpsvr",
        "exefile": "roommpsvrlagp.exe",
        "configfile": "roommpsvr.ini",
        "logfile": "RoomProxyServer.log",
    },
}