# Defense
execute store result score @s stats.max_absorption run attribute @s max_absorption get
execute store result score @s stats.armor_toughness run attribute @s armor_toughness get
execute store result score @s stats.knockback_resistence run attribute @s knockback_resistance get


# Attack
execute store result score @s stats.attack_damage run attribute @s attack_damage get
execute store result score @s stats.attack_speed run attribute @s attack_speed get
execute store result score @s stats.attack_reach run attribute @s entity_interaction_range get

# Other
execute store result score @s stats.speed run attribute @s movement_speed get
scoreboard players operation @s stats.speed *= 20 constant

execute store result score @s stats.safe_fall_distance run attribute @s safe_fall_distance get

execute store result score @s stats.gravity run attribute @s gravity get
scoreboard players operation @s stats.gravity /= 400 constant