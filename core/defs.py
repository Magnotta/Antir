MOLD_TAG_DICTS = [
    {
        "tag_name": "we",
        "text": "armamento",
        "params": [
            "durability",
            "wet",
            "mass",
            "cleanliness",
            "balance",
        ],
    },
    {
        "tag_name": "cu",
        "text": "cortante",
        "params": ["sharpness", "hardness"],
    },
    {
        "tag_name": "bl",
        "text": "contundente",
        "params": ["roughness", "hardness"],
    },
    {
        "tag_name": "pi",
        "text": "perfurante",
        "params": ["pointiness", "hardness", "anchor"],
    },
    {
        "tag_name": "ar",
        "text": "armadura",
        "params": [
            "mass",
            "wieldiness",
            "hardness",
            "durability",
            "wet",
        ],
    },
    {
        "tag_name": "cl",
        "text": "vestimenta",
        "params": [
            "formality",
            "charm",
            "cleanliness",
            "wet",
            "insulation",
        ],
    },
    {
        "tag_name": "eq",
        "text": "equipável",
        "params": ["delay"],
    },
    {
        "tag_name": "wr",
        "text": "escrevível",
        "params": ["fill", "wet"],
    },
    {
        "tag_name": "rd",
        "text": "legível",
        "params": ["legibility"],
    },
    {
        "tag_name": "fl",
        "text": "inflamável",
        "params": ["wet"],
    },
    {
        "tag_name": "to",
        "text": "ferramenta",
        "params": ["durability", "quality", "wet"],
    },
    {
        "tag_name": "mt",
        "text": "material",
        "params": ["quality", "purity"],
    },
    {
        "tag_name": "pa",
        "text": "peça",
        "params": ["durability", "quality"],
    },
    {
        "tag_name": "cp",
        "text": "composição",
        "params": ["durability", "integration"],
    },
    {
        "tag_name": "un",
        "text": "unitário",
        "params": ["count"],
    },
    {
        "tag_name": "qt",
        "text": "quantificável",
        "params": ["volume"],
    },
    {
        "tag_name": "ed",
        "text": "comestível",
        "params": [
            "aroma",
            "flavor",
            "saturation",
            "nutrition",
            "rot",
        ],
    },
    {
        "tag_name": "lu",
        "text": "luminoso",
        "params": ["power"],
    },
    {
        "tag_name": "co",
        "text": "conteiner",
        "params": ["retention"],
    },
    {
        "tag_name": "en",
        "text": "energético",
        "params": ["fill", "power"],
    },
    {
        "tag_name": "dr",
        "text": "bebível",
        "params": ["aroma", "flavor", "saturation"],
    },
    {
        "tag_name": "re",
        "text": "regenerante",
        "params": ["power", "purity"],
    },
    {
        "tag_name": "tx",
        "text": "tóxico",
        "params": ["power"],
    },
    {
        "tag_name": "wd",
        "text": "molha estraga",
        "params": ["condition"],
    },
    {
        "tag_name": "sy",
        "text": "psicoativo",
        "params": ["power", "purity"],
    },
    {
        "tag_name": "so",
        "text": "sonoro",
        "params": ["power"],
    },
    {
        "tag_name": "li",
        "text": "vivo",
        "params": ["health"],
    },
]


TAG_TO_PARAMS = {
    t["tag_name"]: t["params"] for t in MOLD_TAG_DICTS
}


TAG_NAMES = [t["tag_name"] for t in MOLD_TAG_DICTS]


