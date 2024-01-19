import discord
from discord import app_commands
from discord.ext import commands
import locale
import sqlite3
import os
import random
import math
from shlex import quote
from typing import List
from ia_images import *
from re import compile as re_compile

description = """Nilla's reference bot for Idle Angels. Contact: @nillabutt or github.com/nillabutt"""
MY_GUILD = discord.Object(id=1048680051262111785)
locale.setlocale(locale.LC_ALL, '') # for formatting thousands separator

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        # self.tree.copy_global_to(guild=MY_GUILD)
        # await self.tree.sync(guild=MY_GUILD)
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync()

intents = discord.Intents.all()
client = MyClient(intents=intents)

# connect
@client.event
async def on_ready():
    print(f'Rejoice! {client.user} is logged in.')
    print('------------------------------------------')


# AUTOCOMPLETES -----------------------------------------------------------
connection = sqlite3.connect('ia.db')
cursor = connection.cursor()

eudo_query = cursor.execute("SELECT name FROM eudemon").fetchall()
eudo_query.sort()
eudemon_list = []
for i in eudo_query:
    eudemon_list.append(i[0])

angel_query = cursor.execute("SELECT name FROM angel").fetchall()
angel_query.sort()
angel_list = []
for a in angel_query:
    angel_list.append(a[0])

relic_query = cursor.execute("SELECT name FROM relic").fetchall()
relic_query.sort()
relic_list = []
for r in relic_query:
    relic_list.append(r[0])


# card_query = cursor.execute("SELECT name FROM treasure").fetchall()
# card_query.sort()
# card_list = []
# for c in card_query:
#     card_list.append(c[0])

cursor.close()
connection.close() 

async def eudemon_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    eudemons = eudemon_list 
    return [
        app_commands.Choice(name=eudemon, value=eudemon)
        for eudemon in eudemons if current.lower() in eudemon.lower()
    ]

async def angel_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    angels = angel_list 
    return [
        app_commands.Choice(name=angel, value=angel)
        for angel in angels if current.lower() in angel.lower()
    ]

async def relic_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    relics = relic_list 
    return [
        app_commands.Choice(name=relic, value=relic)
        for relic in relics if current.lower() in relic.lower()
    ]

async def rarity_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    rarities = ['SSR', 'SSR+', 'UR', 'UR+', 'MR']
    return [
        app_commands.Choice(name=rarity, value=rarity)
        for rarity in rarities if current.lower() in rarity.lower()
    ]

# async def card_autocomplete(
#     interaction: discord.Interaction,
#     current: str,
# ) -> List[app_commands.Choice[str]]:
#     cards = card_list 
#     return [
#         app_commands.Choice(name=card, value=card)
#         for card in cards if current.lower() in card.lower()
#     ]

# EMOJI VARIABLES -- importing vars from IA_Images.py
# elemental_emoji = '<:image_yuansu:1183254474907717632>' 
# ragnarok_emoji = '<:img_series_1:1183254478250582046>'
# firmament_emoji = '<:img_CQZX:1183254476258291842>'
# sacredbeast_emoji = '<:img_SSS:1183254479726977106>'
# starstone_emoji = '<:starstone:1084156379478102116> '
# elemstone_emoji = '<:elemstone:1084157123916746793>'
# blue_treasure_emoji = '<:1000064:1183498487900405881> '
# purple_treasure_emoji = '<:1000065:1183498489569738783>'
# yellow_treasure_emoji = '<:1000066:1183498492233134278>'
# red_star = '<:ssrstar:1084156383336861736>'
# blue_star = '<:urstar:1084157131315495094>'
# gold_star = '<:urplusstar:1084157133743992922>'
# green_star = '<:mrstar:1175154832852664330>'
# eudo_star = '<:eudo_star:1183506097953321030>'
# empty_star = '<:emptystar:1084157132473122938>'
# red_scroll = ''
# yellow_scroll = ''
# blue_scroll = ''

def get_version():
    connection = sqlite3.connect('ia.db')
    cursor = connection.cursor()
    ver = cursor.execute('SELECT "0" FROM version').fetchall()
    version = ver[1][0]
    return version

# VOID RIFT LOOKUP
@client.tree.command()
@app_commands.describe(
    level = 'Void Rift level, e.g. 100-2')
async def void(interaction: discord.Interaction, level: str):
    """Void Rift boss lookup, e.g. 100-2"""
    await interaction.response.defer()
    try:
        group = str(level.split("-")[0])
        difficulty = str(level.split("-")[1])
    except:
        await interaction.followup.send("Try this format: `/void 100-2`")

    number_pattern = re_compile(r'^[1-9][0-9]*$')
    if number_pattern.match(group) is None:
        await interaction.followup.send("Input the level and difficulty separated by a space\nExample: `.void 200-2`")
        return

    # connect to db
    connection = sqlite3.connect('ia.db')
    cursor = connection.cursor()

    boss = cursor.execute('SELECT boss_name, skill_id_list, max_hp, max_attack, image_id, physc_def, magic_def, defend, decrit, job FROM void WHERE "group"=? AND difficulty=?', (group, difficulty)).fetchall()

    # error handling
    if not boss:
        await interaction.followup.send(f"I didn't find anything for {group}-{difficulty} in Void Rift.")
        return

    boss_name = boss[0][0]
    skill_1 = boss[0][1].split("|")[0]
    skill_2 = boss[0][1].split("|")[1]
    max_hp = boss[0][2]
    max_atk = boss[0][3]
    avatar = boss[0][4]
    pdef = boss[0][5]
    mdef = boss[0][6]
    defense = boss[0][7]
    fort = boss[0][8]
    job = boss[0][9]
    if job == 1:
        job = 'Warrior'
    elif job == 2:
        job == 'Archer'
    elif job == 3:
        job == 'Mage'
    s1 = cursor.execute(f'SELECT info FROM skill WHERE sid={skill_1}').fetchall()
    s2 = cursor.execute(f'SELECT info FROM skill WHERE sid={skill_2}').fetchall()
    s1_text = s1[0][0]
    s1_text = s1_text.replace('\\n', '\n')
    s2_text = s2[0][0]
    s2_text = s2_text.replace('\\n', '\n')

    icon = f"https://raw.githubusercontent.com/nillabutt/ia_dump/main/EN/ASSETS/icon/outlandboss/img_hz_boss{avatar}.png"

    # create embed object
    cur_ver = get_version()
    em = discord.Embed(color=0xa054e3)
    em.set_author(name=f"Void Rift: {group}-{difficulty} | {boss_name} - {job}")
    em.add_field(name="Attributes", value=f"**Max HP** = `{max_hp:n}`\n**Max ATK** = `{max_atk:n}`\n**P.DEF** = `{pdef:n}`\n**M.DEF** = `{mdef:n}`\n**DEF** = `{defense:n}`\n**FOR** = `{fort:n}`", inline=False)
    em.add_field(name="1st Skill", value=f"_{s1_text}_", inline=True)
    em.add_field(name="2nd Skill", value=f"_{s2_text}_", inline=True)
    em.set_thumbnail(url=icon)
    em.set_footer(text=f"Data retrieved from Idle Angels version {cur_ver}")
    await interaction.followup.send(embed=em)

    # close connection
    cursor.close()
    connection.close() 

# example
# @client.tree.command()
# @app_commands.describe(
#     first_value = 'the first value to input', 
#     second_value = 'the second value to input')
# async def add(interaction: discord.Interaction, first_value: int, second_value: int):
#     """docstring"""
#     await interaction.response.send_message(f'{first_value} {second_value}')

