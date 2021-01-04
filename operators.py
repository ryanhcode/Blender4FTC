import bpy
import bpy.types
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, EnumProperty
from bpy_extras.io_utils import ImportHelper
import os
from bpy.types import PropertyGroup, UIList



def import_materials(filepath, context):
    link = False

    currentMats = []

    for mat in bpy.data.materials:
        currentMats.append(mat.name)

    newMats = []

    with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
        for material in data_from.materials:
            if material not in currentMats:
                newMats.append(material)
                data_to.materials = material

    print("Appending materials from Default library : ",newMats)

    addedMats = []
    for mat in newMats:
        if(mat in currentMats):
            continue
        bpy.ops.wm.append(filename=mat, directory=filepath + "\\Material\\")
        #addedMats+=[mat]

    currentMatList = []
    for mat in context.scene.mat_list:
        currentMatList+=mat.name

    for mat in newMats:
        if mat in currentMatList:
            pass
        else:
            addedMats+=[mat]

    return addedMats

def refreshMats(context):    
    while(len(context.scene.mat_list)!=0):
        context.scene.mat_list.remove(0)
    for mat in bpy.data.materials:
        context.scene.mat_list.add()
        context.scene.mat_list[len(context.scene.mat_list)-1].name = mat.name

class CopyCurrentMat(bpy.types.Operator):
    bl_idname = "blend4ftc.copy_mat"
    bl_label = "Copy Material"

    def execute(self, context):
        mat = context.scene.mat_list[context.scene.mat_list_index].name
        mat = bpy.data.materials.get(mat)
        mat.copy().name = "Copy of " + mat.name
        refreshMats(context)
        counter = 0
        for x in context.scene.mat_list:
            if x.name == "Copy of " + mat.name:
                context.scene.mat_list_index = counter
            counter+=1
        return {"FINISHED"}
class RefreshMats(bpy.types.Operator):
    bl_idname = "blend4ftc.refresh_mats"
    bl_label = "Refresh Materials"

    def execute(self, context):
        refreshMats(context)
        return {"FINISHED"}

class OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.apply_material"
    bl_label = "Import Default Lib"

    def execute(self, context):
        # path to the blend
        filepath = os.path.dirname(__file__) + "/packs/default.blend"
        
        mats = import_materials(filepath, context)

        refreshMats(context)

        return {'FINISHED'}



import io
from urllib import request


class BasicWorldOperator(bpy.types.Operator):
    bl_idname = "blend4ftc.basic_world"
    bl_label = "Basic World"

    def execute(self, context):
        bpy.context.scene.render.engine = 'CYCLES'
        filepath = os.path.dirname(__file__) + "/carpentry_shop_02_2k.hdr"
        context.scene.world.light_settings.use_ambient_occlusion = True

        world = context.scene.world
        world.use_nodes = True
        enode = context.scene.world.node_tree.nodes.new("ShaderNodeTexEnvironment")

        #print("Images:::")
        #print(data_from.images)
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.6
            
        bpy.data.images.load(filepath, check_existing=False)
        #loadImageFromUrl("https://hdrihaven.com/files/hdri_images/tonemapped/1500/carpentry_shop_02.jpg", name="hdridef")
        
        enode.image = bpy.data.images['carpentry_shop_02_2k.hdr']

        backNode = context.scene.world.node_tree.nodes['Background']
        enodeOut = enode.outputs['Color']
        backColIn = backNode.inputs['Color']
        context.scene.world.node_tree.links.new(enodeOut, backColIn)

        return {'FINISHED'}


class Make_Field(bpy.types.Operator):
    bl_idname = "blend4ftc.import_field"
    bl_label = "Import Basic Field Scene"

    def execute(self, context):
        filepath = os.path.dirname(__file__) + "/packs/default.blend"
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.startswith("field")]

        scene = bpy.context.scene
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
        return {'FINISHED'}

