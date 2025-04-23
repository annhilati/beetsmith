# Partikel & Sound
execute if score @s lategame.aotd_cooldown matches 0 run function lategame:abilities/aspect_of_the_dragons.particles
execute if score @s lategame.aotd_cooldown matches 0 run playsound entity.ender_dragon.ambient player @a[distance=..10] ~ ~ ~ 0.6

# Damage
execute if score @s lategame.aotd_cooldown matches 0 run tag @s add lategame.ignore
execute if score @s lategame.aotd_cooldown matches 0 at @s positioned ^ ^ ^2 as @e[distance=..2,tag=!lategame.ignore] run damage @s 35 player_attack by @p[tag=lategame.ignore]
execute if score @s lategame.aotd_cooldown matches 0 at @s positioned ^ ^ ^6 as @e[distance=..3,tag=!lategame.ignore] run damage @s 35 player_attack by @p[tag=lategame.ignore]
execute if score @s lategame.aotd_cooldown matches 0 run tag @s remove lategame.ignore

# Knockback
#execute if score @s lategame.aotd_cooldown matches 0 run function lategame:abilities/aspect_of_the_dragons.knockback

# Cooldown
advancement revoke @s only lategame:ability/aspect_of_the_dragons
scoreboard players set @s lategame.aotd_cooldown 600