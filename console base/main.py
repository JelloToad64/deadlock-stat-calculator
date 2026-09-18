import json

name = input("Enter hero name id: ")
level = int(input("How many boons does your hero have? (0-35): "))

with open("data/hero-data.json", "r") as file:
    data = json.load(file)

# global scaling variables (every hero has these)
bullet_damage = data[name]["Weapon"]["BulletDamage"] + (data[name]["LevelScaling"]["BulletDamage"] * level)
light_melee_damage = data[name]["LightMeleeDamage"] + (data[name]["LevelScaling"]["LightMeleeDamage"] * level)
heavy_melee_damage = data[name]["HeavyMeleeDamage"] + (data[name]["LevelScaling"]["HeavyMeleeDamage"] * level)
health = data[name]["MaxHealth"] + (data[name]["LevelScaling"]["MaxHealth"] * level)
spirit_power = 0 + (data[name]["LevelScaling"]["TechPower"] * level)

# misc scaling variables (can be overridden by hero-specific scaling)
bullet_resist = level * data[name].get("LevelScaling", {}).get("BulletResist", 0.0)
spirit_resist = level * data[name].get("LevelScaling", {}).get("SpiritResist", 0.0)
move_speed = data[name]["SprintSpeed"]

if name == "":
    bullet_damage = data[name]["Weapon"]["BulletDamage"] + (data[name]["LevelScaling"]["BulletDamage"] * level) + data[name].get("SpiritScaling", {}).get("BulletDamage", 0.0)
    move_speed = data[name]["SprintSpeed"] + data[name].get("SpiritScaling", {}).get("MaxMoveSpeed", 0.0) 

if name == "hero_priest":
     bullet_resist = spirit_power * data[name].get("SpiritScaling", {}).get("BulletResist", 0.0)
     spirit_resist = spirit_power * data[name].get("SpiritScaling", {}).get("TechResist", 0.0)

print("Hero Name: ", data[name]["Name"])
print("-----")
print("Bullet Damage: " + str(bullet_damage))
print("Ammo: ", data[name]["Weapon"]["ClipSize"])
print("Rounds Per Second: ", data[name]["Weapon"]["RoundsPerSecond"])
print("Reload Time: ", data[name]["Weapon"]["ReloadTime"])
print("Bullet Velocity: ", data[name]["Weapon"]["BulletSpeed"])
print("Light Melee Damage: " + str(light_melee_damage))
print("Heavy Melee Damage: " + str(heavy_melee_damage))
print("-----")
print("Health: " + str(health))
print("Health Regen: ", data[name]["BaseHealthRegen"])
print("Bullet Resist: " + str(bullet_resist))
print("Spirit Resist: " + str(spirit_resist))
print("Move Speed: ", data[name]["MaxMoveSpeed"])
print("Sprint Speed: ", data[name]["SprintSpeed"])
print("Dash Speed (Ground): ", data[name]["GroundDashSpeed"])
print("Dash Speed (Air): ", data[name]["AirDashSpeed"])
print("Stamina: ", data[name]["Stamina"])
print("Stamina Regen: ", data[name]["StaminaCooldown"])
print("-----")
print("Spirit Power: " + str(spirit_power))