ITEM_PARAMS = [
    {
        "param_name": "durability",
        "param_range": 1000,
        "param_mode": "manual",
        "default_distribution": {
            "base": 500,
            "variance": 100,
        },
    },
    {
        "param_name": "quality",
        "param_range": 4,
        "param_mode": "manual",
        "default_distribution": {"base": 1, "variance": 1},
    },
    {
        "param_name": "wet",
        "param_range": 4,
        "param_mode": "manual",
        "default_distribution": {"base": 0, "variance": 1},
    },
    {
        "param_name": "fill",
        "param_range": 1000,
        "param_mode": "manual",
        "default_distribution": {
            "base": 900,
            "variance": 50,
        },
    },
    {
        "param_name": "legibility",
        "param_range": 5,
        "param_mode": "manual",
        "default_distribution": {"base": 2, "variance": 1},
    },
    {
        "param_name": "purity",
        "param_range": 1000,
        "param_mode": "manual",
        "default_distribution": {
            "base": 700,
            "variance": 150,
        },
    },
    {
        "param_name": "count",
        "param_range": 1000000,
        "param_mode": "manual",
        "default_distribution": {"base": 1, "variance": 0},
    },
    {
        "param_name": "volume",
        "param_range": 1000000,
        "param_mode": "manual",
        "default_distribution": {
            "base": 1000,
            "variance": 100,
        },
    },
    {
        "param_name": "rot",
        "param_range": 1000,
        "param_mode": "manual",
        "default_distribution": {"base": 1, "variance": 50},
    },
    {
        "param_name": "condition",
        "param_range": 1000,
        "param_mode": "manual",
        "default_distribution": {
            "base": 950,
            "variance": 50,
        },
    },
    {
        "param_name": "aroma",
        "param_range": 5,
        "param_mode": "semi",
        "default_distribution": {"base": 3, "variance": 1},
    },
    {
        "param_name": "flavor",
        "param_range": 6,
        "param_mode": "semi",
        "default_distribution": {"base": 3, "variance": 1},
    },
    {
        "param_name": "charm",
        "param_range": 5,
        "param_mode": "semi",
        "default_distribution": {"base": 2, "variance": 1},
    },
    {
        "param_name": "balance",
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 300,
            "variance": 200,
        },
    },
    {
        "param_name": "integration",
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 600,
            "variance": 150,
        },
    },
    {
        "param_name": "mass",
        "param_range": 20000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 1000,
            "variance": 500,
        },
    },
    {
        "param_name": "sharpness",
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 300,
            "variance": 100,
        },
    },
    {
        "param_name": "roughness",
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 100,
            "variance": 50,
        },
    },
    {
        "param_name": "wieldiness",
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 600,
            "variance": 200,
        },
    },
    {
        "param_name": "pointiness",
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 500,
            "variance": 100,
        },
    },
    {
        "param_name": "hardness",
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 500,
            "variance": 250,
        },
    },
    {
        "param_name": "cleanliness",
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 800,
            "variance": 100,
        },
    },
    {
        "param_name": "power",
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 350,
            "variance": 150,
        },
    },
    {
        "param_name": "saturation",
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 600,
            "variance": 150,
        },
    },
    {
        "param_name": "nutrition",
        "param_range": 4,
        "param_mode": "auto",
        "default_distribution": {"base": 1, "variance": 0},
    },
    {
        "param_name": "retention",
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 700,
            "variance": 250,
        },
    },
    {
        "param_name": "formality",
        "param_range": 5,
        "param_mode": "auto",
        "default_distribution": {"base": 2, "variance": 0},
    },
    {
        "param_name": "insulation",
        "param_range": 5,
        "param_mode": "auto",
        "default_distribution": {"base": 1, "variance": 0},
    },
    {
        "param_name": "anchor",
        "param_range": 3,
        "param_mode": "auto",
        "default_distribution": {"base": 0, "variance": 0},
    },
    {
        "param_name": "delay",
        "param_range": 60,
        "param_mode": "auto",
        "default_distribution": {"base": 5, "variance": 1},
    },
]


ITEM_PARAM_MAXES = {
    p["param_name"]: p["param_range"] for p in ITEM_PARAMS
}


ITEM_PARAM_MODES = {
    p["param_name"]: p["param_mode"] for p in ITEM_PARAMS
}


ITEM_PARAM_DEFAULTS = {
    p["param_name"]: p["default_distribution"]
    for p in ITEM_PARAMS
}


BASE_PLAYER_STATS = {
    "Joao": {
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
        "stress": 0,
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
        "stress": 0,
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
        "stress": 0,
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
        "stress": 0,
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
        "stress": 0,
    },
}


