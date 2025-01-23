bl_info = {
    "name": "Custom Render Tools",
    "blender": (2, 80, 0),
    "category": "Render",
    "author": "Omid Ghotbi (TAO)",
    "version": (1, 0),
    "description": "Adds custom render buttons to the N Panel.",
}

import bpy
import subprocess
import os

# Option 1: External Rendering Operator
class OBJECT_OT_RenderAllFrames(bpy.types.Operator):
    """Render all frames using Blender's command line"""
    bl_idname = "object.render_all_frames"
    bl_label = "Render All Frames (External)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Ensure the .blend file is saved
        blend_file_path = bpy.data.filepath
        if not blend_file_path:
            self.report({'ERROR'}, "Please save your .blend file before rendering.")
            return {'CANCELLED'}

        # Specify the Blender executable path manually
        blender_executable = r"C:\Program Files\Blender Foundation\Blender\blender.exe"  # Windows Example
        # blender_executable = "/Applications/Blender.app/Contents/MacOS/Blender"  # macOS Example
        # blender_executable = "/usr/bin/blender"  # Linux Example

        if not os.path.exists(blender_executable):
            self.report({'ERROR'}, f"Blender executable not found at: {blender_executable}")
            return {'CANCELLED'}

        # Output directory
        output_dir = bpy.path.abspath("//renders/")
        os.makedirs(output_dir, exist_ok=True)

        # Define the output file path pattern
        bpy.context.scene.render.filepath = os.path.join(output_dir, "render_#####")

        # Prepare the command-line arguments
        cmd = [
            blender_executable,
            '-b', blend_file_path,  # Run Blender in background mode
            '-o', bpy.path.abspath(bpy.context.scene.render.filepath),  # Output path
            '-a'  # Render the animation (all frames)
        ]

        # Optional: Log file for capturing Blender's output
        log_file = os.path.join(output_dir, "render_log.txt")

        try:
            # Open the log file in write mode
            with open(log_file, "w") as log:
                # Launch the subprocess
                subprocess.Popen(cmd, stdout=log, stderr=log)
            self.report({'INFO'}, f"Rendering started. Logs at {log_file}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to start render: {e}")
            return {'CANCELLED'}

# Option 2: Internal Rendering Operator
class OBJECT_OT_InternalRenderAllFrames(bpy.types.Operator):
    """Render all frames using Blender's internal API"""
    bl_idname = "object.internal_render_all_frames"
    bl_label = "Internal Render All Frames"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Ensure the .blend file is saved
        blend_file_path = bpy.data.filepath
        if not blend_file_path:
            self.report({'ERROR'}, "Please save your .blend file before rendering.")
            return {'CANCELLED'}

        # Define the output directory
        output_dir = bpy.path.abspath("//renders/")
        os.makedirs(output_dir, exist_ok=True)

        # Set the render filepath
        bpy.context.scene.render.filepath = os.path.join(output_dir, "render_#####")

        try:
            # Start rendering the animation
            bpy.ops.render.render(animation=True)
            self.report({'INFO'}, f"Rendering started. Check the '{output_dir}' directory for outputs.")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Render failed: {e}")
            return {'CANCELLED'}

# Panel Class
class VIEW3D_PT_CustomRenderPanel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport's N Panel"""
    bl_label = "Custom Render Tools"
    bl_idname = "VIEW3D_PT_custom_render_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Render CL Tools'

    def draw(self, context):
        layout = self.layout
        layout.label(text="External Rendering:")
        layout.operator("object.render_all_frames", icon='RENDER_STILL')
        layout.separator()
        layout.label(text="Internal Rendering:")
        layout.operator("object.internal_render_all_frames", icon='RENDER_ANIMATION')

def register():
    bpy.utils.register_class(OBJECT_OT_RenderAllFrames)
    bpy.utils.register_class(OBJECT_OT_InternalRenderAllFrames)
    bpy.utils.register_class(VIEW3D_PT_CustomRenderPanel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_RenderAllFrames)
    bpy.utils.unregister_class(OBJECT_OT_InternalRenderAllFrames)
    bpy.utils.unregister_class(VIEW3D_PT_CustomRenderPanel)

if __name__ == "__main__":
    register()
