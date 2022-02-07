# Copyright (C) 2022, Francis LaBounty, All rights reserved.

import bpy
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from sympy import symbols, lambdify, diff

from . import nodes

bl_info = {
    "name": "Graph",
    "description": "Blender geometry nodes graphing utility.",
    "author": "Francis LaBounty - labounty3d@gmail.com - github.com/francislabountyjr",
    "version": (1, 0, 0),
    "category": "Node",
    "blender": (3, 00, 0),
    "location": "Geometry Nodes > Toolbar > Graph",
    "wiki_url": "",
    "warning": "",
    "tracker_url": "",
    "support": "COMMUNITY"
}


def parse_functions(funcs, convert_func=True):
    # Parse expression
    for i, func in enumerate(funcs):
        funcs[i] = parse_expr(func, transformations=(
            standard_transformations + (implicit_multiplication_application,)))

    # Instantiate sympy symbols and lambdify function
    x, y, z = symbols('x y z')
    syms = funcs[0].free_symbols
    for i in range(1, len(funcs)):
        syms.update(funcs[i].free_symbols)
    syms.add(x)
    syms.add(y)
    syms.add(z)
    syms = list(syms)

    if convert_func:
        for i, func in enumerate(funcs):
            funcs[i] = lambdify(syms, func)

        syms = [str(x) for x in syms]
    return (funcs, syms)


def replace_symbols(funcs, syms):
    coords = ['x', 'y', 'z']
    for i, func in enumerate(funcs):
        func = list(func)
        for j, char in enumerate(func):
            for k, sym in enumerate(syms):
                if char == sym:
                    func[j] = coords[k]
                elif char == coords[k]:
                    func[j] = sym
        funcs[i] = ''.join(func)

    return funcs


class GN_OT_CreateCurve(bpy.types.Operator):
    """Create curve from X Y Z component functions
    all taking in X variable"""

    bl_idname = "mesh.gn_create_curve"
    bl_label = "Create Curve"

    def execute(self, context):
        wm = context.window_manager

        # Parse expression
        funcs = replace_symbols([wm.curvex, wm.curvey, wm.curvez], ['t'])
        funcs, syms = parse_functions(funcs)

        nodes.create_curve(*funcs, syms, wm.mesh_or_curve, 60, 10)

        return {"FINISHED"}


class GN_OT_CreateGraph(bpy.types.Operator):
    """Create graph from input expression"""

    bl_idname = "mesh.gn_create_graph"
    bl_label = "Create Graph"

    def execute(self, context):
        wm = context.window_manager

        # Parse expression
        funcs, syms = parse_functions([wm.function])

        nodes.create_graph("Graph", *funcs, syms, 20, 20, 50,
                           50, False, False, False, wm.color_flag,
                           wm.color_min, wm.color_max, wm.x_, wm.y_, wm.z_, None)

        return {"FINISHED"}


class GN_OT_CreateScatter(bpy.types.Operator):
    """Create scatter plot from input expression"""

    bl_idname = "mesh.gn_create_scatter_plot"
    bl_label = "Create Scatter Plot"

    def execute(self, context):
        wm = context.window_manager

        # Parse expression
        funcs, syms = parse_functions([wm.function])

        nodes.create_graph("Scatter Graph", *funcs, syms, 20, 20, 50,
                           50, True, False, False, True,
                           wm.color_min, wm.color_max, wm.x_, wm.y_, wm.z_, None)

        return {"FINISHED"}


class GN_OT_CreateContour(bpy.types.Operator):
    """Create contour plot from input expression"""

    bl_idname = "mesh.gn_create_contour_plot"
    bl_label = "Create Contour Plot"

    def execute(self, context):
        wm = context.window_manager

        # Parse expression
        funcs, syms = parse_functions([wm.function])

        nodes.create_contour(*funcs, syms, 20, 20,
                             50, 50, wm.color_min, wm.color_max)

        return {"FINISHED"}


class GN_OT_CreateSlice(bpy.types.Operator):
    """Create slice out of graph"""

    bl_idname = "mesh.gn_create_slice"
    bl_label = "Create Slice"

    def execute(self, context):
        wm = context.window_manager

        nodes.create_slice(20, 20)

        return {"FINISHED"}


class GN_OT_CreateTangentPlane(bpy.types.Operator):
    """Create tangent plane from input expression and evaluation point"""

    bl_idname = "mesh.gn_create_tangent_plane"
    bl_label = "Create Tangent Plane"

    def execute(self, context):
        wm = context.window_manager

        # Parse expression
        func = parse_expr(wm.function, transformations=(
            standard_transformations + (implicit_multiplication_application,)))

        # Instantiate symbolic (x, y, z)
        x, y, z = symbols("x y z")

        diffx = diff(func, x)  # ∂F/∂x
        diffy = diff(func, y)  # ∂F/∂y
        diffz = diff(func, z)  # ∂F/∂z
        diffx = lambdify((x, y, z), diffx)  # lambdify ∂F/∂x
        diffy = lambdify((x, y, z), diffy)  # lambdify ∂F/∂y
        diffz = lambdify((x, y, z), diffz)  # lambdify ∂F/∂z
        func = lambdify((x, y, z), func)  # lambdify function

        tangent_plane_func = func(wm.x_, wm.y_, wm.z_) + \
            diffx(wm.x_, wm.y_, wm.z_) * (x - wm.x_) + diffy(wm.x_, wm.y_, wm.z_) * \
            (y - wm.y_) + diffz(wm.x_, wm.y_, wm.z_) * (z - wm.z_)

        wm.tangent_plane_function = str(tangent_plane_func)

        tangent_plane_func = lambdify((x, y, z), tangent_plane_func)

        nodes.create_graph("Tangent Graph", tangent_plane_func, ['x', 'y', 'z'], 5, 5, 2,
                           2, False, wm.insert_point, True, wm.color_flag,
                           wm.color_min, wm.color_max, wm.x_, wm.y_, wm.z_, 'tangent')

        return {"FINISHED"}


