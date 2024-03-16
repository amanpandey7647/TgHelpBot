import asyncio
import traceback

DELETE_TIMEOUT = 2


@BOTIQUE.on(
  BOTIQUE.botique_cmd(r"(?:re)?load", r"\s+(?P<shortname>\w+)")
)
async def load_reload(event):
    if not BOTIQUE.me.bot:
        await event.delete()
    shortname = event.pattern_match["shortname"]

    try:
        if shortname in BOTIQUE._plugins:
            await BOTIQUE.remove_plugin(shortname)
        await BOTIQUE.load_plugin(shortname)

        msg = await event.respond(
            f"Successfully (re)loaded plugin {shortname}")
        if not BOTIQUE.me.bot:
            await asyncio.sleep(DELETE_TIMEOUT)
            await BOTIQUE.delete_messages(msg.to_id, msg)

    except Exception as e:
        tb = traceback.format_exc()
        logger.warn(f"Failed to (re)load plugin {shortname}: {tb}")
        await event.respond(f"Failed to (re)load plugin {shortname}: {e}")


@BOTIQUE.on(
  BOTIQUE.botique_cmd(r"(?:unload|disable|remove)", r"\s+(?P<shortname>\w+)")
)
async def remove(event):
    if not BOTIQUE.me.bot:
        await event.delete()
    shortname = event.pattern_match["shortname"]

    if shortname == "_core":
        msg = await event.respond(f"Not removing {shortname}")
    elif shortname in BOTIQUE._plugins:
        await BOTIQUE.remove_plugin(shortname)
        msg = await event.respond(f"Removed plugin {shortname}")
    else:
        msg = await event.respond(f"Plugin {shortname} is not loaded")

    if not BOTIQUE.me.bot:
        await asyncio.sleep(DELETE_TIMEOUT)
        await BOTIQUE.delete_messages(msg.to_id, msg)


@BOTIQUE.on(
  BOTIQUE.botique_cmd(r"plugins")
)
async def list_plugins(event):
    result = f'{len(BOTIQUE._plugins)} plugins loaded:'
    for name, mod in sorted(BOTIQUE._plugins.items(), key=lambda t: t[0]):
        desc = (mod.__doc__ or '__no description__').replace('\n', ' ').strip()
        result += f'\n**{name}**: {desc}'

    if not BOTIQUE.me.bot:
        await event.edit(result)
    else:
        await event.respond(result)