# NIGHTMARE LOOKUP ------------------------------------------------------------------
# buttons:
class Nightmare_Menu(discord.ui.View):
    def __init__(self, embeds):
        super().__init__(timeout=None)
        self.value = None
        self.embeds = embeds

    @discord.ui.button(label="Boss1", style=discord.ButtonStyle.blurple)
    async def boss1(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.embeds[0]
        await interaction.response.edit_message(embed=embed)
    @discord.ui.button(label="Boss2", style=discord.ButtonStyle.blurple)
    async def boss2(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.embeds[-1]
        await interaction.response.edit_message(embed=embed)

# slash command
@client.tree.command()
@app_commands.describe(
    level = 'Nightmare Dungeon level, e.g. 35-30')
async def nightmare(interaction: discord.Interaction, level: str):
    """Nightmare boss lookup, e.g. 35-30"""
    await interaction.response.defer()
    # connect to db
    connection = sqlite3.connect('ia.db')
    cursor = connection.cursor()

    boss_list = cursor.execute('SELECT boss_monster_npc_id_list FROM nightmare WHERE "name"=?', (level,)).fetchall()
    npc1 = boss_list[0][0].split("|")[0]
    npc2 = boss_list[0][0].split("|")[1]

    count = 0
    embeds = []
    for npc in boss_list[0][0].split("|"):
        boss = cursor.execute('SELECT name, job, skill_id_list, hp, maxatk, cir, dcir, pdef, mdef, def, avatar_path FROM nightmare_npc WHERE "npc_id"=?', (npc,)).fetchall()
        boss_name = boss[0][0]
        job = boss[0][1]
        job_name = ''
        if job == 1:
            job_name = 'Warrior'
        if job == 2: 
            job_name = 'Archer'
        if job == 3:
            job_name = 'Mage'
        boss_s1_id = boss[0][2].split("|")[0]
        boss_s2_id = boss[0][2].split("|")[-1] # in case boss has only 1 skill
        boss_s1 = cursor.execute(f'SELECT info FROM skill WHERE sid={boss_s1_id}').fetchall()
        boss_s2 = cursor.execute(f'SELECT info FROM skill WHERE sid={boss_s2_id}').fetchall()
        boss_s1_text = boss_s1[0][0]
        boss_s1_text = boss_s1_text.replace('\\n', '\n')
        boss_s2_text = boss_s2[0][0]
        boss_s2_text = boss_s2_text.replace('\\n', '\n')
        HP, ATK, CRIT, FOR = boss[0][3], boss[0][4], boss[0][5], boss[0][6]
        PRES, MRES, DEF = boss[0][7], boss[0][8], boss[0][9]
        boss_icon = f'https://raw.githubusercontent.com/nillabutt/ia_dump/main/EN/ASSETS/icon/face/{boss[0][10]}'
        cur_ver = get_version()

        # create embed
        colors = [0x34eb8f, 0xebd034]
        em = discord.Embed(color=colors[count])
        count += 1
        em.set_author(name=f"Nightmare {level} | {boss_name} | {job_name}")
        em.add_field(name="Attributes", value=f"**Max HP**: `{HP:n}`\n**Max ATK**: `{ATK:n}`\n**CRIT**: `{CRIT:n}`\n**FOR**: `{FOR:n}`\n**P.RES**: `{PRES:n}`\n**M.RES**: `{MRES:n}`\n**DEF**: `{DEF:n}`", inline=False)
        em.add_field(name="1st Skill", value=f"_{boss_s1_text}_", inline=True)
        if len(boss[0][2].split("|")) == 2:
            em.add_field(name="2nd Skill", value=f"_{boss_s2_text}_", inline=True)
        em.set_thumbnail(url=boss_icon)
        em.set_footer(text=f"Data retrieved from Idle Angels version {cur_ver}")

        embeds.append(em)
        # await interaction.response.send_message(embed=em)
    await interaction.followup.send(content=f"Nightmare {level} Bosses", view=Nightmare_Menu(embeds))


    # close connection
    cursor.close()
    connection.close()  
    
# DUNGEON LOOKUP -----------------------------------------------------
@client.tree.command()
@app_commands.describe(
    level = 'Dungeon level, e.g. 42-100')
async def dungeon(interaction: discord.Interaction, level: str):
    """Dungeon boss lookup, e.g. 42-100"""
    await interaction.response.defer()
    # connect to db
    connection = sqlite3.connect('ia.db')
    cursor = connection.cursor()

    boss_id = cursor.execute('SELECT boss_monster_npc_id FROM dungeon WHERE "name"=?', (level,)).fetchall()
    boss_id = boss_id[0][0]
    boss1 = cursor.execute('SELECT name, job, skill_id_list, hp, maxatk, cir, dcir, pdef, mdef, def, avatar_path FROM npc WHERE npc_id = ?', (boss_id,)).fetchall()

    # assign values
    b1_name = boss1[0][0]
    b1_job =  boss1[0][1]
    if b1_job == 1:
        b1_job = 'Warrior'
    elif b1_job ==2:
        b1_job = 'Archer'
    elif b1_job == 3:
        b1_job = 'Mage'
    b1_skill1 = boss1[0][2].split("|")[0]
    b1_skill2 = boss1[0][2].split("|")[-1] # just in case it only has 1 skill
    b1_s1 = cursor.execute(f'SELECT info FROM skill WHERE sid={b1_skill1}').fetchall()
    b1_s2 = cursor.execute(f'SELECT info FROM skill WHERE sid={b1_skill2}').fetchall()
    b1_s1_text = b1_s1[0][0]
    b1_s1_text = b1_s1_text.replace('\\n', '\n')
    b1_s2_text = b1_s2[0][0]
    b1_s2_text = b1_s2_text.replace('\\n', '\n')
    b1_hp =   boss1[0][3]
    b1_atk =  boss1[0][4]
    b1_crit = boss1[0][5]
    b1_for =  boss1[0][6]
    b1_pres = boss1[0][7]
    b1_mres = boss1[0][8]
    b1_def =  boss1[0][9]
    b1_icon = boss1[0][10]
    b1_icon = f'https://raw.githubusercontent.com/nillabutt/ia_dump/main/EN/ASSETS/icon/face/{b1_icon}'
    cur_ver = get_version()

    # create embeds
    em1 = discord.Embed(color=0xc96624)
    em1.set_author(name=f"Main Dungeon {level} | {b1_name} | {b1_job}")
    em1.add_field(name="Attributes", value=f"**Max HP** = `{b1_hp:n}`\n**Max ATK** = `{b1_atk:n}`\n**CRIT** = `{b1_crit:n}`\n**FOR** = `{b1_for:n}`\n**P.RES** = `{b1_pres:n}`\n**M.RES** = `{b1_mres:n}`\n**DEF** = `{b1_def:n}`", inline=False)
    em1.add_field(name="1st Skill", value=f"_{b1_s1_text}_", inline=True)
    if len(boss1[0][2].split("|")) == 2:
        em1.add_field(name="2nd Skill", value=f"_{b1_s2_text}_", inline=True)
    em1.set_footer(text=f"Data retrieved from Idle Angels version {cur_ver}")
    em1.set_thumbnail(url=b1_icon)

    await interaction.followup.send(embed=em1)

    # close connection
    cursor.close()
    connection.close()

# SKYTOWER LOOKUP ===============================================================
@client.tree.command()
@app_commands.describe(
    level = 'Sky Tower layer, e.g. 550')
async def skytower(interaction: discord.Interaction, level: str):
    """Sky Tower boss lookup, e.g. 550"""
    await interaction.response.defer()
    connection = sqlite3.connect('ia.db')
    cursor = connection.cursor()
    tow = cursor.execute("SELECT desc, normal_monster_npc_id_list, reward_first FROM tower WHERE layer = ?",(level,)).fetchall()
    tower_desc = tow[0][0]
    boss_id = tow[0][1].split("|")[0]
    reward_first = tow[0][2]

    towboss = cursor.execute("SELECT name, avatar_path, job, skill_id_list, max_hp, max_attack, defend, physc_def, magic_def, crit, decrit, debuff_resist FROM tower_boss WHERE npc_id = ?",(boss_id,)).fetchall()
    boss_name = towboss[0][0]
    boss_av = towboss[0][1]
    boss_job = towboss[0][2]
    boss_sids = towboss[0][3]
    hp = towboss[0][4]
    atk = towboss[0][5]
    crit = towboss[0][9]
    defend = towboss[0][6]
    pdef = towboss[0][7]
    mdef = towboss[0][8]
    fort = towboss[0][10]
    deb = towboss[0][11]
    debuff = f"{deb/10}%"
    job = ''
    if boss_job == 1:
        job = 'Warrior'
    elif boss_job == 2:
        job = 'Archer'
    elif boss_job == 3:
        job = 'Mage'
    cur_ver = get_version()
    boss_sid1 = boss_sids.split("|")[0]
    s1_name = get_skill(boss_sid1)[0][0]
    s1_text = get_skill(boss_sid1)[0][1]
    s1_text = s1_text.replace('\\n', '\n')
    s1_print = f"**{s1_name}** — _{s1_text}_"    
    if len(boss_sids.split("|")) > 1:
        boss_sid2 = boss_sids.split("|")[1]
        s2_name = get_skill(boss_sid2)[0][0]
        s2_text = get_skill(boss_sid2)[0][1]
        s2_print = f"**{s2_name}** — _{s2_text}_"

    avatar = f'https://raw.githubusercontent.com/nillabutt/ia_dump/main/EN/ASSETS/icon/face/{boss_av}'
    # create embed
    em1 = discord.Embed(color=0x7df8ff)
    em1.set_author(name=f"Sky Tower: {level} | {boss_name} x6 | {job}")
    em1.add_field(name="Description", value=f"_{tower_desc}_", inline=False)
    em1.add_field(name="Attributes", value=f"HP: `{hp:n}`\nATK: `{atk:n}`\nCRIT: `{crit:n}`\nFOR: `{fort:n}`", inline=True)
    em1.add_field(name='', value=f"DEF: `{defend:n}`\nP.RES: `{pdef:n}`\nM.RES: `{mdef:n}`\nDebuff RES: `{debuff}`", inline=True)
    em1.add_field(name="Skills", value='',inline=False)
    em1.add_field(name="1st Skill", value=f"{s1_print}", inline=True)
    em1.set_footer(text=f"Data retrieved from Idle Angels version {cur_ver}")
    em1.set_thumbnail(url=avatar)
    if len(boss_sids.split("|")) > 1:
        em1.add_field(name="2nd Skill", value=f"{s2_print}", inline=True)
    await interaction.followup.send(embed=em1)

    # close connection
    cursor.close()
    connection.close()

# EUDEMON LOOKUP -------------------------------------------------------
def get_eud_id(eud_name):
    connection = sqlite3.connect('ia.db')
    cursor = connection.cursor()
    # trimmed = list(eud_name)
    # trimmed = trimmed[0] + trimmed[1] + trimmed[2] + "%"
    # eud_id = cursor.execute(f"SELECT cid FROM eudemon WHERE name LIKE {trimmed}").fetchall()
    search = eud_name.lower()
    eud_id = cursor.execute("SELECT cid FROM eudemon WHERE name COLLATE NOCASE = ?",(eud_name,)).fetchall()
    result = eud_id[0][0]
    # try:
    #     result = eud_id[0][0]
    # except:
    #     result = 12
    cursor.close()
    connection.close() 

    return result

@client.tree.command()
@app_commands.autocomplete(eudemon_name = eudemon_autocomplete)
@app_commands.describe(
    eudemon_name = 'Name or ID of the Eudemon',
    level = "The Eudemon's level, from 1 thru 150")
async def eudemon(interaction: discord.Interaction, eudemon_name: str, level: int):
    """Eudemon lookup and stat calculator, e.g. undine 120"""
    await interaction.response.defer()
    if eudemon_name == 'Hati&Sköll':
        eudemon_name = '12'
    if eudemon_name.isnumeric() == True:
        eud_id = eudemon_name
    else:
        eud_id = get_eud_id(eudemon_name)

    if level > 150:
        level = 150
    elif level < 1:
        level = 1

    # query
    connection = sqlite3.connect('ia.db')
    cursor = connection.cursor()

    eud_info = cursor.execute("SELECT name, type, race, age, story_content, str_initial, agi_initial, int_initial, sta_initial, unlock_need_goods_count, unlock_favor FROM eudemon WHERE cid =?",(eud_id,)).fetchall()
    
    # basic info
    eud_name= eud_info[0][0]
    eud_type= eud_info[0][1]
    race    = eud_info[0][2]
    age     = eud_info[0][3]
    story   = eud_info[0][4]
    story = story.replace('\\n', '\n')
    strength= eud_info[0][5]
    agility = eud_info[0][6]
    intel   = eud_info[0][7]
    stamina = eud_info[0][8]

    # land info
    land_info = cursor.execute("SELECT land_id, debris_type, add_debris_count FROM eudemon_land WHERE cid = ?",(eud_id,)).fetchall()
    land_id = land_info[0][0]
    shard_type = land_info[0][1]
    shard_coount = land_info[0][2]
    if shard_type == 3:
        shard_emoji = blue_treasure_emoji
    elif shard_type == 4:
        shard_emoji = purple_treasure_emoji
    
    land_name = cursor.execute("SELECT name FROM treasure_land WHERE place_id = ?",(land_id,)).fetchall()
    land_name = land_name[0][0]

    # sum of exp
    exp_info = cursor.execute("SELECT SUM(need_exp) FROM eudemon_exp WHERE level BETWEEN 1 AND ?", (level,)).fetchall()
    total_exp = exp_info[0][0]

    # stats from awaken
    attrib_add = 0
    star_stones = 0
    elem_stones = 0
    star = 0
    if level > 100:
        if level > 140:
            star = 5
        elif level > 130:
            star = 4
        elif level > 120:
            star = 3
        elif level > 110:
            star = 2
        else:
            star = 1
        attrib_info = cursor.execute("SELECT str_add, consume_goods FROM eudemon_awake WHERE cid = ? AND awake_star = ?",(eud_id,star)).fetchall()
        attrib_add = attrib_info[0][0]
        consume_string = attrib_info[0][1]
        attrib_add = attrib_add * star
        
        consume_split = consume_string.split("|")
        if len(consume_split) == 1: # for non-series eudemons
            this_cost = consume_split[0].split(":")[-1] # final value of split is amount of goods used
            cost_per_star = math.floor(int(this_cost) / star)
            star_stones = sum(range(1, star+1)) * cost_per_star
        else:
            star_stone_cost = consume_split[0].split(":")[-1]
            star_stone_per_star = math.floor(int(star_stone_cost) / star)
            star_stones = sum(range(1, star+1)) * star_stone_per_star

            elem_cost = consume_split[1].split(":")[-1]
            elem_per_star = math.floor(int(elem_cost) / star)
            elem_stones = sum(range(1, star+1)) * elem_per_star

    # series stats
    if eud_type == 0:
        series = '*Not in a Series*'
        series_stat = 'No series stats'
    else:
        series_info = cursor.execute("SELECT name, icon_select, attribute_desc FROM eudemon_series WHERE type = ?",(eud_type,)).fetchall()
        series = series_info[0][0]
        series_icon = series_info[0][1]
        series_stat = series_info[0][2]
        series_stat = series_stat.strip('<size=21>').strip('</size>')
    
    # talents
    talent_info = cursor.execute('SELECT name, desc, "add_value[1]" FROM eudemon_talent WHERE cid = ?',(eud_id,)).fetchall()
    talent = talent_info[0][0]
    talent_desc = talent_info[0][1]
    combat = 'No combat talent'
    if eud_type != 0:
        combat_stuff = talent_info[0][2].split("|")[1]
        attr_l = combat_stuff.split(":")[1]
        attr_r = combat_stuff.split(":")[2]
        combat_val = combat_stuff.split(":")[3]
        attr_enum = ":".join([attr_l, attr_r])
        attr_name = get_attrib(attr_enum).replace('Min', '')
        modify = 10
        percent = '%'
        flat_list = ['3:10', '3:21', '2:1', '2:2', '2:3', '2:4', '2:18']
        if attr_enum in flat_list:
            percent = ''
            modify = 1
        combat_stat = int(combat_val) / modify
        if level > 80:
            combat_stat *= 5
        elif level > 60:
            combat_stat *= 4
        elif level > 40:
            combat_stat *= 3
        elif level > 20:
            combat_stat *= 2
        combat = f"{attr_name} +{combat_stat:n}{percent}"
            
    talent_value = '5%'
    if level > 80:
        talent_value = '25%'
    elif level > 60:
        talent_value = '20%'
    elif level > 40:
        talent_value = '15%'
    elif level > 20:
        talent_value = '10%'

    # costs
    # unlock costs
    if eud_type == 0:
        favor = eud_info[0][10]
        unlock_elem_stone = 0
    else:
        favor = 0
        unlock_elem_stone = eud_info[0][9]

    elem_stones += unlock_elem_stone

    # series icons and embed color
    emoji = '\t'
    color = 0xffdd78
    if eud_type == 1001:
        emoji = elemental_emoji 
        color = 0x0044ab
    elif eud_type == 1002:
        emoji = '<:img_series_1:1183254478250582046>'
        color = 0x30b7ff
    elif eud_type == 1003:
        emoji = '<:img_CQZX:1183254476258291842>'
        color = 0xdec400
    elif eud_type == 1004:
        emoji = '<:img_SSS:1183254479726977106>'
        color = 0x49a65f

    # attribute calculation
    STR = (level + 9) * (strength / 10) + attrib_add
    AGI = (level + 9) * (agility / 10) + attrib_add
    INT = (level + 9) * (intel / 10) + attrib_add
    EDR = (level + 9) * (stamina / 10) + attrib_add

    # eudemon stars display
    eudemon_stars = ''
    for i in range(1, star+1):
        eudemon_stars += eudo_star
    for i in range(star, 5):
        eudemon_stars += empty_star

    eudemon_face = cursor.execute("SELECT avatar_icon_small FROM eudemon_skin WHERE animal_cid = ?",(eud_id,)).fetchall()
    face_id = eudemon_face[0][0]
    face = f"https://raw.githubusercontent.com/nillabutt/ia_dump/main/EN/ASSETS/icon/outland/{face_id}"

    cur_ver = get_version()

    # assemble the embed
    em1 = discord.Embed(color=color)
    em1.set_author(name=f"{eud_name} | Level {level}")
    em1.add_field(name=f"{eudemon_stars}", value=f"**Race**: `{race}`\n**Age**: `{age}`\n**Talent**: _{talent}_\n`{talent_desc} +{talent_value}`\n{emoji}**Series Set Bonus**:\n_{series}_\n`{series_stat}`\n**Combat Bonus**:\n`{combat}`", inline = True)
    em1.add_field(name="__Attributes__", value=f"**STR** = `{STR:n}`\n**AGI** = `{AGI:n}`\n**INT** = `{INT:n}`\n**EDR** = `{EDR:n}`", inline=True)
    em1.add_field(name="__Miracle Bonus__", value=f"Land {land_id} | `+{shard_coount}`{shard_emoji} at _{land_name}_", inline = False)
    em1.add_field(name="__Total Costs__", value=f"{favor:n} favor, {star_stones}{starstone_emoji}, {elem_stones}{elemstone_emoji}, `{total_exp:n}` exp", inline = False)
    em1.add_field(name="__Background__", value=f"{story}", inline=False)
    em1.set_footer(text=f"Data retrieved from Idle Angels version {cur_ver}")
    em1.set_thumbnail(url=face)

    await interaction.followup.send(embed=em1)

    # close connection
    cursor.close()
    connection.close() 

# FASHION LOOKUP -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Skin_Menu(discord.ui.View):
    def __init__(self, embeds, names):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.names = names

        for i in range(len(self.embeds)):
            @discord.ui.button(label=self.names[i], style=discord.ButtonStyle.blurple)
            async def skin_button0(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed = self.embeds[i]
    


# ANGEL LOOKUP =====================================================================
                
# functions
def get_skill(sid):
    connection = sqlite3.connect('ia.db')
    cursor = connection.cursor()
    result = cursor.execute("SELECT name, info, init_anger, use_need_anger, mr_skill_add_attr_info FROM skill WHERE sid = ?",(sid, )).fetchall()
    return result
def get_angel(cid):
    connection = sqlite3.connect('ia.db')
    cursor = connection.cursor()
    result = cursor.execute("SELECT name, cid FROM angel WHERE cid = ?",(cid,)).fetchall()
    return result[0][0] 
def get_attrib(key):
    connection = sqlite3.connect('ia.db')
    cursor = connection.cursor()
    result = cursor.execute("SELECT key, attribute FROM attribute_enums WHERE key = ?",(key,)).fetchall()
    attribute = result[0][1]
    return attribute

flat_list = ['3:10', '3:21', '2:1', '2:2', '2:3', '2:4', '2:18']

# buttons
class Angel_Menu(discord.ui.View):
    def __init__(self, embeds):
        super().__init__(timeout=None)
        self.value = None
        self.embeds = embeds

    @discord.ui.button(label="Skills", style=discord.ButtonStyle.blurple)
    async def skill_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.embeds[0]
        await interaction.response.edit_message(embed=embed)
    @discord.ui.button(label="Effects", style=discord.ButtonStyle.blurple)
    async def effects_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.embeds[1]
        await interaction.response.edit_message(embed=embed)    
    @discord.ui.button(label="Fates", style=discord.ButtonStyle.blurple)
    async def fate_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.embeds[2]
        await interaction.response.edit_message(embed=embed)
    @discord.ui.button(label="Relic", style=discord.ButtonStyle.blurple)
    async def relic_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.embeds[3]
        await interaction.response.edit_message(embed=embed)
    @discord.ui.button(label="Destiny", style=discord.ButtonStyle.blurple)
    async def destiny_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.embeds[4]
        await interaction.response.edit_message(embed=embed)
    @discord.ui.button(label="Wonder Zones", style=discord.ButtonStyle.blurple)
    async def wonder_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.embeds[5]
        await interaction.response.edit_message(embed=embed)    
    @discord.ui.button(label="Story", style=discord.ButtonStyle.blurple)
    async def story_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.embeds[6]
        await interaction.response.edit_message(embed=embed)       
    # @discord.ui.button(label="Fashions", style=discord.ButtonStyle.blurple)
    # async def fashion_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     embed = self.embeds[4]
    #     await interaction.response.edit_message(embed=embed)

@client.tree.command()
@app_commands.autocomplete(angel_name = angel_autocomplete)
@app_commands.describe(
    angel_name = 'Name of the Angel',
    awaken_status = "The angel's awaken status, e.g. 5/5 - slashes optional - if awaken exists, put a 0")
async def angel(interaction: discord.Interaction, angel_name: str, awaken_status: str):
    """Angel with awaken lookup - e.g. 5/5 - slashes optional and order doesn't matter - if awaken exists, count the stars (0 to 5)"""
    await interaction.response.defer()
    connection = sqlite3.connect('ia.db')
    cursor = connection.cursor()
    embeds = []
    em1_color = 0xec130d 
    if angel_name.lower() == 'uriel': # TODO create function upon start that creates a list of 'from_ur' angels to compare
        awaken_status = awaken_status + '5' # accounts for lack of SSR+ existence
    awaken_sort = ''.join(sorted(awaken_status.replace("/", ""))) # arranges awaken in normal order
    if awaken_sort.isnumeric() == False:
        await interaction.followup.send(f"`{awaken_status}` is not a valid format. A valid format would be `1/2/5`, `5/2/1`, `2/1/5`, `125`, `521`, etc. Slashes are optional and order does not matter.", ephemeral=True)
    awaken_len = len(awaken_sort) # number of awakens
    awaken_emoji_list = ['','','','','']
    # set awaken flags
    ur_awaken, urp_awaken, mr_awaken, sp_awaken = False, False, False, False
    ur_star, urp_star, mr_star = False, False, False
    base_star = int(awaken_sort[-1])
    if awaken_len == 2:
        ur_awaken = True
        ur_star = awaken_sort[-2]
    elif awaken_len == 3:
        ur_awaken = True
        urp_awaken = True
        ur_star, urp_star = awaken_sort[-2], awaken_sort[-3]
    elif awaken_len == 4:
        ur_awaken = True
        urp_awaken = True
        mr_awaken = True
        ur_star, urp_star, mr_star = awaken_sort[-2], awaken_sort[-3], awaken_sort[-4]

    # query for each awaken flag

    base_star = awaken_sort[-1]
    if angel_name.isnumeric() == True:
        base_result = cursor.execute(
            "SELECT cid, is_sp, job, quality_level, potential, skill_ids, name, avatar_path, from_ur FROM angel \
            WHERE cid = ?", (angel_name,)).fetchall()
    else:
        base_result = cursor.execute(
            "SELECT cid, is_sp, job, quality_level, potential, skill_ids, name, avatar_path, from_ur FROM angel \
            WHERE name COLLATE NOCASE = ?", (angel_name,)).fetchall()

    # assign all variables from result
    cid = base_result[0][0]
    is_sp = base_result[0][1]
    job = base_result[0][2]
    if job == 1:
        job = 'Warrior'
    elif job == 2:
        job = 'Archer'
    elif job == 3:
        job = 'Mage'
    quality = base_result[0][3]
    potential = base_result[0][4]
    skill_ids = base_result[0][5]
    angel_name = base_result[0][6]
    face_icon = base_result[0][7]
    from_ur = base_result[0][8]

    if is_sp == 1:
        print("is_sp", is_sp)
        ur_awaken, urp_awaken, mr_awaken, sp_awaken = False, False, False, True
        awaken_sort = 5
        base_star = 5
        awaken_emoji_list = [blue_star, blue_star, blue_star, blue_star, blue_star]
    
    if from_ur == 0:
        star_count = 0
        while star_count < int(base_star):
            awaken_emoji_list[star_count] = red_star
            star_count += 1
    
    # splits to list, then slices the list up until the max base awaken
    skills = skill_ids.split("|")[0:int(base_star)+1]
    skill_one_id = skills[0]
    try:
        skill_two_id = skills[1]
    except:
        skill_two_id = ''
    urp_passive_id = ''
    mr_skill_id = ''
    
    # skill and passive list for Base and UR - UR will replace entries if awakened
    skill_list = [] # access skill texts via index=base star
    if from_ur == 1:
        skill_list = ['?','?','?','?','?','?']
    else:
        for skill in skills:
            query = get_skill(skill) # get_skill() retrieves: 0 name, 1 info, 2 init_anger, 3 use_need_anger, 4 mr_skill_add_attr_info
            this_name = query[0][0]
            this_text = query[0][1]
            this_name = "**"+ this_name +"** — "
            this_text = this_name + "_" + this_text + "_"
            this_text = this_text.replace('\\n', '\n').replace('<size=16>','').replace('</size>','').replace('<size=19>','')
            skill_list.append(this_text)

    # stats, skills, avatar, frame, 
    if ur_awaken == True:
        em1_color = 0x830dec 
        ur_star = awaken_sort[-2]
        ur_result = cursor.execute("SELECT quality_level, potential, skill_ids, avatar_path FROM ur_angel \
        WHERE cid = ? AND is_open = 1",(cid,)).fetchall()
        try:
            ur_result[0][0]
        except:
            await interaction.followup.send(f"{angel_name} doesn't have UR Awakening.", ephemeral=True)
        quality = ur_result[0][0]
        potential = ur_result[0][1]
        skill_ids = ur_result[0][2]
        face_icon = ur_result[0][3]
        skills = skill_ids.split("|")[0:int(ur_star)+1]
        skill_one_id = skills[0]
        try:
            skill_two_id = skills[1]
        except:
            skill_two_id = skill_two_id
        i = 0
        for skill in skills:        
            query = get_skill(skill)
            this_name = query[0][0]
            this_text = query[0][1]
            this_name = "**"+ this_name +"** — "
            this_name = this_name.replace('<size=17>','').replace('</size>','').replace('<size=19>','')
            this_text = this_name + "_" + this_text + "_"
            this_text = this_text.replace('\\n', '\n').replace('<size=16>','').replace('</size>','').replace('<size=19>','')
            skill_list[i] = this_text
            i += 1
        star_count = 0
        while star_count < int(ur_star):
            awaken_emoji_list[star_count] = blue_star
            star_count += 1

    if urp_awaken == True:
        em1_color = 0x0de5ec 
        urp_star = awaken_sort[-3]
        urp_result = cursor.execute("SELECT quality_level, potential, exclusive_skill_id_arr FROM urp_angel \
        INNER JOIN urp_skill ON urp_angel.cid = urp_skill.hero_id \
        WHERE urp_angel.is_open = 1 AND urp_skill.hero_id = ?",(cid,)).fetchall()
        try:
            urp_result[0][0]
        except: # if index out of range
            await interaction.followup.send(f"{angel_name} doesn't have UR+ Awakening.", ephemeral=True)
        quality = urp_result[0][0]
        potential = urp_result[0][1]
        skill_ids = urp_result[0][2]
        urp_skill_id = skill_ids.split("|")[0]
        urp_passive_id = urp_skill_id
        urp_skill_query = get_skill(urp_skill_id)
        urp_skill_name = urp_skill_query[0][0]
        urp_skill_name = urp_skill_name.replace('<size=17>','').replace('</size>','')
        urp_skill_text = urp_skill_query[0][1]
        urp_skill = "**"+ urp_skill_name +"** — " + "_" + urp_skill_text + "_"
        urp_skill = urp_skill.replace('\\n', '\n')
        star_count = 0
        while star_count < int(urp_star):
            awaken_emoji_list[star_count] = gold_star
            star_count += 1

    if mr_awaken == True:
        em1_color = 0x76ec0d 
        mr_star = awaken_sort[-4]
        mr_result = cursor.execute("SELECT quality_level, potential, active_skill_ids, use_skill_add_anger, normal_attack_add_anger, lose_hp_percent_for_anger, lose_hp_add_anger  \
        FROM mr_angel WHERE cid = ?",(cid,)).fetchall()
        try:
            mr_result[0][0]
        except:
            await interaction.followup.send(f"{angel_name} doesn't have MR Awakening.", ephemeral=True)
        quality = mr_result[0][0]
        potential = mr_result[0][1]
        skill_ids = mr_result[0][2]
        skills = skill_ids.split("|")[0:int(mr_star)+1]
        mr_skill_id = skills[-1]
        star_count = 0
        while star_count < int(mr_star):
            awaken_emoji_list[star_count] = green_star
            star_count += 1
        skill_anger = mr_result[0][3]
        basic_anger = mr_result[0][4]
        lose_hp = mr_result[0][5]
        dmg_anger = mr_result[0][6]
        init_anger = 0
        use_anger = 0
        mr_skill = ''
        mr_passive_list = []
        for skill in skills: # could grab 1 skill at the index, but need passive stats for all lower skills too
            query = get_skill(skill) # get_skill() retrieves: 0 name, 1 info, 2 init_anger, 3 use_need_anger, 4 mr_skill_add_attr_info
            this_name = query[0][0]
            this_text = query[0][1]
            init_anger = query[0][2]
            use_anger = query[0][3]
            try:
                passive_text = query[0][4]
                passive_text = passive_text.replace('\\n', ', ')
                mr_passive_list.append(passive_text)
            except AttributeError:
                passive_text = ''            
            this_name = "**"+ this_name +"** — "
            this_text = this_name + "_" + this_text + "_"
            this_text = this_text.replace('\\n', '\n')
            mr_skill = this_text
        mr_stats = "\n".join(mr_passive_list)
    if is_sp == 1:
        awaken_emoji_list = [blue_star, blue_star, blue_star, blue_star, blue_star]
    print(awaken_emoji_list)
    emoji_list = "".join(awaken_emoji_list)

    if mr_awaken == True:
        face = f'https://raw.githubusercontent.com/nillabutt/ia_dump/main/bot_assets/{cid}_MR.png'
    elif urp_awaken == True:
        face = f'https://raw.githubusercontent.com/nillabutt/ia_dump/main/bot_assets/{cid}_UR_PLUS.png'
    elif ur_awaken == True:
        face = f'https://raw.githubusercontent.com/nillabutt/ia_dump/main/bot_assets/{cid}_UR.png'
    else:
        face = f'https://raw.githubusercontent.com/nillabutt/ia_dump/main/bot_assets/{cid}.png'
    
    awaken_stats = 'None'
    try:
        awaken_stats = '\n'.join(skill_list[2:])
    except:
        pass

    # create first embed
    cur_ver = get_version()
    em1 = discord.Embed(color=em1_color)
    em1.set_author(name=f"{angel_name}'s Awaken-specific Traits")
    em1.add_field(name=f"{emoji_list}", value=f"**Job**: {job}  **Potential**: {potential}", inline = False)
    em1.add_field(name="__Skill 1__", value=f"{skill_list[0]}", inline=True)
    try:
        em1.add_field(name="__Skill 2__", value=f"{skill_list[1]}", inline = True)
    except:
        pass
    if urp_awaken == True:
        em1.add_field(name="__UR+ Passive__", value=f"{urp_skill}", inline = False)
    if mr_awaken == True:   
        em1.add_field(name="__MR Skill__", value=f"Initial/Max Energy: `{init_anger}/{use_anger}`\n`+{skill_anger}` Energy per Skill | `+{basic_anger}` Energy per Basic\n`+{dmg_anger}` Energy per `{lose_hp}%` HP lost. \n{mr_skill}", inline=False)
    try:
        em1.add_field(name="__Awaken Stats__: ", value=f"{awaken_stats}", inline=True)
    except:
        pass
    try:
        em1.add_field(name="__MR Stats__", value=f"{mr_stats}", inline=True)
    except:
        pass
    em1.set_thumbnail(url=face)
    em1.set_footer(text=f"Data retrieved from Idle Angels version {cur_ver}")
    embeds.append(em1)

    # BUFF/DEBUFF EFFECTS
    bid_list = [skill_one_id, skill_two_id, urp_passive_id, mr_skill_id]
    print(bid_list)
    em_buff = discord.Embed(color=0x123abc)
    em_buff.set_author(name=f"{angel_name}'s Buff and Debuff Effects")
    em_buff.set_footer(text=f"Data retrieved from Idle Angels version {cur_ver}")
    for bid in bid_list:
        if bid == '':
            continue
        bid_expression = "%" + str(bid)[1:6] + "_" + "1" + "%"
        buff_query = cursor.execute("SELECT bid, name, info, icon FROM skill_buff WHERE bid LIKE ?",(bid_expression,)).fetchall()
        
        for result in buff_query:
            if result[2] == None:
                continue
            elif str(result[0])[7] in ['0','1']:
                print(result)
                buff_name = result[1]
                buff_effect = result[2]
                buff_lookup = result[3]
                try:
                    buff_emoji = globals()[buff_lookup]
                except:
                    buff_emoji = "`no icon`"
                em_buff.add_field(name=f"**{buff_name}**", value=f"{buff_emoji} _{buff_effect}_")
    embeds.append(em_buff)

    # FATES
    fate_query = cursor.execute("SELECT hero_ids, attr_type_type, attr_type, attr_value, group_name FROM fate WHERE hcid = ?",(cid,)).fetchall()
    fate_list = []
    for fate in fate_query:
        fate_cids = fate[0]
        attr_l = fate[1]
        attr_r = fate[2]
        attr_list = [str(attr_l), str(attr_r)]
        attr_val = fate[3]
        group_name = fate[4]
        attr = ":".join(attr_list)
        if attr == '2:1':
            attr_name = 'Max HP'
            attr_val = str(attr_val)
        elif attr == '3:1':
            attr_name = 'ATK UP'
            attr_val = attr_val / 10
            attr_val = f"{attr_val}%"
        elif attr == '3:2':
            attr_name = 'HP UP'
            attr_val = attr_val / 10
            attr_val = f"{attr_val}%"
        elif attr == '3:8':
            attr_name = 'Crit DMG UP'
            attr_val = attr_val / 10
            attr_val = f"{attr_val}%"
        fate_cids = fate_cids.split("|")
        fate_names = []
        for i in fate_cids:
            fate_angel = get_angel(i)
            if fate_angel != angel_name:
                fate_names.append(fate_angel)
        fate_names_sorted = sorted(fate_names)
        fate_names = ", ".join(fate_names_sorted)
        fate_list.append(f"**{group_name}:** {attr_name} `+{attr_val}`\n— *{fate_names}*")
    fate_print = '\n\n'.join(fate_list)    

    # fate embed
    em2 = discord.Embed(color=0x7756d2)
    em2.set_author(name=f"{angel_name}'s Fates")
    em2.add_field(name='__Fate Groups__', value=f"{fate_print}")
    em2.set_footer(text=f"Data retrieved from Idle Angels version {cur_ver}")
    em2.set_thumbnail(url=face)
    embeds.append(em2)

    # RELIC
    try:
        ex_percent = '%'
        ex_result = cursor.execute("SELECT id, attr_type_type, attr_type, attr_value, desc FROM relic_ex WHERE hero = ?",(cid,)).fetchall()
        flat_list = ['3:10', '3:21', '2:1', '2:2', '2:3', '2:4', '2:18']
        ex_id = ex_result[0][0]
        ex_desc = ex_result[0][4]
        attr_l = ex_result[0][1]
        attr_r = ex_result[0][2]
        attr_list = [str(attr_l), str(attr_r)]
        attr_enum = ":".join(attr_list)
        ex_attr = get_attrib(attr_enum)
        ex_val_base = ex_result[0][3]
        ex_val = ex_val_base
        ex_modify = 1
        if attr_enum in flat_list:
            ex_percent = ''
            ex_modify = 10

        sr_val_ex = ex_val /5 * ex_modify
        urp_val_ex = ex_val / 1.6 * ex_modify
        ur5_val_ex = ex_val / (4 / 3) * ex_modify

        ex_print = f"SR: `+{sr_val_ex:.1f}{ex_percent}`, UR+: `+{urp_val_ex:.1f}{ex_percent}`, UR+5: `+{ur5_val_ex:.1f}{ex_percent}`"
        # except:
        #     print('error in exclusive relic lookup')
    
    
        relic_result = cursor.execute("SELECT strengthen_skill_1, strengthen_skill_awake_1, strengthen_skill_2, strengthen_skill_awake_2, \
                                    relic_pvp_skill, attr_fixd_type_type, attr_fixd_type, attr_fixd_value,name, id, desc FROM relic WHERE attr_exclusive_id = ?",(ex_id,)).fetchall()
        if ur_awaken == True:
            mod_s1_id = relic_result[0][1]
        else:
            mod_s1_id = relic_result[0][0]
        if int(ur_star) >= 0:
            mod_s2_id = relic_result[0][3]
        else:
            mod_s2_id = relic_result[0][2]
        pvp_id = relic_result[0][4]
        ra_1_result = get_skill(mod_s1_id)
        ra_2_result = get_skill(mod_s2_id)
        ra_3_result = get_skill(pvp_id)
        ra1_name = ra_1_result[0][0]
        ra1_text = ra_1_result[0][1]
        ra1_text = ra1_text.replace('\\n', '\n')
        ra2_name = ra_2_result[0][0]
        ra2_text = ra_2_result[0][1]
        ra2_text = ra2_text.replace('\\n', '\n')
        ra3_name = ra_3_result[0][0]
        ra3_text = ra_3_result[0][1]
        ra3_text = ra3_text.replace('\\n', '\n')
        relic_awake_body = f"**+30**: __{ra1_name}__ — _{ra1_text}_\n\n**+60**: __{ra2_name}__ — _{ra2_text}_\n\n**+90**: __{ra3_name}__ — _{ra3_text}_"
        attr_l = relic_result[0][5]
        attr_r = relic_result[0][6]
        main_val = relic_result[0][7]
        relic_name = relic_result[0][8]
        relic_id = relic_result[0][9]
        descrip = relic_result[0][10]
        descrip = descrip.replace('\\n', '\n')
        
        attr_list = [str(attr_l), str(attr_r)]
        attr_enum = ":".join(attr_list)
        main_attr = get_attrib(attr_enum)
        main_modify = 1
        main_percent = '%'
        if attr_enum in flat_list:
            main_percent = ''
            main_modify = 10
        sr_val_main = main_val /5 * main_modify
        urp_val_main = main_val / 1.6 * main_modify
        ur5_val_main = main_val / (4 / 3) * main_modify

        main_print = f"SR: `+{sr_val_main:.1f}{main_percent}`, UR+: `+{urp_val_main:.1f}{main_percent}`, UR+5: `+{ur5_val_main:.1f}{main_percent}`"
        relic_image = f'https://raw.githubusercontent.com/nillabutt/ia_dump/main/EN/ASSETS/icon/relicbig%40/{relic_id}/{relic_id}.png'
    except IndexError:
        relic_name = 'N/A'
        descrip = f'{angel_name} has no exclusive relic!'
        main_attr, main_print, ex_attr, ex_print, relic_awake_body, relic_image = '', '', '', '', '', face

    try: # create embed
        em3 = discord.Embed(color=0xd255b1)
        em3.set_author(name=f"{angel_name}'s Exclusive Relic")
        em3.add_field(name=f'***{relic_name}***', value=f"_{descrip}_", inline=False)
        em3.add_field(name=f'**__Attributes__**', value=f"__Main Attribute:__ **{main_attr}**\n{main_print}\n__{angel_name} Exclusive__ **{ex_attr}**\n{ex_print}", inline=False)
        em3.add_field(name=f'**__Awaken Skills__**', value=f"{relic_awake_body}", inline=False)
        em3.set_thumbnail(url=relic_image)
        embeds.append(em3) 
    except:
        em3 = discord.Embed(color=0xd255b1)
        em3.set_author(name=f"{angel_name}'s Exclusive Relic")
        em3.add_field(name=f'***Not Found***', value=f"{angel_name} has no Exclusive Relic")
        em3.set_footer(text=f"Data retrieved from Idle Angels version {cur_ver}")
        embeds.append(em3)
    
    # DESTINY
    # starprints
    if ur_awaken == True:
        destiny_query = cursor.execute("SELECT signal, skill_id FROM destiny WHERE hero_cid = ?",(cid,)).fetchall()
        signal = destiny_query[0][0]
        sid = f"{destiny_query[0][1]}"
        sid1 = sid[0:5] + '1001'
        sid2 = sid[0:5] + '2001'
        sid3 = sid[0:5] + '3001'
        s1_result = get_skill(sid1)
        s2_result = get_skill(sid2)
        s3_result = get_skill(sid3)
        s1_name = s1_result[0][0]
        s1_text = s1_result[0][1]
        s2_name = s2_result[0][0]
        s2_text = s2_result[0][1]
        s3_name = s3_result[0][0]
        s3_text = s3_result[0][1]
        starprint_1 = f"__Lv 10 Collective Star__\n**{s1_name}**: _{s1_text}_"
        starprint_2 = f"__Lv 20 Collective Star__\n**{s2_name}**: _{s2_text}_"
        starprint_3 = f"__Lv 30 Collective Star__\n**{s3_name}**: _{s3_text}_"

        # signal data
        signal_query = cursor.execute('SELECT type, "index", level, add_attr \
                                    FROM signal WHERE signal = ?',(signal,)).fetchall()
        levels = [1, 2, 3, 4, 5]
        nodes_full = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        node_list = []
        
        for node in nodes_full:
            level_stuff = []
            attr_list = []
            attr1_list = []
            attr2_list = []
            for level in levels:
                # get stats, append to list
                for i in signal_query:
                    if i[1] == node:
                        if i[2] == level:
                            attribs = i[3].split("|")
                            attr_l = attribs[0].split(":")[0]
                            attr_r = attribs[0].split(":")[1]
                            attr_enum = f"{attr_l}:{attr_r}"
                            attr_val = attribs[0].split(":")[2]
                            attr_name_1 = get_attrib(attr_enum)
                            modify = 10
                            percent = '%'
                            if attr_enum in flat_list:
                                percent = ''
                                modify = 1
                            attrib_val_1 = int(attr_val) / modify
                            attr1_list.append(f"{attrib_val_1:.0f}{percent}")
                            if len(attribs) == 2:
                                attr_l = attribs[1].split(":")[0]
                                attr_r = attribs[1].split(":")[1]
                                attr_enum = f"{attr_l}:{attr_r}"
                                attr_val = attribs[1].split(":")[2]
                                attr_name_2 = get_attrib(attr_enum)
                                modify = 10
                                percent = '%'
                                if attr_enum in flat_list:
                                    percent = ''
                                    modify = 1
                                attrib_val_2 = int(attr_val) / modify
                                attr2_list.append(f"{attrib_val_2:.0f}{percent}")
            # create a string to append to node_list
            attr1_string = "|".join(attr1_list)
            if len(attribs) == 1:
                node_string = f"__Node {node}__: **{attr_name_1}** {attr1_string}"
            else:
                attr2_string = "|".join(attr2_list)
                node_string = f"__Node {node}__: **{attr_name_1}** {attr1_string} — **{attr_name_2}** {attr2_string}"
            node_list.append(node_string)

        node_print = "\n".join(node_list)    

        # Destiny Embed
        em4 = discord.Embed(color=0xb1d255)
        em4.set_author(name=f"{angel_name}'s Destiny")
        em4.add_field(name=f'**__Shooting Stars__**', value=f"{starprint_1}\n{starprint_2}\n{starprint_3}", inline=False)
        em4.add_field(name=f'**__Attributes__**', value=f"{node_print}", inline=False)
        em4.set_thumbnail(url=face)
        em4.set_footer(text=f"Data retrieved from Idle Angels version {cur_ver}")
    else:
        em4 = discord.Embed(color=0xb1d255)
        em4.set_author(name=f"{angel_name}'s Destiny")
        em4.add_field(name=f'***Not Found***', value=f"{angel_name} has no UR Awakening")
        em4.set_footer(text=f"Data retrieved from Idle Angels version {cur_ver}")
             

    embeds.append(em4)

    # wonder zones 
    zone_query = cursor.execute("SELECT * FROM urp_common").fetchall()
    skills = []
    if urp_awaken == True:
        urp_star = awaken_sort[-3]
        if urp_star != '0':
            for i in range(int(urp_star)+1):
                if i == 0:
                    continue
                ith_zone = zone_query[i]
                zone_name = ith_zone[3]
                zone_skills = ith_zone[2]
                skill_id_list = zone_skills.split("|")
                zone_string = [f"__{zone_name}__"]
                for skill in skill_id_list:
                    skill_name = get_skill(skill)[0][0]
                    skill_text = get_skill(skill)[0][1]
                    skill_name = f"**{skill_name}**"
                    skill_text = f"_{skill_text}_"
                    skill_string = f"{skill_name} - {skill_text}"
                    zone_string.append(skill_string)
                zone_string = '\n'.join(zone_string)
                skills.append(zone_string)
    zone1, zone2, zone3, zone4, zone5 = '*Unlock __Life Zone__ at UR+ 1 star*', '*Unlock __Faith Zone__ at UR+ 2 stars*', '*Unlock __War Zone__ at UR+ 3 stars*', '*Unlock __Soul Zone__ at UR+ 4 stars*', '*Unlock __Judge Zone__ at UR+ 5 stars*'
    if len(skills) != 0:
        zone1 = skills[0]
        if len(skills) >= 2:
            zone2 = skills[1]
        if len(skills) >= 3:
            zone3 = skills[2]
        if len(skills) >= 4:
            zone4 = skills[3]
        if len(skills) == 5:
            zone5 = skills[4]
    if urp_awaken == False:
        zone1, zone2, zone3, zone4, zone5 = '*Does Not Possess UR+ Awakening*', '*Does Not Possess UR+ Awakening*', '*Does Not Possess UR+ Awakening*', '*Does Not Possess UR+ Awakening*', '*Does Not Possess UR+ Awakening*'
    em5 = discord.Embed(color=0x7654d2)
    em5.set_author(name=f"Available Wonder Zones")
    # em5.add_field(name="", value="Unlocked Wonder Zone contain a selection of passive skills. One passive skill in each zone can be activated. The selection can be changed without limitations.", inline=False)
    em5.add_field(name='', value=f"{zone1}", inline=False)
    em5.add_field(name='', value=f"{zone2}", inline=False)
    em5.add_field(name='', value=f"{zone3}", inline=False)
    em5.add_field(name='', value=f"{zone4}", inline=False)
    em5.add_field(name='', value=f"{zone5}", inline=False)
    em5.set_footer(text=f"Data retrieved from Idle Angels version {cur_ver}")
    embeds.append(em5)

    # Story
    story_query = cursor.execute("SELECT story_title, story_content FROM angel_story WHERE hero_cid = ?",(cid,)).fetchall()
    try:
        pantheon = story_query[0][0]
        story = story_query[0][1]
        story = story.replace('\\n', '\n')
    except:
        pantheon = "None Found"
        story = "None Found"

    em6 = discord.Embed(color=0x000000)
    em6.set_author(name=f"{angel_name}'s Story")
    em6.add_field(name=f"__{pantheon}__", value=f"_{story}_")
    em6.set_footer(text=f"Data retrieved from Idle Angels version {cur_ver}")
    embeds.append(em6)

    await interaction.followup.send(content=f"{emoji_list} **{angel_name}**", view=Angel_Menu(embeds))
    # close connection
    cursor.close()
    connection.close() 


# SCROLL CALCULATOR
@client.tree.command()
@app_commands.autocomplete(rarity = rarity_autocomplete)
@app_commands.describe(
    rarity = 'Quality of shards to pull',
    shards = "The number of shards to pull")
async def pulls(interaction: discord.Interaction, rarity: str, shards: int):
    """Pull calculator for Limited Summons given [quality] and [amount] of shards needed, assuming no pity progress exists."""
    await interaction.response.defer()
    if rarity.lower() in ['ssr', 'ssr+', 'ur', 'ur+', 'mr']:
        rarity = rarity
    else:
        rarity = 'mr'
    target = shards
    if str(target).isnumeric() == False:
        if rarity.lower() == 'mr':
            target = 270
        elif rarity.lower() == 'ur+':
            target = 265
        elif rarity.lower() == 'ur':
            target = 260
        elif rarity.lower() == 'ssr+':
            target = 205
        else:
            target = 200
    pities = []
    if rarity.lower() == 'ssr+':
        pities = [7, 20, 55]
    else:
        pities = [6, 16, 65]
        
    shards = 0
    pulls = 0
    pity = [0, 0, 0]
    while shards < target:
        pulls += 1
        pity[0] += 1
        pity[1] += 1
        pity[2] += 1
        if pity[0] >= pities[0]:
            shards += 1
            pity[0] = 0
        elif pity[1] >= pities[1]:
            shards += 2
            pity[1] = 0
        elif pity[2] >= pities[2]:
            shards += 5
            pity[2] = 0
    await interaction.followup.send(f"A _maximum_ of `{pulls}` pulls will earn `{shards}` **{rarity.upper()}** shards.")
    # return [pulls, shards, rarity.upper(), target]

# SHARDS COUNT LISTING
shards_header = 'star: 0    1    2    3    4    5    '
shards_ssr = ' | '.join(['50', '10', '20', '30', '40', '50', '= 200'])
shards_ssrp = ' | '.join(['55', '10', '20', '30', '40', '50', '= 205'])
shards_ur = ' | '.join(['60', '20', '30', '40', '50', '60', '= 260'])
shards_urp = ' | '.join(['65', '20', '30', '40', '50', '60', '= 265'])
shards_mr = ' | '.join(['70', '20', '30', '40', '50', '60', '= 270'])
@client.tree.command()
async def shards(interaction: discord.Interaction):
    """A list of the number of shards needed at each star of a given rarity."""
    await interaction.response.defer()
    await interaction.followup.send(f"Shards required for each star of a given rarity:\n```\n{shards_header}\nSSR : {shards_ssr}\nSSR+: {shards_ssrp}\nUR  : {shards_ur}\nUR+ : {shards_urp}\nMR  : {shards_mr}\n```", ephemeral=True)


# RELEASE ORDER ===============================================================================
urp_order = ["Hera", "Cupid", "Chaos", "Ra", "Icarus", "Himiko", "Heimdall", "Storm Dragon", 
                "Ember Dragon", "Frost Dragon", "Main Angel", "Horus", "Sim Cheong", "Chang'e", "Gemini", "Freyja", "Frigga", 
                "Athena", "Asura", "Capricornus", "Zeus", "Pisces", "Venus", "Ares", "Enmusubi", 
                "Loki", "Apollo"]
mr_order = ["Hera", "Cupid", "Uriel", "Icarus", "Ra", "to_be_announced"]
block_head = 'UR+ Release Order   MR Release Order' # 20 char col spacing
count_name = 0
for u in urp_order:
    u_just = u.ljust(20)
    urp_order[count_name] = u_just
    count_name += 1    
count_name = 0
append_list = [block_head]
for i in urp_order:
    this_string = i
    try:
        this_string = this_string + mr_order[count_name]
    except:
        this_string = this_string
    count_name += 1
    append_list.append(this_string)
block = '\n'.join(append_list)

@client.tree.command()
async def releases(interaction: discord.Interaction):
    """A list of the UR+ release order compared to current MR release order."""
    await interaction.response.defer()
    await interaction.followup.send(f"```\n{block}\n```", ephemeral=True)

# COMMANDS LIST ===============================================================================
@client.tree.command()
async def commands(interaction: discord.Interaction):
    """A list of commands with syntax and usage examples."""
    await interaction.response.defer()
    angel_help= "`/angel [angel name] [awaken status]` - Retrieves info for the angel at the given awaken status, including skills, relic, destiny, and more.\n*examples:* `/angel himiko 135` or `/angel freyja 1/3/5` or `/angel chang'e 531`\n***Note:*** *The order of awaken stars does not matter and slashes are optional.*\n"
    eudo_help = "`/eudemon [eudemon name] [level]` - Retrieves info for a eudemon at a given level.\n*example:* `/eudemon yvette 150`\n"
    boss_help = "`/dungeon [level]`, `/nightmare [level]`, `/void [level]`, `/skytower [level]` - Retrieves boss info.\n*examples:* `/dungeon 48-100` or `/void 80-2`\n"
    rel_help  = "`/releases` - Displays the release order of UR+ vs MR angels thus far."
    calc_help = "`/pulls [rarity] [shards]` - Calculates the __maximum__ number of pulls needed on Limited Summon to obtain the quantity of shards.\n*example:* `/pulls mr 64`"
    shards_help = "`/shards` - Displays a table of the shards needed for each star of each rarity."
    about = "This bot was created by user `nillabutt`. If there are any issues or suggestions for improvement, please let him know! If you want to show appreciation for his efforts, he doesn't mind donations of Angel Coins to UID: `f5ef29083fe240f4afd1fcd67427a99e`. Angel Coins can be purchased at <https://www.mujoy.sg/recharge>.\n<:Coffee_mug:1189118647168409652>Or buy him a coffee! <https://ko-fi.com/nillabutt>."


    await interaction.followup.send(
        f"{angel_help}\n{eudo_help}\n{boss_help}\n{rel_help}\n{calc_help}\n{shards_help}\n\n{about}", ephemeral=True)




# LIST ALL NAMES AND IDS ----------------------------------------------------------------------
@client.tree.command()
@app_commands.describe(
    query = 'Name or ID of the Eudemon')
async def identify(interaction: discord.Interaction, query: str):
    """Obtain a list of Names and IDs for angels, eudemons or relics"""
    await interaction.response.defer()
    #query
    connection = sqlite3.connect('ia.db')
    cursor = connection.cursor()

    if query in ['angels', 'angel', 'hero', 'units', 'heroes', 'heros', 'unit']:
        result = cursor.execute("SELECT name, cid FROM angel").fetchall()
        result.sort()
        angel_list = []
        for i, n in result:
            angel_list.append(f"{i}: {n}")
        angel_list = " — ".join(angel_list)
        await interaction.followup.send(f"List of `Angel: ID` in alphabetical order:\n```py\n{angel_list}\n```")

    elif query in ['eudemon', 'eudemons', 'eu', 'eudo', 'pokemon']:
        result = cursor.execute("SELECT name, cid FROM eudemon").fetchall()
        result.sort()
        animal_list = []
        for i, n in result:
            animal_list.append(f"{i}: {n}")
        animal_list = " — ".join(animal_list)
        await interaction.followup.send(f"List of `Eudemon: ID` in alphabetical order:\n```py\n{animal_list}\n```")

    elif query in ['relic']:
        result = cursor.execute("SELECT name, id FROM relic").fetchall()
        result.sort()
        relic_list = []
        for i, n in result:
            relic_list.append(f"{i}: {n}")
        relic_list = " — ".join(relic_list)
        await interaction.followup.send(f"List of `Relic: ID` in alphabetical order:\n```py\n{relic_list}\n```")

    elif query == query:
        await interaction.followup.send(f"I don't have a list for `{query}`. Perhaps you can try a query for `angels`, `eudemons`, or `relic` instead?\nIf you think I should have what you're looking for, ping *nillabutt* and let him know!")
    # close connection
    cursor.close()
    connection.close() 


# RUN BOT
TOKEN = os.environ.get('DC_TOKEN')
client.run(TOKEN)