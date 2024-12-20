from icon_lister import *
from collections import OrderedDict
import time

ignore_list = [
    "us_air_c47_para",
    "civilianCar2",
    "arg_jet_a1h_objective",
    "ru_ahe_ka29t",
    "ru_ahe_mi8amtsh",
    "ch_ahe_z9wa"
]

def makeHead(title):
    return [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<title>{}</title>".format(title),
        "<style>",
        "html {"
        "    font: 1rem/1.5 Arial, sans-serif;",
        "    background: lightgray;",
        "}",
        "div.outer {",
        "    text-align: center;",
        "    margin-left: auto;",
        "    margin-right: auto;",
        "}",
        "div.inner {",
        "    display: inline-block;",
        "}",
        "ul {",
        "    list-style-type: none;",
        "    padding: 0;",
        "    margin: 0;",
        "}",
        "img {",
        "    image-rendering: -moz-crisp-edges;",
        "    image-rendering: -webkit-optimize-contrast;",
        "    image-rendering: crisp-edges;",
        "    -ms-interpolation-mode: nearest-neighbor;",
        "    height: 64px;",
        "    text-align: center;",
        "}",
        "table {",
        "    display: table;",
        "    width: 100%;",
        "    text-align: left;",
        "}",
        "td {",
        "    border: 1px solid black;",
        "    vertical-align: center;",
        "    padding: 8px;",
        "    text-align: center;",
        "}",
        "span {",
        "    display: block;",
        "}",
        "</style>",
        "</head>",
        "<body>",
        "",
        "<div class=\"outer\">",
        "<div class=\"inner\">",
        "",
        "<h1>{}</h1>".format(title),
        "",
    ]

tail = [
    "",
    "</div>",
    "</div>",
    "",
    "</body>",
    "</html>",
]

facTr = {
    "civ": "Civilian",
    "gb82": "GB",
    "mil": "Militia",
    "boat": "Generic"
}

claimingDict = {
  "APC": [["apc_light", "apc_medium", "apc_heavy"], ["ifv_light", "ifv_medium", "ifv_heavy"], ["rec_light", "rec_medium", "rec_medium_scorpion", "rec_heavy"]],
  "TANK": [["tnk_light", "tnk_medium", "tnk_heavy"]],
  "SPG": [["tec_spg"]],
  "ROCKET": [["tec_rocket"]],
  "AAV": [["trk_aa"]],
  "TRANS": [["the_scout", "the_scout_escort"], ["the_light", "the_light_escort"], ["the_medium", "the_medium_escort"], ["the_heavy", "the_heavy_chinook"], ["the_heavy_osprey"]],
  "CAS": [["ahe_scout_50", "ahe_scout_hd", "ahe_scout_hf"], ["ahe_light_50", "ahe_light_hd", "ahe_light_hf"], ["ahe_medium_50", "ahe_medium_hd", "ahe_medium_hf"], ["ahe_heavy", "ahe_heavy_alt"], ["ahe_heavy_hind", "ahe_heavy_hind_alt"], ["jet_1_attack", "jet_1_strikefighter", "jet_1_asf"], ["jet_2_attack", "jet_2_strikefighter", "jet_2_asf", "jet_2_antiship"], ["jet_4_attack", "jet_4_strikefighter", "jet_4_asf"], ["jet_6_attack", "jet_7_attack", "jet_8_attack"], ["jet_10_attack", "jet_10_strikefighter", "jet_10_asf", "jet_10_as"], ["jet_9_attack", "jet_9_strikefighter", "jet_9_asf"], ["jet_11_attack"]],
  "APC + TANK": [["atm_medium", "jep_atgm"]],
  "APC + TANK + CAS": [["aav_light", "aav_medium", "aav_heavy"], ["jep_aa"]],
}

claimOverrides = {
    "ger_aav_flak38blitz": "APC + TANK + CAS"
}

def vehToName(veh):
    vehOrig = veh
    if veh in names_map:
        veh = names_map[veh]
        if veh[0] == "\"":
            veh = veh[1:]
        if veh[-1] == "\"":
            veh = veh[:-1]
    else:
        print("No HUD name found for: {}".format(vehOrig))

    return veh


