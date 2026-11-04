from .classes import ItemParamName


MOLD_TAG_DICTS = [
    {
        "tag_name": "we",
        "text": "armamento",
        "params": [
            ItemParamName.DURABILITY,
            ItemParamName.WET,
            ItemParamName.MASS,
            ItemParamName.CLEANLINESS,
            ItemParamName.BALANCE,
        ],
    },
    {
        "tag_name": "cu",
        "text": "cortante",
        "params": [
            ItemParamName.SHARPNESS,
            ItemParamName.HARDNESS,
        ],
    },
    {
        "tag_name": "bl",
        "text": "contundente",
        "params": [
            ItemParamName.ROUGHNESS,
            ItemParamName.HARDNESS,
        ],
    },
    {
        "tag_name": "pi",
        "text": "perfurante",
        "params": [
            ItemParamName.POINTINESS,
            ItemParamName.HARDNESS,
            ItemParamName.ANCHOR,
        ],
    },
    {
        "tag_name": "ar",
        "text": "armadura",
        "params": [
            ItemParamName.MASS,
            ItemParamName.WIELDINESS,
            ItemParamName.HARDNESS,
            ItemParamName.DURABILITY,
            ItemParamName.WET,
        ],
    },
    {
        "tag_name": "cl",
        "text": "vestimenta",
        "params": [
            ItemParamName.FORMALITY,
            ItemParamName.CHARM,
            ItemParamName.CLEANLINESS,
            ItemParamName.SMELL,
            ItemParamName.WET,
            ItemParamName.INSULATION,
        ],
    },
    {
        "tag_name": "eq",
        "text": "equipável",
        "params": [ItemParamName.DELAY],
    },
    {
        "tag_name": "wr",
        "text": "escrevível",
        "params": [ItemParamName.FILL, ItemParamName.WET],
    },
    {
        "tag_name": "rd",
        "text": "legível",
        "params": [ItemParamName.LEGIBILITY],
    },
    {
        "tag_name": "fl",
        "text": "inflamável",
        "params": [ItemParamName.WET],
    },
    {
        "tag_name": "to",
        "text": "ferramenta",
        "params": [
            ItemParamName.DURABILITY,
            ItemParamName.WET,
            ItemParamName.BALANCE,
        ],
    },
    {
        "tag_name": "mt",
        "text": "material",
        "params": [
            ItemParamName.QUALITY,
            ItemParamName.PURITY,
        ],
    },
    {
        "tag_name": "pa",
        "text": "peça",
        "params": [
            ItemParamName.DURABILITY,
            ItemParamName.QUALITY,
        ],
    },
    {
        "tag_name": "cp",
        "text": "composição",
        "params": [
            ItemParamName.DURABILITY,
            ItemParamName.INTEGRATION,
        ],
    },
    {
        "tag_name": "un",
        "text": "unitário",
        "params": [ItemParamName.QUANTITY],
    },
    {
        "tag_name": "qt",
        "text": "quantificável",
        "params": [ItemParamName.VOLUME],
    },
    {
        "tag_name": "ed",
        "text": "comestível",
        "params": [
            ItemParamName.AROMA,
            ItemParamName.FLAVOR,
            ItemParamName.SATURATION,
            ItemParamName.NUTRITION,
            ItemParamName.ROT,
        ],
    },
    {
        "tag_name": "lu",
        "text": "luminoso",
        "params": [ItemParamName.POWER],
    },
    {
        "tag_name": "co",
        "text": "conteiner",
        "params": [ItemParamName.RETENTION],
    },
    {
        "tag_name": "en",
        "text": "energético",
        "params": [ItemParamName.FILL, ItemParamName.POWER],
    },
    {
        "tag_name": "dr",
        "text": "bebível",
        "params": [
            ItemParamName.AROMA,
            ItemParamName.FLAVOR,
            ItemParamName.SATURATION,
        ],
    },
    {
        "tag_name": "re",
        "text": "regenerante",
        "params": [
            ItemParamName.POWER,
            ItemParamName.PURITY,
        ],
    },
    {
        "tag_name": "tx",
        "text": "tóxico",
        "params": [ItemParamName.POWER],
    },
    {
        "tag_name": "wd",
        "text": "molha estraga",
        "params": [ItemParamName.CONDITION],
    },
    {
        "tag_name": "sy",
        "text": "psicoativo",
        "params": [
            ItemParamName.POWER,
            ItemParamName.PURITY,
        ],
    },
    {
        "tag_name": "so",
        "text": "sonoro",
        "params": [ItemParamName.POWER],
    },
    {
        "tag_name": "li",
        "text": "vivo",
        "params": [ItemParamName.HEALTH],
    },
]


TAG_TO_PARAMS = {
    t["tag_name"]: t["params"] for t in MOLD_TAG_DICTS
}


TAG_NAMES = [t["tag_name"] for t in MOLD_TAG_DICTS]


