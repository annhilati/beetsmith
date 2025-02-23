# AS marker

# this function is executed as the marker entity, positioned at 0 0 0 and still rotated as the player
# (as that wasn't changed with the function call)

# Die gewünschte Geschwindigkeit als 3-Vektor in Blöcken pro Tick
tp @s ^ ^ ^1
tp @s ~ 0.5 ~

# Geschwindigkeit als Pos an den storage übergeben
data modify storage lategame:knockback_motion Motion set from entity @s Pos

kill @s