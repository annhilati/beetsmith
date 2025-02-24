execute if score @s lategame.healing_wand_cooldown matches 0 run effect give @s regeneration 5 0 true
execute if score @s lategame.healing_wand_cooldown matches 0 run playsound minecraft:entity.experience_orb.pickup player @a ~ ~ ~ 0.6 1
execute if score @s lategame.healing_wand_cooldown matches 0 run particle minecraft:heart ~ ~1 ~ .6 .6 .6 1 10

advancement revoke @s only lategame:abilities/healing_wand
scoreboard players set @s lategame.healing_wand_cooldown 200