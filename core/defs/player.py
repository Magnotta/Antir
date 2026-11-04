from enum import Enum


<<<<<<< HEAD
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
=======
PLAYER_ATTRIBUTE_MAX = 10_000


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


class PlayerStat(str, Enum):
    BLOOD_LOST = "blood_lost"
    PNEUMA_LOST = "pneuma_lost"
    COMPOSURE_LOST = "composure_lost"
    SWEAT = "sweat"
    ANXIETY = "anxiety"
    TIREDNESS = "tiredness"
    HUNGER = "hunger"
    THIRST = "thirst"
    SLEEPYNESS = "sleepyness"
    PEE = "pee"
    POO = "poo"
    NAUSEA = "nausea"
    PAIN = "pain"
    ITCH = "itch"
    COLD = "cold"
    HEAT = "heat"


CHARACTER_STATS = [stat.value for stat in PlayerStat]


CHARACTER_STAT_MAX_RATES = {
    PlayerStat.BLOOD_LOST: 30,
    PlayerStat.PNEUMA_LOST: 30,
    PlayerStat.COMPOSURE_LOST: 30,
    PlayerStat.SWEAT: 30,
    PlayerStat.ANXIETY: 30,
    PlayerStat.TIREDNESS: 30,
    PlayerStat.HUNGER: 30,
    PlayerStat.THIRST: 30,
    PlayerStat.SLEEPYNESS: 30,
    PlayerStat.PEE: 30,
    PlayerStat.POO: 30,
    PlayerStat.NAUSEA: 30,
    PlayerStat.PAIN: 30,
    PlayerStat.ITCH: 30,
    PlayerStat.COLD: 30,
    PlayerStat.HEAT: 30,
}

''' "stat_name": (caution, critical, lose control) '''
CHARACTER_STAT_BASE_THRESHOLDS = {
    PlayerStat.BLOOD_LOST: (1500, 3000, 5000),
    PlayerStat.PNEUMA_LOST: (1000, 3000, 6200),
    PlayerStat.COMPOSURE_LOST: (500, 1660, 3800),
    PlayerStat.SWEAT: (7000, 9000, 9500),
    PlayerStat.ANXIETY: (4000, 7000, 9000),
    PlayerStat.TIREDNESS: (2500, 5000, 7000),
    PlayerStat.HUNGER: (5000, 7500, 9500),
    PlayerStat.THIRST: (7000, 9000, 9500),
    PlayerStat.SLEEPYNESS: (1800, 5400, 7200),
    PlayerStat.PEE: (5000, 7000, 9000),
    PlayerStat.POO: (7000, 8500, 9500),
    PlayerStat.NAUSEA: (2000, 5000, 8500),
    PlayerStat.PAIN: (5000, 8500, 9500),
    PlayerStat.ITCH: (3000, 5000, 9500),
    PlayerStat.COLD: (3000, 6000, 9000),
    PlayerStat.HEAT: (6000, 8000, 9500),
>>>>>>> 0f59876 (Added foundation for task execution. Reorganized systems into classes files)
}


BASE_PLAYER_STATS = {
    "Joao": {
<<<<<<< HEAD
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
=======
        PlayerStat.BLOOD_LOST: 0,
        PlayerStat.PNEUMA_LOST: 0,
        PlayerStat.COMPOSURE_LOST: 0,
        PlayerStat.SWEAT: 0,
        PlayerStat.ANXIETY: 0,
        PlayerStat.TIREDNESS: 1600,
        PlayerStat.HUNGER: 0,
        PlayerStat.THIRST: 0,
        PlayerStat.SLEEPYNESS: 0,
        PlayerStat.PEE: 0,
        PlayerStat.POO: 0,
        PlayerStat.NAUSEA: 0,
        PlayerStat.PAIN: 0,
        PlayerStat.ITCH: 0,
        PlayerStat.COLD: 0,
        PlayerStat.HEAT: 0,
    },
    "Jose": {
        PlayerStat.BLOOD_LOST: 0,
        PlayerStat.PNEUMA_LOST: 0,
        PlayerStat.COMPOSURE_LOST: 0,
        PlayerStat.SWEAT: 0,
        PlayerStat.ANXIETY: 0,
        PlayerStat.TIREDNESS: 0,
        PlayerStat.HUNGER: 0,
        PlayerStat.THIRST: 0,
        PlayerStat.SLEEPYNESS: 0,
        PlayerStat.PEE: 0,
        PlayerStat.POO: 0,
        PlayerStat.NAUSEA: 0,
        PlayerStat.PAIN: 0,
        PlayerStat.ITCH: 0,
        PlayerStat.COLD: 0,
        PlayerStat.HEAT: 0,
    },
    "Estranha": {
        PlayerStat.BLOOD_LOST: 0,
        PlayerStat.PNEUMA_LOST: 0,
        PlayerStat.COMPOSURE_LOST: 0,
        PlayerStat.SWEAT: 0,
        PlayerStat.ANXIETY: 0,
        PlayerStat.TIREDNESS: 0,
        PlayerStat.HUNGER: 0,
        PlayerStat.THIRST: 0,
        PlayerStat.SLEEPYNESS: 0,
        PlayerStat.PEE: 0,
        PlayerStat.POO: 0,
        PlayerStat.NAUSEA: 0,
        PlayerStat.PAIN: 0,
        PlayerStat.ITCH: 0,
        PlayerStat.COLD: 0,
        PlayerStat.HEAT: 0,
    },
    "Malina": {
        PlayerStat.BLOOD_LOST: 0,
        PlayerStat.PNEUMA_LOST: 0,
        PlayerStat.COMPOSURE_LOST: 0,
        PlayerStat.SWEAT: 0,
        PlayerStat.ANXIETY: 0,
        PlayerStat.TIREDNESS: 0,
        PlayerStat.HUNGER: 0,
        PlayerStat.THIRST: 0,
        PlayerStat.SLEEPYNESS: 0,
        PlayerStat.PEE: 0,
        PlayerStat.POO: 0,
        PlayerStat.NAUSEA: 0,
        PlayerStat.PAIN: 0,
        PlayerStat.ITCH: 0,
        PlayerStat.COLD: 0,
        PlayerStat.HEAT: 0,
    },
    "Ricardo": {
        PlayerStat.BLOOD_LOST: 0,
        PlayerStat.PNEUMA_LOST: 0,
        PlayerStat.COMPOSURE_LOST: 0,
        PlayerStat.SWEAT: 0,
        PlayerStat.ANXIETY: 0,
        PlayerStat.TIREDNESS: 0,
        PlayerStat.HUNGER: 0,
        PlayerStat.THIRST: 0,
        PlayerStat.SLEEPYNESS: 0,
        PlayerStat.PEE: 0,
        PlayerStat.POO: 0,
        PlayerStat.NAUSEA: 0,
        PlayerStat.PAIN: 0,
        PlayerStat.ITCH: 0,
        PlayerStat.COLD: 0,
        PlayerStat.HEAT: 0,
>>>>>>> 0f59876 (Added foundation for task execution. Reorganized systems into classes files)
    },
}


