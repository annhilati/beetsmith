execute as @a[scores={lategame.aotd_cooldown=1..}] run scoreboard players remove @s lategame.aotd_cooldown 1
execute as @a[scores={lategame.healing_wand_cooldown=1..}] run scoreboard players remove @s lategame.healing_wand_cooldown 1

# advancement revoke @s only lategame:cooldown