def assign_mat(obj, mat):
    #if mat is None:
    #    return
    #if obj is None:
    #    return
    #if obj.data is not None:
    #    obj.data.materials.append(mat)
    #    obj.data.materials[0] = mat
    if obj.data is not None:
        if len(obj.material_slots) < 1:
            # if there is no slo2t then we append to create the slot and assign
            obj.data.materials.append(mat)
        else:
            # we always want the material in slot[0]
            obj.material_slots[0].material = mat

smartShadeDictNon = {
    "square beam": "[OLD] Standard Metal",
    "shaft beam": "[OLD] Standard Metal",
    "sonic": "[OLD] Standard Metal",
    "stainless": "steel",
    "aluminum": "[OLD] Standard Metal",
    "grid plate": "[OLD] Standard Metal",
    "pattern bracket": "[OLD] Standard Metal",
    "pattern plate": "[OLD] Standard Metal",
    "1100-0009-0240": "[OLD] Standard Metal",
    "Base Plate": "[OLD] Standard Metal",
    "Side Holder": "[OLD] Standard Metal",
    "screw": "[OLD] Standard Metal",
    "2802-0004-0014": "[OLD] Standard Metal",
    "Roller Locknut": "[OLD] Standard Metal",
    "1309-0016-1006": "[OLD] Standard Metal",
    "3606-0100-0100 Side Plate": "Dark Standard Metal",
    "3606-0000-0100 Side Plate": "Dark Standard Metal",
    "3606-XXXX-0100 Wheel Center": "Dark Standard Metal",
    "Hi Durability Roller": "mecanumrollers yellow",
    "1501-0006-0026": "[OLD] Standard Metal",
    "2104-0012-0043": "[OLD] Standard Metal",
    "REV-11-1271-2 ALT": "Dark Rubber",
    "REV-11-1271-1": "Dark Rubber",
    "2800-0004-0010": "[OLD] Standard Metal",
    "S6B-PH-K-S": "HDPE",
    "servo arm": "[OLD] Standard Metal",
    "series l-beam": "[OLD] Standard Metal",
    "u-channel": "[OLD] Standard Metal",
    "clamping mount": "[OLD] Standard Metal",
    "case": "[OLD] Standard Metal",
    "servo body": "servo",
    "servo case": "servo",
    "servo spline": "[OLD] Standard Metal",
    "1201-0043-0002": "[OLD] Standard Metal",
    "back cover": "dark jacket",
    "black part of gearbox": "oxide",
    "outer clip": "yellow jacket",
    "shaft": "[OLD] Standard Metal",
    "motor metal": "[OLD] Standard Metal",
    "servoblock": "[OLD] Standard Metal",
    "set screw": "[OLD] Standard Metal",
    "standoff": "[OLD] Standard Metal",
    "delrin": "Delrin",
    "belt": "dark rubber",
    "1.5´ç90¶È»¡ÐÎÂÖ": "dark rubber",
    "1.5´ç90¶ÈÂÖ¹Ì¶": "hdpe",
    "1.5´ç90¶ÈÂÖÈü¸ÖÌ×_5":"[OLD] Standard Metal",
    "3606-XXXX-0100 Roller Shim_8":"[OLD] Standard Metal",
    "brass": "brass",
    "4103-0032-0072": "[OLD] Standard Metal",
    "1514 Series": "[OLD] Standard Metal",
    "3400 Series": "[OLD] Standard Metal",
    "1514 Series": "[OLD] Standard Metal",
    "1501 Series": "[OLD] Standard Metal",
    "2102 Series": "steel",
    "2315-4008-0030": "[OLD] Standard Metal",
    "2315 Series": "[OLD] Standard Metal",
    "2806-0005-0004": "[OLD] Standard Metal",
    "2803-0039-0022": "[OLD] Standard Metal",
    "3414 Series": "[OLD] Standard Metal",
    "1400 Series": "[OLD] Standard Metal",
    "1112 Series": "[OLD] Standard Metal",
    "outer race": "[OLD] Standard Metal",
    "2303 Series": "[OLD] Standard Metal",
    "1802 Series": "[OLD] Standard Metal",
    "Prevailing torque nut": "[OLD] Standard Metal",
    "servo body": "servo",
    "roller e-clip":"[OLD] Standard Metal",
    "roller e-clip":"[OLD] Standard Metal",
    "roller axle":"[OLD] Standard Metal",
    "roller cover":"dark rubber"
}
from collections import OrderedDict

