import bpy
import os

from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import StringProperty
from bpy.utils import register_class, unregister_class


def create_directory_tree(path, indent=''):
    file_list = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            file_list.append(indent + item + '/')
            file_list.extend(create_directory_tree(item_path, indent + '  '))
        else:
            file_list.append(indent + item)
    return file_list


class FT_OT_folder_tree(Operator):
    bl_idname = "object.folder_tree_operator"
    bl_label = "Add folder tree"


    def execute(self, context):
        return {'FINISHED'}


class FT_PT_folder_tree(Panel):
    bl_label = "Folder Tree"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Folder Tree"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        directory_path = r'C:\Users\One\Desktop\Новая папка'
        
        for i in create_directory_tree(directory_path):
            if i[-1] == '/':
                row = layout.row()
                row.label(text=i, icon='FILE_FOLDER')
            if i[-6::] == '.blend':         
                row = layout.row()
                row.label(text=i, icon='BLENDER')
            if i[-3::] == '.py':         
                row = layout.row()
                row.label(text=i, icon='FILE_SCRIPT')


classes = (
    FT_OT_folder_tree,
    FT_PT_folder_tree
)


def register():
    for cl in classes:
        register_class(cl)


def unregister():
    for cl in reversed(classes):
        unregister_class(cl)


if __name__ == "__main__":
    register()
