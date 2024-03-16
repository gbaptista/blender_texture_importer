from .logic import map_candidates


def test_map_candidates():
    assert map_candidates(
        ['Dry_Sand/8K_AO.jpg',
         'Dry_Sand/8K_Albedo.jpg',
         'Dry_Sand/8K_Displacement.exr',
         'Dry_Sand/8K_Displacement.jpg',
         'Dry_Sand/8K_Normal.jpg',
         'Dry_Sand/8K_Roughness.jpg',
         'Dry_Sand/Sand_Desert_surface_Preview.png']
    ) == {
        'ambient_occlusion': 'Dry_Sand/8K_AO.jpg',
        'displacement': 'Dry_Sand/8K_Displacement.exr',
        'color': 'Dry_Sand/8K_Albedo.jpg',
        'normal': 'Dry_Sand/8K_Normal.jpg',
        'roughness': 'Dry_Sand/8K_Roughness.jpg'}

    assert map_candidates(
        ['Metal_Treated/Metal_Treated_sglfedgc_surface_Preview.png',
         'Metal_Treated/4K_Roughness.jpg',
         'Metal_Treated/4K_Normal.jpg',
         'Metal_Treated/4K_Metalness.jpg',
         'Metal_Treated/4K_Albedo.jpg']
    ) == {
        'color': 'Metal_Treated/4K_Albedo.jpg',
        'metalness': 'Metal_Treated/4K_Metalness.jpg',
        'normal': 'Metal_Treated/4K_Normal.jpg',
        'roughness': 'Metal_Treated/4K_Roughness.jpg'}

    assert map_candidates(
        ['Wood/wood_table_001_diff_4k.jpg',
         'Wood/wood_table_001_disp_4k.png',
         'Wood/wood_table_001_nor_gl_4k.exr',
         'Wood/wood_table_001_rough_4k.jpg']
    ) == {
        'color': 'Wood/wood_table_001_diff_4k.jpg',
        'displacement': 'Wood/wood_table_001_disp_4k.png',
        'normal': 'Wood/wood_table_001_nor_gl_4k.exr',
        'roughness': 'Wood/wood_table_001_rough_4k.jpg'}

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
