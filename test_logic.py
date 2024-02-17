from .logic import map_candidates


def test_map_candidates():
    assert map_candidates(
        ['Wood/Wood_NRM16_8K.tif',
         'Wood/Wood_Sphere.png',
         'Wood/Wood_REFL_8K.jpg',
         'Wood/Wood_COL_8K.jpg',
         'Wood/Wood_GLOSS_8K.jpg',
         'Wood/Wood_NRM_8K.jpg']
    ) == {
        'color': 'Wood/Wood_COL_8K.jpg',
        'gloss': 'Wood/Wood_GLOSS_8K.jpg',
        'normal': 'Wood/Wood_NRM16_8K.tif',
        'reflection': 'Wood/Wood_REFL_8K.jpg'}

    assert map_candidates(
        ['/Planked/Planked_NRM16_8K.tif',
         '/Planked/Planked_DISP16_8K.tif',
         '/Planked/Planked_Sphere.png',
         '/Planked/Planked_NRM_8K.jpg',
         '/Planked/Planked_REFL_8K.jpg',
         '/Planked/Planked_AO_8K.jpg',
         '/Planked/Planked_DISP_8K.jpg',
         '/Planked/Planked_GLOSS_8K.jpg',
         '/Planked/Planked_COL_8K.jpg']
    ) == {
        'ambient_occlusion': '/Planked/Planked_AO_8K.jpg',
        'color': '/Planked/Planked_COL_8K.jpg',
        'displacement': '/Planked/Planked_DISP16_8K.tif',
        'gloss': '/Planked/Planked_GLOSS_8K.jpg',
        'normal': '/Planked/Planked_NRM16_8K.tif',
        'reflection': '/Planked/Planked_REFL_8K.jpg'}

    assert map_candidates(
        ['/Bricks/Bricks_COL_8K_METALNESS.png',
         '/Bricks/Bricks_BUMP_8K_METALNESS.png',
         '/Bricks/Bricks_DISP16_8K_METALNESS.png',
         '/Bricks/Bricks_AO_8K_METALNESS.png',
         '/Bricks/Bricks_NRM_8K_METALNESS.png',
         '/Bricks/Bricks_DISP_8K_METALNESS.png',
         '/Bricks/Bricks_Sphere.png',
         '/Bricks/Bricks_METALNESS_8K_METALNESS.png',
         '/Bricks/Bricks_ROUGHNESS_8K_METALNESS.png',
         '/Bricks/Bricks_IDMAP_8K_METALNESS.png']
    ) == {
        'ambient_occlusion': '/Bricks/Bricks_AO_8K_METALNESS.png',
        'bump': '/Bricks/Bricks_BUMP_8K_METALNESS.png',
        'color': '/Bricks/Bricks_COL_8K_METALNESS.png',
        'displacement': '/Bricks/Bricks_DISP16_8K_METALNESS.png',
        'metalness': '/Bricks/Bricks_METALNESS_8K_METALNESS.png',
        'normal': '/Bricks/Bricks_NRM_8K_METALNESS.png',
        'roughness': '/Bricks/Bricks_ROUGHNESS_8K_METALNESS.png'}
