import requests, os, psutil, sys, jwt, pickle, json, binascii, time, urllib3, base64, datetime, re, socket, threading, ssl, pytz, aiohttp, traceback, asyncio, random
from aiohttp import web
from protobuf_decoder.protobuf_decoder import Parser
from xPARA import *
from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2, sQ_pb2, Team_msg_pb2
from cfonts import render, say
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Chat_Leave = False
joining_team = False

login_url, ob, version = AuToUpDaTE()

Hr = {
    'User-Agent': Uaa(),
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': ob
}

# Helper functions (ensure they exist; some from xPARA)
async def ArA_CoLor():
    Tp = ["32CD32", "00BFFF", "00FA9A", "90EE90", "FF4500", "FF6347", "FF69B4", "FF8C00", "FF6347", "FFD700", "FFDAB9", "F0F0F0", "F0E68C", "D3D3D3", "A9A9A9", "D2691E", "CD853F", "BC8F8F", "6A5ACD", "483D8B", "4682B4", "9370DB", "C71585", "FF8C00", "FFA07A"]
    return random.choice(Tp)

def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]", "[191970]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)

async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status != 200:
                return await response.read()
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = version
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return await encrypted_proto(string)

async def MajorLogin(payload):
    url = f"{login_url}MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization'] = f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto

async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9:
        headers = '0000000'
    elif uid_length == 8:
        headers = '00000000'
    elif uid_length == 10:
        headers = '000000'
    elif uid_length == 7:
        headers = '000000000'
    else:
        print('Unexpected length')
        headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

