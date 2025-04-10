# Partikel & Sound
execute if score @s lategame.aotd_cooldown matches 0 run function lategame:abilities/aspect_of_the_dragons.particles
execute if score @s lategame.aotd_cooldown matches 0 run playsound entity.ender_dragon.ambient player @a[distance=..10] ~ ~ ~ 0.6

# Damage
tag @s add lategame.ignore
execute if score @s lategame.aotd_cooldown matches 0 at @s positioned ^ ^ ^3 as @e[distance=..5,tag=!lategame.ignore] run damage @s 22 magic by @p[tag=lategame.ignore]
tag @s remove lategame.ignore

# Knockback
execute if score @s lategame.aotd_cooldown matches 0 run function lategame:abilities/aspect_of_the_dragons.knockback

# Cooldown
advancement revoke @s only lategame:ability/aspect_of_the_dragons
scoreboard players set @s lategame.aotd_cooldown 600