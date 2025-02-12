execute anchored eyes run particle witch ^ ^ ^3 0 0.1 0 0.2 30

tag @s add lategame.ignore
execute if score @s lategame.aotd_cooldown matches 0 at @s positioned ^ ^ ^1 as @e[distance=..5,tag=!lategame.ignore] run damage @s 10 dragon_breath by @p[tag=lategame.ignore] from @s
tag @s remove lategame.ignore

advancement revoke @s only lategame:abilities/aspect_of_the_dragons
scoreboard players set @s lategame.aotd_cooldown 100