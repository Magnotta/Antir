ITEMMOLD_TAGS = [
    {"tagname": "we", "text": "armamento", "params":["durability","quality", "wet", "mass", "com"]},
    {"tagname": "cu", "text": "cortante", "params":["sharpness"]},
    {"tagname": "bl", "text": "contundente", "params":["roughness"]},
    {"tagname": "pi", "text": "perfurante", "params":["pointiness"]},
    {"tagname": "ar", "text": "armadura", "params":["durability", "hardness", "wet"]},
    {"tagname": "cl", "text": "vestimenta", "params":["elegance", "cleanliness", "wet"]},
    {"tagname": "wr", "text": "escrevível", "params":["fill", "wet"]},
    {"tagname": "rd", "text": "legível", "params":["clarity"]},
    {"tagname": "fl", "text": "inflamável", "params":["wet"]},
    {"tagname": "to", "text": "ferramenta", "params":["durability", "quality", "wet"]},
    {"tagname": "mt", "text": "material", "params":["quality", "purity"]},
    {"tagname": "pa", "text": "peça", "params":["durability", "quality"]},
    {"tagname": "cp", "text": "composição", "params":["durability", "integration"]},
    {"tagname": "un", "text": "unitário", "params":["count"]},
    {"tagname": "qt", "text": "quantificável", "params":["quantity"]},
    {"tagname": "ed", "text": "comestível", "params":["aroma", "flavor", "saturation", "nutrition", "rot"]},
    {"tagname": "lu", "text": "luminoso", "params":["power"]},
    {"tagname": "co", "text": "conteiner", "params":["leakage"]},
    {"tagname": "en", "text": "energético", "params":["fill", "power"]},
    {"tagname": "dr", "text": "bebível", "params":["aroma", "flavor", "saturation"]},
    {"tagname": "re", "text": "regenerante", "params":["power", "purity"]},
    {"tagname": "tx", "text": "tóxico", "params":["power"]},
    {"tagname": "wd", "text": "molha estraga", "params":["damage"]},
    {"tagname": "sy", "text": "psicoativo", "params":["power", "purity"]},
    {"tagname": "so", "text": "sonoro", "params":["power"]},
    {"tagname": "li", "text": "vivo", "params":["health"]}
]



ITEM_PARAMS = [
    {"paramname":"durability","paramrange":1000},
    {"paramname":"quality","paramrange":4},
    {"paramname":"integration","paramrange":1000},
    {"paramname":"wet","paramrange":1000},
    {"paramname":"mass","paramrange":20},
    {"paramname":"com","paramrange":1000},
    {"paramname":"sharpness","paramrange":1000},
    {"paramname":"roughness","paramrange":1000},
    {"paramname":"pointiness","paramrange":1000},
    {"paramname":"hardness","paramrange":1000},
    {"paramname":"elegance","paramrange":5},
    {"paramname":"cleanliness","paramrange":1000},
    {"paramname":"fill","paramrange":1000},
    {"paramname":"clarity","paramrange":1000},
    {"paramname":"purity","paramrange":1000},
    {"paramname":"count","paramrange":1000000},
    {"paramname":"quantity","paramrange":10000},
    {"paramname":"aroma","paramrange":1000},
    {"paramname":"flavor","paramrange":1000},
    {"paramname":"rot","paramrange":1000},
    {"paramname":"power","paramrange":1000},
    {"paramname":"damage","paramrange":1000},
    {"paramname":"saturation","paramrange":1000},
    {"paramname":"nutrition","paramrange":1000},
    {"paramname":"leakage","paramrange":1000}
]



EVENTS = {}



SLOT_RULES = {
    "earring": 6,
    "hat": 1,
    "headband": 1,
    "around": 1,
    "necklace": 5,
    "front": 1,
    "back": 1,
    "bag": 2,
    "armband": 2,
    "bracelet": 6,
    "ring": 9,
    "belt": 2,
    "holster": 1,
    "anklet": 3
}



BASE_PLAYER_STATS = {
    "Joao" : {
        "height": 180,
        "weight": 75,
        "arm_strength": 500,
        "leg_strength": 500,
        "dexterity": 500,
        "vitality": 500,
        "blood": 1000,
        "blood_change": 0,
        "pneuma": 1000,
        "pneuma_change": 0,
        "stamina": 1000,
        "exhaustion_level": 0,
        "hunger": 0,
        "thirst": 0,
        "awake": 1000,
        "stress": 0
    },
    "Jose": {
        "height": 175,
        "weight": 85,
        "arm_strength": 500,
        "leg_strength": 500,
        "dexterity": 500,
        "vitality": 500,
        "blood": 1000,
        "blood_change": 0,
        "pneuma": 1000,
        "pneuma_change": 0,
        "stamina": 1000,
        "exhaustion_level": 0,
        "hunger": 0,
        "thirst": 0,
        "awake": 1000,
        "stress": 0
    },
    "Malina": {
        "height": 180,
        "weight": 75,
        "arm_strength": 500,
        "leg_strength": 500,
        "dexterity": 500,
        "vitality": 500,
        "blood": 1000,
        "blood_change": 0,
        "pneuma": 1000,
        "pneuma_change": 0,
        "stamina": 1000,
        "exhaustion_level": 0,
        "hunger": 0,
        "thirst": 0,
        "awake": 1000,
        "stress": 0
    },
    "Estranha": {
        "height": 180,
        "weight": 75,
        "arm_strength": 500,
        "leg_strength": 500,
        "dexterity": 500,
        "vitality": 500,
        "blood": 1000,
        "blood_change": 0,
        "pneuma": 1000,
        "pneuma_change": 0,
        "stamina": 1000,
        "exhaustion_level": 0,
        "hunger": 0,
        "thirst": 0,
        "awake": 1000,
        "stress": 0
    },
    "Ricardo": {
        "height": 180,
        "weight": 75,
        "arm_strength": 500,
        "leg_strength": 500,
        "dexterity": 500,
        "vitality": 500,
        "blood": 1000,
        "blood_change": 0,
        "pneuma": 1000,
        "pneuma_change": 0,
        "stamina": 1000,
        "exhaustion_level": 0,
        "hunger": 0,
        "thirst": 0,
        "awake": 1000,
        "stress": 0
    }
}



PLAYERS_SCHEMA = {
    "0": {
        "name": "Joao"
    },
    "1": {
        "name": "Jose"
    },
    "2": {
        "name": "Malina"
    },
    "3": {
        "name": "Estranha"
    },
    "4": {
        "name": "Ricardo"
    }
}
