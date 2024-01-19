import sqlite3
import pandas as pd

connection = sqlite3.connect('ia.db')
cursor = connection.cursor()

# huge dictionary of {table name: csv file} i will manually select
# csv files are prepared for db insertion by translating all non-ASCII fields beforehand
csv_dict = {'void': r'E:\GitHub\IA\ia_dump\EN\FILES\outland\cfg_outland_boss.csv', 
            'skill': r'E:\GitHub\IA\ia_dump\EN\FILES\skill\cfg_skill.csv', 
            'fear_enemy': r'E:\GitHub\IA\ia_dump\EN\FILES\abysm\cfg_abysm_enemy.csv',
            'fear_urplus': r'E:\GitHub\IA\ia_dump\EN\FILES\abysm\cfg_abysm_enemy_ur_plus_skill.csv',
            'fear_team': r'E:\GitHub\IA\ia_dump\EN\FILES\abysm\cfg_abysm_team_hero.csv',
            'dungeon': r'E:\GitHub\IA\ia_dump\EN\FILES\dungeon\cfg_dungeon.csv',
            'npc': r'E:\GitHub\IA\ia_dump\EN\FILES\cfg_npc.csv',
            'nightmare': r'E:\GitHub\IA\ia_dump\EN\FILES\nightmare_dungeon\cfg_nightmare_dungeon.csv',
            'nightmare_npc': r'E:\GitHub\IA\ia_dump\EN\FILES\nightmare_dungeon\cfg_nightmare_npc.csv',
            'ur_angel': r'E:\GitHub\IA\ia_dump\EN\FILES\god_awake\cfg_god_hero.csv',
            'mr_angel': r'E:\GitHub\IA\ia_dump\EN\FILES\god_awake\cfg_mr_hero.csv',
            'urp_angel': r'E:\GitHub\IA\ia_dump\EN\FILES\god_awake\cfg_super_hero.csv',
            'urp_skill': r'E:\GitHub\IA\ia_dump\EN\FILES\god_awake\cfg_super_hero_skill.csv',
            'urp_common': r'E:\GitHub\IA\ia_dump\EN\FILES\god_awake\cfg_super_common_skill.csv',
            'angel': r'E:\GitHub\IA\ia_dump\EN\FILES\hero\cfg_hero.csv',
            'angel_story': r'E:\GitHub\IA\ia_dump\EN\FILES\palace\cfg_hero_story.csv',
            'fate': r'E:\GitHub\IA\ia_dump\EN\FILES\hero\cfg_hero_group.csv',
            'destiny': r'E:\GitHub\IA\ia_dump\EN\FILES\hero\cfg_hero_group_star.csv',
            'signal': r'E:\GitHub\IA\ia_dump\EN\FILES\hero\cfg_hero_life_star.csv',
            'fashion': r'E:\GitHub\IA\ia_dump\EN\FILES\hero\cfg_hero_skin_unlock.csv',
            'mc_fashion': r'E:\GitHub\IA\ia_dump\EN\FILES\hero\cfg_hero_skin_upgrade.csv',
            'mc_awake': r'E:\GitHub\IA\ia_dump\EN\FILES\hero\cfg_main_hero_awake.csv',
            'eudemon_series': r'E:\GitHub\IA\ia_dump\EN\FILES\outland\cfg_animal_series.csv',
            'eudemon': r'E:\GitHub\IA\ia_dump\EN\FILES\outland\cfg_outland_animal.csv',
            'eudemon_awake': r'E:\GitHub\IA\ia_dump\EN\FILES\outland\cfg_outland_animal_awake.csv',
            'eudemon_chat': r'E:\GitHub\IA\ia_dump\EN\FILES\outland\cfg_outland_animal_dialogue.csv',
            'eudemon_talent': r'E:\GitHub\IA\ia_dump\EN\FILES\outland\cfg_outland_animal_talent.csv',
            'eudemon_exp': r'E:\GitHub\IA\ia_dump\EN\FILES\outland\cfg_outland_animal_level.csv',
            'eudemon_land': r'E:\GitHub\IA\ia_dump\EN\FILES\treasure\cfg_treasure_animal.csv',
            'eudemon_skin': r'E:\GitHub\IA\ia_dump\EN\FILES\outland\cfg_outland_animal_skin_unlock.csv',
            'treasure_land': r'E:\GitHub\IA\ia_dump\EN\FILES\treasure\cfg_secret_land_place.csv',
            'treasure': r'E:\GitHub\IA\ia_dump\EN\FILES\treasure\cfg_treasure.csv',
            'goods': r'E:\GitHub\IA\ia_dump\EN\FILES\goods\cfg_goods_cost.csv',
            'goods_box': r'E:\GitHub\IA\ia_dump\EN\FILES\goods\cfg_goods_treasure_box.csv',
            'goods_select': r'E:\GitHub\IA\ia_dump\EN\FILES\goods\cfg_goods_custom_box.csv',
            'goods_func': r'E:\GitHub\IA\ia_dump\EN\FILES\goods\cfg_goods_functional.csv',
            # 'treasure_shop': f'',
            # 'treasure_find': f'',
            # 'treasure_awake': f'',
            # '': f'',
            'relic': r'E:\GitHub\IA\ia_dump\EN\FILES\relic\cfg_relic.csv',
            'relic_ex': r'E:\GitHub\IA\ia_dump\EN\FILES\relic\cfg_relic_attr_exclusive.csv',
            'relic_rand': r'E:\GitHub\IA\ia_dump\EN\FILES\relic\cfg_relic_attr_random.csv',
            'relic_awake': r'E:\GitHub\IA\ia_dump\EN\FILES\relic\cfg_relic_awake.csv',
            'relic_growth': r'E:\GitHub\IA\ia_dump\EN\FILES\relic\cfg_relic_quality_level.csv',
            'ur_shards': r'E:\GitHub\IA\ia_dump\EN\FILES\god_awake\cfg_god_debris.csv',
            'urp_shards': r'E:\GitHub\IA\ia_dump\EN\FILES\god_awake\cfg_super_debris.csv',
            'mr_shards': r'E:\GitHub\IA\ia_dump\EN\FILES\god_awake\cfg_mr_hero_debris.csv',
            'skill_buff': r'E:\GitHub\IA\ia_dump\EN\FILES\skill\cfg_skill_buff.csv',
            'tower': r'E:\GitHub\IA\ia_dump\EN\FILES\sky_tower\cfg_sky_tower_info.csv',
            'tower_boss': r'E:\GitHub\IA\ia_dump\EN\FILES\sky_tower\cfg_sky_tower_npc.csv',
            'attribute_enums': r'E:\GitHub\IA\ia_dump\attribute_enums.csv',
            'version': r'E:\GitHub\IA\ia_dump\EN\version.csv'
           }

update_list = []
for key in csv_dict:
  csv = csv_dict[key]
  df = pd.read_csv(csv)
  df.to_sql(name = key, con = connection, if_exists='replace')
  update_list.append(key)

cursor.execute("DELETE FROM ur_angel WHERE is_open = 0")

connection.commit()

cursor.close()
connection.close()
print(f"Updated the following tables: {sorted(update_list)}")