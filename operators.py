import importlib
import os

import bpy  # pylint: disable=E0401
from bpy_extras.io_utils import ImportHelper  # pylint: disable=E0401

if __name__.startswith('blender_texture_importer'):
    from . import controllers
else:
    import controllers  # pylint: disable=E0401

    importlib.reload(controllers)


class ImportTextureOperator(bpy.types.Operator, ImportHelper):
    bl_idname = 'shader.import_texture_operator'
    bl_label = 'Choose Folder'

    directory: bpy.props.StringProperty(
        name='Choose Folder', subtype='DIR_PATH')

    def invoke(self, context, _event):
        opened_blender_file_path = bpy.data.filepath

        if context.window_manager.get(
            "import_texture_operator/last_imported_directory"
        ):
            self.directory = context.window_manager.get(
                "import_texture_operator/last_imported_directory")
        elif opened_blender_file_path:
            self.directory = os.path.dirname(
                bpy.path.abspath(opened_blender_file_path))

        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}

    def execute(self, context):  # pylint: disable=R0912,R0915
        active_object = context.active_object

        if not active_object:
            self.report({'WARNING'}, 'No active object.')
            return {'CANCELLED'}

        if not active_object.type == 'MESH':
            self.report({'WARNING'}, 'Active object is not a Mesh.')
            return {'CANCELLED'}

        if not active_object.active_material:
            self.report(
                {'WARNING'}, 'Active Mesh does not have an active Material.')
            return {'CANCELLED'}

        active_material = active_object.active_material

        if not active_material.use_nodes:
            self.report({'WARNING'}, 'Active material does not use Nodes.')
            return {'CANCELLED'}

        context.window_manager[
            "import_texture_operator/last_imported_directory"] = self.directory

        images = controllers.NodesController.identify_and_map_images(
            self, self.directory)

        node_tree = active_material.node_tree

        for node in node_tree.nodes:
            node_tree.nodes.remove(node)

        nodes = {}

        nodes['principled_bsdf'] = node_tree.nodes.new(
            'ShaderNodeBsdfPrincipled')

        nodes['material_output'] = node_tree.nodes.new(
            'ShaderNodeOutputMaterial')

        controllers.NodesController.connect(
            node_tree,
            nodes['principled_bsdf'], 'BSDF',
            nodes['material_output'], 'Surface')

        # Color
        if 'ambient_occlusion' in images:
            controllers.NodesController.add_image(
                node_tree,
                nodes, 'color',
                images['color'], 'Color',
                non_color=False)

            controllers.NodesController.add_image(
                node_tree,
                nodes, 'ambient_occlusion',
                images['ambient_occlusion'], 'Ambient Occlusion')

            nodes['node_mix'] = node_tree.nodes.new('ShaderNodeMix')

            nodes['node_mix'].data_type = 'RGBA'
            nodes['node_mix'].blend_type = 'MULTIPLY'

            nodes['node_mix'].label = 'Multiply (Ambient Occlusion)'

            controllers.NodesController.connect(
                node_tree,
                nodes['color'], 'Color',
                nodes['node_mix'], 'A')

            controllers.NodesController.connect(
                node_tree,
                nodes['ambient_occlusion'], 'Color',
                nodes['node_mix'], 'B')

            controllers.NodesController.connect(
                node_tree,
                nodes['node_mix'], 'Result',
                nodes['principled_bsdf'], 'Base Color')

        elif 'color' in images:
            controllers.NodesController.add_image(
                node_tree,
                nodes, 'color',
                images['color'], 'Color',
                non_color=False)

            controllers.NodesController.connect(
                node_tree,
                nodes['color'], 'Color',
                nodes['principled_bsdf'], 'Base Color')

        # Specular (Reflection) vs Metalness Workflow
        if 'reflection' in images:
            controllers.NodesController.add_image(
                node_tree,
                nodes, 'reflection',
                images['reflection'], 'Reflection')

            controllers.NodesController.connect(
                node_tree,
                nodes['reflection'], 'Color',
                nodes['principled_bsdf'], 'IOR')

        if 'metalness' in images:
            controllers.NodesController.add_image(
                node_tree,
                nodes, 'metalness',
                images['metalness'], 'Metalness')

            controllers.NodesController.connect(
                node_tree,
                nodes['metalness'], 'Color',
                nodes['principled_bsdf'], 'Metallic')

        # Specular (Gloss) vs Metalness (Roughness) Workflow
        if 'gloss' in images:
            controllers.NodesController.add_image(
                node_tree,
                nodes, 'gloss',
                images['gloss'], 'Gloss')

            nodes['node_invert'] = node_tree.nodes.new('ShaderNodeInvert')

            controllers.NodesController.connect(
                node_tree,
                nodes['gloss'], 'Color',
                nodes['node_invert'], 'Color')

            controllers.NodesController.connect(
                node_tree,
                nodes['node_invert'], 'Color',
                nodes['principled_bsdf'], 'Roughness')

        if 'roughness' in images:
            controllers.NodesController.add_image(
                node_tree,
                nodes, 'roughness',
                images['roughness'], 'Roughness')

            controllers.NodesController.connect(
                node_tree,
                nodes['roughness'], 'Color',
                nodes['principled_bsdf'], 'Roughness')

        # Surface Detail Height
        #
        #   Displacement Maps:
        #     Create the most realistic surface detail by altering
        #     geometry, offering the highest visual quality at the
        #     cost of significant performance impact.
        #
        #   Normal Maps:
        #     Offer more detailed, realistic surface texturing than bump maps
        #     with moderate performance cost, but don't affect actual geometry.
        #
        #   Bump Maps:
        #     Provide simple surface detail with minimal performance impact,
        #     but lack realism, especially at close range or in silhouettes.
        if 'normal' in images:
            controllers.NodesController.add_image(
                node_tree,
                nodes, 'normal',
                images['normal'], 'Normal')

            nodes['node_normal_map'] = node_tree.nodes.new(
                'ShaderNodeNormalMap')

            controllers.NodesController.connect(
                node_tree,
                nodes['normal'], 'Color',
                nodes['node_normal_map'], 'Color')

            controllers.NodesController.connect(
                node_tree,
                nodes['node_normal_map'], 'Normal',
                nodes['principled_bsdf'], 'Normal')

        if 'bump' in images:
            controllers.NodesController.add_image(
                node_tree,
                nodes, 'bump',
                images['bump'], 'Bump')

            nodes['node_displacement_bump'] = node_tree.nodes.new(
                'ShaderNodeDisplacement')

            nodes['node_displacement_bump'].label = 'Displacement (Bump)'

            controllers.NodesController.connect(
                node_tree,
                nodes['bump'], 'Color',
                nodes['node_displacement_bump'], 'Height')

            controllers.NodesController.connect(
                node_tree,
                nodes['node_displacement_bump'], 'Displacement',
                nodes['material_output'], 'Displacement')

        if 'displacement' in images:
            controllers.NodesController.add_image(
                node_tree,
                nodes, 'displacement',
                images['displacement'], 'Displacement')

            nodes['node_displacement'] = node_tree.nodes.new(
                'ShaderNodeDisplacement')

            controllers.NodesController.connect(
                node_tree,
                nodes['displacement'], 'Color',
                nodes['node_displacement'], 'Height')

            controllers.NodesController.connect(
                node_tree,
                nodes['node_displacement'], 'Displacement',
                nodes['material_output'], 'Displacement')

        nodes['tex_coord'] = node_tree.nodes.new('ShaderNodeTexCoord')

        nodes['value_scale'] = node_tree.nodes.new('ShaderNodeValue')
        nodes['value_scale'].label = 'Value (Scale)'
        nodes['value_scale'].outputs[0].default_value = 1.0

        nodes['mapping'] = node_tree.nodes.new('ShaderNodeMapping')

        controllers.NodesController.connect(
            node_tree,
            nodes['tex_coord'], 'UV',
            nodes['mapping'], 'Vector')

        controllers.NodesController.connect(
            node_tree,
            nodes['value_scale'], 'Value',
            nodes['mapping'], 'Scale')

        for node in node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                controllers.NodesController.connect(
                    node_tree,
                    nodes['mapping'], 'Vector',
                    node, 'Vector')

        return {'FINISHED'}


class OpenImportTextureOperator(bpy.types.Operator):  # pylint: disable=R0903
    bl_idname = "shader.open_import_texture_operator"
    bl_label = "Import Texture"

    def execute(self, _context):
        bpy.ops.shader.import_texture_operator('INVOKE_DEFAULT')
        return {'FINISHED'}


registrable = (ImportTextureOperator, OpenImportTextureOperator)

drawable = (OpenImportTextureOperator,)