class GN_OT_CreateQuadraticApproximation(bpy.types.Operator):
    """Create quadratic approximation from input expression and evaluation point"""

    bl_idname = "mesh.gn_create_quadratic_approximation"
    bl_label = "Create Quadratic Approximation"

    def execute(self, context):
        wm = context.window_manager

        # Parse expression
        func = parse_expr(wm.function, transformations=(
            standard_transformations + (implicit_multiplication_application,)))

        # Instantiate symbolic (x, y, z)
        x, y, z = symbols("x y z")

        diffx = diff(func, x)  # ∂F/∂x
        diffy = diff(func, y)  # ∂F/∂y
        diffz = diff(func, z)  # ∂F/∂z
        diffxx = diff(diffx, x)  # ∂²F/∂x²
        diffyy = diff(diffy, y)  # ∂²F/∂y²
        diffzz = diff(diffz, z)  # ∂²F/∂z²
        diffxy = diff(diffx, y)  # ∂²F/∂xy
        diffxz = diff(diffx, z)  # ∂²F/∂xz
        diffyz = diff(diffy, z)  # ∂²F/∂yz

        diffx = lambdify((x, y, z), diffx)  # lambdify ∂F/∂x
        diffy = lambdify((x, y, z), diffy)  # lambdify ∂F/∂y
        diffz = lambdify((x, y, z), diffz)  # lambdify ∂F/∂z
        diffxx = lambdify((x, y, z), diffxx)  # ∂²F/∂x²
        diffyy = lambdify((x, y, z), diffyy)  # ∂²F/∂y²
        diffzz = lambdify((x, y, z), diffzz)  # ∂²F/∂z²
        diffxy = lambdify((x, y, z), diffxy)  # ∂²F/∂xy
        diffxz = lambdify((x, y, z), diffxz)  # ∂²F/∂xz
        diffyz = lambdify((x, y, z), diffyz)  # ∂²F/∂yz
        func = lambdify((x, y, z), func)  # lambdify function

        quad_approx_func = func(wm.x_, wm.y_, wm.z_) + \
            diffx(wm.x_, wm.y_, wm.z_) * (x - wm.x_) + diffy(wm.x_, wm.y_, wm.z_) * \
            (y - wm.y_) + diffz(wm.x_, wm.y_, wm.z_) * (z - wm.z_) + \
            diffxy(wm.x_, wm.y_, wm.z_) * (x - wm.x_) * (y - wm.y_) + \
            diffxz(wm.x_, wm.y_, wm.z_) * (x - wm.x_) * (z - wm.y_) + \
            diffyz(wm.x_, wm.y_, wm.z_) * (y - wm.y_) * (z - wm.z_) + \
            0.5 * (diffxx(wm.x_, wm.y_, wm.z_) * (x - wm.x_)**2 +
                   diffyy(wm.x_, wm.y_, wm.z_) * (y - wm.y_)**2 +
                   diffzz(wm.x_, wm.y_, wm.z_) * (z - wm.z_)**2)

        wm.quadratic_approximation_function = str(quad_approx_func)

        quad_approx_func = lambdify((x, y, z), quad_approx_func)

        nodes.create_graph("Quad Approx Graph", quad_approx_func, ['x', 'y', 'z'], 5, 5, 50,
                           50, False, wm.insert_point, True, wm.color_flag,
                           wm.color_min, wm.color_max, wm.x_, wm.y_, wm.z_, 'quad')

        return {"FINISHED"}


class GN_OT_CreateGradientField(bpy.types.Operator):
    """Create gradient field from input expression"""

    bl_idname = "mesh.gn_create_gradient_field"
    bl_label = "Create Gradient Field"

    def execute(self, context):
        wm = context.window_manager

        # Parse expression
        funcs, syms = parse_functions([wm.function], False)

        # Instantiate symbolic (x, y, z)
        x, y, z = symbols("x y z")

        diffx = diff(*funcs, x)  # ∂F/∂x
        diffy = diff(*funcs, y)  # ∂F/∂y
        diffz = diff(*funcs, z)  # ∂F/∂z

        wm.diffx = str(diffx)
        wm.diffy = str(diffy)
        wm.diffz = str(diffz)

        diffx = lambdify(syms, diffx)  # lambdify ∂F/∂x
        diffy = lambdify(syms, diffy)  # lambdify ∂F/∂y
        diffz = lambdify(syms, diffz)  # lambdify ∂F/∂z
        func = lambdify(syms, *funcs)  # lambdify function

        syms = [str(x) for x in syms]

        nodes.create_vector_field(
            func, diffx, diffy, diffz, syms, wm.join_graph, wm.join_graph, wm.use_length, wm.color_flag, wm.color_min, wm.color_max, 20, 20, 50, 50)

        return {"FINISHED"}