smartShadeDict = OrderedDict(smartShadeDictNon)


def getChildren(myObject): 
    children = [] 
    for ob in bpy.data.objects: 
        if ob.parent == myObject: 
            children.append(ob) 
    return children 

#Smart Shade
class OT_AutoAssign(bpy.types.Operator):
    bl_idname = "view3d.auto_material"
    bl_label = "SmartShade"
    bl_description = "Smart-Shade mapped parts"

    def execute(self, context):
        smartMats = {}

        objec = bpy.data.objects

        objs = []

        for obj in objec:
            objs.append(obj)
            for i in getChildren(obj):
                objs.append(i)


        for key in smartShadeDict:
            for mat in bpy.data.materials:
                if(smartShadeDict[key].lower() in mat.name.lower()):
                    smartMats[key] = mat
        
        for obj in objs:
            print(obj.name)
            for key in smartMats:
                if(key.lower() in obj.name.lower()):
                    assign_mat(obj, smartMats[key])
        return {'FINISHED'}


class OT_Import_Custom(bpy.types.Operator, ImportHelper):
    bl_idname = "blend4ftc.import_custom"
    bl_label = "Import custom material lib"

    filter_glob: StringProperty(
        default='*.blend',
        options={'HIDDEN'}
    )

    some_boolean: BoolProperty(
        name="Import Materials",
        description="Import the Materials from the selected file",
        default=True
    )

    def execute(self,context):
        filepath = self.filepath
        mats = import_materials(filepath, context)
        
        refreshMats()
        return {'FINISHED'}

class OT_AssignMaterial(bpy.types.Operator):
    bl_idname = "blend4ftc.assign_material"
    bl_label = "Assign Material"
    bl_description = "Assign selected material"


    def execute(self,context):
        mat = context.scene.mat_list[context.scene.mat_list_index].name
        mat = bpy.data.materials.get(mat)

        selection_names = bpy.context.selected_objects

        for ob in selection_names:
            assign_mat(ob, mat)

        return {'FINISHED'}

class OT_Void_Panel(bpy.types.Operator):
    bl_idname = "blend4ftc.void_panel"
    bl_label = "Void Panel"

    def execute(self, context):
        obj = bpy.context.scene.objects.get("VoidPlane")
        if obj:
            pass
        else:
            bpy.ops.mesh.primitive_plane_add(size=500, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(20, 20, 20))
            context.active_object.name = 'VoidPlane'
            assign_mat(context.active_object, bpy.data.materials['Void Background'])
        return {'FINISHED'}

class OT_StartMoveCamera(bpy.types.Operator):
    bl_idname = "blend4ftc.move_camera"
    bl_label = "Move Camera"
    bl_description = "Adjust Camera"


    def execute(self,context):
        area = next(area for area in context.screen.areas if area.type == 'VIEW_3D')
        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        bpy.context.space_data.lock_camera = True
        return {'FINISHED'}


class OT_CameraView(bpy.types.Operator):
    bl_idname = "blend4ftc.camera_view"
    bl_label = "Camera View"
    bl_description = "Enter Camera View"


    def execute(self,context):
        area = next(area for area in context.screen.areas if area.type == 'VIEW_3D')
        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        bpy.context.space_data.lock_camera = False
        return {'FINISHED'}


class OT_StopMoveCamera(bpy.types.Operator):
    bl_idname = "blend4ftc.stop_move_camera"
    bl_label = "Stop Move Camera"
    bl_description = "Stop Adjust Camera"


    def execute(self,context):
        area = next(area for area in context.screen.areas if area.type == 'VIEW_3D')
        area.spaces[0].region_3d.view_perspective = 'PERSP'
        bpy.context.space_data.lock_camera = False
        return {'FINISHED'}

