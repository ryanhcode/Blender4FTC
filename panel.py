import bpy


class PT_Panel(bpy.types.Panel):
    bl_idname = "PT_Panel"
    bl_label = "MaterialLib"
    bl_category = "Blend4FTC"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        row.operator('view3d.apply_material', text="Import Default MaterialLib")
        row2 = layout.row()
        row2.operator("blend4ftc.import_custom", text="Import Custom Material Lib")

        row3 = layout.row()
        row3.operator('view3d.auto_material', text="SmartShade")

        row4 = layout.row()
        row4.template_list("Mat_UI_List", "The_List", scene, "mat_list", scene, "mat_list_index")

        row5 = layout.row()
        row5.operator("blend4ftc.assign_material", text="Assign")
        layout.row().operator("blend4ftc.refresh_mats", text="Refresh")

class PT_Scene_Management(bpy.types.Panel):
    bl_idname = "PT_Scene_Management"
    bl_label = "Scene Management"
    bl_category = "Blend4FTC"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.row().prop(scene, "performance")
        
        layout.row().prop(scene, "theme")

        layout.row().label(text="")

        layout.row().label(text="Compositing Effects")
        layout.row().prop(scene,"voidColor")
        layout.row().prop(scene, "lensD")
        layout.row().prop(scene, "denoisingFac")
        row1  = layout.row()
        row1.prop(scene, "contrast")
        row1.prop(scene, "brightness")

        
        layout.row().label(text="")
        
        row = layout.row()
        row.operator("blend4ftc.move_camera", text="Adjust Camera")
        row.operator("blend4ftc.stop_move_camera", text="Stop Adjust")
        layout.row().operator("blend4ftc.setupop1", text="Save and Apply")

class PT_Make_Scene(bpy.types.Panel):
    bl_idname = "PT_Make_Scene"
    bl_label = "Scene Presets"
    bl_category = "Blend4FTC"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.row().operator("blend4ftc.import_field", text="Make Field")
        layout.row().operator("blend4ftc.basic_world", text="Basic World & Lighting")


        
        mat = bpy.data.materials.get('Void Background')
        if(mat):
            layout.row().label(text="")
            for node in mat.node_tree.nodes:
                if(node.name.startswith("P]")):
                    name = node.name.replace("P] ", "").replace("P]", "")
                    row = layout.row()
                    row.label(text=name)
                    row.prop(node.outputs[0], "default_value", text="Value")
            layout.row().operator("blend4ftc.void_panel", text="Void Panel")
        


def refreshMats(context):    
    while(len(context.scene.mat_list)!=0):
        context.scene.mat_list.remove(0)
    for mat in bpy.data.materials:
        context.scene.mat_list.add()
        context.scene.mat_list[len(context.scene.mat_list)-1].name = mat.name

last_name = ""

class PT_Material_Config(bpy.types.Panel):
    bl_idname = "PT_Material_Config"
    bl_label = "Material Workshop"
    bl_category = "Blend4FTC"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if(scene.mat_list_index == -1 or scene.mat_list_index == None or len(scene.mat_list) == 0):
            layout.row().box().label(text="Select a material for options")
            return
        mat = scene.mat_list[scene.mat_list_index].name
        mat = bpy.data.materials.get(mat)

        if(mat is None or mat.node_tree == None):
            layout.row().box().label(text="Select a material for options")
            return
        
        layout.row().box().label(text=mat.name)
        if(len(mat.node_tree.nodes) == 0):
            layout.row().label(text="No Exposed Properties")
        else:
            layout.row().label(text="Exposed Properties:")
        for node in mat.node_tree.nodes:
            if(node.name.startswith("P]")):
                name = node.name.replace("P] ", "").replace("P]", "")
                row = layout.row()
                row.label(text=name)
                row.prop(node.outputs[0], "default_value", text="Value")
        
        layout.row().prop(mat, "name", text="Name")
        layout.row().operator("blend4ftc.copy_mat", text="Copy")

def update():
    refreshMats(bpy.context)


# Pie
class Nav_Pie(bpy.types.Menu):
    bl_idname = "Nav_Pie"
    bl_label= "NavMenu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator("blend4ftc.move_camera", icon="CAMERA_DATA")
        pie.operator("blend4ftc.camera_view", icon="CAMERA_DATA")
        pie.operator("blend4ftc.stop_move_camera", icon="CAMERA_DATA")