VEHICLE_TYPE_UNKNOWN = 0
VEHICLE_TYPE_ARMOR = 1
VEHICLE_TYPE_AAV = VEHICLE_TYPE_UNKNOWN #82
VEHICLE_TYPE_APC = 3
VEHICLE_TYPE_IFV = 4
VEHICLE_TYPE_JET = 5
VEHICLE_TYPE_HELI = 6
VEHICLE_TYPE_HELIATTACK = 7
VEHICLE_TYPE_TRANSPORT = VEHICLE_TYPE_UNKNOWN #8
VEHICLE_TYPE_RECON = 9
VEHICLE_TYPE_STATIC = VEHICLE_TYPE_UNKNOWN #10
VEHICLE_TYPE_SOLDIER = VEHICLE_TYPE_UNKNOWN #11
VEHICLE_TYPE_ASSET = VEHICLE_TYPE_UNKNOWN #12
VEHICLE_TYPE_SHIP = VEHICLE_TYPE_UNKNOWN #13
VEHICLE_TYPE_TURBOPROP = 14
VEHICLE_TYPE_AFV = VEHICLE_TYPE_UNKNOWN #15  # open top shitboxes Armoured Fighting Vehicle
VEHICLE_TYPE_ALC = VEHICLE_TYPE_UNKNOWN #16  # Armoured Logistics Carrier
VEHICLE_TYPE_UAV = VEHICLE_TYPE_UNKNOWN #17
VEHICLE_TYPE_FREE = VEHICLE_TYPE_UNKNOWN #18  # recyclable vehicles that cost no tickets

claimingTypeDict = {
  "APC": [VEHICLE_TYPE_APC, VEHICLE_TYPE_IFV, VEHICLE_TYPE_RECON],
  "TANK": [VEHICLE_TYPE_ARMOR],
  "SPG": [],
  "ROCKET": [],
  "AAV": [],
  "TRANS": [VEHICLE_TYPE_HELI],
  "CAS": [VEHICLE_TYPE_JET, VEHICLE_TYPE_HELIATTACK, VEHICLE_TYPE_TURBOPROP],
  "APC + TANK": [],
  "APC + TANK + CAS": [],
}

