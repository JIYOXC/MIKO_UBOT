
__MODULE__ = "ᴠᴄᴛᴏᴏʟꜱ"
__HELP__ = """

<b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴠᴄᴛᴏᴏʟꜱ 』</b>

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}joinvc</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ʙᴇʀɢᴀʙᴜɴɢ ᴋᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɢʀᴏᴜᴘ

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}leavevc</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɪɴɢɢᴀʟᴋᴀɴ ᴅᴀʀɪ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɢʀᴏᴜᴘ

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}startvc</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɢʀᴜᴘ

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}stopvc</code>
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴋʜɪʀɪ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɢʀᴜᴘ
"""


from asyncio import sleep

from contextlib import suppress

from random import randint
from typing import Optional

from pyrogram import Client, enums
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import Message
from miko import *

async def get_group_call(

    client: Client, message: Message, err_msg: str = ""

) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (
                await client.invoke(GetFullChannel(channel=chat_peer))
            ).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.invoke(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await eor(message, f"**No group call Found** {err_msg}")
    return False

@MIKO.UBOT("joinvc")
async def join_os(client, message):
    # global turun_dewek
    ky = await message.reply("<code>Processing....</code>")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    with suppress(ValueError):
        chat_id = int(chat_id)
    if chat_id:
        file = "./storage/vc.mp3"
        try:
            # daftar_join.append(chat_id)
            # if turun_dewek: turun_dewek = False
            await client.call_py.join_group_call(
                chat_id,
                InputStream(
                    InputAudioStream(
                        file,
                    ),
                ),
            )
            await sleep(2)
            await ky.edit(
                f"❏ <b>Berhasil Join Voice Chat</b>\n└ <b>Chat :</b><code>{message.chat.title}</code>"
           )

        await sleep(1)
        except AlreadyJoinedError:
            await ky.edit("Akun anda sudah diatas.")
        except Exception as e:
            return await ky.edit(f"ERROR: {e}") 
@MIKO.UBOT("leavevc")
async def turun_os(client, message):
    # global turun_dewek
    ky = await message.reply("<code>Processing....</code>")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    with suppress(ValueError):
        chat_id = int(chat_id)
    if chat_id:
        try:
            # daftar_join.remove(chat_id)
            await client.call_py.leave_group_call(chat_id)
            # turun_dewek = True
            await ky.edit(
                f"❏ <b>Berhasil Meninggalkan Voice Chat</b>\n└ <b>Chat :</b><code>{message.chat.title}</code>"
            )
        except Exception as e:
            return await ky.edit(f"<b>ERROR:</b> {e}")

@MIKO.UBOT("startvc")
async def start_vctools(client, message):
    flags = " ".join(message.command[1:])
    ky = await message.reply("<code>Processing....</code>")
    vctitle = get_arg(message)
    if flags == enums.ChatType.CHANNEL:
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    args = (
        f"<b>• Obrolan Suara Aktif</b>\n<b>• Chat : </b><code>{message.chat.title}</code>"
    )
    try:
        if not vctitle:
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                )
            )
        else:
            args += f"\n • <b>Title : </b> <code>{vctitle}</code>"
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                    title=vctitle,
                )
            )
        await ky.edit(args)
    except Exception as e:
        await ky.edit(f"<b>INFO:</b> `{e}`")


@MIKO.UBOT("stopvc")
async def stop_vctools(client, message):
    ky = await message.reply("<code>Processing....</code>")
    message.chat.id
    if not (
        group_call := (await get_group_call(client, message, err_msg=", Kesalahan..."))
    ):
        return
    await client.invoke(DiscardGroupCall(call=group_call))
    await ky.edit(
        f"<b>• Obrolan Suara Diakhiri</b>\n<b>• Chat : </b><code>{message.chat.title}</code>"
               )
                   
