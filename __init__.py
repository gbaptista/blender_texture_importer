import sys
import importlib


bl_info = {
    'name': 'Texture Importer',
    'author': 'gbaptista',
    'version': (1, 0, 0),
    'blender': (4, 0, 0),
    'location': 'Shader Editor > Context Menu',
    'description': 'Automatically import texture files and create appropriate shader nodes from a specified directory.',  # noqa: E501 pylint: disable=C0301
    'doc_url': 'https://github.com/gbaptista/blender_texture_importer',
    'category': 'Node',
}


if 'pytest' not in sys.modules:
    if __name__.startswith('blender_texture_importer'):
        from . import boot

        importlib.reload(boot)

        register = boot.register
        unregister = boot.unregister
    else:
        import os

        init_dir = os.path.dirname(init_path)  # pylint: disable=E0602
        if init_dir not in sys.path:
            sys.path.append(init_dir)

        import boot  # pylint: disable=E0401

        importlib.reload(boot)

        boot.boot()
