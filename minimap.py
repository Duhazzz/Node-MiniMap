bl_info = {
    "name": "Node MiniMap",
    "author": "ChatGPT, deepseek, duhazzz",
    "version": (2, 8),
    "blender": (3, 0, 0),
    "location": "Node Editor > N Panel > Node MiniMap",
    "description": "The Mini Map is created based on a tree of nodes and is displayed as buttons.",
    "category": "Node",
}

import bpy
from collections import defaultdict

GRID_COLS = 12
GRID_ROWS = 8
BLOCK_SIZE = 1.5
SMILEY = "😊"

def norm(val, min_val, max_val):
    if max_val - min_val == 0:
        return 0.5
    return (val - min_val) / (max_val - min_val)

def draw_minimap(layout, context, region_width=None):
    if region_width is None:
        region_width = getattr(context.region, "width", 600)

    cols = GRID_COLS
    rows = GRID_ROWS
    cell_width = region_width // cols

    show_full_text = cell_width >= 60
    show_short_text = cell_width >= 35

    space = context.space_data
    tree = space.edit_tree

    if not tree:
        layout.label(text="No node tree open")
        return

    nodes = tree.nodes
    if not nodes:
        layout.label(text="No nodes")
        return

    selected_nodes = {n.name for n in nodes if n.select}

    min_x = min(n.location.x for n in nodes)
    max_x = max(n.location.x + n.width for n in nodes)
    min_y = min(n.location.y - n.height for n in nodes)
    max_y = max(n.location.y for n in nodes)

    def norm_x(x): return norm(x, min_x, max_x)
    def norm_y(y): return norm(y, min_y, max_y)

    cell_map = defaultdict(list)

    for n in nodes:
        nx = norm_x(n.location.x + n.width / 2)
        ny = norm_y(n.location.y - n.height / 2)

        col = min(cols - 1, int(nx * cols * BLOCK_SIZE))
        row = min(rows - 1, int((1 - ny) * rows * BLOCK_SIZE))

        label = n.label.strip() if hasattr(n, 'label') and n.label else ""
        display_name = label if label else n.name

        icon = 'NONE' if label else ('FRAME_NEXT' if n.bl_idname == "NodeFrame" else 'NODE')

        cell_map[(col, row)].append({
            "name": n.name,
            "label": label,
            "text": display_name,
            "icon": icon,
        })

    for row in range(rows):
        row_layout = layout.row(align=True)
        for col in range(cols):
            nodes_in_cell = cell_map.get((col, row), [])
            if nodes_in_cell:
                nodes_sorted = sorted(nodes_in_cell, key=lambda n: 0 if n["label"] else 1)
                nd = nodes_sorted[0]

                if nd["name"] in selected_nodes:
                    text = SMILEY
                    icon = 'NONE'
                else:
                    text = nd["text"] if show_full_text else (nd["text"][:10] + "…" if show_short_text and len(nd["text"]) > 11 else nd["text"])
                    icon = nd["icon"]

                op = row_layout.operator(
                    "node.minimap_jump",
                    text=text if not (nd["name"] in selected_nodes) else SMILEY,
                    icon=icon if not (nd["name"] in selected_nodes) else 'NONE',
                    emboss=True,
                )
                op.node_name = nd["name"]
            else:
                row_layout.label(text=" ", icon='BLANK1')

class NODE_OT_minimap_popup(bpy.types.Operator):
    bl_idname = "node.minimap_popup"
    bl_label = "Node MiniMap Popup"
    bl_description = "Popup with Node MiniMap"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        draw_minimap(self.layout, context, region_width=600)

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.invoke_popup(self, width=600)
        return {'RUNNING_MODAL'}

class NODE_PT_minimap_panel(bpy.types.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Node MiniMap"
    bl_label = "Node MiniMap"

    def draw(self, context):
        layout = self.layout

        layout.operator("node.minimap_popup", text="Open in Popup", icon='WINDOW')
        layout.separator()
        draw_minimap(layout, context)

class NODE_OT_minimap_jump(bpy.types.Operator):
    bl_idname = "node.minimap_jump"
    bl_label = "Jump to Node"
    bl_description = "Jump to node in editor"

    node_name: bpy.props.StringProperty()

    def execute(self, context):
        space = context.space_data
        tree = space.edit_tree

        if not tree:
            self.report({'WARNING'}, "No node tree")
            return {'CANCELLED'}

        node = tree.nodes.get(self.node_name)
        if not node:
            self.report({'WARNING'}, f"Node {self.node_name} not found")
            return {'CANCELLED'}

        # Сохраняем текущее выделение и активный узел
        selected_node_names = {n.name for n in tree.nodes if n.select}
        active_node = tree.nodes.active

        # Временно выделяем только нужный узел
        for n in tree.nodes:
            n.select = False
        node.select = True
        tree.nodes.active = node

        # Выполняем фокус с правильным масштабом
        bpy.ops.node.view_selected()

        # Восстанавливаем старое выделение
        for n in tree.nodes:
            n.select = n.name in selected_node_names
        tree.nodes.active = active_node if active_node else None

        return {'FINISHED'}

classes = [
    NODE_PT_minimap_panel,
    NODE_OT_minimap_jump,
    NODE_OT_minimap_popup,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