class GN_OT_CreateGradientDescentAscent(bpy.types.Operator):
    """Create gradient descent or gradient ascent vector stream from < Fx(x,y,z), Fy(x,y,z), Fz(x,y,z) >"""

    bl_idname = "mesh.gn_create_gradient_descent_ascent"
    bl_label = "Create Gradient Descent/Ascent"

    def execute(self, context):
        wm = context.window_manager

        # Parse expression
        func = parse_expr(wm.function, transformations=(
            standard_transformations + (implicit_multiplication_application,)))

        # Instantiate symbolic (x, y, z)
        x, y, z = symbols("x y z")

        diffx = diff(func, x)  # ∂F/∂x
        diffy = diff(func, y)  # ∂F/∂y
        diffz = diff(func, z)  # ∂F/∂z

        wm.diffx = str(diffx)
        wm.diffy = str(diffy)
        wm.diffz = str(diffz)

        diffx = lambdify((x, y, z), diffx)  # lambdify ∂F/∂x
        diffy = lambdify((x, y, z), diffy)  # lambdify ∂F/∂y
        diffz = lambdify((x, y, z), diffz)  # lambdify ∂F/∂z
        func = lambdify((x, y, z), func)  # lambdify function

        gradient = 'descent' if wm.gradient_dir else 'ascent'

        nodes.create_vector_stream(
            func, diffx, diffy, diffz, wm.dt, wm.steps, wm.color_flag, wm.color_min,
            wm.color_max, wm.limit, gradient)

        return {"FINISHED"}


class GN_OT_CreateVectorField(bpy.types.Operator):
    """Create vector field from < Fx(x,y,z), Fy(x,y,z), Fz(x,y,z) >"""

    bl_idname = "mesh.gn_create_vector_field"
    bl_label = "Create Vector Field"

    def execute(self, context):
        wm = context.window_manager

        if wm.on_graph:
            # Parse expression
            funcs, syms = parse_functions(
                [wm.function, wm.functionx, wm.functiony, wm.functionz])
        else:
            funcs, syms = parse_functions(
                [wm.functionx, wm.functiony, wm.functionz])
            funcs.insert(0, None)

        nodes.create_vector_field(
            *funcs, syms, wm.on_graph, wm.join_graph, wm.use_length, wm.color_flag, wm.color_min, wm.color_max, 20, 20, 50, 50)

        return {"FINISHED"}


class GN_OT_CreateCurlField(bpy.types.Operator):
    """Create curl vector field from < Fx(x,y,z), Fy(x,y,z), Fz(x,y,z) >"""

    bl_idname = "mesh.gn_create_curl_field"
    bl_label = "Create Curl Vector Field"

    def execute(self, context):
        wm = context.window_manager

        # Parse expression
        if wm.on_graph:
            funcs, syms = parse_functions(
                [wm.function, wm.functionx, wm.functiony, wm.functionz], False)
            idx = 1
        else:
            funcs, syms = parse_functions(
                [wm.functionx, wm.functiony, wm.functionz], False)
            idx = 0

        # Instantiate symbolic (x, y, z)
        x, y, z = symbols('x y z')

        diffXy = diff(funcs[idx], y)  # ∂Fx/∂y
        diffXz = diff(funcs[idx], z)  # ∂Fx/∂z
        diffYx = diff(funcs[idx+1], x)  # ∂Fy/∂x
        diffYz = diff(funcs[idx+1], z)  # ∂Fy/∂z
        diffZy = diff(funcs[idx+2], y)  # ∂Fz/∂y
        diffZx = diff(funcs[idx+2], x)  # ∂Fz/∂x

        funcX = diffZy - diffYz
        funcY = diffXz - diffZx
        funcZ = diffYx - diffXy

        wm.curl_x = str(funcX)
        wm.curl_y = str(funcY)
        wm.curl_z = str(funcZ)

        # Lambdify Fx, Fy, Fz
        funcX = lambdify(syms, funcX)
        funcY = lambdify(syms, funcY)
        funcZ = lambdify(syms, funcZ)

        if wm.on_graph:
            # Lambdify function
            func = lambdify(syms, funcs[0])
        else:
            func = None

        syms = [str(x) for x in syms]

        nodes.create_vector_field(
            func, funcX, funcY, funcZ, syms, wm.on_graph, wm.join_graph, wm.use_length, wm.color_flag, wm.color_min, wm.color_max, 20, 20, 50, 50)

        return {"FINISHED"}