class CLIENT:
    def __init__(self):
        self.msg = None
        self.ghost_name = None
        self.whisper_writer = None
        self.online_writer = None
        self.uid = None          # will be set from incoming messages (last sender)
        self.chat_id = None       # will be set from incoming messages
        self.room_uid = None
        self.response = None
        self.inPuTMsG = None
        self.data = None
        self.data2 = None
        self.key = None
        self.iv = None
        self.STATUS = None
        self.AutHToKen = None
        self.OnLineiP = None
        self.OnLineporT = None
        self.ChaTiP = None
        self.ChaTporT = None
        self.LoGinDaTaUncRypTinG = None
        self.bot_uid = None
        self.teamcode = None
        self.ready_for_api = asyncio.Event()  # set when online_writer is ready

    async def cHTypE(self, H):
        if not H:
            return 'Squid'
        elif H == 1:
            return 'CLan'
        elif H == 2:
            return 'PrivaTe'

    async def SEndMsG(self, H, message, Uid, chat_id, key, iv):
        TypE = await self.cHTypE(H)
        if TypE == 'Squid':
            msg_packet = await xSEndMsgsQ(message, chat_id, key, iv)
        elif TypE == 'CLan':
            msg_packet = await xSEndMsg(message, 1, chat_id, chat_id, key, iv)
        elif TypE == 'PrivaTe':
            msg_packet = await xSEndMsg(message, 2, Uid, Uid, key, iv)
        return msg_packet

    async def SEndPacKeT(self, target, TypE, PacKeT):
        if TypE == 'ChaT' and self.whisper_writer:
            self.whisper_writer.write(PacKeT)
            await self.whisper_writer.drain()
        elif TypE == 'OnLine' and self.online_writer:
            self.online_writer.write(PacKeT)
            await self.online_writer.drain()
        else:
            print(f"Unsupported type or writer not ready: {TypE}")

    async def api_join_team(self, teamcode, ghostname):
        """Trigger ghost join via API."""
        # Wait up to 10 seconds for online writer to be ready
        for _ in range(20):  # 20 * 0.5 = 10 seconds
            if self.online_writer:
                break
            await asyncio.sleep(0.5)
        else:
            raise Exception("Bot not connected to online server (timeout)")

        self.ghost_name = f'[B][C]{get_random_color()}{ghostname.upper()}'
        self.teamcode = teamcode
        join_packet = await RedZedTeamCode(teamcode, self.key, self.iv)
        await self.SEndPacKeT(None, 'OnLine', join_packet)
        return {"status": "ok", "message": f"Join packet sent for team {teamcode} with ghost {ghostname}"}

    async def TcPOnLine(self, ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
        while True:
            try:
                reader, writer = await asyncio.open_connection(ip, int(port))
                self.online_writer = writer
                writer.write(bytes.fromhex(AutHToKen))
                await writer.drain()
                print(f"[Online] Connected to {ip}:{port}")
                # Signal that online is ready
                self.ready_for_api.set()

                while True:
                    data = await reader.read(9999)
                    if not data:
                        break
                    hex_data = data.hex()

                    if hex_data.startswith("0f00"):  # Player status
                        info = await DeCode_PackEt(hex_data[10:])
                        self.STATUS = get_player_status(info)
                        if isinstance(self.STATUS, dict) and self.STATUS.get("IN_ROOM"):
                            room_uid = self.STATUS['room_uid']
                            room_packet = await SendRoomInfo(int(room_uid), key, iv)
                            await self.SEndPacKeT(None, 'OnLine', room_packet)
                        else:
                            # Only send status message if we have a target (uid/chat_id)
                            if self.uid and self.chat_id:
                                msg_packet = await self.SEndMsG(2, str(self.STATUS), self.uid, self.chat_id, key, iv)
                                await self.SEndPacKeT(None, 'ChaT', msg_packet)

                    elif hex_data.startswith("0e00"):  # Room info
                        info = await DeCode_PackEt(hex_data[10:])
                        room_message = get_room_info(info)
                        if self.uid and self.chat_id:
                            msg_packet = await self.SEndMsG(2, room_message, self.uid, self.chat_id, key, iv)
                            await self.SEndPacKeT(None, 'ChaT', msg_packet)

                    elif hex_data.startswith('0500') and len(hex_data) > 2000:  # Squad data
                        try:
                            packet_json = await DeCode_PackEt(hex_data[10:])
                            packet = json.loads(packet_json)
                            squad_data = await GeTSQDaTa(packet)
                            if squad_data:
                                owner_uid, _, squad_code = squad_data
                                exit_packet = await ExiT(owner_uid, key, iv)
                                await self.SEndPacKeT(None, 'OnLine', exit_packet)
                                await asyncio.sleep(0.5)
                                if self.ghost_name:
                                    ghost_packet = await Send_GhosTs(owner_uid, self.ghost_name, squad_code, key, iv)
                                    await self.SEndPacKeT(None, 'OnLine', ghost_packet)
                                    print(f"[Ghost] Sent ghost packet for {self.ghost_name}")
                                else:
                                    print("[Ghost] No ghost name set, skipping")
                        except Exception as e:
                            print(f"Error processing squad packet: {e}")

                # Cleanup
                if self.online_writer:
                    self.online_writer.close()
                    await self.online_writer.wait_closed()
                    self.online_writer = None
                self.ready_for_api.clear()
            except Exception as e:
                print(f"[Online] Connection error: {e}")
                self.online_writer = None
                self.ready_for_api.clear()
            await asyncio.sleep(reconnect_delay)

    async def TcPChaT(self, ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, reconnect_delay=0.5):
        while True:
            try:
                reader, writer = await asyncio.open_connection(ip, int(port))
                self.whisper_writer = writer
                writer.write(bytes.fromhex(AutHToKen))
                await writer.drain()
                ready_event.set()
                print(f"[Chat] Connected to {ip}:{port}")

                if LoGinDaTaUncRypTinG.Clan_ID:
                    clan_id = LoGinDaTaUncRypTinG.Clan_ID
                    clan_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                    print(f"[Clan] Bot is in clan {clan_id}, authenticating...")
                    clan_auth = await AuthClan(clan_id, clan_data, key, iv)
                    writer.write(clan_auth)
                    await writer.drain()

                while True:
                    data = await reader.read(9999)
                    if not data:
                        break
                    hex_data = data.hex()
                    if hex_data.startswith("120000"):  # Incoming message
                        try:
                            self.response = await DecodeWhisperMessage(hex_data[10:])
                            self.uid = self.response.Data.uid
                            self.chat_id = self.response.Data.Chat_ID
                            msg_text = self.response.Data.msg.lower()
                            chat_type = self.response.Data.chat_type
                        except Exception as e:
                            print(f"Error parsing message: {e}")
                            continue

                        if msg_text.startswith('/x'):
                            parts = msg_text.strip().split()
                            if len(parts) < 3:
                                reply = f"[B][C]{get_random_color()}Usage: /x teamcode name"
                                packet = await self.SEndMsG(chat_type, reply, self.uid, self.chat_id, key, iv)
                                await self.SEndPacKeT(None, 'ChaT', packet)
                            else:
                                teamcode = parts[1]
                                ghostname = parts[2]
                                self.ghost_name = f'[B][C]{get_random_color()}{ghostname.upper()}'
                                self.teamcode = teamcode
                                join_packet = await RedZedTeamCode(teamcode, key, iv)
                                await self.SEndPacKeT(None, 'OnLine', join_packet)
                                print(f"[Chat] Sent join for {teamcode} with ghost {ghostname}")

                        elif msg_text in ("hi", "hello", "fin", "fen", "wach", "slm", "cc", "salam"):
                            reply = 'Hello Im Dev RedZed\nTelegram : @RedZedKing'
                            packet = await self.SEndMsG(chat_type, reply, self.uid, self.chat_id, key, iv)
                            await self.SEndPacKeT(None, 'ChaT', packet)

                # Cleanup
                if self.whisper_writer:
                    self.whisper_writer.close()
                    await self.whisper_writer.wait_closed()
                    self.whisper_writer = None
            except Exception as e:
                print(f"[Chat] Connection error: {e}")
                self.whisper_writer = None
            await asyncio.sleep(reconnect_delay)

    async def MaiiiinE(self):
        Uid, Pw = '4366901723', 'F168167C3C1BA46A000B873C94D273711CE2CE3F51277A9DAC8156668E361445'

        open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
        if not open_id or not access_token:
            print("Error: Invalid account")
            return None

        payload = await EncRypTMajoRLoGin(open_id, access_token)
        login_response = await MajorLogin(payload)
        if not login_response:
            print("Error: Account banned or not registered")
            return None

        auth_data = await DecRypTMajoRLoGin(login_response)
        base_url = auth_data.url
        token = auth_data.token
        self.bot_uid = auth_data.account_uid
        self.key = auth_data.key
        self.iv = auth_data.iv
        timestamp = auth_data.timestamp

        login_data_raw = await GetLoginData(base_url, payload, token)
        if not login_data_raw:
            print("Error: Failed to get login data")
            return None
        login_data = await DecRypTLoGinDaTa(login_data_raw)

        region = login_data.Region
        account_name = login_data.AccountName
        online_ip_port = login_data.Online_IP_Port
        chat_ip_port = login_data.AccountIP_Port

        self.OnLineiP, self.OnLineporT = online_ip_port.split(":")
        self.ChaTiP, self.ChaTporT = chat_ip_port.split(":")

        self.AutHToKen = await xAuThSTarTuP(int(self.bot_uid), token, int(timestamp), self.key, self.iv)

        ready_event = asyncio.Event()
        task_chat = asyncio.create_task(
            self.TcPChaT(self.ChaTiP, self.ChaTporT, self.AutHToKen, self.key, self.iv, login_data, ready_event)
        )
        await ready_event.wait()
        await asyncio.sleep(1)
        task_online = asyncio.create_task(
            self.TcPOnLine(self.OnLineiP, self.OnLineporT, self.key, self.iv, self.AutHToKen)
        )

        print(render('REDZED', colors=['white', 'red'], align='center'))
        print(f"Server URL: {login_url} | Base URL: {base_url}")
        print(f"OB: {ob} | Version: {version}")
        print(f"Bot: {account_name} (UID: {self.bot_uid}) | Region: {region}")
        print("Bot is online and ready.")

        return task_chat, task_online

# Global client
client = None

# Web handlers
async def handle_x(request):
    global client
    teamcode = request.match_info.get('teamcode')
    ghostname = request.match_info.get('ghostname')
    if not teamcode or not ghostname:
        return web.json_response({"error": "Missing teamcode or ghostname"}, status=400)
    try:
        result = await client.api_join_team(teamcode, ghostname)
        return web.json_response(result)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

async def handle_status(request):
    global client
    return web.json_response({
        "status": "running",
        "bot_uid": client.bot_uid if client else None,
        "online_connected": client.online_writer is not None if client else False
    })

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

async def start_web_server():
    app = web.Application()
    app.router.add_get('/x/{teamcode}/{ghostname}', handle_x)
    app.router.add_get('/status', handle_status)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5050)
    await site.start()
    local_ip = get_local_ip()
    print("\n" + "="*50)
    print("API server is running!")
    print(f"Local access: http://127.0.0.1:5050")
    print(f"Network access: http://{local_ip}:5050")
    print("Endpoints:")
    print("  GET /x/{teamcode}/{ghostname}  - Trigger ghost join")
    print("  GET /status                    - Bot status")
    print("="*50 + "\n")
    await asyncio.Event().wait()  # run forever

async def main():
    global client
    web_task = asyncio.create_task(start_web_server())

    while True:
        client = CLIENT()
        try:
            tasks = await client.MaiiiinE()
            if tasks is None:
                print("Bot failed to start, retrying in 5 seconds...")
                await asyncio.sleep(5)
                continue
            task1, task2 = tasks
            await asyncio.wait_for(asyncio.gather(task1, task2), timeout=7*60*60)
        except asyncio.TimeoutError:
            print("Token expired, restarting bot...")
        except Exception as e:
            print(f"Bot error: {e}, restarting...")
            traceback.print_exc()
        await asyncio.sleep(2)

if __name__ == '__main__':
    asyncio.run(main())