vehicleTypeMap = OrderedDict(
    [
        ("cargoship_atlantic_conveyor", VEHICLE_TYPE_SHIP),
        ("_fri_type21", VEHICLE_TYPE_SHIP),
        ("_jet_a1h", VEHICLE_TYPE_TURBOPROP),
        ("_jet_bf109g6", VEHICLE_TYPE_TURBOPROP),
        ("_jet_p51d", VEHICLE_TYPE_TURBOPROP),
        ("_jet_i16", VEHICLE_TYPE_TURBOPROP),
        ("_jet_il2", VEHICLE_TYPE_TURBOPROP),
        ("_jet_il2m", VEHICLE_TYPE_TURBOPROP),
        ("_jet_la5fn", VEHICLE_TYPE_TURBOPROP),
        ("_atm_technical", VEHICLE_TYPE_APC),
        ("_apc_mtlb_30mm", VEHICLE_TYPE_APC),
        ("_apc_fuchs", VEHICLE_TYPE_AFV),
        ("_apc_mtlb", VEHICLE_TYPE_APC),
        ("_apc_boragh", VEHICLE_TYPE_AFV),
        ("_apc_m113", VEHICLE_TYPE_AFV),
        ("_apc_m3", VEHICLE_TYPE_AFV),
        ("_apc_m113_logistics", VEHICLE_TYPE_ALC),
        ("_apc_mtplb", VEHICLE_TYPE_ALC),
        ("_apc_acav", VEHICLE_TYPE_AFV),
        ("_apc_ypr50", VEHICLE_TYPE_AFV),
        ("_apc_vab", VEHICLE_TYPE_AFV),
        ("_apc_wz551a", VEHICLE_TYPE_AFV),
        ("_apc_251c", VEHICLE_TYPE_AFV),
        ("_ifv_scimitar", VEHICLE_TYPE_APC),
        ("_ifv_scorpion", VEHICLE_TYPE_APC),
        ("_ifv_coyote", VEHICLE_TYPE_APC),
        ("_jep_vn3", VEHICLE_TYPE_APC),
        ("_jep_fennek", VEHICLE_TYPE_APC),
        ("_shp_pbr", VEHICLE_TYPE_APC),
        ("_tnk_", VEHICLE_TYPE_ARMOR),
        ("_aav_", VEHICLE_TYPE_AAV),
        ("_apc_", VEHICLE_TYPE_APC),
        ("_ifv_", VEHICLE_TYPE_IFV),
        ("_atm_", VEHICLE_TYPE_IFV),
        ("_jet_", VEHICLE_TYPE_JET),
        ("_the_", VEHICLE_TYPE_HELI),
        ("_ahe_", VEHICLE_TYPE_HELIATTACK),
        ("_jep_", VEHICLE_TYPE_TRANSPORT),
        ("_jep_brdm2", VEHICLE_TYPE_TRANSPORT),
        ("_trk_", VEHICLE_TYPE_TRANSPORT),
        ("_civ_", VEHICLE_TYPE_TRANSPORT),
        ("_bik_", VEHICLE_TYPE_TRANSPORT),
        ("_shp_", VEHICLE_TYPE_TRANSPORT),
        ("boat", VEHICLE_TYPE_FREE),
        ("soldier", VEHICLE_TYPE_SOLDIER),
        ("commandpost", VEHICLE_TYPE_ASSET),
        ("rallypoint", VEHICLE_TYPE_ASSET),
        ("firebase", VEHICLE_TYPE_ASSET),
        ("bunker", VEHICLE_TYPE_ASSET),
        ("hideout", VEHICLE_TYPE_ASSET),
        ("acv", VEHICLE_TYPE_ASSET),
        ("ru_ship_andreev_lpd_atc", VEHICLE_TYPE_ASSET),
        ("deployable", VEHICLE_TYPE_STATIC),
        ("ats", VEHICLE_TYPE_STATIC),
        ("bipod", VEHICLE_TYPE_STATIC),
        ("hmg", VEHICLE_TYPE_STATIC),
        ("djigit", VEHICLE_TYPE_STATIC),
        ("stinger", VEHICLE_TYPE_STATIC),
        ("zis", VEHICLE_TYPE_STATIC),
        ("zpu", VEHICLE_TYPE_STATIC),
        ("uav", VEHICLE_TYPE_UAV), ]
)

_vehicleTypeCache = OrderedDict()

def getVehicleType(templateName):
    templateName = templateName.lower()
    try:
        return _vehicleTypeCache[templateName]
    except KeyError:
        for vtype in vehicleTypeMap:
            if templateName.find(vtype) != -1:
                _vehicleTypeCache[templateName] = vehicleTypeMap[vtype]
                return vehicleTypeMap[vtype]
        _vehicleTypeCache[templateName] = VEHICLE_TYPE_UNKNOWN
        return VEHICLE_TYPE_UNKNOWN