BASE_PLAYER_ATTRIBUTES = {
    "Joao": {
<<<<<<< HEAD
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
=======
        PlayerAttribute.HEIGHT: 1767,
        PlayerAttribute.WEIGHT: 84561,
        PlayerAttribute.ARM_STRENGTH: 6971,
        PlayerAttribute.CORE_STRENGTH: 6382,
        PlayerAttribute.DEXTERITY: 3259,
        PlayerAttribute.AGILITY: 4135,
        PlayerAttribute.VITALITY: 8648,
        PlayerAttribute.COGNITIVE_FLEXIBILITY: 2181,
        PlayerAttribute.HOLISTIC_THOUGHT: 5663,
        PlayerAttribute.EMOTIONAL_REGULATION: 6450,
        PlayerAttribute.EMOTIONAL_CAMOUFLAGE: 874,
    },
    "Jose": {
        PlayerAttribute.HEIGHT: 1718,
        PlayerAttribute.WEIGHT: 62890,
        PlayerAttribute.ARM_STRENGTH: 3826,
        PlayerAttribute.CORE_STRENGTH: 4055,
        PlayerAttribute.DEXTERITY: 7287,
        PlayerAttribute.AGILITY: 4452,
        PlayerAttribute.VITALITY: 4916,
        PlayerAttribute.COGNITIVE_FLEXIBILITY: 6123,
        PlayerAttribute.HOLISTIC_THOUGHT: 6741,
        PlayerAttribute.EMOTIONAL_REGULATION: 7386,
        PlayerAttribute.EMOTIONAL_CAMOUFLAGE: 4811,
    },
    "Estranha": {
        PlayerAttribute.HEIGHT: 1618,
        PlayerAttribute.WEIGHT: 53311,
        PlayerAttribute.ARM_STRENGTH: 3264,
        PlayerAttribute.CORE_STRENGTH: 4818,
        PlayerAttribute.DEXTERITY: 6117,
        PlayerAttribute.AGILITY: 3856,
        PlayerAttribute.VITALITY: 7234,
        PlayerAttribute.COGNITIVE_FLEXIBILITY: 3569,
        PlayerAttribute.HOLISTIC_THOUGHT: 4831,
        PlayerAttribute.EMOTIONAL_REGULATION: 8315,
        PlayerAttribute.EMOTIONAL_CAMOUFLAGE: 7651,
    },
    "Malina": {
        PlayerAttribute.HEIGHT: 1593,
        PlayerAttribute.WEIGHT: 60034,
        PlayerAttribute.ARM_STRENGTH: 2074,
        PlayerAttribute.CORE_STRENGTH: 3615,
        PlayerAttribute.DEXTERITY: 7493,
        PlayerAttribute.AGILITY: 4135,
        PlayerAttribute.VITALITY: 6984,
        PlayerAttribute.COGNITIVE_FLEXIBILITY: 6437,
        PlayerAttribute.HOLISTIC_THOUGHT: 6224,
        PlayerAttribute.EMOTIONAL_REGULATION: 6945,
        PlayerAttribute.EMOTIONAL_CAMOUFLAGE: 4103,
    },
    "Ricardo": {
        PlayerAttribute.HEIGHT: 1751,
        PlayerAttribute.WEIGHT: 71211,
        PlayerAttribute.ARM_STRENGTH: 6118,
        PlayerAttribute.CORE_STRENGTH: 6025,
        PlayerAttribute.DEXTERITY: 6814,
        PlayerAttribute.AGILITY: 7350,
        PlayerAttribute.VITALITY: 6749,
        PlayerAttribute.COGNITIVE_FLEXIBILITY: 7736,
        PlayerAttribute.HOLISTIC_THOUGHT: 7682,
        PlayerAttribute.EMOTIONAL_REGULATION: 7374,
        PlayerAttribute.EMOTIONAL_CAMOUFLAGE: 1120,
>>>>>>> 0f59876 (Added foundation for task execution. Reorganized systems into classes files)
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
<<<<<<< HEAD


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
=======
>>>>>>> 0f59876 (Added foundation for task execution. Reorganized systems into classes files)
