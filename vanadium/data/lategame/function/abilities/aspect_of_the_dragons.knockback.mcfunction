# AS and AT player

tag @s add lategame.ignore

# summon the temporary entity at the players position
summon marker ~ ~ ~ {Tags:["direction"]}

# Motion in den storage laden
execute as @e[tag=direction,limit=1] positioned 0.0 0.0 0.0 run function lategame:abilities/get_motion

# Auswählen, welche Entities knockback bekommen sollen
execute anchored eyes as @e[distance=..5,tag=!lategame.ignore] run tag @s add projectile

# Knockback auf alle nicht-Spieler anwenden
execute as @e[tag=projectile,distance=..5,type=!player] run data modify entity @s Motion set from storage lategame:knockback_motion Motion

# Knockback für Spieler
execute store result score $x player_motion.api.launch run data get storage lategame:knockback_motion Motion[0]
execute store result score $y player_motion.api.launch run data get storage lategame:knockback_motion Motion[1]
execute store result score $z player_motion.api.launch run data get storage lategame:knockback_motion Motion[2]
execute as @a[tag=projectile,distance=..5] run function player_motion:api/launch_xyz

# clean up the tag
tag @e[tag=projectile] remove projectile