class SetupOp1(bpy.types.Operator):
    bl_idname = "blend4ftc.setupop1"
    bl_label = "Basic Scene Setup"
    bl_description = "Configure Basics"

    def execute(self, context):
        scene = context.scene
        scene.render.engine = 'CYCLES'
        if(scene.performance != "LOW"):
            bpy.context.scene.cycles.device = 'GPU'
        scene.render.film_transparent = True
        if(scene.performance == "LOW"):
            scene.cycles.samples = 130
        if(scene.performance == "MEDIUM"):
            scene.cycles.samples = 175
        if(scene.performance == "HIGH"):
            scene.cycles.samples = 230
        if(scene.theme == "DRAMATIC"):
            scene.view_settings.look = 'Very High Contrast'
        if(scene.theme == "MEDIUM"):
            scene.view_settings.look = 'Medium High Contrast'
        if(scene.theme == "NORMAL"):
            scene.view_settings.look = 'None'
        if(scene.theme == "LOW"):
            scene.view_settings.look = 'Medium Low Contrast'
        
        ##################################

        # switch on nodes and get reference
        scene.use_nodes = True
        tree = scene.node_tree

        # clear default nodes
        for node in tree.nodes:
            tree.nodes.remove(node)

        # create input image node

        input_node = tree.nodes.new(type="CompositorNodeRLayers")
        input_node.location = -400,0

        alpha_over_node = tree.nodes.new(type='CompositorNodeAlphaOver')
        alpha_over_node.location = 0,0
        alpha_over_node.inputs[1].default_value = scene.voidColor

        denoise_mix_node = tree.nodes.new(type='CompositorNodeMixRGB')
        denoise_mix_node.location = 0,0
        denoise_mix_node.inputs[0].default_value = scene.denoisingFac
        denoise_node = tree.nodes.new(type='CompositorNodeDenoise')
        denoise_node.location = 0,0

        despeckle_node = tree.nodes.new(type="CompositorNodeDespeckle")
        despeckle_node.location = 0,0

        lens_d_node = tree.nodes.new(type="CompositorNodeLensdist")
        lens_d_node.location = 0,0
        lens_d_node.use_fit = True
        lens_d_node.inputs[1].default_value = 0.01 if scene.lensD else 0.0

        # create output node
        comp_node = tree.nodes.new('CompositorNodeComposite')   
        comp_node.location = 400,0

        bc_node = tree.nodes.new("CompositorNodeBrightContrast")
        bc_node.location = 0,0
        bc_node.inputs[1].default_value = scene.brightness
        bc_node.inputs[2].default_value = scene.contrast


        # link nodes
        links = tree.links
        link = links.new(input_node.outputs[0], alpha_over_node.inputs[2])
        #link = links.new(alpha_over_node.outputs[0], comp_node.inputs[0])
        link = links.new(alpha_over_node.outputs[0], denoise_mix_node.inputs[1])
        link = links.new(alpha_over_node.outputs[0], denoise_node.inputs[0])
        link = links.new(denoise_node.outputs[0], denoise_mix_node.inputs[2])
        link = links.new(denoise_mix_node.outputs[0], despeckle_node.inputs[1])
        link = links.new(despeckle_node.outputs[0], lens_d_node.inputs[0])
        link = links.new(lens_d_node.outputs[0], bc_node.inputs[0])
        link = links.new(bc_node.outputs[0], comp_node.inputs[0])
        #link = links.new(denoise_mix_node.outputs[0], comp_node.inputs[0])


        ##################################

        return {'FINISHED'}



class ListItem(PropertyGroup):
    name: StringProperty(
        name="Name",
        description="A name for this entry",
        default="Unnamed"
    )

class Mat_UI_List(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        custom_icon = "OBJECT_DATAMODE"
        if self.layout_type in {'DEFAULT',"COMPACT"}:
            layout.label(text=item.name, icon=custom_icon)
        elif self.layout_type in {'GRID'}:
            layout_alignment = 'CENTER'
            layout.label(text="",icon=custom_icon)