class GN_OT_CreateVectorStream(bpy.types.Operator):
    """Create vector stream from < Fx(x,y,z), Fy(x,y,z), Fz(x,y,z) >"""

    bl_idname = "mesh.gn_create_vector_stream"
    bl_label = "Create Vector Stream"

    def execute(self, context):
        wm = context.window_manager

        # Parse expressions
        funcX = parse_expr(wm.functionx, transformations=(
            standard_transformations + (implicit_multiplication_application,)))
        funcY = parse_expr(wm.functiony, transformations=(
            standard_transformations + (implicit_multiplication_application,)))
        funcZ = parse_expr(wm.functionz, transformations=(
            standard_transformations + (implicit_multiplication_application,)))

        # Instantiate symbolic (x, y, z)
        x, y, z = symbols('x y z')

        # Lambdify Fx, Fy, Fz
        funcX = lambdify((x, y, z), funcX)
        funcY = lambdify((x, y, z), funcY)
        funcZ = lambdify((x, y, z), funcZ)

        nodes.create_vector_stream(
            None, funcX, funcY, funcZ, wm.dt, wm.steps, wm.color_flag, wm.color_min,
            wm.color_max, wm.limit, False)

        return {"FINISHED"}


class GN_OT_CreateSurface(bpy.types.Operator):
    """Create surface from X Y Z component functions
    parameterized by X and Y"""

    bl_idname = "mesh.gn_create_surface"
    bl_label = "Create Parametric Surface"

    def execute(self, context):
        wm = context.window_manager

        # Parse expression
        funcs = replace_symbols([wm.surfx, wm.surfy, wm.surfz], ['u', 'v'])
        funcs, syms = parse_functions(funcs)

        nodes.create_surface(*funcs, syms, 50, 50)

        return {"FINISHED"}


class GN_PT_Panel(bpy.types.Panel):
    """Create a panel in the shader editor tool shelf"""

    bl_label = "Graph"
    bl_idname = "panel.gn_node_editor_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Graph"

    def draw(self, context):
        return


