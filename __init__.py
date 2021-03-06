bl_info = {
    "name": "Blender2Nier (NieR:Automata Model Exporter)",
    "author": "Woeful_Wolf",
    "version": (0, 1, 10),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Export Blender model to Nier:Automata wmb model data",
    "category": "Import-Export"}

import traceback
import sys
import bpy
from bpy_extras.io_utils import ExportHelper,ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty

class ExportBlender2Nier(bpy.types.Operator, ExportHelper):
    '''Export a NieR:Automata WMB File'''
    bl_idname = "export.wmb_data"
    bl_label = "Export WMB File"
    bl_options = {'PRESET'}
    filename_ext = ".wmb"
    filter_glob: StringProperty(default="*.wmb", options={'HIDDEN'})

    purge_materials: bpy.props.BoolProperty(name="Purge Materials", description="This permanently removes all unused materials from the .blend file before exporting. Enable if you have invalid materials remaining in your project.", default=False)

    def execute(self, context):
        from . import wmb_exporter
        from . import util
        

        if self.purge_materials:
            wmb_exporter.purge_unused_materials()

        try:
            wmb_exporter.main(self.filepath)
            return wmb_exporter.restore_blend()
        except:
            print(traceback.format_exc())
            util.show_message('Error: An unexpected error has occurred during export. Please check the console for more info.', 'WMB Export Error', 'ERROR')
            return {'CANCELLED'}

def menu_func_export(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ExportBlender2Nier.bl_idname, text="WMB File for Nier: Automata (.wmb)")


def register():
    from .wta_wtp_exporter import wta_wtp_ui_manager
    from .dat_dtt_exporter import dat_dtt_ui_manager

    bpy.utils.register_class(ExportBlender2Nier)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    wta_wtp_ui_manager.register()
    dat_dtt_ui_manager.register()


def unregister():
    from .wta_wtp_exporter import wta_wtp_ui_manager
    from .dat_dtt_exporter import dat_dtt_ui_manager

    bpy.utils.unregister_class(ExportBlender2Nier)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    wta_wtp_ui_manager.unregister()
    dat_dtt_ui_manager.unregister()


if __name__ == '__main__':
    register()