ITEM_PARAM_DICTS = [
    {
        "param_name": ItemParamName.DURABILITY.value,
        "param_range": 1000,
        "param_mode": "manual",
        "default_distribution": {
            "base": 500,
            "variance": 100,
        },
    },
    {
        "param_name": ItemParamName.QUALITY.value,
        "param_range": 4,
        "param_mode": "manual",
        "default_distribution": {"base": 1, "variance": 1},
    },
    {
        "param_name": ItemParamName.WET.value,
        "param_range": 4,
        "param_mode": "manual",
        "default_distribution": {"base": 0, "variance": 1},
    },
    {
        "param_name": ItemParamName.FILL.value,
        "param_range": 1000,
        "param_mode": "manual",
        "default_distribution": {
            "base": 900,
            "variance": 50,
        },
    },
    {
        "param_name": ItemParamName.LEGIBILITY.value,
        "param_range": 5,
        "param_mode": "manual",
        "default_distribution": {"base": 2, "variance": 1},
    },
    {
        "param_name": ItemParamName.HEALTH.value,
        "param_range": 1000,
        "param_mode": "manual",
        "default_distribution": {
            "base": 1000,
            "variance": 50,
        },
    },
    {
        "param_name": ItemParamName.PURITY.value,
        "param_range": 1000,
        "param_mode": "manual",
        "default_distribution": {
            "base": 700,
            "variance": 150,
        },
    },
    {
        "param_name": ItemParamName.QUANTITY.value,
        "param_range": 1000000,
        "param_mode": "manual",
        "default_distribution": {"base": 1, "variance": 0},
    },
    {
        "param_name": ItemParamName.VOLUME.value,
        "param_range": 1000000,
        "param_mode": "manual",
        "default_distribution": {
            "base": 1000,
            "variance": 100,
        },
    },
    {
        "param_name": ItemParamName.ROT.value,
        "param_range": 1000,
        "param_mode": "manual",
        "default_distribution": {"base": 1, "variance": 50},
    },
    {
        "param_name": ItemParamName.CONDITION.value,
        "param_range": 1000,
        "param_mode": "manual",
        "default_distribution": {
            "base": 950,
            "variance": 50,
        },
    },
    {
        "param_name": ItemParamName.AROMA.value,
        "param_range": 5,
        "param_mode": "semi",
        "default_distribution": {"base": 3, "variance": 1},
    },
    {
        "param_name": ItemParamName.FLAVOR.value,
        "param_range": 6,
        "param_mode": "semi",
        "default_distribution": {"base": 3, "variance": 1},
    },
    {
        "param_name": ItemParamName.CHARM.value,
        "param_range": 5,
        "param_mode": "semi",
        "default_distribution": {"base": 2, "variance": 1},
    },
    {
        "param_name": ItemParamName.SMELL.value,
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 100,
            "variance": 100,
        },
    },
    {
        "param_name": ItemParamName.BALANCE.value,
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 300,
            "variance": 200,
        },
    },
    {
        "param_name": ItemParamName.INTEGRATION.value,
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 600,
            "variance": 150,
        },
    },
    {
        "param_name": ItemParamName.MASS.value,
        "param_range": 20000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 1000,
            "variance": 500,
        },
    },
    {
        "param_name": ItemParamName.SHARPNESS.value,
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 300,
            "variance": 100,
        },
    },
    {
        "param_name": ItemParamName.ROUGHNESS.value,
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 100,
            "variance": 50,
        },
    },
    {
        "param_name": ItemParamName.WIELDINESS.value,
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 600,
            "variance": 200,
        },
    },
    {
        "param_name": ItemParamName.POINTINESS.value,
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 500,
            "variance": 100,
        },
    },
    {
        "param_name": ItemParamName.HARDNESS.value,
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 500,
            "variance": 250,
        },
    },
    {
        "param_name": ItemParamName.CLEANLINESS.value,
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 800,
            "variance": 100,
        },
    },
    {
        "param_name": ItemParamName.POWER.value,
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 350,
            "variance": 150,
        },
    },
    {
        "param_name": ItemParamName.SATURATION.value,
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 600,
            "variance": 150,
        },
    },
    {
        "param_name": ItemParamName.NUTRITION.value,
        "param_range": 4,
        "param_mode": "auto",
        "default_distribution": {"base": 1, "variance": 0},
    },
    {
        "param_name": ItemParamName.RETENTION.value,
        "param_range": 1000,
        "param_mode": "auto",
        "default_distribution": {
            "base": 700,
            "variance": 250,
        },
    },
    {
        "param_name": ItemParamName.FORMALITY.value,
        "param_range": 5,
        "param_mode": "auto",
        "default_distribution": {"base": 2, "variance": 0},
    },
    {
        "param_name": ItemParamName.INSULATION.value,
        "param_range": 5,
        "param_mode": "auto",
        "default_distribution": {"base": 1, "variance": 0},
    },
    {
        "param_name": ItemParamName.ANCHOR.value,
        "param_range": 3,
        "param_mode": "auto",
        "default_distribution": {"base": 0, "variance": 0},
    },
    {
        "param_name": ItemParamName.DELAY.value,
        "param_range": 60,
        "param_mode": "auto",
        "default_distribution": {"base": 5, "variance": 1},
    },
]


ITEM_PARAM_MAXES = {
    p["param_name"]: p["param_range"]
    for p in ITEM_PARAM_DICTS
}


ITEM_PARAM_MODES = {
    p["param_name"]: p["param_mode"]
    for p in ITEM_PARAM_DICTS
}


ITEM_PARAM_DEFAULTS = {
    p["param_name"]: p["default_distribution"]
    for p in ITEM_PARAM_DICTS
}
