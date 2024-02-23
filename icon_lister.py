import os
import sys

pr_repo = sys.argv[1]

minimap_icons_path = os.path.join(pr_repo, "menu/HUD/Texture/Ingame/Vehicles/Icons/Minimap")
menuIcons_path = os.path.join(pr_repo, "menu/HUD/Texture/Ingame/Vehicles/Icons/Hud/MenuIcons")

vehicles_path = "objects/vehicles/"
vehicles_subfolders = ["Air", "civilian", "Land", "Sea"]

factions = ["arg", "cf", "ch", "fr", "gb", "ger", "idf", "mec", "nl", "nva", "pl", "ru", "us", "civ", "fsa", "gb82", "mil"]

prefix1 = "ObjectTemplate.vehicleHud.miniMapIcon Ingame\\Vehicles\\Icons\\Minimap\\"
prefix2 = "ObjectTemplate.vehicleHud.typeIcon Ingame\\Vehicles\\Icons\\Hud\\MenuIcons\\"
prefixName = "ObjectTemplate.vehicleHud.hudName "

pre1 = "mini_"
pre2 = "menuIcon_"

icons_list = []
menuIcons_list = []

for f in os.listdir(minimap_icons_path):
    if not os.path.isdir(f) and f[-len(".tga"):] == ".tga":
        icons_list.append(f.lower())

for f in os.listdir(menuIcons_path):
    if not os.path.isdir(f) and f[-len(".tga"):] == ".tga":
        menuIcons_list.append(f.lower())

icons_map = {}
names_map = {}

missing_icons = {}
missing_menuIcons = {}

inconsistent_icons = []
inconsistent_menuIcons = []
inconsistent_names = []

wrong_menuIcons = []

base_vehicles = {}
bf2_vehicles = []
prsp_vehicles = []
sp_vehicles = []

bf2 = "_bf2"
prsp = "_prsp"
sp = "_sp"

for icon in icons_list:
    icons_map[icon] = []

for f1 in vehicles_subfolders:
    cur_path = os.path.join(pr_repo, vehicles_path + f1)
    for f2 in os.listdir(cur_path):
        if f2[0:2] in factions or f2[0:3] in factions:
            vehicle = os.path.join(pr_repo, vehicles_path + f1 + "/" + f2)
            if os.path.isdir(vehicle):
                for tweak in os.listdir(vehicle):
                    #print(tweak)
                    #print("  {}".format(tweak[-len(".tweak"):]))
                    if tweak[-len(".tweak"):] == ".tweak":
                        p = os.path.join(pr_repo, vehicles_path + f1 + "/" + f2 + "/" + tweak)
                        with open(p) as f:
                            veh = tweak[:-len(".tweak")]
                            icon = None
                            menuIcon = None
                            name = None
                            consistentMini = True
                            for line in f.readlines():
                                if line.lower()[:len(prefix1)] == prefix1.lower():
                                    icon2 = line[len(prefix1):].rstrip()
                                    if icon == None:
                                        icon = icon2
                                    else:
                                        if icon[-len(".tga"):] != ".tga":
                                            print("!!!!!!! {} {}".format(veh, icon2))
                                        if icon != icon2 and veh not in inconsistent_icons:
                                            inconsistent_icons.append(veh)
                                            consistentMini = False
                                elif line.lower()[:len(prefix2)] == prefix2.lower():
                                    menuIcon2 = line[len(prefix2):].rstrip()
                                    if menuIcon == None:
                                        menuIcon = menuIcon2
                                    else:
                                        if menuIcon[-len(".tga"):] != ".tga":
                                            print("!!!!!!! {} {}".format(veh, menuIcon2))
                                        if menuIcon != menuIcon2 and veh not in inconsistent_menuIcons:
                                            inconsistent_menuIcons.append(veh)
                                elif line.lower()[:len(prefixName)] == prefixName.lower():
                                    name2 = line[len(prefixName):].rstrip()
                                    if name == None:
                                        name = name2
                                    else:
                                        if name != name2 and veh not in inconsistent_names:
                                            inconsistent_names.append(veh)
                            if icon == None:
                                print("No mini_ icon found for: {}".format(veh))
                            elif icon.lower() not in icons_list:
                                if icon not in missing_icons:
                                    missing_icons[icon] = []
                                if veh not in missing_icons[icon]:
                                    missing_icons[icon].append(veh)
                            elif veh not in icons_map[icon]:
                                icons_map[icon].append(veh)

                            if menuIcon == None:
                                print("No menuIcon_ icon found for: {}".format(veh))
                            elif menuIcon.lower() not in menuIcons_list:
                                if menuIcon not in missing_menuIcons:
                                    missing_menuIcons[menuIcon] = []
                                if veh not in missing_menuIcons[menuIcon]:
                                    missing_menuIcons[menuIcon].append(veh)

                            if icon == None and menuIcon == None:
                                pass
                            elif icon == None or menuIcon == None:
                                print("Some icon not found for {}: minimap: {} // hud: {}".format(veh, icon, menuIcon))
                            elif consistentMini and icon[len(pre1):] != menuIcon[len(pre2):]:
                                wrong_menuIcons.append((veh, icon, menuIcon, p))

                            if veh[-len(bf2):] == bf2:
                                bf2_vehicles.append((veh, icon, menuIcon))
                            elif veh[-len(prsp):] == prsp:
                                prsp_vehicles.append((veh, icon, menuIcon))
                            elif veh[-len(sp):] == sp:
                                sp_vehicles.append((veh, icon, menuIcon))
                            else:
                                base_vehicles[veh] = (veh, icon, menuIcon)
                            
                            if name is not None:
                                names_map[veh] = name