SLOT_MAX_INDEX = {
    "earring": 6,
    "hat": 1,
    "headband": 1,
    "around": 1,
    "necklace": 4,
    "front": 1,
    "back": 1,
    "shirt": 2,
    "bag": 2,
    "armband": 2,
    "bracelet": 6,
    "ring": 9,
    "glove": 1,
    "belt": 2,
    "underpants": 1,
    "holster": 1,
    "pants": 2,
    "armor": 1,
    "anklet": 3,
    "sock": 1,
    "shoe": 1,
}


PLAYERS_SCHEMA = {
    "0": {"name": "Joao"},
    "1": {"name": "Jose"},
    "2": {"name": "Malina"},
    "3": {"name": "Estranha"},
    "4": {"name": "Ricardo"},
}

BODY_SCHEMA = {
    "head": {
        "slots": ["earring", "hat", "headband"],
        "depth": 0,
        "children": {
            "spine": {
                "slots": [],
                "depth": 1,
                "children": {
                    "neck": {
                        "slots": ["around", "necklace"],
                        "depth": 2,
                        "children": {
                            "torso": {
                                "slots": [
                                    "front",
                                    "back",
                                    "shirt",
                                    "armor",
                                ],
                                "depth": 7,
                                "children": {
                                    "right_shoulder": {
                                        "slots": ["bag"],
                                        "depth": 3,
                                        "children": {
                                            "right_arm": {
                                                "slots": [
                                                    "armband"
                                                ],
                                                "depth": 4,
                                                "children": {
                                                    "right_forearm": {
                                                        "slots": [
                                                            "bracelet"
                                                        ],
                                                        "depth": 5,
                                                        "children": {
                                                            "right_hand": {
                                                                "slots": [
                                                                    "ring",
                                                                    "glove",
                                                                ],
                                                                "depth": 6,
                                                                "children": {},
                                                            }
                                                        },
                                                    }
                                                },
                                            }
                                        },
                                    },
                                    "left_shoulder": {
                                        "slots": ["bag"],
                                        "depth": 3,
                                        "children": {
                                            "left_arm": {
                                                "slots": [
                                                    "armband"
                                                ],
                                                "depth": 4,
                                                "children": {
                                                    "left_forearm": {
                                                        "slots": [
                                                            "bracelet"
                                                        ],
                                                        "depth": 5,
                                                        "children": {
                                                            "left_hand": {
                                                                "slots": [
                                                                    "ring",
                                                                    "glove",
                                                                ],
                                                                "depth": 6,
                                                                "children": {},
                                                            }
                                                        },
                                                    }
                                                },
                                            }
                                        },
                                    },
                                },
                            }
                        },
                    },
                    "hips": {
                        "slots": ["belt", "underpants"],
                        "depth": 8,
                        "children": {
                            "right_leg": {
                                "slots": [
                                    "holster",
                                    "pants",
                                    "armor",
                                ],
                                "depth": 9,
                                "children": {
                                    "right_shank": {
                                        "slots": [],
                                        "depth": 10,
                                        "children": {
                                            "right_foot": {
                                                "slots": [
                                                    "anklet",
                                                    "sock",
                                                    "shoe",
                                                ],
                                                "depth": 11,
                                                "children": {},
                                            }
                                        },
                                    }
                                },
                            },
                            "left_leg": {
                                "slots": [
                                    "holster",
                                    "pants",
                                    "armor",
                                ],
                                "depth": 9,
                                "children": {
                                    "left_shank": {
                                        "slots": [],
                                        "depth": 10,
                                        "children": {
                                            "left_foot": {
                                                "slots": [
                                                    "anklet",
                                                    "sock",
                                                    "shoe",
                                                ],
                                                "depth": 11,
                                                "children": {},
                                            }
                                        },
                                    }
                                },
                            },
                        },
                    },
                },
            }
        },
    }
}


def enumerate_slots(node_name, node_dict, initial=0):
    results = []
    for slot in node_dict["slots"]:
        results.append(
            (node_dict["depth"], f"{node_name} {slot}")
        )
    for child in node_dict["children"]:
        results.extend(
            enumerate_slots(
                child, node_dict["children"][child]
            )
        )
    if not initial:
        return results
    final = sorted(results, key=lambda d: d[0])
    return [e[1] for e in final]


SLOTS_LIST = enumerate_slots(
    "head", BODY_SCHEMA["head"], initial=1
)