class GN_PT_CreateGraphSettingsPanel(bpy.types.Panel):
    """Create graph settings sub panel"""

    bl_label = "Graph Settings"
    bl_idname = "panel.gn_node_editor_create_graph_settings_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Graph Settings"
    bl_parent_id = "panel.gn_node_editor_panel"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 0

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        if bpy.context.active_object and 'Graph' in bpy.context.active_object.name:
            slice_mod = bpy.context.active_object.modifiers.get(
                "Slice")
            if slice_mod:
                slice_nodes = slice_mod.node_group.nodes
                slice_transform = nodes.node_search(
                    slice_nodes, "Slice_Transform")
                slice_grid = nodes.node_search(slice_nodes, "Grid")
                if slice_transform and slice_grid:
                    row = layout.row(align=True)
                    row.label(text="Slice Plane Settings")
                    row = layout.row(align=True)
                    row.label(text="Size X")
                    row.prop(slice_grid.inputs[0], "default_value", text="")
                    row.label(text="Size Y")
                    row.prop(slice_grid.inputs[1], "default_value", text="")
                    row = layout.row(align=True)
                    row.label(text="Location")
                    row.prop(
                        slice_transform.inputs[1], "default_value", text="")
                    row = layout.row(align=True)
                    row.label(text="Rotation")
                    row.prop(
                        slice_transform.inputs[2], "default_value", text="")
                    row = layout.row(align=True)
                    row.label(text="Scale")
                    row.prop(
                        slice_transform.inputs[3], "default_value", text="")

            geo_mod = bpy.context.active_object.modifiers.get(
                "GeometryNodes")
            if geo_mod:
                geo_node_group = geo_mod.node_group
                geo_nodes = geo_mod.node_group.nodes

                for input in geo_node_group.inputs:
                    if input.name.endswith('variable') or input.name == "Vector Scale":
                        row = layout.row(align=True)
                        row.label(text=input.name)
                        row.prop(geo_mod, f'["{input.identifier}"]', text="")

                if bpy.context.active_object.name.startswith('contour'):
                    row = layout.row(align=True)
                    row.prop(wm, "line_count")
                    row.prop(wm, "start_z")
                    row.prop(wm, "end_z")
                    row.prop(wm, "scale_z")

                    row = layout.row(align=True)
                    row.prop(wm, "bool_x")
                    row.prop(wm, "bool_y")
                    row.prop(
                        bpy.data.objects["contour_boolean"].modifiers["Solidify"], 'thickness')
                    row.prop(
                        bpy.data.objects["contour_plot"].modifiers["Weld"], 'merge_threshold')

                    geo_mod_curves = bpy.context.active_object.modifiers.get(
                        "GeometryNodes.001")
                    if geo_mod_curves:
                        geo_curve_nodes = geo_mod_curves.node_group.nodes
                        curve_circle_node = nodes.node_search(
                            geo_curve_nodes, "Curve Circle")
                        if curve_circle_node:
                            row = layout.row(align=True)
                            row.label(text="Contour Resolution")
                        row.prop(
                            curve_circle_node.inputs[0], "default_value", text="")
                        row = layout.row(align=True)
                        row.label(text="Contour Radius")
                        row.prop(
                            curve_circle_node.inputs[4], "default_value", text="")

                surface_range_x = nodes.node_search(
                    geo_nodes, "Surface Range X")
                if surface_range_x:
                    row = layout.row(align=True)
                    row.label(text="U Range Settings")
                    row = layout.row(align=True)
                    row.label(text="Min")
                    row.prop(
                        surface_range_x.inputs[3], "default_value", text="")
                    row.label(text="Max")
                    row.prop(
                        surface_range_x.inputs[4], "default_value", text="")

                surface_range_y = nodes.node_search(
                    geo_nodes, "Surface Range Y")
                if surface_range_y:
                    row = layout.row(align=True)
                    row.label(text="V Range Settings")
                    row = layout.row(align=True)
                    row.label(text="Min")
                    row.prop(
                        surface_range_y.inputs[3], "default_value", text="")
                    row.label(text="Max")
                    row.prop(
                        surface_range_y.inputs[4], "default_value", text="")

                icosphere = nodes.node_search(geo_nodes, "Ico Sphere")
                if icosphere:
                    row = layout.row(align=True)
                    row.label(text="Ico Sphere Settings")
                    row = layout.row(align=True)
                    row.label(text="Radius")
                    row.prop(icosphere.inputs[0], "default_value", text="")
                    row.label(text="Subdivisions")
                    row.prop(icosphere.inputs[1], "default_value", text="")

                uvsphere = nodes.node_search(geo_nodes, "UV Sphere")
                if uvsphere:
                    row = layout.row(align=True)
                    row.label(text="UV Sphere Settings")
                    row = layout.row(align=True)
                    row.label(text="Segments")
                    row.prop(uvsphere.inputs[0], "default_value", text="")
                    row.label(text="Rings")
                    row.prop(uvsphere.inputs[1], "default_value", text="")
                    row.label(text="Radius")
                    row.prop(uvsphere.inputs[2], "default_value", text="")

                mesh_line = nodes.node_search(geo_nodes, "Mesh Line")
                if mesh_line:
                    row = layout.row(align=True)
                    row.label(text="Mesh Line Settings")
                    row = layout.row(align=True)
                    row.label(text="Count")
                    row.prop(mesh_line.inputs[0], "default_value", text="")
                    row = layout.row(align=True)
                    row.label(text="Start")
                    row.prop(mesh_line.inputs[2], "default_value", text="")
                    row = layout.row(align=True)
                    row.label(text="End")
                    row.prop(mesh_line.inputs[3], "default_value", text="")

                curve_line = nodes.node_search(geo_nodes, "Curve Line")
                if curve_line:
                    row = layout.row(align=True)
                    row.label(text="Curve Line Settings")
                    row = layout.row(align=True)
                    row.label(text="Start")
                    row.prop(curve_line.inputs[0], "default_value", text="")
                    row = layout.row(align=True)
                    row.label(text="End")
                    row.prop(curve_line.inputs[1], "default_value", text="")

                grid = nodes.node_search(geo_nodes, "Grid")
                if grid:
                    row = layout.row(align=True)
                    row.label(text="Grid Settings")
                    row = layout.row(align=True)
                    row.label(text="Size X")
                    row.prop(grid.inputs[0], "default_value", text="")
                    row.label(text="Size Y")
                    row.prop(grid.inputs[1], "default_value", text="")
                    row.label(text="Vertices X")
                    row.prop(grid.inputs[2], "default_value", text="")
                    row.label(text="Vertices Y")
                    row.prop(grid.inputs[3], "default_value", text="")

                subdivision = nodes.node_search(
                    geo_nodes, "Subdivision Surface")
                shade_smooth = nodes.node_search(geo_nodes, "Set Shade Smooth")
                if subdivision or shade_smooth:
                    row = layout.row(align=True)
                    if subdivision:
                        row.label(text="Subdivisions")
                        row.prop(subdivision.inputs[1],
                                 "default_value", text="")
                    if shade_smooth:
                        row.label(text="Shade Smooth")
                        row.prop(
                            shade_smooth.inputs[2], "default_value", text="")

                resample_curve = nodes.node_search(geo_nodes, "Resample Curve")
                if resample_curve:
                    row = layout.row(align=True)
                    row.label(text="Resample Curve Amount")
                    row.prop(resample_curve.inputs[2],
                             "default_value", text="")

                curve_circle = nodes.node_search(geo_nodes, "Curve Circle")
                if curve_circle:
                    row = layout.row(align=True)
                    row.label(text="Curve Circle")
                    row = layout.row(align=True)
                    row.label(text="Curve Resolution")
                    row.prop(curve_circle.inputs[0], "default_value", text="")
                    row = layout.row(align=True)
                    row.label(text="Curve Radius")
                    row.prop(curve_circle.inputs[4], "default_value", text="")

                transform = nodes.node_search(geo_nodes, "Master_Transform")
                if transform:
                    row = layout.row(align=True)
                    row.label(text="Pre Function Transform")
                    row = layout.row(align=True)
                    row.label(text="Location")
                    row.prop(transform.inputs[1], "default_value", text="")
                    row = layout.row(align=True)
                    row.label(text="Rotation")
                    row.prop(transform.inputs[2], "default_value", text="")
                    row = layout.row(align=True)
                    row.label(text="Scale")
                    row.prop(transform.inputs[3], "default_value", text="")

                secondary_transform = nodes.node_search(
                    geo_nodes, "Secondary_Transform")
                if secondary_transform:
                    row = layout.row(align=True)
                    row.label(text="Post Function Pre vField Transform")
                    row = layout.row(align=True)
                    row.label(text="Location")
                    row.prop(
                        secondary_transform.inputs[1], "default_value", text="")
                    row = layout.row(align=True)
                    row.label(text="Rotation")
                    row.prop(
                        secondary_transform.inputs[2], "default_value", text="")
                    row = layout.row(align=True)
                    row.label(text="Scale")
                    row.prop(
                        secondary_transform.inputs[3], "default_value", text="")

                post_transform = nodes.node_search(geo_nodes, "Post_Transform")
                if post_transform:
                    row = layout.row(align=True)
                    row.label(text="Post Function Transform")
                    row = layout.row(align=True)
                    row.label(text="Location")
                    row.prop(post_transform.inputs[1],
                             "default_value", text="")
                    row = layout.row(align=True)
                    row.label(text="Rotation")
                    row.prop(post_transform.inputs[2],
                             "default_value", text="")
                    row = layout.row(align=True)
                    row.label(text="Scale")
                    row.prop(post_transform.inputs[3],
                             "default_value", text="")


