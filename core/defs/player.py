from enum import Enum


CHARACTER_STATS = [
    "blood_lost",
    "pneuma_lost",
    "composure_lost",
    "sweat",
    "anxiety",
    "tiredness",
    "hunger",
    "thirst",
    "sleepyness",
    "pee",
    "poo",
    "nausea",
    "pain",
    "itch",
    "cold",
    "heat",
]


CHARACTER_STAT_MAX_RATES = {
    "blood_lost": 30,
    "pneuma_lost": 30,
    "composure_lost": 30,
    "sweat": 30,
    "anxiety": 30,
    "tiredness": 30,
    "hunger": 30,
    "thirst": 30,
    "sleepyness": 30,
    "pee": 30,
    "poo": 30,
    "nausea": 30,
    "pain": 30,
    "itch": 30,
    "cold": 30,
    "heat": 30,
}


CHARACTER_STAT_BASE_THRESHOLDS = {
    ''' "stat_name": (caution, critical, lose control) '''
    "blood_lost": (1500, 3000, 5000),
    "pneuma_lost": (1000, 3000, 6200),
    "composure_lost": (500, 1660, 3800),
    "sweat": (7000, 9000, 9500),
    "anxiety": (4000, 7000, 9000),
    "tiredness": (2500, 5000, 7000),
    "hunger": (5000, 7500, 9500),
    "thirst": (7000, 9000, 9500),
    "sleepyness": (1800, 5400, 7200),
    "pee": (5000, 7000, 9000),
    "poo": (7000, 8500, 9500),
    "nausea": (2000, 5000, 8500),
    "pain": (5000, 8500, 9500),
    "itch": (3000, 5000, 9500),
    "cold": (3000, 6000, 9000),
    "heat": (6000, 8000, 9500),
}


BASE_PLAYER_STATS = {
    "Joao": {
        "blood_lost": 0,
        "pneuma_lost": 0,
        "composure_lost": 0,
        "sweat": 0,
        "anxiety": 0,
        "tiredness": 1600,
        "hunger": 0,
        "thirst": 0,
        "sleepyness": 0,
        "pee": 0,
        "poo": 0,
        "nausea": 0,
        "pain": 0,
        "itch": 0,
        "cold": 0,
        "heat": 0,
    },
    "Jose": {
        "blood_lost": 0,
        "pneuma_lost": 0,
        "composure_lost": 0,
        "sweat": 0,
        "anxiety": 0,
        "tiredness": 0,
        "hunger": 0,
        "thirst": 0,
        "sleepyness": 0,
        "pee": 0,
        "poo": 0,
        "nausea": 0,
        "pain": 0,
        "itch": 0,
        "cold": 0,
        "heat": 0,
    },
    "Estranha": {
        "blood_lost": 0,
        "pneuma_lost": 0,
        "composure_lost": 0,
        "sweat": 0,
        "anxiety": 0,
        "tiredness": 0,
        "hunger": 0,
        "thirst": 0,
        "sleepyness": 0,
        "pee": 0,
        "poo": 0,
        "nausea": 0,
        "pain": 0,
        "itch": 0,
        "cold": 0,
        "heat": 0,
    },
    "Malina": {
        "blood_lost": 0,
        "pneuma_lost": 0,
        "composure_lost": 0,
        "sweat": 0,
        "anxiety": 0,
        "tiredness": 0,
        "hunger": 0,
        "thirst": 0,
        "sleepyness": 0,
        "pee": 0,
        "poo": 0,
        "nausea": 0,
        "pain": 0,
        "itch": 0,
        "cold": 0,
        "heat": 0,
    },
    "Ricardo": {
        "blood_lost": 0,
        "pneuma_lost": 0,
        "composure_lost": 0,
        "sweat": 0,
        "anxiety": 0,
        "tiredness": 0,
        "hunger": 0,
        "thirst": 0,
        "sleepyness": 0,
        "pee": 0,
        "poo": 0,
        "nausea": 0,
        "pain": 0,
        "itch": 0,
        "cold": 0,
        "heat": 0,
    },
}


