#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import time
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

pokemon_dict = {"1":"Bulbasaur","2":"Ivysaur","3":"Venusaur","4":"Charmander","5":"Charmeleon","6":"Charizard","7":"Squirtle","8":"Wartortle","9":"Blastoise","10":"Caterpie","11":"Metapod","12":"Butterfree","13":"Weedle","14":"Kakuna","15":"Beedrill","16":"Pidgey","17":"Pidgeotto","18":"Pidgeot","19":"Rattata","20":"Raticate","21":"Spearow","22":"Fearow","23":"Ekans","24":"Arbok","25":"Pikachu","26":"Raichu","27":"Sandshrew","28":"Sandslash","29":"Nidoran\u2640","30":"Nidorina","31":"Nidoqueen","32":"Nidoran\u2642","33":"Nidorino","34":"Nidoking","35":"Clefairy","36":"Clefable","37":"Vulpix","38":"Ninetales","39":"Jigglypuff","40":"Wigglytuff","41":"Zubat","42":"Golbat","43":"Oddish","44":"Gloom","45":"Vileplume","46":"Paras","47":"Parasect","48":"Venonat","49":"Venomoth","50":"Diglett","51":"Dugtrio","52":"Meowth","53":"Persian","54":"Psyduck","55":"Golduck","56":"Mankey","57":"Primeape","58":"Growlithe","59":"Arcanine","60":"Poliwag","61":"Poliwhirl","62":"Poliwrath","63":"Abra","64":"Kadabra","65":"Alakazam","66":"Machop","67":"Machoke","68":"Machamp","69":"Bellsprout","70":"Weepinbell","71":"Victreebel","72":"Tentacool","73":"Tentacruel","74":"Geodude","75":"Graveler","76":"Golem","77":"Ponyta","78":"Rapidash","79":"Slowpoke","80":"Slowbro","81":"Magnemite","82":"Magneton","83":"Farfetch'd","84":"Doduo","85":"Dodrio","86":"Seel","87":"Dewgong","88":"Grimer","89":"Muk","90":"Shellder","91":"Cloyster","92":"Gastly","93":"Haunter","94":"Gengar","95":"Onix","96":"Drowzee","97":"Hypno","98":"Krabby","99":"Kingler","100":"Voltorb","101":"Electrode","102":"Exeggcute","103":"Exeggutor","104":"Cubone","105":"Marowak","106":"Hitmonlee","107":"Hitmonchan","108":"Lickitung","109":"Koffing","110":"Weezing","111":"Rhyhorn","112":"Rhydon","113":"Chansey","114":"Tangela","115":"Kangaskhan","116":"Horsea","117":"Seadra","118":"Goldeen","119":"Seaking","120":"Staryu","121":"Starmie","122":"Mr. Mime","123":"Scyther","124":"Jynx","125":"Electabuzz","126":"Magmar","127":"Pinsir","128":"Tauros","129":"Magikarp","130":"Gyarados","131":"Lapras","132":"Ditto","133":"Eevee","134":"Vaporeon","135":"Jolteon","136":"Flareon","137":"Porygon","138":"Omanyte","139":"Omastar","140":"Kabuto","141":"Kabutops","142":"Aerodactyl","143":"Snorlax","144":"Articuno","145":"Zapdos","146":"Moltres","147":"Dratini","148":"Dragonair","149":"Dragonite","150":"Mewtwo","151":"Mew"}
fav_pokemon = ["1","2","3","4","5","6","7","8","9","12","15","23","24","25","26","31","34","37","39","49","58","63","64","65","67","77","78","93","94","95","104","106","107","111","113","115","123","125","126","128","130","131","133","137","138","140","142","143","147"]
cannon_coords = {"lat":"42.40653753463761","lon":"-71.11905097961426"}
CEEO_coords = {"lat":"42.4154547","lon":"-71.1266362"}
ellis_oval_coords = {"lat":"42.403210231279765","lon":"-71.1179780960083"}

coords = CEEO_coords

curr_pokemon = []
while(True):
    requests.get('https://pokevision.com/map/scan/'+coords['lat']+'/'+coords['lon'])
    time.sleep(5)
    r = requests.get('https://pokevision.com/map/data/'+coords['lat']+'/'+coords['lon'])
    rj = r.json()
    epoch_time = int(time.time())

    new_pokemon = rj['pokemon']
    new_pokemon_ids = []
    for pokemon in new_pokemon:
        if str(pokemon['pokemonId']) in fav_pokemon:
            new_pokemon_ids.append(str(pokemon['pokemonId']))
            if str(pokemon['pokemonId']) not in curr_pokemon:
                curr_pokemon.append(str(pokemon['pokemonId']))

                pkmn_name = pokemon_dict[str(pokemon['pokemonId'])].lower()
                pkmn_duration = str((int(pokemon['expiration_time']) - epoch_time)/60)+'_minutes_'+str((int(pokemon['expiration_time']) - epoch_time)%60)+"_seconds"
                pkmn_distance = str(haversine(float(pokemon['latitude']),float(pokemon['longitude']),float(coords['lat']),float(coords['lon'])))
                pkmn_distance +="_km_"
                if float(pokemon['latitude']) < float(coords['lat']):
                    pkmn_distance += 'South'
                else:
                    pkmn_distance += 'North'
                if float(pokemon['longitude']) < float(coords['lon']):
                    pkmn_distance += 'West'
                else:
                    pkmn_distance += 'East'

                print pkmn_name +' alive for ' + pkmn_duration
                print pkmn_distance
                r2 = requests.get('https://maker.ifttt.com/trigger/new_pokemon/with/key/cc4tiyJ1yeYS79kk8nP45V?value1='+pkmn_name+'&value2='+pkmn_distance+'&value3='+pkmn_duration)

    for pokemon_id in curr_pokemon:
        if pokemon_id not in new_pokemon_ids:
            curr_pokemon.remove(pokemon_id)

    time.sleep(30)