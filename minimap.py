bl_info = {
    "name": "Node MiniMap Color Blocks with Popup",
    "author": "ChatGPT",
    "version": (2, 8),
    "blender": (3, 0, 0),
    "location": "Node Editor > N Panel > Node MiniMap",
    "description": "Миникарта с цветными блоками, смайликом при выделении и возможностью открытия в Popup",
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

        label = n.label.strip() if hasattr(n, 'label') else ""
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
                    icon = nd["icon"]
                    if show_full_text:
                        text = nd["text"]
                    elif show_short_text:
                        text = nd["text"][:10] + "…" if len(nd["text"]) > 11 else nd["text"]
                    else:
                        text = ""

                op = row_layout.operator(
                    "node.minimap_jump",
                    text=text,
                    icon=icon,
                    emboss=True,
                )
                if op is not None:
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

        for n in tree.nodes:
            n.select = False
        node.select = True
        tree.nodes.active = node

        bpy.ops.node.view_selected()
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
