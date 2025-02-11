execute as @a[gamemode=survival,tag=!itemlib:preventPlacement] if items entity @s weapon.* *[custom_data={prevent_placement:true}] run tellraw @s {"text":"You were temporarily set to adventure mode to prevent you from placing a block-based item. Take the item out of your hand to return to suvival mode!","color":"red"}
execute as @a[gamemode=survival] if items entity @s weapon.* *[custom_data={prevent_placement:true}] run tag @s add itemlib:preventPlacement

execute as @a[tag=itemlib:preventPlacement] run gamemode adventure @s

execute as @a[tag=itemlib:preventPlacement] unless items entity @s weapon.* *[custom_data={prevent_placement:true}] run gamemode survival
execute as @a[tag=itemlib:preventPlacement] unless items entity @s weapon.* *[custom_data={prevent_placement:true}] run tag @s remove itemlib:preventPlacement