if __name__ == "__main__":

    print()
    print()

    print("Check if _bf2 vehicles use the same icons as base...")
    for veh, icon, menuIcon in bf2_vehicles:
        veh2 = veh[:-len(bf2)]
        if veh2 in base_vehicles:
            _, icon2, menuIcon2 = base_vehicles[veh2]
            if icon != icon2:
                print("    Different mini_ icons for {} and {}: {} != {}".format(veh2, veh, icon2, icon))
            if menuIcon != menuIcon2:
                print("    Different mini_ icons for {} and {}: {} != {}".format(veh2, veh, menuIcon2, menuIcon))
        else:
            print("    Base {} not found for {}!".format(veh2, veh))
    print("Done!")

    print()
    print()

    print("Check if _prsp vehicles use the same icons as base...")
    for veh, icon, menuIcon in prsp_vehicles:
        veh2 = veh[:-len(prsp)]
        if veh2 in base_vehicles:
            _, icon2, menuIcon2 = base_vehicles[veh2]
            if icon != icon2:
                print("    Different menuIcon_ icons for {} and {}: {} != {}".format(veh2, veh, icon2, icon))
            if menuIcon != menuIcon2:
                print("    Different menuIcon_ icons for {} and {}: {} != {}".format(veh2, veh, menuIcon2, menuIcon))
        else:
            print("    Base {} not found for {}!".format(veh2, veh))
    print("Done!")

    print()
    print()

    print("Check if _sp vehicles use the same icons as base...")
    for veh, icon, menuIcon in sp_vehicles:
        veh2 = veh[:-len(sp)]
        if veh2 in base_vehicles:
            _, icon2, menuIcon2 = base_vehicles[veh2]
            if icon != icon2:
                print("    Different menuIcon_ icons for {} and {}: {} != {}".format(veh2, veh, icon2, icon))
            if menuIcon != menuIcon2:
                print("    Different menuIcon_ icons for {} and {}: {} != {}".format(veh2, veh, menuIcon2, menuIcon))
        else:
            print("    Base {} not found for {}!".format(veh2, veh))
    print("Done!")

    print()
    print()

    print("Unknown mini_ icons (total: {}):".format(len(missing_icons)))
    for k, v in missing_icons.items():
        print(k)
        for v2 in v:
            print("    {}".format(v2))

    print()
    print()

    print("Unknown menuIcon_ icons (total: {}):".format(len(missing_menuIcons)))
    for k, v in missing_menuIcons.items():
        print(k)
        for v2 in v:
            print("    {}".format(v2))

    print()
    print()

    print("Inconsistent mini_ icons (total: {}):".format(len(inconsistent_icons)))
    for v in inconsistent_icons:
        print("    {}".format(v))

    print()
    print()

    print("Inconsistent menuIcon_ icons (total: {}):".format(len(inconsistent_menuIcons)))
    for v in inconsistent_menuIcons:
        print("    {}".format(v))

    print()
    print()

    print("Vehicles with different mini_ and menuIcon_ icons (total: {}):".format(len(wrong_menuIcons)))
    for veh, icon, menuIcon, path in wrong_menuIcons:
        print("    {}: {} != {}".format(veh, icon, menuIcon))

    #print()
    #print()

    #print("Known Icons + Vehicles:")
    #for k, v in icons_map.items():
        #if len(v) > 0:
            #print("    {}".format(k))
            #for v2 in v:
                #if v2[-len(bf2):] != bf2 and v2[-len(prsp):] != prsp and v2[-len(sp):] != sp:
                    #print("        {}".format(v2))

    print()
    print()

    print("Unused Icons:")
    for k, v in icons_map.items():
        if len(v) == 0:
            print("    {}".format(k))

