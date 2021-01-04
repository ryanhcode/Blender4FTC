# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Blender For FTC",
    "author" : "RyanHCode",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "Object",
    "warning" : "",
    "category" : "Generic"
}

import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, FloatVectorProperty, FloatProperty

from .operators import *
from .panel import *


classes = (
    SetupOp1,
    BasicWorldOperator,
    RefreshMats,
    OT_CameraView,
    CopyCurrentMat,
    OT_Void_Panel,
    Make_Field,
    OT_StartMoveCamera,
    OT_StopMoveCamera,
    Nav_Pie,
    OT_AutoAssign,
    ListItem, 
    Mat_UI_List, 
    OT_Operator, 
    OT_AssignMaterial, 
    PT_Panel,
    PT_Scene_Management,
    PT_Make_Scene, 
    PT_Material_Config, 
    OT_Import_Custom
)


def register():
    bpy.types.Scene.performance = EnumProperty(
        items=[
            ("LOW", "Low", "Integrated/Very Old GPU"),
            ("MEDIUM", "Medium", "Decent GPU/Good integrated"),
            ("HIGH", "High", "Powerful GPU")
        ],
        name="Performance",
        description="Choose computer performance"
    )
    bpy.types.Scene.theme = EnumProperty(
        items=[
            ("DRAMATIC", "Dramatic", "High contrast- Dramatic look. Recommended for field renders."),
            ("MEDIUM", "Medium", "Middle ground. Recommend for any plain-background scenes."),
            ("NORMAL", "Normal", "Default blender. Good overall, higher contrasts better for realistic renders however."),
            ("LOW", "Dull", "Dull colors. Not recommended.")
        ],
        name="Theme",
        description="Choose a color theme"
    )
    bpy.types.Scene.voidColor = FloatVectorProperty(
        name="Void Color",
        description="Color of background/Void",
        subtype="COLOR",
        size = 4,
        min = 0.0,
        max = 1.0,
        default = (1.0,1.0,1.0,1.0)
    )
    bpy.types.Scene.lensD = BoolProperty(
        name="Lens Distortion",
        description="Lens Distortion",
        default = False
    )
    bpy.types.Scene.denoisingFac = FloatProperty(
        name="Denoising Fac",
        default=0.4,
        min=0.0,
        max=1.0,
        subtype="FACTOR"
    )
    bpy.types.Scene.contrast = FloatProperty(
        name="ContrastMod",
        default=0,
        min=-1.0,
        max=1.0,
        subtype="FACTOR"
    )
    bpy.types.Scene.brightness = FloatProperty(
        name="BrightnessMod",
        default=0,
        min=-1.0,
        max=1.0,
        subtype="FACTOR"
    )
    for cls in classes:
        bpy.utils.register_class(cls)
    
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi_mnu = km.keymap_items.new("wm.call_menu_pie", "Q", "PRESS", shift=True)
    kmi_mnu.properties.name = Nav_Pie.bl_idname

    bpy.types.Scene.mat_list = CollectionProperty(type = ListItem)
    bpy.types.Scene.mat_list_index = IntProperty(name = "Index for mat_list", default = 0)

def unregister():
    del bpy.types.Scene.brightness
    del bpy.types.Scene.contrast
    del bpy.types.Scene.performance
    del bpy.types.Scene.lensD
    del bpy.types.Scene.denoisingFac
    del bpy.types.Scene.theme
    del bpy.types.Scene.mat_list 
    del bpy.types.Scene.mat_list_index
    del bpy.types.Scene.voidColor
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()