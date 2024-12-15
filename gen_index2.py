from icon_lister import *
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
        "    vertical-align: top;",
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
  "Tank": [["tnk_light", "tnk_medium", "tnk_heavy"]],
  "SPG": [["tec_spg"]],
  "Rocket": [["tec_rocket"]],
  "AAV": [["aav_light", "aav_medium", "aav_heavy"]],
  "Trans": [["the_scout", "the_scout_escort"], ["the_light", "the_light_escort"], ["the_medium", "the_medium_escort"], ["the_heavy", "the_heavy_chinook"], ["the_heavy_osprey"]],
  "CAS": [["jet_1_attack", "jet_1_strikefighter", "jet_1_asf"], ["jet_2_attack", "jet_2_strikefighter", "jet_2_asf"], ["jet_4_attack", "jet_4_strikefighter", "jet_4_asf"], ["jet_6_attack", "jet_7_attack", "jet_8_attack"], ["jet_10_attack", "jet_10_strikefighter", "jet_10_asf", "jet_10_as"], ["jet_9_attack", "jet_9_strikefighter", "jet_9_asf"], ["jet_11_attack"]],
}

def vehToFactionName(veh):
    vehOrig = veh
    fac = None
    
    for i in range(2, 5):
        if veh[i] == "_":
            fac = veh[:i]
            break
    
    if veh in names_map:
        veh = names_map[veh]
        if veh[0] == "\"":
            veh = veh[1:]
        if veh[-1] == "\"":
            veh = veh[:-1]
    else:
        print("No HUD name found for: {}".format(vehOrig))
    
    if fac == None:
        print("Unknown faction: {}".format(vehOrig))
        return veh
    
    if fac in facTr:
        fac = facTr[fac]
    else:
        fac = fac.upper()
    
    return (fac, veh)

if __name__ == "__main__":
    # ########################################################################################
    # index.html
    # ########################################################################################
    file = os.path.join(os.path.curdir + "/index.html")
    print(file)

    lines = []
    lines.extend(makeHead("PR Assets Indexes"))
    lines.extend([
        "<h2>Automatically generated at {} using a script by CAS_ual_TY</h2>".format(time.asctime()),
        "<h2>Vehicles</h2>",
        "<span><a href=\"squad-to-icon_index.html\">Asset-to-Icon Index (click here)</a></span>",
        "<span><a href=\"asset-to-icon_index.html\">PR Assets-to-Icon Index (click here)</a></span>"
        "<span><a href=\"faction-asset-to-icon_index.html\">PR Faction-Assets-to-Icon Index (click here)</a></span>",
        "<h2>Kits</h2>",
        "<span><a href=\"icon-to-kit_index.html\">PR Icon-to-Kit Index (click here)</a></span>",
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
    lines.extend(makeHead("PR Icon-to-Assets Index"))
    lines.append("<a href=\"index.html\">Return to Index</a>")
    lines.extend([
        "<h3>Sorted alphabetically by asset name (ignoring faction identifier in front).</h3>",
        "<table>",
        "<hr>",
    ])
    
    for squad, list in claimingDict.items():
        lines.append("<hr>")
        lines.append("<h2>{}</h2>".format(squad))
        lines.append("<table>")
        for sub_list in list:
            lines.append("<tr>")
            for icon in sub_list:
                lines.append("<td><img src=\"./vehicles/{}\"></td>".format("mini_" + icon + ".png"))
            #lines.append("<td>")
            #lines.append("<b>{}</b>:".format(icon))
            #lines.append("<ul>")
            
            #k = "mini_" + squad + ".tga"
            #v = icons_map[k]
            #for v2 in v:
            #    if v2[-len(bf2):] != bf2 and v2[-len(prsp):] != prsp and v2[-len(sp):] != sp:
            #        fac, veh = vehToFactionName(v2)
            #        lines.append("<li>{} <b>{}</b> ({})</li>".format(fac, veh, v2))
            #lines.append("</ul>")
            #lines.append("</td>")
            lines.append("</tr>")
        lines.append("</table>")
    
    lines.extend(tail)
    with open(file, "w") as f:
        f.writelines([l + "\n" for l in lines])
        f.close()