BASE_PLAYER_ATTRIBUTES = {
    "Joao": {
        "height": 1767,
        "weight": 84561,
        "arm_strength": 6971,
        "leg_strength": 6382,
        "dexterity": 3259,
        "agility": 4135,
        "vitality": 8648,
        "cognitive_flexibility": 2181,
        "holistic_thought": 5663,
        "emotional_regulation": 6450,
        "emotional_camouflage": 874,
    },
    "Jose": {
        "height": 1718,
        "weight": 62890,
        "arm_strength": 3826,
        "leg_strength": 4055,
        "dexterity": 7287,
        "agility": 4452,
        "vitality": 4916,
        "cognitive_flexibility": 6123,
        "holistic_thought": 6741,
        "emotional_regulation": 7386,
        "emotional_camouflage": 4811,
    },
    "Estranha": {
        "height": 1618,
        "weight": 53311,
        "arm_strength": 3264,
        "leg_strength": 4818,
        "dexterity": 6117,
        "agility": 3856,
        "vitality": 7234,
        "cognitive_flexibility": 3569,
        "holistic_thought": 4831,
        "emotional_regulation": 8315,
        "emotional_camouflage": 7651,
    },
    "Malina": {
        "height": 1593,
        "weight": 60034,
        "arm_strength": 2074,
        "leg_strength": 3615,
        "dexterity": 7493,
        "agility": 4135,
        "vitality": 6984,
        "cognitive_flexibility": 6437,
        "holistic_thought": 6224,
        "emotional_regulation": 6945,
        "emotional_camouflage": 4103,
    },
    "Ricardo": {
        "height": 1751,
        "weight": 71211,
        "arm_strength": 6118,
        "leg_strength": 6025,
        "dexterity": 6814,
        "agility": 7350,
        "vitality": 6749,
        "cognitive_flexibility": 7736,
        "holistic_thought": 7682,
        "emotional_regulation": 7374,
        "emotional_camouflage": 1120,
    },
}


PLAYERS_SCHEMA = {
    "0": {"name": "Joao"},
    "1": {"name": "Jose"},
    "2": {"name": "Malina"},
    "3": {"name": "Estranha"},
    "4": {"name": "Ricardo"},
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
    "pauldron": 1,
    "armband": 2,
    "bracelet": 6,
    "ring": 9,
    "glove": 1,
    "belt": 1,
    "underpants": 1,
    "holster": 1,
    "pants": 2,
    "skirt": 1,
    "armor": 1,
    "anklet": 2,
    "sock": 1,
    "shoe": 1,
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
                                        "slots": [
                                            "bag",
                                            "pauldron",
                                        ],
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
                                        "slots": [
                                            "bag",
                                            "pauldron",
                                        ],
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
                        "slots": [
                            "pants",
                            "skirt",
                            "belt",
                            "underpants",
                        ],
                        "depth": 8,
                        "children": {
                            "right_leg": {
                                "slots": ["holster"],
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
                                "slots": ["holster"],
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


def flatten_body_schema(schema, parent=None):
    parts = []
    for name, info in schema.items():
        parts.append(
            {
                "name": name,
                "depth": info["depth"],
                "parent": parent,
                "slots": info["slots"],
                "children": list(info["children"].keys()),
            }
        )
        for child in flatten_body_schema(
            info["children"], name
        ):
            parts.append(child)
    return parts


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


INJURY_TYPES = [
    "broken_bone",
    "torn_ligament",
    "dislocated_joint",
    "severed",
    "venomous_bite",
    "insect_bite",
    "poison_sting",
    "swollen_joint",
    "muscle_strain",
    "sliced",
    "pierced",
    "bludgeoned",
    "sunburn",
]


SWEAT_ABSORPTION_BY_NODE = {
    "torso": 300,
    "hips": 400,
    "right_shoulder": 50,
    "left_shoulder": 50,
    "right_foot": 100,
    "left_foot": 100,
}


class PlayerAttribute(str, Enum):
    HEIGHT = "height"
    WEIGHT = "weight"
    ARM_STRENGTH = "arm_strength"
    CORE_STRENGTH = "core_strength"
    DEXTERITY = "dexterity"
    AGILITY = "agility"
    VITALITY = "vitality"
    COGNITIVE_FLEXIBILITY = "cognitive_flexibility"
    HOLISTIC_THOUGHT = "holistic_thought"
    EMOTIONAL_REGULATION = "emotional_regulation"
    EMOTIONAL_CAMOUFLAGE = "emotional_camouflage"
