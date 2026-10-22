PATH_CONDITION_KINDS_DICT = {
    "fallen_tree": ["width", "hardness"],
    "muddy": ["depth"],
    "washout": ["traceability"],
    "gully": ["depth", "width"],
    "exposed_roots": ["height", "coverage"],
    "inclination_change": ["angle"],
    "thorny_overgrowth": ["height", "pests", "poison"],
    "fibrous_overgrowth": ["height", "pests", "thickness"],
    "bushy_overgrowth": ["height", "pests", "hardness"],
    "bridge": ["height", "length", "width", "capacity"],
    "river_crossing": ["length", "depth", "water_speed"],
    "rock_slide": ["height"],
    "scenic_view": [],
    "cliff_edge": ["height"],
    "lakeside": ["lake"],
    "terrain": ["type"],
    "landmark": ["toponym"],
}


def get_path_cond_params():
    aux = []
    for param_list in PATH_CONDITION_KINDS_DICT.values():
        aux.extend(param_list)
    return set(aux)


PATH_COND_PARAMS = get_path_cond_params()


STR_PATH_COND_PARAMS = {
    "lake": [],
    "type": [
        "packed_dirt",
        "unpacked_dirt",
        "grassy",
        "wooded",
        "bouldery",
        "sandy",
        "scree",
        "snow",
        "slush",
    ],
    "toponym": [],
    "pests": ["none", "ants", "wasps", "ticks", "leeches"],
}


SEGM_COND_KINDS = [
    "terrain",
    "lakeside",
    "cliff_edge",
    "thorny_overgrowth",
    "bushy_overgrowth",
    "fibrous_overgrowth",
    "exposed_roots",
    "gully",
    "washout",
    "muddy",
]