if __name__ == "__main__":
    # ########################################################################################
    # index.html
    # ########################################################################################
    file = os.path.join(os.path.curdir + "/index.html")
    print(file)

    lines = []
    lines.extend(makeHead("Alliance Claiming Index"))
    lines.extend([
        "<h2>Automatically generated at {} using a script by CAS_ual_TY</h2>".format(time.asctime()),
        "<h2>Vehicles</h2>",
        "<span><a href=\"squad-to-icon_index.html\">Squad-to-Icon Index (click here)</a></span>",
        "<span><a href=\"asset-to-squad_index.html\">Asset-to-Squad Index (click here)</a></span>"
        #"<span><a href=\"faction-asset-to-icon_index.html\">PR Faction-Assets-to-Icon Index (click here)</a></span>",
    ])
    lines.extend(tail)

    with open(file, "w") as f:
        f.writelines([l + "\n" for l in lines])
        f.close()

    # ########################################################################################
    # Squad -> Icon
    # ########################################################################################

    file = os.path.join(os.path.curdir + "/squad-to-icon_index.html")
    print(file)

    lines = []
    lines.extend(makeHead("Alliance Squad-to-Icon Index"))
    lines.append("<a href=\"index.html\">Return to Index</a>")
    lines.extend([
        "<h3>Claims of vehicle asset squads by vehicle icon.</h3>",
        "<table>",
        "<tbody>",
        "<tr><td>Squad Name</td><td>Claims</td></tr>"
    ])
    
    for squad, list in claimingDict.items():
        lines.append("<tr>")
        
        lines.append("<td><b>{}</b></td>".format(squad))
        
        lines.append("<td><ul>")
        for sub_list in list:
            lines.append("<li>")
            for icon in sub_list:
                lines.append("<img src=\"./vehicles/{}\">".format("mini_" + icon + ".png"))
            lines.append("</li>")
        lines.append("</ul></td>")
        
        lines.append("</tr>")

    lines.append("</tbody>")
    lines.append("</table>")
    
    lines.extend(tail)
    with open(file, "w") as f:
        f.writelines([l + "\n" for l in lines])
        f.close()

    # ########################################################################################
    # Squad -> Icon
    # ########################################################################################

    file = os.path.join(os.path.curdir + "/asset-to-squad_index.html")
    print(file)
    
    reverseMap = {}
    
    for squad, list in claimingDict.items():
        for sub_list in list:
            for icon in sub_list:
                reverseMap[icon] = squad

    lines = []
    lines.extend(makeHead("Alliance Asset-to-Squad Index"))
    lines.append("<a href=\"index.html\">Return to Index</a>")
    lines.extend([
        "<h3>Sorted alphabetically by asset name.</h3>",
        "<table>"
        "<tr><td>Vehicle Icon</td><td>Asset Name</td><td>Squad Name</td></tr>"
    ])
    
    assets = []
    assetNames = []
    
    for k, v in icons_map.items():
        v = [a for a in v if a not in ignore_list]
        if k[:len("mini_")] == "mini_" and len(v) > 0:
            for v2 in v:
                if v2[-len(bf2):] != bf2 and v2[-len(prsp):] != prsp and v2[-len(sp):] != sp:
                    icon = k[len("mini_"):-len(".tga")]
                    if not icon in reverseMap:
                        continue
                    name = vehToName(v2)
                    key = (name, icon)
                    if key not in assetNames:
                        assets.append((name, v2, icon))
                        assetNames.append(key)
    
    sortedAssets = sorted(assets, key=lambda tup: tup[0])
    
    reverseClaiming = {}
    
    for squad, list in claimingTypeDict.items():
        for l in list:
            reverseClaiming[l] = squad

    for name, veh, icon in sortedAssets:
        squad = reverseMap[icon]
        if veh in claimOverrides:
            squad = claimOverrides[veh]
        lines.append("<tr>")
        lines.append("<td><img src=\"./vehicles/{}\"></td>".format("mini_" + icon + ".png"))
        lines.append("<td><b>{}</b></td>".format(name))
        lines.append("<td><b>{}</b></td>".format(squad))
        lines.append("</tr>")
        t = getVehicleType(veh)
        if squad is not reverseClaiming.get(t, "None"):
            r = reverseClaiming.get(t, "None")
            if squad == "APC + TANK" or squad == "APC + TANK + CAS":
                if t == VEHICLE_TYPE_UNKNOWN:
                    pass
                else:
                    
                    print("{} ({}) should be removed from {} (it is type {})".format(veh, icon, r, t))
            else:
                if claimingTypeDict[squad] == []:
                    if r == "None":
                        print("{} ({}) should be in {} (custom type must be made)".format(veh, icon, squad))
                    else:
                        print("{} ({}) should be in {} (custom type must be made) and removed from {} (it is type {})".format(veh, icon, squad, r, t))
                else:
                    if r == "None":
                        print("{} ({}) should be in {} (containing types {})".format(veh, icon, squad, claimingTypeDict[squad]))
                    else:
                        print("{} ({}) should be in {} (containing types {}) and removed from {} (it is type {})".format(veh, icon, squad, claimingTypeDict[squad], r, t))
            
    
    lines.extend([
        "",
        "</table>"
    ])
    lines.extend(tail)
    
    with open(file, "w") as f:
        f.writelines([l + "\n" for l in lines])
        f.close()
