import importlib
import os
import glob

import bpy  # pylint: disable=E0401

if __name__.startswith('blender_texture_importer'):
    from . import logic
else:
    import logic  # pylint: disable=E0401

    importlib.reload(logic)


class NodesController:
    @staticmethod
    def add_image(
        node_tree, nodes, key, path, label, non_color=True
    ):  # pylint: disable=R0913
        nodes[key] = node_tree.nodes.new('ShaderNodeTexImage')
        nodes[key].label = f'Image Texture ({label})'
        nodes[key].hide = True

        image = bpy.data.images.load(path)

        if non_color:
            image.colorspace_settings.name = 'Non-Color'

        nodes[key].image = image

    @staticmethod
    def connect(node_tree, from_node, output_channel, to_node, input_channel):
        from_node.location = (
            to_node.location.x - to_node.dimensions.x,
            to_node.location.y)

        node_tree.links.new(
            from_node.outputs[output_channel],
            to_node.inputs[input_channel])

    @staticmethod
    def identify_and_map_images(_operator, directory):
        extension_preferences = ['tif', 'png', 'jpg', 'jpeg']

        candidates = []
        for extension in extension_preferences:
            candidates.extend(
                glob.glob(os.path.join(directory, f'*.{extension}')))

        return logic.map_candidates(candidates)
