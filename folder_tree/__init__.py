import bpy
import os
import subprocess

from bpy.types import Operator, Panel
from bpy.props import StringProperty
from bpy.utils import register_class, unregister_class

directory_path = r'C:\Users\One\Desktop\Новая папка'


class SomeFolder:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path


def create_directory_tree(path, indent=''):
    file_list = []
    
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            folder_name = indent + item + '/'
            file_list.append(SomeFolder(folder_name, item_path))
            file_list.extend(create_directory_tree(item_path, indent + ' ' * 8))
        else:
            file_list.append(SomeFolder(indent + item, item_path))
    return file_list


class FT_OT_folder_tree(Operator):
    bl_idname = "object.folder_tree_operator"
    bl_label = "OPEN"
    button_id = bpy.props.StringProperty(attr="button_id")

    def execute(self, context):
        file_list = create_directory_tree(directory_path)
        print(file_list)
        try:
            subprocess.Popen(['explorer', self.button_id])
        except:
            print("Ошибка при открытии папки")
        return {'FINISHED'}


class FT_PT_folder_tree(Panel):
    bl_label = "Folder Tree"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Folder Tree"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        file_list = create_directory_tree(directory_path)
        
        for item in file_list:
            if item.name[-1] == '/':
                row = layout.row()
                row.alignment = 'LEFT'
                row.operator('object.folder_tree_operator', icon='FILE_FOLDER', text='->').button_id = item.path
                row.label(text=item.name)
            elif item.name[-6:] == '.blend':
                row = layout.row()
                row.alignment = 'LEFT'
                row.operator('object.folder_tree_operator', icon='BLENDER', text='->').button_id = item.path
                row.label(text=item.name)
            elif item.name[-3:] == '.py':
                row = layout.row()
                row.alignment = 'LEFT'
                row.operator('object.folder_tree_operator', icon='FILE_SCRIPT', text='->').button_id = item.path
                row.label(text=item.name)


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

