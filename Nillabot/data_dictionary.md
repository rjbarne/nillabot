# tables are:
- angel
- destiny
- dungeon
- eudemon
- eudemon_awake
- eudemon_chat
- eudemon_talent
- eudemon_series
- eudemon_exp
- eudemon_land
- fashion
- fate
- fear_enemy
- fear_team
- fear_urplus
- mc_awake
- mc_fashion
- mr_angel
- nightmare
- nightmare_npc
- npc
- relic
- relic_awake
- relic_ex
- relic_growth
- relic_rand
- signal
- skill
- treasure_land
- ur_angel
- urp_angel
- urp_skill
- version
- void

## column names for angel:
- index
- cid
- is_sp
- review_show
- role
- job
- main
- quality
- quality_level
- potential
- str_initial
- agi_initial
- int_initial
- sta_initial
- fight_power_initial
- skill_ids
- name
- avatar_path
- bg_path
- spine_name
- spine_index
- recover

## column names for destiny:
- index
- id
- hero_cid
- signal
- need_other_hero_count
- skill_id

## column names for dungeon:
- index
- dungeon_id
- boss_monster_npc_id
- normal_monster_npc_id_list
- armor_drop_rate_when_offline_fight
- bg_path
- bg_path_shenhe
- name
- map_id
- reward

## column names for eudemon:
- index
- cid
- type
- unlock_need_goods_count
- unlock_favor
- str_initial
- agi_initial
- int_initial
- sta_initial
- race
- name
- age
- story_content
- dialog

## column names for eudemon_awake:
- index
- id
- cid
- awake_star
- consume_goods
- add_level
- str_add
- agi_add
- int_add
- sta_add

## column names for eudemon_chat:
- index
- id
- cid
- type
- dialogue

## column names for eudemon_talent:
- index
- cid
- name
- build_id
- desc
- att_type
- add_value[1]
- add_value[2]
- add_value[3]
- add_value[4]
- add_value[5]

## column names for eudemon_exp:
- level
- need_exp

## column names for eudemon_land:
- cid
- type
- land_id
- debris_type
- add_debris_count
- add_goods_count
- tab_desc
- desc

## column names for eudemon_skin:
- id
- avatar_name
- spine_name
- avatar_icon_big
- avatar_icon_small
- long_image
- avatar_quality
- animal_cid
- is_default
- unlock_cond1
- unlock_operation
- unlock_cond2
- unlock_desc
- is_show
- image_bg

## column names for treasure_land:
- place_id
- name

## column names for eudemon_series:
- index
- type
- name
- desc
- open
- halo_image
- icon_select
- icon_none
- contain_animals
- consume_goods_id
- attribute
- attribute_desc

## column names for fashion:
- index
- id
- collect_id
- is_activity_charge
- hide_in_normal_charge
- avatar_name
- spine_name
- review_spine_name
- avatar_icon_b
- avatar_icon_dynamic
- avatar_icon_review_b
- avatar_icon_small
- avatar_icon_small_review
- is_advanced
- avatar_quality
- hero_cid
- is_default
- is_new_default
- attribute
- unlock_cond1
- unlock_operation
- unlock_cond2
- ui_link
- unlock_desc
- is_show
- audio_folder_name
- audio_name
- audio_random_count
- need_show
- scene_path
- image_bg_path
- attack_hide_spine_bg

## column names for fate:
- index
- gid
- group_name
- hero_ids
- attr_type_type
- attr_type
- attr_value
- content
- hcid

## column names for fear_enemy:
- index
- id
- name
- if_use_ur_plus_skill
- npc_level
- hero_level
- reward
- refresh_index
- fight_value

## column names for fear_team:
- index
- id
- team
- super_awake_arr
- show_hero

## column names for fear_urplus:
- index
- hero_cid
- life_star_skill_arr

## column names for mc_awake:
- index
- awake_count
- quality_level
- hero_star
- quality
- hero_quality_level_need
- hero_count_need
- skill_open
- potential
- ignore_advance

## column names for mc_fashion:
- index
- cfg_id
- quality_or_skin_cid
- level
- cosume_goods
- attr_type_type
- attr_type
- attr_value

## column names for mr_angel:
- index
- cid
- quality_level
- potential
- str_initial
- agi_initial
- int_initial
- sta_initial
- active_skill_ids
- passive_skill_ids
- use_skill_add_anger
- normal_attack_add_anger
- lose_hp_percent_for_anger
- lose_hp_add_anger

## column names for nightmare:
- index
- dungeon_id
- boss_monster_npc_id_list
- normal_monster_npc_id_list
- bg_path
- name
- map_id
- reward

