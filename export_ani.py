bl_info = {
    "name": "Export ANI format",
    "author": "Yannick Suter",
    "version": (1, 0, 0),
    "blender": (2, 77, 0),
    "location": "File > Export > Animation (.ani)",
    "description": "Exports animation data (keyframes, etc.).",
    "warning": "",
    "wiki_url": "",
    "support": 'OFFICIAL',
    "category": "Import-Export"}

import bpy, os
from bpy.props import (
        BoolProperty,
        FloatProperty,
        StringProperty,
        EnumProperty,
        )
from bpy_extras.io_utils import (
        ExportHelper,
        orientation_helper_factory,
        path_reference_mode,
        axis_conversion,
        )

#
#    Export animation
#

def export_ani(context, filepath):
    name = os.path.basename(filepath)
    realpath = os.path.realpath(os.path.expanduser(filepath))
    fp = open(realpath, 'w')    
    print('Exporting %s' % realpath)

    sce = bpy.context.scene

    fp.write("start %d\n" % int(sce.frame_start))
    fp.write("end %d\n" % int(sce.frame_end))
    fp.write("fps %d\n" % int(sce.render.fps))

    for object in bpy.data.objects:
        if object.type == 'MESH':
            fp.write("o %s\n" % object.name)
            for fcu in object.animation_data.action.fcurves:
                fp.write("fc %s %s\n" % (fcu.data_path, str(fcu.array_index)))
                for modifier in fcu.modifiers:
                    fp.write("mod %s\n" % modifier.type)
                for keyframe in fcu.keyframe_points:
                    fp.write("kf %d %f %s" % (int(keyframe.co.x), keyframe.co.y, keyframe.interpolation))
                    try:
                        fp.write(" %f %f %f %f" % (keyframe.handle_left.x, keyframe.handle_left.y, keyframe.handle_right.x, keyframe.handle_right.y))
                    except:
                        pass
                    fp.write("\n")

    print('%s successfully exported' % realpath)
    fp.close()
    return {'FINISHED'}

#
#    Export menu
#

class ExportANI(bpy.types.Operator, ExportHelper):
    bl_idname = "export_scene.ani"
    bl_label = 'Export ANI'
    bl_options = {'PRESET'}

    # From ExportHelper. Filter filenames.
    filename_ext = ".ani"
    filter_glob = StringProperty(default="*.ani", options={'HIDDEN'})
 
    # context group
    use_selection = BoolProperty(
            name="Selection Only",
            description="Export selected objects only",
            default=False)

    path_mode = path_reference_mode
    check_extension = True

    def execute(self, context):
        return export_ani(context, self.properties.filepath)

#
#    Registration
#

def menu_func_export(self, context):
    self.layout.operator(ExportANI.bl_idname, text="Animation (.ani)")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
