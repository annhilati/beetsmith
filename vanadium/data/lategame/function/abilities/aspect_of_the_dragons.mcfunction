execute anchored eyes run particle witch ^ ^ ^3 0 0.1 0 0.2 30
# execute as Annhilati at @s anchored eyes run particle minecraft:flame ^1 ^ ^ ^0000000 ^0000000 ^1000000 0.0000002 0 force

tag @s add lategame.ignore
execute if score @s lategame.aotd_cooldown matches 0 at @s positioned ^ ^ ^1 as @e[distance=..5,tag=!lategame.ignore] run damage @s 22 dragon_breath by @p[tag=lategame.ignore]
tag @s remove lategame.ignore

advancement revoke @s only lategame:abilities/aspect_of_the_dragons
scoreboard players set @s lategame.aotd_cooldown 600

