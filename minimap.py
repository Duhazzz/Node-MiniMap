bl_info = {
    "name": "Node MiniMap Popup",
    "author": "ChatGPT, deepseek, duhazzz",
    "version": (2, 9),
    "blender": (3, 0, 0),
    "location": "Node Editor > N Panel > Node MiniMap",
    "description": "Shows node minimap in popup when activated from N Panel",
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

def analyze_nodes(context):
    space = context.space_data
    tree = space.edit_tree

    if not tree or not tree.nodes:
        return None

    nodes = tree.nodes
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

        col = min(GRID_COLS - 1, int(nx * GRID_COLS * BLOCK_SIZE))
        row = min(GRID_ROWS - 1, int((1 - ny) * GRID_ROWS * BLOCK_SIZE))

        label = n.label.strip() if hasattr(n, 'label') and n.label else ""
        display_name = label if label else n.name

        icon = 'NONE' if label else ('FRAME_NEXT' if n.bl_idname == "NodeFrame" else 'NODE')

        cell_map[(col, row)].append({
            "name": n.name,
            "label": label,
            "text": display_name,
            "icon": icon,
            "selected": n.name in selected_nodes,
        })

    return {
        "cell_map": cell_map,
        "show_full_text": True,  # Always show full text in popup
    }

def draw_minimap(layout, analysis_result):
    if analysis_result is None:
        layout.label(text="No nodes to display")
        return

    cell_map = analysis_result["cell_map"]
    show_full_text = analysis_result["show_full_text"]

    for row in range(GRID_ROWS):
        row_layout = layout.row(align=True)
        for col in range(GRID_COLS):
            nodes_in_cell = cell_map.get((col, row), [])
            if nodes_in_cell:
                nodes_sorted = sorted(nodes_in_cell, key=lambda n: 0 if n["label"] else 1)
                nd = nodes_sorted[0]

                op = row_layout.operator(
                    "node.minimap_jump",
                    text=SMILEY if nd["selected"] else nd["text"],
                    icon='NONE' if nd["selected"] else nd["icon"],
                    emboss=True,
                )
                op.node_name = nd["name"]
            else:
                row_layout.label(text=" ", icon='BLANK1')

class NODE_OT_minimap_popup(bpy.types.Operator):
    bl_idname = "node.minimap_popup"
    bl_label = "Node MiniMap"
    bl_description = "Show node minimap in popup"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        analysis_result = analyze_nodes(context)
        draw_minimap(self.layout, analysis_result)

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=600)

class NODE_PT_minimap_panel(bpy.types.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Node MiniMap"
    bl_label = "Node MiniMap"

    def draw(self, context):
        layout = self.layout
        layout.operator("node.minimap_popup", text="Show MiniMap", icon='WINDOW')

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

        # Save current selection
        selected_node_names = {n.name for n in tree.nodes if n.select}
        active_node = tree.nodes.active

        # Select only the target node
        for n in tree.nodes:
            n.select = False
        node.select = True
        tree.nodes.active = node

        # Focus on the node
        bpy.ops.node.view_selected()

        # Restore selection
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