class GN_PT_CreateUtilitiesPanel(bpy.types.Panel):
    """Create utilities sub panel"""

    bl_label = "Utilities"
    bl_idname = "panel.gn_node_editor_create_utilities_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Utilities"
    bl_parent_id = "panel.gn_node_editor_panel"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 1

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row(align=True)
        row.operator("mesh.gn_create_slice",
                     icon="FILE_REFRESH", text="Plane Slice")


class GN_PT_CreateCurvePanel(bpy.types.Panel):
    """Create curve sub panel"""

    bl_label = "Curve"
    bl_idname = "panel.gn_node_editor_create_curve_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Curve"
    bl_parent_id = "panel.gn_node_editor_panel"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 2

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row(align=True)
        row.operator("mesh.gn_create_curve",
                     icon="FILE_REFRESH", text="Create Curve")
        row.prop(wm, "mesh_or_curve", text="Use Mesh")

        row = layout.row(align=True)
        row.label(text="c(t) -> R³")
        row = layout.row(align=True)
        row.prop(wm, "curvex", text='x(t)')
        row = layout.row(align=True)
        row.prop(wm, "curvey", text='y(t)')
        row = layout.row(align=True)
        row.prop(wm, "curvez", text='z(t)')


class GN_PT_CreateGraphPanel(bpy.types.Panel):
    """Create graph sub panel"""

    bl_label = "Graph"
    bl_idname = "panel.gn_node_editor_create_graph_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Graph"
    bl_parent_id = "panel.gn_node_editor_panel"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 3

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row(align=True)
        row.operator("mesh.gn_create_graph",
                     icon="FILE_REFRESH", text="Create Graph")

        row = layout.row(align=True)
        row.operator("mesh.gn_create_scatter_plot",
                     icon="FILE_REFRESH", text="Create Scatter Plot")
        row.operator("mesh.gn_create_contour_plot",
                     icon="FILE_REFRESH", text="Create Contour Plot")

        row = layout.row(align=True)
        row.operator("mesh.gn_create_gradient_field",
                     icon="FILE_REFRESH", text="Create Gradient Field")
        row.operator("mesh.gn_create_gradient_descent_ascent",
                     icon="FILE_REFRESH", text="Create Gradient Descent/Ascent")

        row = layout.row(align=True)
        row.label(text="f(x, y, z) -> R")

        row = layout.row(align=True)
        row.prop(wm, "function", text='f(x, y, z)')

        row = layout.row(align=True)
        row.prop(wm, "join_graph")
        row.prop(wm, "gradient_dir", text="Descent")
        row.prop(wm, "color_flag", text="Use Color")
        row.prop(wm, "color_min")
        row.prop(wm, "color_max")

        row = layout.row(align=True)
        row.prop(wm, "diffx")
        row.prop(wm, "diffy")
        row.prop(wm, "diffz")

        row = layout.row(align=True)
        row.operator("mesh.gn_create_tangent_plane",
                     icon="FILE_REFRESH", text="Create Tangent Plane")
        row.operator("mesh.gn_create_quadratic_approximation",
                     icon="FILE_REFRESH", text="Create Quadratic Approximation")

        row = layout.row(align=True)
        row.prop(wm, "insert_point", text='Insert Point')
        row.prop(wm, "x_", text='x₀')
        row.prop(wm, "y_", text='y₀')
        row.prop(wm, "z_", text='z₀')

        row = layout.row(align=True)
        row.prop(wm, "tangent_plane_function")

        row = layout.row(align=True)
        row.prop(wm, "quadratic_approximation_function")


