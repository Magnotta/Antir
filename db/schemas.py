BODY_SCHEMA = {
    "Head": {
        "slots": ["earring", "hat", "headband"],
        "children": {
            "Spine": {
                "slots": [],
                "children": {
                    "Neck":{
                        "slots": ["around", "necklace"],
                        "children": {
                            "Torso":{
                                "slots": ["front", "back"],
                                "children": {
                                    "Right_shoulder": {
                                        "slots": ["bag"],
                                        "children": {
                                            "Right_arm": {
                                                "slots": ["armband"],
                                                "children": {
                                                    "Right_forearm": {
                                                        "slots": ["bracelet"],
                                                        "children": {
                                                            "Right_hand": {
                                                                "slots": ["ring"],
                                                                "children": {}
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "Left_shoulder": {
                                        "slots": ["bag"],
                                        "children": {
                                            "Left_arm": {
                                                "slots": ["armband"],
                                                "children": {
                                                    "Left_forearm":{
                                                        "slots": ["bracelet"],
                                                        "children": {
                                                            "Left_hand": {
                                                                "slots": ["ring"],
                                                                "children": {}
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "Hips": {
                        "slots": ["belt"],
                        "children": {
                            "Right_leg": {
                                "slots": ["holster"],
                                "children": {
                                    "Right_shank": {
                                        "slots": [],
                                        "children": {
                                            "Right_foot":{
                                                "slots": ["anklet"],
                                                "children": {}
                                            }
                                        }
                                    }
                                }
                            },
                            "Left_leg":{
                                "slots": ["holster"],
                                "children": {
                                    "Left_shank": {
                                        "slots": [],
                                        "children": {
                                            "Left_foot": {
                                                "slots": ["anklet"],
                                                "children": {}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