## column names for nightmare_npc:
- index
- npc_id
- name
- avatar_path
- spine_name
- spine_name_shenhe
- role
- job
- level
- skill_id_list
- skill_id_normal_attack
- hp
- minatk
- maxatk
- pdef
- mdef
- def
- defend_ignore_level
- hit
- dhit
- cir
- dcir
- damage_add
- damage_minus
- crit_damage_add
- drain_hp
- defend_ignore
- physc_def_ignore
- magic_def_ignore
- debuff_resist
- hp_recover
- bounce_rate
- speed

## column names for npc:
- index
- npc_id
- name
- avatar_path
- spine_name
- spine_name_shenhe
- role
- job
- level
- skill_id_list
- skill_id_normal_attack
- hp
- minatk
- maxatk
- pdef
- mdef
- def
- defend_ignore_level
- hit
- dhit
- cir
- dcir
- damage_add
- damage_minus
- crit_damage_add
- drain_hp
- defend_ignore
- physc_def_ignore
- magic_def_ignore
- debuff_resist
- hp_recover
- bounce_rate
- speed

## column names for relic:
- index
- id
- quality
- quality_level_init
- quality_level_max
- awake_level_max
- strengthen_skill_1
- strengthen_skill_awake_1
- strengthen_skill_2
- strengthen_skill_awake_2
- relic_pvp_skill
- attr_fixd_type_type
- attr_fixd_type
- attr_fixd_value
- attr_exclusive_id
- name
- icon_path
- desc

## column names for relic_awake:
- index
- id
- attr_fixd_type_type_1
- attr_fixd_type_1
- attr_fixd_value_1
- attr_fixd_type_type_2
- attr_fixd_type_2
- attr_fixd_value_2
- consume_1
- consume_2
- unlock_skill
- need_quality

## column names for relic_ex:
- index
- id
- job
- hero
- attr_type_type
- attr_type
- attr_value
- desc

## column names for relic_growth:
- index
- quality_level
- quality
- attr_random_count
- need_same_count
- need_all_count
- need_quality_level
- attr_param
- original_relic_num
- common_relic_num
- content

## column names for relic_rand:
- index
- id
- attr_type_type
- attr_type
- attr_value
- reset_weight

## column names for signal:
- level_0
- id
- signal
- index
- pre_index
- type
- level
- add_attr
- value_type
- show_type
- cost_count

## column names for skill:
- index
- sid
- type
- is_normal
- init_anger
- use_need_anger
- kill_enemy_trigger
- cause_damage_trigger
- before_fight_trigger
- action_trigger
- die_trigger
- after_action_trigger
- mp_cost
- eid
- open_level
- show_popup
- adjust_target_position
- prepare_anim
- skill_anim
- multi_target_spacing_time
- name
- icon
- info
- mr_skill_add_attr_info
- mr_skill_awake_enhance_info
- anger_skill_hero_bg
- frame_id

## column names for tower:
- layer
- reward
- reward_first
- normal_monster_npc_id_list
- max_round
- desc

## column names for tower_boss
- npc_id
- name
- avatar_path
- spine_name
- role
- quality
- star
- job
- level
- skill_id_list
- fight_value
- max_hp
- min_attack
- max_attack
- defend
- defend_ignore_level
- physc_def
- magic_def
- hit
- dehit
- crit
- decrit
- damage_add
- damage_minus
- crit_damage_add
- drain_hp
- defend_ignore
- physc_def_ignore
- magic_def_ignore
- debuff_resist
- hp_recover - is 0
- bounce_rate - is 0
- speed - is 0

## column names for ur_angel:
- index
- cid
- is_open
- quality_level
- potential
- str_initial
- agi_initial
- int_initial
- sta_initial
- skill_ids
- name
- avatar_path
- bg_path
- spine_name

## column names for urp_angel:
- index
- cid
- is_open
- quality_level
- potential
- str_initial
- agi_initial
- int_initial
- sta_initial

## column names for urp_common:
- index: star unlock
- skill_ids: array of pipe delimited skill ids
- name: wonder zone name

## column names for urp_skill:
- index
- hero_id
- exclusive_skill_id_arr

## column names for version:
- index
- 0

## column names for void:
- index
- id
- group
- difficulty
- boss_name
- kill_reward
- avatar_path
- spine_name
- image_id
- role
- quality
- star
- job
- level
- skill_id_list
- fight_value
- max_hp
- min_attack
- max_attack
- defend
- defend_ignore_level
- physc_def
- magic_def
- hit
- dehit
- crit
- decrit
- damage_add
- damage_minus
- crit_damage_add
- drain_hp
- defend_ignore
- physc_def_ignore
- magic_def_ignore
- debuff_resist
- hp_recover
- bounce_rate
- speed

## column names for attribute_enums:
- key
- attribute

## column names for mr_shards:
- cfg_ig
- unlock_count
- quality
- restore
- name
- icon
- description

## column names for urp_shards:
- cfg_ig
- unlock_count
- quality
- restore
- name
- icon
- description