class GN_PT_CreateVectorPanel(bpy.types.Panel):
    """Create vector sub panel"""

    bl_label = "Vector"
    bl_idname = "panel.gn_node_editor_create_vector_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Vector"
    bl_parent_id = "panel.gn_node_editor_panel"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 4

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row(align=True)
        row.operator("mesh.gn_create_vector_field",
                     icon="FILE_REFRESH", text="Create Vector Field")
        row.operator("mesh.gn_create_vector_stream",
                     icon="FILE_REFRESH", text="Create Vector Stream")

        row = layout.row(align=True)
        row.operator("mesh.gn_create_curl_field",
                     icon="FILE_REFRESH", text="Create Curl Vector Field")

        row = layout.row(align=True)
        row.prop(wm, "use_length", text="Use Length")
        row.prop(wm, "on_graph", text="On graph")
        row.prop(wm, "dt")
        row.prop(wm, "steps")
        row.prop(wm, "limit")

        row = layout.row(align=True)
        row.prop(wm, "color_flag", text="Use Color")
        row.prop(wm, "color_min")
        row.prop(wm, "color_max")

        row = layout.row(align=True)
        row.label(text="v(x, y, z) -> R³")
        row = layout.row(align=True)
        row.prop(wm, "functionx", text="Q(x, y, z)")
        row = layout.row(align=True)
        row.prop(wm, "functiony", text="R(x, y, z)")
        row = layout.row(align=True)
        row.prop(wm, "functionz", text="S(x, y, z)")

        row = layout.row(align=True)
        row.prop(wm, "curl_x")
        row.prop(wm, "curl_y")
        row.prop(wm, "curl_z")


class GN_PT_CreateSurfacePanel(bpy.types.Panel):
    """Create Parametric Surface sub panel"""

    bl_label = "Surface"
    bl_idname = "panel.gn_node_editor_create_surface_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Surface"
    bl_parent_id = "panel.gn_node_editor_panel"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 5

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row(align=True)
        row.operator("mesh.gn_create_surface",
                     icon="FILE_REFRESH", text="Create Parametric Surface")

        row = layout.row(align=True)
        row.label(text="r(u, v) -> R³")
        row = layout.row(align=True)
        row.prop(wm, "surfx", text='x(u, v)')
        row = layout.row(align=True)
        row.prop(wm, "surfy", text='y(u, v)')
        row = layout.row(align=True)
        row.prop(wm, "surfz", text='z(u, v)')


classes = (
    GN_OT_CreateCurve,
    GN_OT_CreateGraph,
    GN_OT_CreateContour,
    GN_OT_CreateScatter,
    GN_OT_CreateSlice,
    GN_OT_CreateTangentPlane,
    GN_OT_CreateQuadraticApproximation,
    GN_OT_CreateGradientField,
    GN_OT_CreateGradientDescentAscent,
    GN_OT_CreateVectorField,
    GN_OT_CreateVectorStream,
    GN_OT_CreateCurlField,
    GN_OT_CreateSurface,
    GN_PT_Panel,
    GN_PT_CreateGraphSettingsPanel,
    GN_PT_CreateUtilitiesPanel,
    GN_PT_CreateCurvePanel,
    GN_PT_CreateGraphPanel,
    GN_PT_CreateVectorPanel,
    GN_PT_CreateSurfacePanel
)


