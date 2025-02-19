# AS and AT player

tag @s add lategame.ignore

# summon the temporary entity at the players position
execute positioned 0.0 0.0 0.0 run summon marker ^ ^ ^1 {Tags:["direction"]}

# Motion in den storage laden
execute as @e[tag=direction,limit=1] run function lategame:abilities/get_motion

# Auswählen, welche Entities knockback bekommen sollen
execute anchored eyes as @e[distance=..5,tag=!lategame.ignore] run tag @s add lategame.apply_knockback

# Knockback auf alle nicht-Spieler anwenden
execute as @e[tag=lategame.apply_knockback,distance=..5,type=!player] run data modify entity @s Motion set from storage lategame:knockback_motion Motion

# Knockback für Spieler
execute store result score $x player_motion.api.launch run data get storage lategame:knockback_motion Motion[0]
execute store result score $y player_motion.api.launch run data get storage lategame:knockback_motion Motion[1]
execute store result score $z player_motion.api.launch run data get storage lategame:knockback_motion Motion[2]
execute as @a[tag=lategame.apply_knockback,distance=..5] run function player_motion:api/launch_xyz

# clean up the tag
tag @e[tag=lategame.apply_knockback] remove lategame.apply_knockback