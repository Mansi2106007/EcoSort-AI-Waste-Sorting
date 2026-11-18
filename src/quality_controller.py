
MATERIAL_GROUPS = {
    "plastic": {
        "plastic-foil/bag",
        "plastic-other",
        "plastic-lid",
        "plastic-cup/pot",
        "foamed-plastic",
        "plastic-bottle"
    },

    "paper": {
        "paper-bag",
        "beverage-carton",
        "tissue",
        "paper-other",
        "paper-cup/pot"
    },

    "metal": {
        "aluminium-coated-foil",
        "metal-can",
        "metal-foil",
        "metal-lid",
        "metal-other"
    },

    "other": {
        "blister",
        "net",
        "wood",
        "textile",
        "ribbon/tape",
        "tube",
        "undefined"
    }
}


def get_material_group(class_name):

    for material, classes in MATERIAL_GROUPS.items():
        if class_name in classes:
            return material

    return "other"


def check_contamination(detections, expected_material):

    contaminants = []

    for item in detections:

        material = get_material_group(item["class"])

        if material != expected_material:

            contaminants.append({
                "class": item["class"],
                "material": material,
                "confidence": item["confidence"]
            })

    return len(contaminants) > 0, contaminants