def register():
    from bpy.types import WindowManager
    from bpy.props import (
        StringProperty,
        FloatProperty,
        IntProperty,
        BoolProperty,
        FloatVectorProperty
    )

    WindowManager.mesh_or_curve = BoolProperty(
        name="Use Mesh",
        default=False,
        description="Whether to use a mesh line or a curve line"
    )

    WindowManager.curvex = StringProperty(
        name="Curve X",
        default='0',
        description="Curve X component",
    )

    WindowManager.curvey = StringProperty(
        name="Curve Y",
        default='0',
        description="Curve Y component",
    )

    WindowManager.curvez = StringProperty(
        name="Curve Z",
        default='0',
        description="Curve Z component",
    )

    WindowManager.surfx = StringProperty(
        name="Surface X",
        default='0',
        description="Surface X component",
    )

    WindowManager.surfy = StringProperty(
        name="Surface Y",
        default='0',
        description="Surface Y component",
    )

    WindowManager.surfz = StringProperty(
        name="Surface Z",
        default='0',
        description="Surface Z component",
    )

    WindowManager.functionx = StringProperty(
        name="Function X",
        default='0',
        description="Function X",
    )

    WindowManager.functiony = StringProperty(
        name="Function Y",
        default='0',
        description="Function Y",
    )

    WindowManager.functionz = StringProperty(
        name="Function Z",
        default='0',
        description="Function Z",
    )

    WindowManager.diffx = StringProperty(
        name="∂F/∂x",
        default='',
        description="∂F/∂x",
    )

    WindowManager.diffy = StringProperty(
        name="∂F/∂y",
        default='',
        description="∂F/∂y",
    )

    WindowManager.diffz = StringProperty(
        name="∂F/∂z",
        default='',
        description="∂F/∂z",
    )

    WindowManager.curl_x = StringProperty(
        name="Curl x",
        default='∂R/∂y - ∂Q/∂z',
        description="Curl x",
    )

    WindowManager.curl_y = StringProperty(
        name="Curl y",
        default='∂P/∂z - ∂R/∂x',
        description="Curl y",
    )

    WindowManager.curl_z = StringProperty(
        name="Curl z",
        default='∂Q/∂x - ∂P/∂y',
        description="Curl z",
    )

    WindowManager.function = StringProperty(
        name="Function",
        default='',
        description="Function",
    )

    WindowManager.tangent_plane_function = StringProperty(
        name="Tangent Plane Function",
        default='f(x₀) + ∇f(x₀) ○ (x - x₀)',
        description="Tangent Plane Function",
    )

    WindowManager.quadratic_approximation_function = StringProperty(
        name="Quadratic Approximation Function",
        default='f(x₀) + ∇f(x₀) ○ (x - x₀) + 1/2(x - x₀).T * Hբ(x₀)(x - x₀)',
        description="Quadratic Approximation Function",
    )

    # WindowManager.size_x = FloatProperty(
    #     name="Size x",
    #     default=20,
    #     description="Size in x dimension",
    #     min=.001,
    #     max=100000
    # )

    # WindowManager.size_y = FloatProperty(
    #     name="Size y",
    #     default=20,
    #     description="Size in y dimension",
    #     min=.001,
    #     max=100000
    # )

    WindowManager.bool_x = FloatProperty(
        name="Bool X",
        default=1,
        description="Size in x dimension to add to bool object",
        min=.001,
        max=100000
    )

    WindowManager.bool_y = FloatProperty(
        name="Bool Y",
        default=1,
        description="Size in y dimension to add to bool object",
        min=.001,
        max=100000
    )

    WindowManager.x_ = FloatProperty(
        name="x₀",
        default=0,
        description="x₀",
        min=-100000,
        max=100000
    )

    WindowManager.y_ = FloatProperty(
        name="y₀",
        default=0,
        description="y₀",
        min=-100000,
        max=100000
    )

    WindowManager.z_ = FloatProperty(
        name="z₀",
        default=0,
        description="z₀",
        min=-100000,
        max=100000
    )

    WindowManager.insert_point = BoolProperty(
        name="Insert Point",
        default=True,
        description="Whether or not to insert point at specified position"
    )

    WindowManager.color_flag = BoolProperty(
        name="Color Flag",
        default=True,
        description="Whether or not to color visualization"
    )

    WindowManager.join_graph = BoolProperty(
        name="Join Graph",
        default=True,
        description="Whether or not to join graph and vector field geometry"
    )

    WindowManager.gradient_dir = BoolProperty(
        name="Gradient Dir",
        default=True,
        description="Whether to use gradient descent or ascent. True = descent"
    )

    WindowManager.use_length = BoolProperty(
        name="Use Length",
        default=True,
        description="Whether or not to use vector length in vector field visualization"
    )

    WindowManager.on_graph = BoolProperty(
        name="On Graph",
        default=False,
        description="Whether or not to place vectors on points of a specified function"
    )

    WindowManager.dt = FloatProperty(
        name="dt",
        default=.1,
        description="dt",
        min=-1000,
        max=1000
    )

    WindowManager.steps = IntProperty(
        name="Steps",
        default=50,
        description="steps",
        min=1,
        max=100000
    )

    WindowManager.line_count = IntProperty(
        name="Count",
        default=11,
        description="Contour Line Count",
        min=1,
        max=10000
    )

    WindowManager.limit = FloatProperty(
        name="Limit",
        default=100,
        description="Set limit for vector values to avoid overflow",
        min=.001,
        max=100000
    )

    WindowManager.start_z = FloatProperty(
        name="Start Z",
        default=-5,
        description="Starting Z value for contour lines",
        min=-100000,
        max=100000
    )

    WindowManager.end_z = FloatProperty(
        name="End Z",
        default=5,
        description="Ending Z value for contour lines",
        min=-100000,
        max=100000
    )

    WindowManager.scale_z = FloatProperty(
        name="Scale Z",
        default=0,
        description="Z value to scale contour plot",
        min=0,
        max=1
    )

    WindowManager.color_min = FloatVectorProperty(
        name="Color Min",
        default=(0, 0, 1, 1),
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        description="Value to go into color ramp minimum"
    )

    WindowManager.color_max = FloatVectorProperty(
        name="Color Max",
        default=(1, 0, 0, 1),
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        description="Value to go into color ramp maximum"
    )

    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    from bpy.types import WindowManager

    del WindowManager.mesh_or_curve
    del WindowManager.curvex
    del WindowManager.curvey
    del WindowManager.curvez
    del WindowManager.surfx
    del WindowManager.surfy
    del WindowManager.surfz
    del WindowManager.function
    del WindowManager.functionx
    del WindowManager.functiony
    del WindowManager.functionz
    del WindowManager.curlx
    del WindowManager.curly
    del WindowManager.curlz
    del WindowManager.tangent_plane_function
    del WindowManager.bool_x
    del WindowManager.bool_y
    del WindowManager.x_
    del WindowManager.y_
    del WindowManager.z_
    del WindowManager.insert_point
    del WindowManager.color_flag
    del WindowManager.join_graph
    del WindowManager.use_length
    del WindowManager.on_graph
    del WindowManager.dt
    del WindowManager.steps
    del WindowManager.color_min
    del WindowManager.color_max
    del WindowManager.line_count
    del WindowManager.start_z
    del WindowManager.end_z
    del WindowManager.scale_z

    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
