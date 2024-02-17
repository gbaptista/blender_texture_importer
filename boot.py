import importlib
import bpy  # pylint: disable=E0401


if __name__.startswith('blender_texture_importer'):
    from . import operators
else:
    import operators  # pylint: disable=E0401


def draw_menu(self, _context):
    self.layout.separator()

    for operator in operators.drawable:
        self.layout.operator(operator.bl_idname)


def register():
    importlib.reload(operators)

    for operator in operators.registrable:
        bpy.utils.register_class(operator)

    bpy.types.Scene.registered = True

    if not hasattr(bpy.types.Scene, 'appended'):
        bpy.types.NODE_MT_context_menu.append(draw_menu)
        bpy.types.Scene.appended = True


def unregister():
    del bpy.types.Scene.registered

    for operator in operators.registrable:
        bpy.utils.unregister_class(operator)


def boot():
    if hasattr(bpy.types.Scene, 'registered'):
        unregister()

    register()
