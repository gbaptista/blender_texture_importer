import re
import os


def map_candidates(candidates):
    patterns = {
        'color': ['_COL16_', '_COL_', '_DIFF_', '_Albedo'],
        'ambient_occlusion': ['_AO16_', '_AO_', '_AO'],
        'normal': ['_NRM16_', '_NRM_', '_NOR_', '_Normal'],
        'metalness': ['_METALNESS16_', '_METALNESS_', '_Metalness'],
        'roughness': ['_ROUGHNESS16_', '_ROUGHNESS_', '_ROUGH_', '_Roughness'],
        'bump': ['_BUMP16_', '_BUMP_'],
        'displacement': ['_DISP16_', '_DISP_', '_Displacement'],
        'gloss': ['_GLOSS16_', '_GLOSS_'],
        'reflection': ['_REFL16_', '_REFL_']
    }

    extensions = ['exr', 'tif', 'png', 'jpg', 'jpeg']

    images = {}

    for pattern, variants in patterns.items():  # pylint: disable=R1702
        for variant in variants:
            for file in candidates:
                if re.search(
                    variant,
                    os.path.basename(file),
                    re.IGNORECASE
                ):
                    if pattern in images:
                        current_ext = os.path.splitext(
                            images[pattern]
                        )[1].lstrip('.')

                        new_ext = os.path.splitext(file)[1].lstrip('.')

                        if (
                            extensions.index(new_ext)
                            < extensions.index(current_ext)
                        ):
                            images[pattern] = file
                    else:
                        images[pattern] = file
                    break

            if pattern in images:
                break

    return images
