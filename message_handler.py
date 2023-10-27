import re
import tool_SD
import discord
import llm_backend
from datetime import datetime



async def send_message(message, is_private, bot):
    user_timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    user_tag_pattern = r'<@(\d+)>'
    user_tag_matches = re.findall(user_tag_pattern, message.content)
    for match in user_tag_matches:
        name = await message.guild.fetch_member(match)
        message.content = message.content.replace(f"<@{match}>", "@"+str(name))
    if "@SIA" in message.content:
        async with message.channel.typing():
            response = llm_backend.call_Model(message.content, message.channel, user_timestamp, message.author)
            channel_pattern = r'\[(.*?)\]'
            picture_pattern = r'\{(.+?)\}'
            tag_pattern = r"@(\w+)"

            tag_matches = re.findall(tag_pattern, response)
            for match in tag_matches:
                try:
                    response = response.replace(f"@{match}", f"<@{message.guild.get_member_named(match).id}>")
                except Exception as e:
                    pass
            channel_matches = re.findall(channel_pattern, response)
            images_matches = re.findall(picture_pattern, response)
            if "```" in response:
                channel_matches = []
                images_matches = []
            else:
                for match in channel_matches:
                    response = response.replace(f'[{match}]', '')

            if channel_matches and images_matches and not is_private:
                await images(images_matches, response, discord.utils.get(message.guild.channels, name=channel_matches[0]))
            elif images_matches:
                if is_private:
                    await images(images_matches, response, message.author)
                else:
                    await images(images_matches, response, message.channel)
            elif channel_matches and not is_private:
                await discord.utils.get(message.guild.channels, name=channel_matches[0]).send(response)
            else:
                await message.author.send(response) if is_private else await message.channel.send(response)
    else:
        llm_backend.memory.add_Memory(message.author, message.content, message.channel, user_timestamp)







async def images(image_match:list[str], response:str, message):
    image_files = []
    for match in image_match:
        path = tool_SD.generate_image(match)
        response = response.replace(f'{{{match}}}', '')
        image_files.append(discord.File(path))
    if image_files:
        if response:
            await message.send(response, files=image_files)
        else:
            await message.send(" ", files=image_files)
    else:
        if response:
            await message.send(response + "\n''''Image Error'''")
        else:
            await message.send(" " + "\n''''Image Error'''")