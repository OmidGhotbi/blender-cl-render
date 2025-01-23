import bpy
import subprocess
import sys
import os

class OBJECT_OT_RenderCommandLine(bpy.types.Operator):
    """Render the current scene using Blender's command line"""
    bl_idname = "object.render_command_line"
    bl_label = "Render via Command Line"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the current blend file path
        blend_file_path = bpy.data.filepath
        if not blend_file_path:
            self.report({'ERROR'}, "Please save your .blend file before rendering.")
            return {'CANCELLED'}

        # Specify the Blender executable path manually
        blender_executable = r"C:\Program Files\Blender Foundation\Blender\blender.exe"  # Update this path

        if not os.path.exists(blender_executable):
            self.report({'ERROR'}, f"Blender executable not found at: {blender_executable}")
            return {'CANCELLED'}

        # Prepare the command line arguments
        # Example: blender -b file.blend -a
        cmd = [
            blender_executable,
            '-b', blend_file_path,  # Run in background mode
            '-a'  # Render animation. Use '-f 1' to render frame 1, etc.
        ]

        try:
            # Run the command
            subprocess.Popen(cmd)
            self.report({'INFO'}, "Render started via command line.")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to start render: {e}")
            return {'CANCELLED'}


class VIEW3D_PT_CustomNPanel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport's N Panel"""
    bl_label = "Render Tools"
    bl_idname = "VIEW3D_PT_custom_npanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Render CL Tools'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.render_command_line")


def register():
    bpy.utils.register_class(OBJECT_OT_RenderCommandLine)
    bpy.utils.register_class(VIEW3D_PT_CustomNPanel)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_RenderCommandLine)
    bpy.utils.unregister_class(VIEW3D_PT_CustomNPanel)


if __name__ == "__main__":
    register()
