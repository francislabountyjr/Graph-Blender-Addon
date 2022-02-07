# Copyright (C) 2022, Francis LaBounty, All rights reserved.

import bpy
import sympy
import numpy as np


class NodeMath():
    """
    NodeMath class that overloads common math expressions in order to programmatically
    set up functions inside of Blender's node system
    """

    def __init__(self, output, node_group, offset_x=0, offset_y=0):
        self.output = output
        self.node_group = node_group
        self.nodes = self.node_group.nodes
        self.offset_x = offset_x
        self.offset_y = offset_y

    def __add__(self, var):
        add_node = self.nodes.new("ShaderNodeMath")
        add_node.operation = 'ADD'

        self.node_group.links.new(self.output, add_node.inputs[0])

        if isinstance(var, float) or isinstance(var, int):
            add_node.inputs[1].default_value = var
        else:
            self.node_group.links.new(var.output, add_node.inputs[1])

        add_node.location = (self.offset_x, self.offset_y)

        return NodeMath(add_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def __radd__(self, var):
        add_node = self.nodes.new("ShaderNodeMath")
        add_node.operation = 'ADD'

        self.node_group.links.new(self.output, add_node.inputs[1])

        if isinstance(var, float) or isinstance(var, int):
            add_node.inputs[0].default_value = var
        else:
            self.node_group.links.new(var.output, add_node.inputs[0])

        add_node.location = (self.offset_x, self.offset_y)

        return NodeMath(add_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def __sub__(self, var):
        sub_node = self.nodes.new("ShaderNodeMath")
        sub_node.operation = 'SUBTRACT'

        self.node_group.links.new(self.output, sub_node.inputs[0])

        if isinstance(var, float) or isinstance(var, int):
            sub_node.inputs[1].default_value = var
        else:
            self.node_group.links.new(var.output, sub_node.inputs[1])

        sub_node.location = (self.offset_x, self.offset_y)

        return NodeMath(sub_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def __rsub__(self, var):
        sub_node = self.nodes.new("ShaderNodeMath")
        sub_node.operation = 'ADD'

        self.node_group.links.new(self.output, sub_node.inputs[1])

        if isinstance(var, float) or isinstance(var, int):
            sub_node.inputs[0].default_value = var
        else:
            self.node_group.links.new(var.output, sub_node.inputs[0])

        sub_node.location = (self.offset_x, self.offset_y)

        return NodeMath(sub_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def __mul__(self, var):
        mul_node = self.nodes.new("ShaderNodeMath")
        mul_node.operation = 'MULTIPLY'

        self.node_group.links.new(self.output, mul_node.inputs[0])

        if isinstance(var, float) or isinstance(var, int):
            mul_node.inputs[1].default_value = var
        else:
            self.node_group.links.new(var.output, mul_node.inputs[1])

        mul_node.location = (self.offset_x, self.offset_y)

        return NodeMath(mul_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def __rmul__(self, var):
        mul_node = self.nodes.new("ShaderNodeMath")
        mul_node.operation = 'MULTIPLY'

        self.node_group.links.new(self.output, mul_node.inputs[1])

        if isinstance(var, float) or isinstance(var, int):
            mul_node.inputs[0].default_value = var
        else:
            self.node_group.links.new(var.output, mul_node.inputs[0])

        mul_node.location = (self.offset_x, self.offset_y)

        return NodeMath(mul_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def __floordiv__(self, var):
        div_node = self.nodes.new("ShaderNodeMath")
        div_node.operation = 'DIVIDE'

        floor_node = self.nodes.new("ShaderNodeMath")
        floor_node.operation = 'FLOOR'

        self.node_group.links.new(self.output, div_node.inputs[0])

        if isinstance(var, float) or isinstance(var, int):
            div_node.inputs[1].default_value = var
        else:
            self.node_group.links.new(var.output, div_node.inputs[1])

        self.node_group.links.new(
            div_node.outputs['Value'], floor_node.inputs[0])

        div_node.location = (self.offset_x, self.offset_y)
        floor_node.location = (self.offset_x, self.offset_y)

        return NodeMath(floor_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def __rfloordiv__(self, var):
        div_node = self.nodes.new("ShaderNodeMath")
        div_node.operation = 'DIVIDE'

        floor_node = self.nodes.new("ShaderNodeMath")
        floor_node.operation = 'FLOOR'

        self.node_group.links.new(self.output, div_node.inputs[1])

        if isinstance(var, float) or isinstance(var, int):
            div_node.inputs[0].default_value = var
        else:
            self.node_group.links.new(var.output, div_node.inputs[0])

        self.node_group.links.new(
            div_node.outputs['Value'], floor_node.inputs[0])

        div_node.location = (self.offset_x, self.offset_y)
        floor_node.location = (self.offset_x, self.offset_y)

        return NodeMath(floor_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def __truediv__(self, var):
        div_node = self.nodes.new("ShaderNodeMath")
        div_node.operation = 'DIVIDE'

        self.node_group.links.new(self.output, div_node.inputs[0])

        if isinstance(var, float) or isinstance(var, int):
            div_node.inputs[1].default_value = var
        else:
            self.node_group.links.new(var.output, div_node.inputs[1])

        div_node.location = (self.offset_x, self.offset_y)

        return NodeMath(div_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def __rtruediv__(self, var):
        div_node = self.nodes.new("ShaderNodeMath")
        div_node.operation = 'DIVIDE'

        self.node_group.links.new(self.output, div_node.inputs[1])

        if isinstance(var, float) or isinstance(var, int):
            div_node.inputs[0].default_value = var
        else:
            self.node_group.links.new(var.output, div_node.inputs[0])

        div_node.location = (self.offset_x, self.offset_y)

        return NodeMath(div_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def __pow__(self, var):
        pow_node = self.nodes.new("ShaderNodeMath")
        pow_node.operation = 'POWER'

        self.node_group.links.new(self.output, pow_node.inputs[0])

        if isinstance(var, float) or isinstance(var, int):
            pow_node.inputs[1].default_value = var
        else:
            self.node_group.links.new(var.output, pow_node.inputs[1])

        pow_node.location = (self.offset_x, self.offset_y)

        return NodeMath(pow_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def __rpow__(self, var):
        pow_node = self.nodes.new("ShaderNodeMath")
        pow_node.operation = 'POWER'

        self.node_group.links.new(self.output, pow_node.inputs[1])

        if isinstance(var, float) or isinstance(var, int):
            pow_node.inputs[0].default_value = var
        else:
            self.node_group.links.new(var.output, pow_node.inputs[0])

        pow_node.location = (self.offset_x, self.offset_y)

        return NodeMath(pow_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def __mod__(self, var):
        mod_node = self.nodes.new("ShaderNodeMath")
        mod_node.operation = 'MODULO'

        self.node_group.links.new(self.output, mod_node.inputs[0])

        if isinstance(var, float) or isinstance(var, int):
            mod_node.inputs[1].default_value = var
        else:
            self.node_group.links.new(var.output, mod_node.inputs[1])

        mod_node.location = (self.offset_x, self.offset_y)

        return NodeMath(mod_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def __rmod__(self, var):
        mod_node = self.nodes.new("ShaderNodeMath")
        mod_node.operation = 'MODULO'

        self.node_group.links.new(self.output, mod_node.inputs[1])

        if isinstance(var, float) or isinstance(var, int):
            mod_node.inputs[0].default_value = var
        else:
            self.node_group.links.new(var.output, mod_node.inputs[0])

        mod_node.location = (self.offset_x, self.offset_y)

        return NodeMath(mod_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def __neg__(self):
        neg_node = self.nodes.new("ShaderNodeMath")
        neg_node.operation = 'MULTIPLY'

        self.node_group.links.new(self.output, neg_node.inputs[0])

        neg_node.inputs[1].default_value = -1.0

        neg_node.location = (self.offset_x, self.offset_y)

        return NodeMath(neg_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def cos(self):
        cos_node = self.nodes.new("ShaderNodeMath")
        cos_node.operation = 'COSINE'

        self.node_group.links.new(self.output, cos_node.inputs[0])

        cos_node.location = (self.offset_x, self.offset_y)

        return NodeMath(cos_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def sin(self):
        sin_node = self.nodes.new("ShaderNodeMath")
        sin_node.operation = 'SINE'

        self.node_group.links.new(self.output, sin_node.inputs[0])

        sin_node.location = (self.offset_x, self.offset_y)

        return NodeMath(sin_node.outputs['Value'], self.node_group, self.offset_x, self.offset_y)

    def sqrt(self):
        return self**0.5


def sin(var):
    # Handle different cases for sin depending on input type
    if isinstance(var, NodeMath):
        return var.sin()
    elif isinstance(var, sympy.Symbol):
        return sympy.sin(var)
    else:
        return np.sin(var)


def cos(var):
    # Handle different cases for cos depending on input type
    if isinstance(var, NodeMath):
        return var.cos()
    elif isinstance(var, sympy.Symbol):
        return sympy.cos(var)
    else:
        return np.cos(var)


def sqrt(var):
    # Handle different cases for sqrt depending on input type
    if isinstance(var, NodeMath):
        return var.sqrt()
    elif isinstance(var, sympy.Symbol):
        return sympy.sqrt(var)
    else:
        return np.sqrt(var)


def scalar_check(var, node_group, location=(0, 0)):
    """
    Check if output is scalar and not an instance of NodeMath
    """
    if isinstance(var, float) or isinstance(var, int):
        value_node = node_group.nodes.new("ShaderNodeValue")
        value_node.outputs[0].default_value = var
        value_node.location = location
        return NodeMath(value_node.outputs['Value'], node_group)
    else:
        return var


def instantiate_nodemath(syms, node_group, node_group_in, separate_xyz_node, offset_x=0, offset_y=0):
    """
    Instantiate NodeMath objects
    """
    nodemath_syms = []
    for i in range(len(syms)):
        if syms[i] == 'x':
            nodemath_syms.append(
                NodeMath(separate_xyz_node.outputs['X'], node_group, offset_x, offset_y))
        elif syms[i] == 'y':
            nodemath_syms.append(
                NodeMath(separate_xyz_node.outputs['Y'], node_group, offset_x, offset_y))
        elif syms[i] == 'z':
            nodemath_syms.append(
                NodeMath(separate_xyz_node.outputs['Z'], node_group, offset_x, offset_y))
        else:
            node_group.inputs.new('NodeSocketFloat', f"{syms[i]} variable")
            nodemath_syms.append(NodeMath(
                node_group_in.outputs[f"{syms[i]} variable"], node_group, offset_x, offset_y))
    return nodemath_syms


def add_driver(source, target, prop, name, dataPath, index=-1, func='', id_type='WINDOWMANAGER', d_type=''):
    '''
    Add driver to source prop (at index) driven by the target dataPath
    '''
    if index != -1:
        driver = source.driver_add(prop, index).driver
    else:
        driver = source.driver_add(prop).driver

    if isinstance(name, list):
        for i in range(len(name)):
            variable = driver.variables.new()
            variable.name = name[i]
            variable.targets[0].id_type = id_type[i] if isinstance(
                id_type, list) else id_type
            variable.targets[0].id = target[i] if isinstance(
                target, list) else target
            variable.targets[0].data_path = dataPath[i] if isinstance(
                dataPath, list) else dataPath

    else:
        variable = driver.variables.new()
        variable.name = name
        variable.targets[0].id_type = id_type
        variable.targets[0].id = target
        variable.targets[0].data_path = dataPath

    if d_type == '':
        driver.expression = func
    else:
        driver.type = d_type


def node_search(nodes, name):
    """
    Search for a node by name given the nodes of a node group
    """
    for node in nodes:
        if name in node.name:
            return node
    return None


def create_material(mat_name, attribute_name, color_min, color_max, set_material_node):
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True

    mat_nodes = mat.node_tree.nodes
    mat_links = mat.node_tree.links

    # Populate and position shader nodes
    color_ramp_node = mat_nodes.new("ShaderNodeValToRGB")
    color_ramp_node.color_ramp.elements[0].color = color_min
    color_ramp_node.color_ramp.elements[1].color = color_max
    color_ramp_node.location = (-300, 200)

    attribute_node = mat_nodes.new("ShaderNodeAttribute")
    attribute_node.attribute_name = attribute_name
    attribute_node.location = (-500, 200)

    # Create shader node links
    mat_links.new(
        color_ramp_node.outputs[0], mat_nodes['Principled BSDF'].inputs[0])
    mat_links.new(attribute_node.outputs[2], color_ramp_node.inputs[0])

    bpy.context.active_object.data.materials.append(mat)

    # Set the set material geometry node to use the new material
    set_material_node.inputs[2].default_value = mat


def create_graph(name, func, syms, size_x, size_y, x_dim, y_dim, is_scatter, insert_point, translate_graph, color_flag, color_min, color_max, x_, y_, z_, type=''):
    """
    Function to create a 3D surface plot of a three variable function with
    a scalar output. F(x, y, z) -> R
    Leave out variable(s) from equation to graph lower dimensional functions
    """
    # Create object and link it to scene
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    # Set as active object
    bpy.context.view_layer.objects.active = obj

    # Add geometry nodes modifier to object
    bpy.ops.object.modifier_add(type='NODES')

    # Get geometry node group from active object
    node_group = obj.modifiers.get(
        "GeometryNodes").node_group
    nodes = node_group.nodes

    # populate, position, and set default values for nodes
    node_group_in = nodes.get('Group Input')

    if insert_point or translate_graph:
        input_vec_node = nodes.new("FunctionNodeInputVector")
        input_vec_node.vector[0] = x_
        input_vec_node.vector[1] = y_
        input_vec_node.vector[2] = z_
        input_vec_node.location = (-600, 0)

    input_position_node = nodes.new("GeometryNodeInputPosition")
    input_position_node.location = (-400, -200)

    separate_xyz_node = nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_node.location = (-200, -100)

    if is_scatter:
        mesh_grid_node = nodes.new("GeometryNodeMeshGrid")
        mesh_grid_node.inputs[0].default_value = 6
        mesh_grid_node.inputs[1].default_value = 6
        mesh_grid_node.inputs[2].default_value = 13
        mesh_grid_node.inputs[3].default_value = 13
        mesh_grid_node.location = (-600, 100)

        mesh_line_node = nodes.new("GeometryNodeMeshLine")
        mesh_line_node.inputs[0].default_value = 13
        mesh_line_node.inputs[3].default_value[2] = 0.5
        mesh_line_node.location = (-600, 380)

        instance_points_scatter_node = nodes.new(
            "GeometryNodeInstanceOnPoints")
        instance_points_scatter_node.location = (-400, 380)

        realize_instances_scatter_node = nodes.new(
            "GeometryNodeRealizeInstances")
        realize_instances_scatter_node.location = (-200, 380)

        icosphere_node = nodes.new("GeometryNodeMeshIcoSphere")
        icosphere_node.inputs[0].default_value = 0.1
        icosphere_node.location = (-200, 280)

        instance_points_scatter_second_node = nodes.new(
            "GeometryNodeInstanceOnPoints")
        instance_points_scatter_second_node.location = (0, 380)

        realize_instances_scatter_second_node = nodes.new(
            "GeometryNodeRealizeInstances")
        realize_instances_scatter_second_node.location = (1800, 0)

    else:
        mesh_grid_node = nodes.new("GeometryNodeMeshGrid")
        mesh_grid_node.inputs[0].default_value = size_x
        mesh_grid_node.inputs[1].default_value = size_y
        mesh_grid_node.inputs[2].default_value = x_dim
        mesh_grid_node.inputs[3].default_value = y_dim
        mesh_grid_node.location = (0, 200)

    if insert_point:
        line_node = nodes.new("GeometryNodeMeshLine")
        line_node.inputs[0].default_value = 1
        line_node.name = "Point Vertex"
        line_node.location = (-200, -250)

        uv_sphere_node = nodes.new("GeometryNodeMeshUVSphere")
        uv_sphere_node.inputs[2].default_value = 0.5
        uv_sphere_node.location = (0, -200)

        set_position_line_node = nodes.new("GeometryNodeSetPosition")
        set_position_line_node.location = (0, -350)

        instance_points_node = nodes.new("GeometryNodeInstanceOnPoints")
        instance_points_node.location = (200, -200)

        subdivision_sphere_node = nodes.new("GeometryNodeSubdivisionSurface")
        subdivision_sphere_node.inputs[1].default_value = 0
        subdivision_sphere_node.name = "Subdivision Point"
        subdivision_sphere_node.location = (400, -200)

        shade_smooth_sphere_node = nodes.new("GeometryNodeSetShadeSmooth")
        shade_smooth_sphere_node.name = "Shade Smooth Point"
        shade_smooth_sphere_node.location = (600, -200)

        join_geometry_node = nodes.new("GeometryNodeJoinGeometry")
        if color_flag:
            if translate_graph:
                join_geometry_node.location = (1800, -100)
            else:
                join_geometry_node.location = (1600, -100)
        else:
            if translate_graph:
                join_geometry_node.location = (1200, -200)
            else:
                join_geometry_node.location = (1000, -100)

    if not is_scatter:
        combine_xyz_node = nodes.new("ShaderNodeCombineXYZ")
        combine_xyz_node.location = (200, 0)

    transform_node = nodes.new("GeometryNodeTransform")
    transform_node.name = "Master_Transform"
    transform_node.location = (200, 380)

    if color_flag:
        attribute_statistic_node = nodes.new("GeometryNodeAttributeStatistic")
        if is_scatter:
            attribute_statistic_node.domain = 'INSTANCE'
        else:
            attribute_statistic_node.domain = 'POINT'
        attribute_statistic_node.location = (400, 200)

        map_range_node = nodes.new("ShaderNodeMapRange")
        map_range_node.clamp = False
        map_range_node.location = (600, 120)

        capture_attribute_node = nodes.new("GeometryNodeCaptureAttribute")
        if is_scatter:
            capture_attribute_node.domain = 'INSTANCE'
        else:
            capture_attribute_node.domain = 'POINT'
        capture_attribute_node.location = (800, 90)

        set_material_node = nodes.new("GeometryNodeSetMaterial")
        if is_scatter:
            set_material_node.location = (1400, 30)
        else:
            set_material_node.location = (1600, 30)

    if not is_scatter:
        set_position_node = nodes.new("GeometryNodeSetPosition")
        if color_flag:
            set_position_node.location = (1000, 100)
        else:
            set_position_node.location = (400, 100)

    subdivision_node = nodes.new("GeometryNodeSubdivisionSurface")
    subdivision_node.inputs[1].default_value = 0
    if color_flag:
        if is_scatter:
            subdivision_node.location = (1000, 80)
        else:
            subdivision_node.location = (1200, 80)
    else:
        subdivision_node.location = (600, 80)

    shade_smooth_node = nodes.new("GeometryNodeSetShadeSmooth")
    shade_smooth_node.inputs[2].default_value = False
    if color_flag:
        if is_scatter:
            shade_smooth_node.location = (1200, 40)
        else:
            shade_smooth_node.location = (1400, 40)
    else:
        shade_smooth_node.location = (800, 40)

    post_transform_node = nodes.new("GeometryNodeTransform")
    post_transform_node.name = "Post_Transform"
    if color_flag:
        node_group.outputs.new('NodeSocketFloat', 'Attribute')
        if insert_point:
            post_transform_node.location = (2000, -100)
        else:
            if is_scatter:
                post_transform_node.location = (1600, 15)
            else:
                post_transform_node.location = (1800, 15)
    else:
        post_transform_node.location = (1000, 0)

    node_group_out = nodes.get('Group Output')
    if color_flag:
        node_group.outputs.new('NodeSocketFloat', 'Attribute')
        if insert_point:
            node_group_out.location = (2200, -100)
        else:
            node_group_out.location = (2000, 15)
    else:
        node_group_out.location = (1200, 0)

    # Instantiate NodeMath objects
    if syms is not None:
        nodemath_syms = instantiate_nodemath(
            syms, node_group, node_group_in, separate_xyz_node)

    # Populate Blender nodes by running NodeMath (x, y, z) through function
    if func is not None:
        out = scalar_check(func(*nodemath_syms), node_group, (0, 0))

    # Link nodes
    if is_scatter:
        node_group.links.new(
            mesh_line_node.outputs['Mesh'], instance_points_scatter_node.inputs['Points'])
        node_group.links.new(
            mesh_grid_node.outputs['Mesh'], instance_points_scatter_node.inputs['Instance'])
        node_group.links.new(
            instance_points_scatter_node.outputs['Instances'], realize_instances_scatter_node.inputs['Geometry'])

        node_group.links.new(
            realize_instances_scatter_node.outputs['Geometry'], instance_points_scatter_second_node.inputs['Points'])
        node_group.links.new(
            icosphere_node.outputs['Mesh'], instance_points_scatter_second_node.inputs['Instance'])

        node_group.links.new(
            instance_points_scatter_second_node.outputs['Instances'], transform_node.inputs['Geometry'])
    else:
        node_group.links.new(
            mesh_grid_node.outputs['Mesh'], transform_node.inputs['Geometry'])

    node_group.links.new(
        input_position_node.outputs['Position'], separate_xyz_node.inputs['Vector'])

    if not is_scatter:
        if func is not None:
            node_group.links.new(
                separate_xyz_node.outputs['X'], combine_xyz_node.inputs['X'])
            node_group.links.new(
                separate_xyz_node.outputs['Y'], combine_xyz_node.inputs['Y'])
            node_group.links.new(out.output, combine_xyz_node.inputs['Z'])

        node_group.links.new(
            combine_xyz_node.outputs['Vector'], set_position_node.inputs['Position'])
        node_group.links.new(
            set_position_node.outputs['Geometry'], subdivision_node.inputs['Mesh'])

    node_group.links.new(
        subdivision_node.outputs['Mesh'], shade_smooth_node.inputs['Geometry'])

    if translate_graph:
        node_group.links.new(
            input_vec_node.outputs['Vector'], transform_node.inputs['Translation'])

    if insert_point:
        node_group.links.new(
            input_vec_node.outputs['Vector'], line_node.inputs[2])

        node_group.links.new(
            line_node.outputs['Mesh'], set_position_line_node.inputs['Geometry'])
        node_group.links.new(
            combine_xyz_node.outputs['Vector'], set_position_line_node.inputs['Position'])
        node_group.links.new(
            set_position_line_node.outputs['Geometry'], instance_points_node.inputs['Points'])

        node_group.links.new(
            uv_sphere_node.outputs['Mesh'], instance_points_node.inputs['Instance'])
        node_group.links.new(
            instance_points_node.outputs['Instances'], subdivision_sphere_node.inputs['Mesh'])
        node_group.links.new(
            subdivision_sphere_node.outputs['Mesh'], shade_smooth_sphere_node.inputs['Geometry'])
        node_group.links.new(
            shade_smooth_sphere_node.outputs['Geometry'], join_geometry_node.inputs['Geometry'])

    if color_flag:
        node_group.links.new(
            transform_node.outputs['Geometry'], attribute_statistic_node.inputs['Geometry'])
        node_group.links.new(
            transform_node.outputs['Geometry'], capture_attribute_node.inputs['Geometry'])

        node_group.links.new(
            out.output, attribute_statistic_node.inputs['Attribute'])
        node_group.links.new(out.output, map_range_node.inputs[0])

        node_group.links.new(
            attribute_statistic_node.outputs['Min'], map_range_node.inputs[1])
        node_group.links.new(
            attribute_statistic_node.outputs['Max'], map_range_node.inputs[2])

        node_group.links.new(
            map_range_node.outputs[0], capture_attribute_node.inputs[2])

        node_group.links.new(
            capture_attribute_node.outputs[2], node_group_out.inputs['Attribute'])

        if is_scatter:
            node_group.links.new(
                capture_attribute_node.outputs['Geometry'], subdivision_node.inputs['Mesh'])
        else:
            node_group.links.new(
                capture_attribute_node.outputs['Geometry'], set_position_node.inputs['Geometry'])

        node_group.links.new(
            shade_smooth_node.outputs['Geometry'], set_material_node.inputs['Geometry'])

        if insert_point:
            node_group.links.new(
                set_material_node.outputs['Geometry'], join_geometry_node.inputs['Geometry'])
            node_group.links.new(
                join_geometry_node.outputs['Geometry'], post_transform_node.inputs['Geometry'])
            node_group.links.new(
                post_transform_node.outputs['Geometry'], node_group_out.inputs['Geometry'])
        else:
            node_group.links.new(
                set_material_node.outputs['Geometry'], post_transform_node.inputs['Geometry'])

            if is_scatter:
                node_group.links.new(
                    post_transform_node.outputs['Geometry'], realize_instances_scatter_second_node.inputs['Geometry'])
                node_group.links.new(
                    realize_instances_scatter_second_node.outputs['Geometry'], node_group_out.inputs['Geometry'])
            else:
                node_group.links.new(
                    post_transform_node.outputs['Geometry'], node_group_out.inputs['Geometry'])

        # Name output attribute
        bpy.context.object.modifiers['GeometryNodes']['Output_2_attribute_name'] = "graph_col"

        # Set up material
        create_material("Graph_Mat", "graph_col", color_min,
                        color_max, set_material_node)

    else:
        node_group.links.new(
            transform_node.outputs['Geometry'], set_position_node.inputs['Geometry'])

        if insert_point:
            node_group.links.new(
                shade_smooth_node.outputs['Geometry'], join_geometry_node.inputs['Geometry'])
            node_group.links.new(
                join_geometry_node.outputs['Geometry'], post_transform_node.inputs['Geometry'])
            node_group.links.new(
                post_transform_node.outputs['Geometry'], node_group_out.inputs['Geometry'])
        else:
            node_group.links.new(
                shade_smooth_node.outputs['Geometry'], post_transform_node.inputs['Geometry'])
            node_group.links.new(
                post_transform_node.outputs['Geometry'], node_group_out.inputs['Geometry'])


def create_vector_field(func, funcX, funcY, funcZ, syms, on_graph=False, join_graph=False, use_length=True, color_flag=True, color_min=None, color_max=None, size_x=0, size_y=0, x_dim=0, y_dim=0):
    """
    Function to create a vector field from v = < P, Q, R > where P, Q, R are functions mapping
    (x, y, z) to their respective outputs. R³ -> R³
    """
    # Get geometry node group from active object
    if not on_graph and (bpy.context.active_object is None or bpy.context.active_object not in bpy.context.selected_objects or bpy.context.active_object.type != 'MESH'):
        # create grid array
        x = np.linspace(-5, 5, 11, dtype=np.float32)
        y = x.copy()
        z = x.copy()
        grid = np.vstack(np.meshgrid(x, y, z)).reshape(3, -1).T

        # Create empty mesh and add vertices
        mesh = bpy.data.meshes.new("vField Graph")
        mesh.vertices.add(grid.shape[0])
        mesh.vertices.foreach_set("co", np.ravel(grid))

        # Create object and link it to scene
        obj = bpy.data.objects.new('vField Graph', mesh)
        bpy.context.collection.objects.link(obj)

        # Set as active object
        bpy.context.view_layer.objects.active = obj

        # Add geometry nodes modifer
        bpy.ops.object.modifier_add(type='NODES')
    elif on_graph:
        # Create object and link it to scene
        mesh = bpy.data.meshes.new("vField Graph")
        obj = bpy.data.objects.new("vField Graph", mesh)
        bpy.context.collection.objects.link(obj)

        # Set as active object
        bpy.context.view_layer.objects.active = obj

        # Add geometry nodes modifier to object
        bpy.ops.object.modifier_add(type='NODES')

    if not bpy.context.active_object.modifiers.get("GeometryNodes"):
        bpy.ops.object.modifier_add(type='NODES')

    node_group = bpy.context.active_object.modifiers.get(
        "GeometryNodes").node_group
    nodes = node_group.nodes

    # Populate, position, and set default values for nodes
    if on_graph:
        separate_xyz_graph_node = nodes.new("ShaderNodeSeparateXYZ")
        separate_xyz_graph_node.location = (-800, 250)

        mesh_grid_node = nodes.new("GeometryNodeMeshGrid")
        mesh_grid_node.inputs[0].default_value = size_x
        mesh_grid_node.inputs[1].default_value = size_y
        mesh_grid_node.inputs[2].default_value = x_dim
        mesh_grid_node.inputs[3].default_value = y_dim
        mesh_grid_node.location = (-800, 450)

        transform_graph_node = nodes.new("GeometryNodeTransform")
        transform_graph_node.name = "Master_Transform"
        transform_graph_node.location = (-600, 600)

        combine_xyz_graph_node = nodes.new("ShaderNodeCombineXYZ")
        combine_xyz_graph_node.location = (-400, 250)

        set_position_graph_node = nodes.new("GeometryNodeSetPosition")
        set_position_graph_node.location = (0, 430)

    node_group_in = nodes.get('Group Input')
    node_group.inputs.new('NodeSocketVectorXYZ', 'Vector Scale')
    node_group_in.location = (-600, 0)

    if use_length:
        separate_xyz_vec_node = nodes.new("ShaderNodeSeparateXYZ")
        separate_xyz_vec_node.location = (-400, 0)

    input_position_node = nodes.new("GeometryNodeInputPosition")
    if on_graph:
        input_position_node.location = (-1000, -50)
    else:
        input_position_node.location = (-400, -50)

    separate_xyz_node = nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_node.location = (-200, 0)

    combine_xyz_node = nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_node.location = (200, 0)

    transform_node = nodes.new("GeometryNodeTransform")
    if join_graph or on_graph:
        transform_node.name = "Secondary_Transform"
    else:
        transform_node.name = "Master_Transform"
    transform_node.location = (200, 380)

    val_node = nodes.new("ShaderNodeValue")
    val_node.outputs[0].default_value = .2
    val_node.location = (200, -200)

    cylinder_node = nodes.new("GeometryNodeMeshCylinder")
    cylinder_node.inputs[3].default_value = .015
    cylinder_node.inputs[4].default_value = .18
    cylinder_node.location = (400, 90)

    cone_node = nodes.new("GeometryNodeMeshCone")
    cone_node.inputs[4].default_value = .035
    cone_node.inputs[5].default_value = .07
    cone_node.location = (400, 400)

    mul_cylinder_node = nodes.new("ShaderNodeMath")
    mul_cylinder_node.operation = 'MULTIPLY'
    mul_cylinder_node.location = (400, -200)

    combine_xyz_cone_node = nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_cone_node.location = (400, -380)

    combine_xyz_cylinder_node = nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_cylinder_node.location = (600, -200)

    transform_cylinder_node = nodes.new("GeometryNodeTransform")
    transform_cylinder_node.location = (600, 300)

    transform_cone_node = nodes.new("GeometryNodeTransform")
    transform_cone_node.location = (600, 600)

    align_euler_to_vec_node = nodes.new("FunctionNodeAlignEulerToVector")
    align_euler_to_vec_node.axis = 'Z'
    align_euler_to_vec_node.location = (600, 0)

    join_geometry_node = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_node.location = (800, 320)

    instance_points_node = nodes.new("GeometryNodeInstanceOnPoints")
    instance_points_node.location = (1000, 100)

    if use_length or color_flag:
        length_vector_node = nodes.new("ShaderNodeVectorMath")
        length_vector_node.operation = 'LENGTH'
        length_vector_node.location = (800, -150)

    if use_length:
        mul_node = nodes.new("ShaderNodeMath")
        mul_node.operation = 'MULTIPLY'
        mul_node.inputs[1].default_value = 0.5
        mul_node.location = (800, 40)

        combine_xyz_length_node = nodes.new("ShaderNodeCombineXYZ")
        combine_xyz_length_node.inputs[0].default_value = 1
        combine_xyz_length_node.inputs[1].default_value = 1
        combine_xyz_length_node.location = (800, 200)

    if color_flag:
        attribute_statistic_graph_node = nodes.new(
            "GeometryNodeAttributeStatistic")
        attribute_statistic_graph_node.domain = 'POINT'
        attribute_statistic_graph_node.location = (-400, 600)

        map_range_graph_node = nodes.new("ShaderNodeMapRange")
        map_range_graph_node.clamp = False
        map_range_graph_node.location = (-200, 580)

        capture_attribute_graph_node = nodes.new(
            "GeometryNodeCaptureAttribute")
        capture_attribute_graph_node.domain = 'POINT'
        capture_attribute_graph_node.location = (-200, 300)

        set_material_graph_node = nodes.new("GeometryNodeSetMaterial")
        set_material_graph_node.location = (000, 580)

        map_range_node = nodes.new("ShaderNodeMapRange")
        map_range_node.clamp = False
        map_range_node.location = (1200, -100)

        attribute_statistic_node = nodes.new("GeometryNodeAttributeStatistic")
        attribute_statistic_node.domain = 'INSTANCE'
        attribute_statistic_node.location = (1200, 250)

        capture_attribute_node = nodes.new("GeometryNodeCaptureAttribute")
        capture_attribute_node.domain = 'INSTANCE'
        capture_attribute_node.location = (1400, 0)

        set_material_node = nodes.new("GeometryNodeSetMaterial")
        set_material_node.location = (2000, 0)

        realize_instances_node = nodes.new("GeometryNodeRealizeInstances")
        realize_instances_node.location = (2200, 0)

    subdivision_node = nodes.new("GeometryNodeSubdivisionSurface")
    subdivision_node.inputs[1].default_value = 0
    if color_flag:
        subdivision_node.location = (1600, 0)
    else:
        subdivision_node.location = (1400, 0)

    shade_smooth_node = nodes.new("GeometryNodeSetShadeSmooth")
    shade_smooth_node.inputs[2].default_value = False
    if color_flag:
        shade_smooth_node.location = (1800, 0)
    else:
        shade_smooth_node.location = (1600, 0)

    if join_graph and on_graph:
        join_graph_geometry_node = nodes.new("GeometryNodeJoinGeometry")
        if color_flag:
            join_graph_geometry_node.location = (2400, 0)
        else:
            join_graph_geometry_node.location = (1800, 0)

    post_transform_node = nodes.new("GeometryNodeTransform")
    post_transform_node.name = "Post_Transform"
    if color_flag:
        if join_graph and on_graph:
            post_transform_node.location = (2600, 0)
        else:
            post_transform_node.location = (2400, 0)
    else:
        if join_graph and on_graph:
            post_transform_node.location = (2000, 0)
        else:
            post_transform_node.location = (1800, 0)

    node_group_out = nodes.get('Group Output')
    if color_flag:
        node_group.outputs.new('NodeSocketFloat', 'Attribute_field')
        node_group.outputs.new('NodeSocketFloat', 'Attribute_graph')
        if join_graph and on_graph:
            node_group_out.location = (2800, 0)
        else:
            node_group_out.location = (2600, 0)
    else:
        if join_graph and on_graph:
            node_group_out.location = (2200, 0)
        else:
            node_group_out.location = (2000, 0)

    # Instantiate NodeMath objects
    nodemath_syms = instantiate_nodemath(
        syms, node_group, node_group_in, separate_xyz_node, 0, 200)

    # Populate and offset Blender nodes for Fx
    outX = scalar_check(funcX(*nodemath_syms), node_group, (0, 200))

    # Populate and offset Blender nodes for Fy
    for sym in nodemath_syms:
        sym.offset_y = 0
    outY = scalar_check(funcY(*nodemath_syms), node_group, (0, 0))

    # Populate and offset Blender nodes for Fz
    for sym in nodemath_syms:
        sym.offset_y = -200
    outZ = scalar_check(funcZ(*nodemath_syms), node_group, (0, -200))

    if on_graph:
        # Instantiate NodeMath objects
        for i, sym in enumerate(nodemath_syms):
            if sym.output == separate_xyz_node.outputs['X']:
                nodemath_syms[i] = NodeMath(
                    separate_xyz_graph_node.outputs['X'], node_group)
            elif sym.output == separate_xyz_node.outputs['Y']:
                nodemath_syms[i] = NodeMath(
                    separate_xyz_graph_node.outputs['Y'], node_group)
            elif sym.output == separate_xyz_node.outputs['Z']:
                nodemath_syms[i] = NodeMath(
                    separate_xyz_graph_node.outputs['Z'], node_group)

        for sym in nodemath_syms:
            sym.offset_y = -600
            sym.offset_y = 250

        # Populate and offset Blender nodes for F
        out = scalar_check(func(*nodemath_syms), node_group, (-600, 250))

    # Link nodes
    node_group.links.new(
        input_position_node.outputs['Position'], separate_xyz_node.inputs['Vector'])

    if on_graph:
        node_group.links.new(
            input_position_node.outputs['Position'], separate_xyz_graph_node.inputs['Vector'])

        node_group.links.new(
            separate_xyz_graph_node.outputs['X'], combine_xyz_graph_node.inputs['X'])
        node_group.links.new(
            separate_xyz_graph_node.outputs['Y'], combine_xyz_graph_node.inputs['Y'])
        node_group.links.new(out.output, combine_xyz_graph_node.inputs['Z'])

        node_group.links.new(
            mesh_grid_node.outputs['Mesh'], transform_graph_node.inputs['Geometry'])
        node_group.links.new(
            transform_graph_node.outputs['Geometry'], attribute_statistic_graph_node.inputs['Geometry'])
        node_group.links.new(
            out.output, attribute_statistic_graph_node.inputs['Attribute'])

        node_group.links.new(
            length_vector_node.outputs['Value'], map_range_node.inputs[0])

        node_group.links.new(
            out.output, map_range_graph_node.inputs[0])
        node_group.links.new(
            attribute_statistic_graph_node.outputs['Min'], map_range_graph_node.inputs[1])
        node_group.links.new(
            attribute_statistic_graph_node.outputs['Max'], map_range_graph_node.inputs[2])

        node_group.links.new(
            transform_graph_node.outputs['Geometry'], capture_attribute_graph_node.inputs['Geometry'])
        node_group.links.new(
            map_range_graph_node.outputs[0], capture_attribute_graph_node.inputs[2])

        node_group.links.new(
            capture_attribute_graph_node.outputs[2], node_group_out.inputs['Attribute_graph'])

        node_group.links.new(
            capture_attribute_graph_node.outputs['Geometry'], set_material_graph_node.inputs['Geometry'])

        node_group.links.new(
            capture_attribute_graph_node.outputs['Geometry'], set_material_graph_node.inputs['Geometry'])
        node_group.links.new(
            set_material_graph_node.outputs['Geometry'], set_position_graph_node.inputs['Geometry'])

        node_group.links.new(
            combine_xyz_graph_node.outputs['Vector'], set_position_graph_node.inputs['Position'])

        node_group.links.new(
            set_position_graph_node.outputs['Geometry'], transform_node.inputs['Geometry'])

    else:
        node_group.links.new(
            node_group_in.outputs['Geometry'], transform_node.inputs['Geometry'])

    node_group.links.new(outX.output, combine_xyz_node.inputs['X'])
    node_group.links.new(outY.output, combine_xyz_node.inputs['Y'])
    node_group.links.new(outZ.output, combine_xyz_node.inputs['Z'])

    node_group.links.new(
        combine_xyz_node.outputs['Vector'], align_euler_to_vec_node.inputs['Vector'])

    node_group.links.new(
        val_node.outputs['Value'], cylinder_node.inputs['Depth'])
    node_group.links.new(
        val_node.outputs['Value'], mul_cylinder_node.inputs[0])
    node_group.links.new(
        val_node.outputs['Value'], combine_xyz_cone_node.inputs['Z'])

    node_group.links.new(
        mul_cylinder_node.outputs['Value'], combine_xyz_cylinder_node.inputs['Z'])

    node_group.links.new(
        combine_xyz_cone_node.outputs['Vector'], transform_cone_node.inputs['Translation'])
    node_group.links.new(
        combine_xyz_cylinder_node.outputs['Vector'], transform_cylinder_node.inputs['Translation'])

    node_group.links.new(
        transform_node.outputs['Geometry'], instance_points_node.inputs['Points'])
    node_group.links.new(
        align_euler_to_vec_node.outputs['Rotation'], instance_points_node.inputs['Rotation'])

    node_group.links.new(
        cylinder_node.outputs['Mesh'], transform_cylinder_node.inputs['Geometry'])
    node_group.links.new(
        cone_node.outputs['Mesh'], transform_cone_node.inputs['Geometry'])

    node_group.links.new(
        transform_cylinder_node.outputs['Geometry'], join_geometry_node.inputs['Geometry'])
    node_group.links.new(
        transform_cone_node.outputs['Geometry'], join_geometry_node.inputs['Geometry'])

    node_group.links.new(
        join_geometry_node.outputs['Geometry'], instance_points_node.inputs['Instance'])

    if use_length:
        node_group.links.new(
            node_group_in.outputs['Vector Scale'], separate_xyz_vec_node.inputs['Vector'])

        node_group.links.new(
            length_vector_node.outputs['Value'], mul_node.inputs[0])
        node_group.links.new(
            separate_xyz_vec_node.outputs['Z'], mul_node.inputs[1])

        node_group.links.new(
            separate_xyz_vec_node.outputs['X'], combine_xyz_length_node.inputs['X'])
        node_group.links.new(
            separate_xyz_vec_node.outputs['Y'], combine_xyz_length_node.inputs['Y'])
        node_group.links.new(
            mul_node.outputs['Value'], combine_xyz_length_node.inputs['Z'])

        node_group.links.new(
            combine_xyz_length_node.outputs['Vector'], instance_points_node.inputs['Scale'])

    else:
        node_group.links.new(
            node_group_in.outputs['Vector Scale'], instance_points_node.inputs['Scale'])

    if color_flag or use_length:
        node_group.links.new(
            combine_xyz_node.outputs['Vector'], length_vector_node.inputs['Vector'])

    if color_flag:
        node_group.links.new(
            instance_points_node.outputs['Instances'], attribute_statistic_node.inputs['Geometry'])
        node_group.links.new(
            instance_points_node.outputs['Instances'], capture_attribute_node.inputs['Geometry'])

        node_group.links.new(
            length_vector_node.outputs['Value'], map_range_node.inputs[0])
        node_group.links.new(
            length_vector_node.outputs['Value'], attribute_statistic_node.inputs['Attribute'])

        node_group.links.new(
            attribute_statistic_node.outputs['Min'], map_range_node.inputs[1])
        node_group.links.new(
            attribute_statistic_node.outputs['Max'], map_range_node.inputs[2])

        node_group.links.new(
            map_range_node.outputs[0], capture_attribute_node.inputs[2])

        node_group.links.new(
            capture_attribute_node.outputs[2], node_group_out.inputs['Attribute_field'])
        node_group.links.new(
            capture_attribute_node.outputs['Geometry'], subdivision_node.inputs['Mesh'])

        node_group.links.new(
            subdivision_node.outputs['Mesh'], shade_smooth_node.inputs['Geometry'])
        node_group.links.new(
            shade_smooth_node.outputs['Geometry'], set_material_node.inputs['Geometry'])
        node_group.links.new(
            set_material_node.outputs['Geometry'], realize_instances_node.inputs['Geometry'])

        if join_graph and on_graph:
            node_group.links.new(
                realize_instances_node.outputs['Geometry'], join_graph_geometry_node.inputs['Geometry'])
            node_group.links.new(
                set_position_graph_node.outputs['Geometry'], join_graph_geometry_node.inputs['Geometry'])
            node_group.links.new(
                join_graph_geometry_node.outputs['Geometry'], post_transform_node.inputs['Geometry'])
            node_group.links.new(
                post_transform_node.outputs['Geometry'], node_group_out.inputs['Geometry'])
        else:
            node_group.links.new(
                realize_instances_node.outputs['Geometry'], post_transform_node.inputs['Geometry'])
            node_group.links.new(
                post_transform_node.outputs['Geometry'], node_group_out.inputs['Geometry'])

        # Name output attributes
        bpy.context.object.modifiers['GeometryNodes']['Output_3_attribute_name'] = "vfield_col"
        bpy.context.object.modifiers['GeometryNodes']['Output_4_attribute_name'] = "graph_col"

        # Set up materials
        create_material("vField_Mat", "vfield_col", color_min,
                        color_max, set_material_node)
        create_material("Graph_Mat", "graph_col", color_min,
                        color_max, set_material_graph_node)

    else:
        node_group.links.new(
            instance_points_node.outputs['Instances'], subdivision_node.inputs['Mesh'])
        node_group.links.new(
            subdivision_node.outputs['Mesh'], shade_smooth_node.inputs['Geometry'])

        if join_graph and on_graph:
            node_group.links.new(
                shade_smooth_node.outputs['Geometry'], join_graph_geometry_node.inputs['Geometry'])
            node_group.links.new(
                set_position_graph_node.outputs['Geometry'], join_graph_geometry_node.inputs['Geometry'])
            node_group.links.new(
                join_graph_geometry_node.outputs['Geometry'], post_transform_node.inputs['Geometry'])
            node_group.links.new(
                post_transform_node.outputs['Geometry'], node_group_out.inputs['Geometry'])
        else:
            node_group.links.new(
                shade_smooth_node.outputs['Geometry'], post_transform_node.inputs['Geometry'])
            node_group.links.new(
                post_transform_node.outputs['Geometry'], node_group_out.inputs['Geometry'])

    # Set default inputs
    bpy.context.object.modifiers['GeometryNodes']['Input_2'][0] = 1.0
    bpy.context.object.modifiers['GeometryNodes']['Input_2'][1] = 1.0
    bpy.context.object.modifiers['GeometryNodes']['Input_2'][2] = 1.0


def create_vector_stream(func, funcX, funcY, funcZ, dt=0.1, steps=50, color_flag=True, color_min=None, color_max=None, limit=1000, gradient=False):
    """
    Function to create a vector stream from v = < P, Q, R > where P, Q, R are functions mapping
    (x, y, z) to their respective outputs. R³ -> R³
    """
    # Get active object
    context = bpy.context

    # Get geometry node group from active object
    if bpy.context.active_object is None or bpy.context.active_object not in bpy.context.selected_objects or bpy.context.active_object.type != 'MESH':  # and bpy.context.active_object.type == 'MESH'
        # create grid array
        x = np.linspace(-2, 2, 5, dtype=np.float32)
        y = x.copy()
        z = x.copy()
        grid = np.vstack(np.meshgrid(x, y, z)).reshape(3, -1).T

        # Create empty mesh and add vertices
        mesh = bpy.data.meshes.new("vStream Graph")
        mesh.vertices.add(grid.shape[0])
        mesh.vertices.foreach_set("co", np.ravel(grid))

        # Create object and link it to scene
        obj = bpy.data.objects.new('vStream Graph', mesh)
        bpy.context.collection.objects.link(obj)

        # Set as active object
        bpy.context.view_layer.objects.active = obj

    bpy.ops.object.mode_set(mode='OBJECT')
    mesh = context.view_layer.objects.active.data
    nverts = len(mesh.vertices)

    # Get vertex array from mesh
    verts = np.empty(nverts*3, dtype=np.float32)
    mesh.vertices.foreach_get('co', verts)

    # Collect list of return vectors
    verts_out = []
    if color_flag:
        # Collect list of magnitude vectors
        color_fac = []
    for point in verts.reshape(-1, 3):
        points = [point]

        for _ in range(steps-1):
            prev = points[-1]
            func_eval = np.array([funcX(*prev), funcY(*prev), funcZ(*prev)])
            if color_flag:
                color_fac.append(func_eval)
            if gradient == 'ascent':
                point_eval = prev + dt * func_eval
                point_eval[2] = func(*(point_eval))
                points.append(point_eval)
            elif gradient == 'descent':
                point_eval = prev - dt * func_eval
                point_eval[2] = func(*(point_eval))
                points.append(point_eval)
            else:
                points.append(prev + dt * func_eval)

        if color_flag:
            color_fac.append(
                np.array([funcX(*points[-1]), funcY(*points[-1]), funcZ(*points[-1])]))
        verts_out.append(points)

    # Convert verts and color_fac lists into numpy arrays and reshape to (-1, 3)
    verts = np.asarray(verts_out, dtype=np.float32).reshape(-1, 3)
    color_fac = np.asarray(color_fac, dtype=np.float32).reshape(-1, 3)

    # Handle overflow and division by zero
    np.nan_to_num(verts, copy=False)
    np.clip(verts, -limit, limit, verts)
    np.nan_to_num(color_fac, copy=False)
    np.clip(color_fac, -limit, limit, color_fac)

    if color_flag:
        # Get magnitude of vectors and then min-max scale
        # to the range 0-1 to encode magnitude in to color
        norms = np.linalg.norm(color_fac, axis=1)
        min = np.min(norms)
        max = np.max(norms)
        norms = (norms - min)/(max - min)

    # Split verts and norms array and then set in to a bezier spline
    bpy.ops.object.select_all(action='DESELECT')
    for i in range(nverts):
        cu = bpy.data.curves.new(name="poly", type="CURVE")
        cu.dimensions = '3D'

        spline = cu.splines.new('BEZIER')
        spline.bezier_points.add(steps - 1)
        spline.bezier_points.foreach_set(
            "co", np.ravel(verts[i*steps:(i+1)*steps, ]))

        if color_flag:
            spline.bezier_points.foreach_set(
                "radius", np.ravel(norms[i*steps:(i+1)*steps, ]))

        if i == nverts-1:
            obj = bpy.data.objects.new(f"vStream Graph", cu)
        else:
            obj = bpy.data.objects.new(f"vStream_{i}", cu)
        context.collection.objects.link(obj)

        # Select spline
        obj.select_set(True)

    # Join all spline in to one object
    context.view_layer.objects.active = obj
    bpy.ops.object.join()

    # Set all spline handles to 'AUTOMATIC'
    bpy.ops.object.editmode_toggle()
    bpy.ops.curve.select_all(action='SELECT')
    bpy.ops.curve.handle_type_set(type='AUTOMATIC')
    bpy.ops.object.editmode_toggle()

    # Add geometry nodes modifier to spline object
    bpy.ops.object.modifier_add(type='NODES')

    # Get geometry node group
    node_group = bpy.context.active_object.modifiers.get(
        "GeometryNodes").node_group
    nodes = node_group.nodes

    # Populate, position, and set default values for nodes
    node_group_in = nodes.get('Group Input')
    node_group.inputs.new('NodeSocketFloat', 'Start')
    node_group.inputs.new('NodeSocketFloat', 'End')
    if color_flag:
        node_group_in.location = (-600, 0)
    else:
        node_group_in.location = (-400, 0)

    if color_flag:
        radius_node = nodes.new("GeometryNodeInputRadius")
        radius_node.location = (-600, -150)

        capture_attribute_node = nodes.new("GeometryNodeCaptureAttribute")
        capture_attribute_node.domain = 'POINT'
        capture_attribute_node.location = (-400, 0)

        set_material_node = nodes.new("GeometryNodeSetMaterial")
        set_material_node.location = (600, 0)

    set_radius_node = nodes.new("GeometryNodeSetCurveRadius")
    set_radius_node.inputs[2].default_value = 0.2
    set_radius_node.location = (-200, -30)

    resample_curve_node = nodes.new("GeometryNodeResampleCurve")
    resample_curve_node.inputs[2].default_value = steps
    resample_curve_node.location = (0, 0)

    circle_curve_node = nodes.new("GeometryNodeCurvePrimitiveCircle")
    circle_curve_node.inputs[0].default_value = 8
    circle_curve_node.inputs[4].default_value = 0.2
    circle_curve_node.location = (200, -180)

    trim_curve_node = nodes.new("GeometryNodeTrimCurve")
    trim_curve_node.location = (200, 0)

    curve_to_mesh_node = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_node.location = (400, 0)

    node_group_out = nodes.get('Group Output')
    if color_flag:
        node_group.outputs.new('NodeSocketFloat', 'Attribute')
        node_group_out.location = (800, 0)
    else:
        node_group_out.location = (600, 0)

    # Link nodes
    node_group.links.new(
        set_radius_node.outputs['Curve'], resample_curve_node.inputs['Curve'])
    node_group.links.new(
        resample_curve_node.outputs['Curve'], trim_curve_node.inputs['Curve'])

    node_group.links.new(
        trim_curve_node.outputs['Curve'], curve_to_mesh_node.inputs['Curve'])
    node_group.links.new(
        circle_curve_node.outputs['Curve'], curve_to_mesh_node.inputs['Profile Curve'])

    node_group.links.new(
        node_group_in.outputs['Start'], trim_curve_node.inputs['Start'])
    node_group.links.new(
        node_group_in.outputs['End'], trim_curve_node.inputs['End'])

    if color_flag:
        node_group.links.new(
            node_group_in.outputs['Geometry'], capture_attribute_node.inputs['Geometry'])
        node_group.links.new(
            radius_node.outputs['Radius'], capture_attribute_node.inputs[2])

        node_group.links.new(
            capture_attribute_node.outputs['Geometry'], set_radius_node.inputs['Curve'])

        node_group.links.new(
            capture_attribute_node.outputs[2], node_group_out.inputs['Attribute'])

        node_group.links.new(
            curve_to_mesh_node.outputs['Mesh'], set_material_node.inputs['Geometry'])
        node_group.links.new(
            set_material_node.outputs['Geometry'], node_group_out.inputs['Geometry'])

        # Name output attribute
        context.object.modifiers['GeometryNodes']['Output_4_attribute_name'] = "stream_col"

        # Set up material
        create_material("Stream_Mat", "stream_col", color_min,
                        color_max, set_material_node)

    else:
        node_group.links.new(
            node_group_in.outputs['Geometry'], set_radius_node.inputs['Curve'])
        node_group.links.new(
            curve_to_mesh_node.outputs['Mesh'], node_group_out.inputs['Geometry'])

    # Set input (trim curve end) to 1.00
    context.object.modifiers['GeometryNodes']['Input_3'] = 1.00


def create_contour(func, syms, size_x, size_y, x_dim, y_dim, color_min, color_max):
    """
    Function to create a contour plot of an up to three variable function with
    a scalar output. F(x, y, z) -> R
    Leave out variable(s) from equation to graph lower dimensional functions
    """
    # Create boolean object and link it to scene
    mesh = bpy.data.meshes.new("Contour Boolean Graph")
    boolean_obj = bpy.data.objects.new("Contour Boolean Graph", mesh)
    bpy.context.collection.objects.link(boolean_obj)

    # Set as active object
    bpy.context.view_layer.objects.active = boolean_obj

    # Add geometry nodes modifier to object
    bpy.ops.object.modifier_add(type='NODES')

    # Get geometry node group from active object
    node_group = boolean_obj.modifiers.get("GeometryNodes").node_group
    nodes = node_group.nodes

    # populate, position, and set default values for nodes
    mesh_line_node = nodes.new("GeometryNodeMeshLine")
    mesh_line_node.mode = 'END_POINTS'
    # set up drivers
    target = bpy.data.window_managers["WinMan"]
    prop = 'default_value'
    source = mesh_line_node.inputs[0]
    name = 'line_count'
    dataPath = 'line_count'
    d_type = 'AVERAGE'
    add_driver(source, target, prop, name, dataPath, -
               1, '', 'WINDOWMANAGER', d_type)
    source = mesh_line_node.inputs[2]
    name = 'start_z'
    dataPath = 'start_z'
    add_driver(source, target, prop, name, dataPath,
               2, '', 'WINDOWMANAGER', d_type)
    source = mesh_line_node.inputs[3]
    name = 'end_z'
    dataPath = 'end_z'
    add_driver(source, target, prop, name, dataPath,
               2, '', 'WINDOWMANAGER', d_type)
    mesh_line_node.location = (-200, -200)

    mesh_grid_node = nodes.new("GeometryNodeMeshGrid")
    mesh_grid_node.inputs[2].default_value = 2
    mesh_grid_node.inputs[3].default_value = 2
    mesh_grid_node.location = (-200, 0)

    instance_points_node = nodes.new("GeometryNodeInstanceOnPoints")
    instance_points_node.location = (0, 0)

    realize_instances_node = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_node.location = (200, 0)

    node_group_out = nodes.get('Group Output')
    node_group_out.location = (400, 0)

    # Link nodes
    node_group.links.new(
        mesh_grid_node.outputs['Mesh'], instance_points_node.inputs['Instance'])
    node_group.links.new(
        mesh_line_node.outputs['Mesh'], instance_points_node.inputs['Points'])

    node_group.links.new(
        instance_points_node.outputs['Instances'], realize_instances_node.inputs['Geometry'])

    node_group.links.new(
        realize_instances_node.outputs['Geometry'], node_group_out.inputs['Geometry'])

    # Add solidify modifier with 0.001m thickness to prevent boolean issues
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.active_object.modifiers.get("Solidify").thickness = 0.001

    # Create graph object and link it to scene
    create_graph("Contour Function Graph", func, syms, size_x, size_y, x_dim, y_dim,
                 False, False, False, True, color_min, color_max, 0, 0, 0, '')
    graph_obj = bpy.context.active_object

    # Get geometry node group from active object
    node_group = graph_obj.modifiers.get("GeometryNodes").node_group
    nodes = node_group.nodes

    # Retrieve existing nodes that need updated links by name
    attribute_statistic_graph_node = node_search(nodes, 'Attribute Statistic')
    map_range_graph_node = node_search(nodes, 'Map Range')
    set_material_graph_node = node_search(nodes, 'Set Material')
    node_group_out_graph = node_search(nodes, 'Group Output')
    node_group_out_graph.location = (2000, 15)

    # Populate, position, and set default values for nodes
    compare_min_graph_node = nodes.new("FunctionNodeCompare")
    compare_min_graph_node.operation = 'LESS_EQUAL'
    # set up drivers
    source = compare_min_graph_node.inputs[0]
    name = 'start_z'
    dataPath = 'start_z'
    add_driver(source, target, prop, name, dataPath, -
               1, '', 'WINDOWMANAGER', d_type)
    compare_min_graph_node.location = (400, -100)

    compare_max_graph_node = nodes.new("FunctionNodeCompare")
    compare_max_graph_node.operation = 'GREATER_EQUAL'
    # set up drivers
    source = compare_max_graph_node.inputs[0]
    name = 'end_z'
    dataPath = 'end_z'
    add_driver(source, target, prop, name, dataPath, -
               1, '', 'WINDOWMANAGER', d_type)
    compare_max_graph_node.location = (400, 0)

    switch_min_graph_node = nodes.new("GeometryNodeSwitch")
    switch_min_graph_node.input_type = 'FLOAT'
    # set up drivers
    source = switch_min_graph_node.inputs[2]
    name = 'start_z'
    dataPath = 'start_z'
    add_driver(source, target, prop, name, dataPath, -
               1, '', 'WINDOWMANAGER', d_type)
    switch_min_graph_node.location = (600, -100)

    switch_max_graph_node = nodes.new("GeometryNodeSwitch")
    switch_max_graph_node.input_type = 'FLOAT'
    # set up drivers
    source = switch_max_graph_node.inputs[2]
    name = 'end_z'
    dataPath = 'end_z'
    add_driver(source, target, prop, name, dataPath, -
               1, '', 'WINDOWMANAGER', d_type)
    switch_max_graph_node.location = (600, 0)

    transform_graph_node = nodes.new("GeometryNodeTransform")
    # set up drivers
    source = transform_graph_node.inputs[3]
    name = 'scale_z'
    dataPath = 'scale_z'
    add_driver(source, target, prop, name, dataPath,
               2, '', 'WINDOWMANAGER', d_type)
    transform_graph_node.location = (1800, 0)

    # Link nodes
    node_group.links.new(
        attribute_statistic_graph_node.outputs['Min'], compare_min_graph_node.inputs[1])
    node_group.links.new(
        attribute_statistic_graph_node.outputs['Max'], compare_max_graph_node.inputs[1])

    node_group.links.new(
        compare_min_graph_node.outputs[0], switch_min_graph_node.inputs[0])
    node_group.links.new(
        attribute_statistic_graph_node.outputs['Min'], switch_min_graph_node.inputs[3])

    node_group.links.new(
        compare_max_graph_node.outputs[0], switch_max_graph_node.inputs[0])
    node_group.links.new(
        attribute_statistic_graph_node.outputs['Max'], switch_max_graph_node.inputs[3])

    node_group.links.new(
        switch_min_graph_node.outputs[0], map_range_graph_node.inputs[1])
    node_group.links.new(
        switch_max_graph_node.outputs[0], map_range_graph_node.inputs[2])

    node_group.links.new(
        set_material_graph_node.outputs['Geometry'], transform_graph_node.inputs['Geometry'])

    node_group.links.new(
        transform_graph_node.outputs['Geometry'], node_group_out_graph.inputs['Geometry'])

    # Create plot object and link it to scene
    create_graph("Contour Graph", func, syms, size_x, size_y, x_dim, y_dim, False, False,
                 False, False, color_min, color_max, 0, 0, 0, '')
    contour_obj = bpy.context.active_object

    # Set up drivers
    graph_obj_geo_mod = graph_obj.modifiers.get("GeometryNodes")
    graph_obj_geo_node_group = graph_obj_geo_mod.node_group
    graph_nodes = graph_obj_geo_node_group.nodes
    contour_obj_geo_mod = contour_obj.modifiers.get("GeometryNodes")
    contour_obj_geo_node_group = contour_obj_geo_mod.node_group
    contour_nodes = contour_obj_geo_node_group.nodes
    boolean_obj_geo_mod = boolean_obj.modifiers.get("GeometryNodes")
    boolean_obj_geo_node_group = boolean_obj_geo_mod.node_group
    boolean_nodes = boolean_obj_geo_node_group.nodes

    for contour_input in contour_obj_geo_node_group.inputs:
        if contour_input.name.endswith('variable'):
            for graph_input in graph_obj_geo_node_group.inputs:
                if contour_input.name == graph_input.name:
                    source = graph_obj_geo_mod
                    target = contour_obj
                    prop = f'["{graph_input.identifier}"]'
                    name = contour_input.identifier
                    dataPath = f'modifiers["GeometryNodes"]["{contour_input.identifier}"]'
                    index = -1
                    #func = contour_input.identifier
                    id_type = 'OBJECT'
                    d_type = 'AVERAGE'
                    add_driver(source, target, prop, name,
                               dataPath, index, '', id_type, d_type)
                    continue

    graph_master_transform_node = node_search(graph_nodes, 'Master_Transform')
    graph_secondary_transform_node = node_search(
        graph_nodes, 'Secondary_Transform')

    target = contour_obj_geo_node_group
    prop = 'default_value'
    source = graph_master_transform_node.inputs[1]
    name = 'translation_x'
    dataPath = 'nodes["Master_Transform"].inputs[1].default_value[0]'
    d_type = 'AVERAGE'
    id_type = 'NODETREE'
    add_driver(source, target, prop, name, dataPath, 0, '', id_type, d_type)
    name = 'translation_y'
    dataPath = 'nodes["Master_Transform"].inputs[1].default_value[1]'
    add_driver(source, target, prop, name, dataPath, 1, '', id_type, d_type)
    name = 'translation_z'
    dataPath = 'nodes["Master_Transform"].inputs[1].default_value[2]'
    add_driver(source, target, prop, name, dataPath, 2, '', id_type, d_type)

    source = graph_master_transform_node.inputs[2]
    name = 'rotation_x'
    dataPath = 'nodes["Master_Transform"].inputs[2].default_value[0]'
    add_driver(source, target, prop, name, dataPath, 0, '', id_type, d_type)
    name = 'rotation_y'
    dataPath = 'nodes["Master_Transform"].inputs[2].default_value[1]'
    add_driver(source, target, prop, name, dataPath, 1, '', id_type, d_type)
    name = 'rotation_z'
    dataPath = 'nodes["Master_Transform"].inputs[2].default_value[2]'
    add_driver(source, target, prop, name, dataPath, 2, '', id_type, d_type)

    source = graph_master_transform_node.inputs[3]
    name = 'scale_x'
    dataPath = 'nodes["Master_Transform"].inputs[3].default_value[0]'
    add_driver(source, target, prop, name, dataPath, 0, '', id_type, d_type)
    name = 'scale_y'
    dataPath = 'nodes["Master_Transform"].inputs[3].default_value[1]'
    add_driver(source, target, prop, name, dataPath, 1, '', id_type, d_type)
    name = 'scale_z'
    dataPath = 'nodes["Master_Transform"].inputs[3].default_value[2]'
    add_driver(source, target, prop, name, dataPath, 2, '', id_type, d_type)

    graph_grid_node = node_search(graph_nodes, 'Grid')

    source = graph_grid_node.inputs[0]
    name = 'size_x'
    dataPath = 'nodes["Grid"].inputs[0].default_value'
    add_driver(source, target, prop, name, dataPath, -1, '', id_type, d_type)
    source = graph_grid_node.inputs[1]
    name = 'size_y'
    dataPath = 'nodes["Grid"].inputs[1].default_value'
    add_driver(source, target, prop, name, dataPath, -1, '', id_type, d_type)
    source = graph_grid_node.inputs[2]
    name = 'x_dim'
    dataPath = 'nodes["Grid"].inputs[2].default_value'
    add_driver(source, target, prop, name, dataPath, -1, '', id_type, d_type)
    source = graph_grid_node.inputs[3]
    name = 'y_dim'
    dataPath = 'nodes["Grid"].inputs[3].default_value'
    add_driver(source, target, prop, name, dataPath, -1, '', id_type, d_type)

    boolean_grid_node = node_search(boolean_nodes, 'Grid')

    target1 = contour_obj_geo_node_group
    target2 = bpy.data.window_managers["WinMan"]
    source = boolean_grid_node.inputs[0]
    name1 = 'size_x'
    name2 = 'bool_x'
    dataPath1 = 'nodes["Grid"].inputs[0].default_value'
    dataPath2 = 'bool_x'
    function = 'size_x + bool_x'
    id_type2 = 'WINDOWMANAGER'
    add_driver(source, [target1, target2], prop, [name1, name2], [
               dataPath1, dataPath2], -1, function, [id_type, id_type2])
    source = boolean_grid_node.inputs[1]
    name1 = 'size_y'
    name2 = 'bool_y'
    dataPath1 = 'nodes["Grid"].inputs[1].default_value'
    dataPath2 = 'bool_y'
    function = 'size_y + bool_y'
    add_driver(source, [target1, target2], prop, [name1, name2], [
               dataPath1, dataPath2], -1, function, [id_type, id_type2])

    # Add boolean modifier
    boolean = contour_obj.modifiers.new(
        name="Intersect Boolean", type='BOOLEAN')
    boolean.operation = 'INTERSECT'
    boolean.object = boolean_obj
    boolean.solver = 'FAST'
    boolean.double_threshold = 0.000003

    # Add weld modifier
    weld = contour_obj.modifiers.new(name="Weld", type='WELD')
    weld.mode = 'CONNECTED'
    weld.merge_threshold = 0.003

    # Add geometry nodes modifier to object
    geo_nodes = contour_obj.modifiers.new(
        name="GeometryNodes.001", type='NODES')

    # Get geometry node group from active object
    node_group = geo_nodes.node_group
    nodes = node_group.nodes

    # Populate, position, and set default values for nodes
    node_group_in = nodes.get('Group Input')
    node_group_in.location = (-600, 0)

    mesh_to_curve_node = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_node.location = (-400, 0)

    input_position_node = nodes.new("GeometryNodeInputPosition")
    input_position_node.location = (-800, -400)

    separate_xyz_node = nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_node.location = (-600, -400)

    attribute_statistic_node = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_node.domain = 'CURVE'
    attribute_statistic_node.location = (-400, -300)

    capture_attribute_node = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_node.domain = 'CURVE'
    capture_attribute_node.location = (-200, 0)

    map_range_node = nodes.new("ShaderNodeMapRange")
    map_range_node.clamp = False
    map_range_node.location = (-200, -300)

    resample_curve_node = nodes.new("GeometryNodeResampleCurve")
    resample_curve_node.mode = 'LENGTH'
    resample_curve_node.location = (0, 0)

    transform_node = nodes.new("GeometryNodeTransform")
    # set up drivers
    target = bpy.data.window_managers["WinMan"]
    prop = 'default_value'
    source = transform_node.inputs[3]
    name = 'scale_z'
    dataPath = 'scale_z'
    d_type = 'AVERAGE'
    add_driver(source, target, prop, name, dataPath,
               2, '', 'WINDOWMANAGER', d_type)
    transform_node.name = "Transform_Master"
    transform_node.location = (200, 0)

    curve_to_mesh_node = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_node.location = (400, 0)

    circle_curve_node = nodes.new("GeometryNodeCurvePrimitiveCircle")
    circle_curve_node.inputs[0].default_value = 16
    circle_curve_node.inputs[4].default_value = 0.08
    circle_curve_node.location = (400, -180)

    set_material_node = nodes.new("GeometryNodeSetMaterial")
    set_material_node.location = (600, 0)

    object_info_node = nodes.new("GeometryNodeObjectInfo")
    object_info_node.inputs[0].default_value = graph_obj
    object_info_node.location = (600, -200)

    join_geometry_node = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_node.location = (800, 0)

    node_group_out = nodes.get('Group Output')
    node_group.outputs.new('NodeSocketFloat', 'Attribute')
    node_group_out.location = (1000, 0)

    # Link nodes
    node_group.links.new(
        node_group_in.outputs['Geometry'], mesh_to_curve_node.inputs['Mesh'])
    node_group.links.new(
        mesh_to_curve_node.outputs['Curve'], attribute_statistic_node.inputs['Geometry'])
    node_group.links.new(
        mesh_to_curve_node.outputs['Curve'], capture_attribute_node.inputs['Geometry'])

    node_group.links.new(
        input_position_node.outputs['Position'], separate_xyz_node.inputs['Vector'])
    node_group.links.new(
        separate_xyz_node.outputs['Z'], attribute_statistic_node.inputs['Attribute'])
    node_group.links.new(
        separate_xyz_node.outputs['Z'], map_range_node.inputs[0])

    node_group.links.new(
        attribute_statistic_node.outputs['Min'], map_range_node.inputs[1])
    node_group.links.new(
        attribute_statistic_node.outputs['Max'], map_range_node.inputs[2])

    node_group.links.new(
        map_range_node.outputs[0], capture_attribute_node.inputs[2])

    node_group.links.new(
        capture_attribute_node.outputs[2], node_group_out.inputs['Attribute'])
    node_group.links.new(
        capture_attribute_node.outputs['Geometry'], resample_curve_node.inputs['Curve'])

    node_group.links.new(
        resample_curve_node.outputs['Curve'], transform_node.inputs['Geometry'])
    node_group.links.new(
        transform_node.outputs['Geometry'], curve_to_mesh_node.inputs['Curve'])
    node_group.links.new(
        circle_curve_node.outputs['Curve'], curve_to_mesh_node.inputs['Profile Curve'])

    node_group.links.new(
        curve_to_mesh_node.outputs['Mesh'], set_material_node.inputs['Geometry'])

    node_group.links.new(
        set_material_node.outputs['Geometry'], join_geometry_node.inputs['Geometry'])
    node_group.links.new(
        object_info_node.outputs['Geometry'], join_geometry_node.inputs['Geometry'])

    node_group.links.new(
        join_geometry_node.outputs['Geometry'], node_group_out.inputs['Geometry'])

    # Name output attribute
    bpy.context.object.modifiers['GeometryNodes.001']['Output_2_attribute_name'] = "contour_col"

    # Set up material
    create_material("Contour_Mat", "contour_col",
                    color_min, color_max, set_material_node)

    # Create collection for objs
    collection = bpy.data.collections.new("Contour Plot")
    bpy.context.scene.collection.children.link(collection)
    bpy.context.scene.collection.objects.unlink(boolean_obj)
    bpy.context.scene.collection.objects.unlink(graph_obj)
    bpy.context.scene.collection.objects.unlink(contour_obj)
    collection.objects.link(boolean_obj)
    collection.objects.link(graph_obj)
    collection.objects.link(contour_obj)

    # Hide graph and boolean objs
    boolean_obj.hide_viewport = True
    boolean_obj.hide_render = True
    boolean_obj.hide_set(True)

    graph_obj.hide_viewport = True
    graph_obj.hide_render = True
    graph_obj.hide_set(True)


def create_slice(size_x, size_y):
    # Add geometry nodes modifier to object
    obj = bpy.context.active_object
    geo_nodes = obj.modifiers.new(name="Slice", type='NODES')
    node_group = geo_nodes.node_group
    nodes = node_group.nodes

    node_group_in = nodes.get('Group Input')
    node_group_in.location = (-200, 0)

    mesh_grid_node = nodes.new("GeometryNodeMeshGrid")
    mesh_grid_node.inputs[0].default_value = size_x + 2
    mesh_grid_node.inputs[1].default_value = size_y + 2
    mesh_grid_node.inputs[2].default_value = 2
    mesh_grid_node.inputs[3].default_value = 2
    mesh_grid_node.location = (-200, -200)

    transform_node = nodes.new("GeometryNodeTransform")
    transform_node.name = "Slice_Transform"
    transform_node.location = (0, -200)

    boolean_node = nodes.new("GeometryNodeMeshBoolean")
    boolean_node.location = (200, 0)

    node_group_out = nodes.get('Group Output')
    node_group_out.location = (400, 0)

    # Link nodes
    node_group.links.new(
        mesh_grid_node.outputs['Mesh'], transform_node.inputs['Geometry'])

    node_group.links.new(
        node_group_in.outputs['Geometry'], boolean_node.inputs['Mesh 1'])
    node_group.links.new(
        transform_node.outputs['Geometry'], boolean_node.inputs['Mesh 2'])

    node_group.links.new(
        boolean_node.outputs['Mesh'], node_group_out.inputs['Geometry'])


def create_curve(funcX, funcY, funcZ, syms, use_mesh, resolution, length):
    # Create object and link it to scene
    mesh = bpy.data.meshes.new("Curve Graph")
    obj = bpy.data.objects.new("Curve Graph", mesh)
    bpy.context.collection.objects.link(obj)

    # Set as active object
    bpy.context.view_layer.objects.active = obj

    # Add geometry nodes modifier to object
    bpy.ops.object.modifier_add(type='NODES')

    # Get geometry node group from active object
    node_group = obj.modifiers.get(
        "GeometryNodes").node_group
    nodes = node_group.nodes

    # populate, position, and set default values for nodes
    node_group_in = nodes.get('Group Input')
    if use_mesh:
        node_group_in.location = (-600, 0)
    else:
        node_group_in.location = (-400, 0)

    if use_mesh:
        mesh_line_node = nodes.new("GeometryNodeMeshLine")
        mesh_line_node.mode = 'END_POINTS'
        mesh_line_node.inputs[0].default_value = resolution
        mesh_line_node.inputs[3].default_value[0] = length
        mesh_line_node.inputs[3].default_value[2] = 0
        mesh_line_node.location = (-200, 0)
    else:
        curve_line_node = nodes.new("GeometryNodeCurvePrimitiveLine")
        curve_line_node.inputs[1].default_value[0] = length
        curve_line_node.inputs[1].default_value[2] = 0
        curve_line_node.location = (-400, 0)

        resample_curve_node = nodes.new("GeometryNodeResampleCurve")
        resample_curve_node.inputs[2].default_value = resolution
        resample_curve_node.location = (-200, 0)

    input_position_node = nodes.new("GeometryNodeInputPosition")
    input_position_node.location = (-400, -500)

    separate_xyz_node = nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_node.location = (-200, -500)

    combine_xyz_node = nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_node.location = (200, -500)

    transform_node = nodes.new("GeometryNodeTransform")
    transform_node.name = "Master_Transform"
    transform_node.location = (0, 0)

    set_position_node = nodes.new("GeometryNodeSetPosition")
    set_position_node.location = (200, 0)

    post_transform_node = nodes.new("GeometryNodeTransform")
    post_transform_node.name = "Post_Transform"
    post_transform_node.location = (400, 0)

    node_group_out = nodes.get('Group Output')
    node_group_out.location = (600, 0)

    # Instantiate NodeMath objects
    nodemath_syms = instantiate_nodemath(
        syms, node_group, node_group_in, separate_xyz_node, 0, -350)

    # Populate and offset Blender nodes for X component
    outX = scalar_check(funcX(*nodemath_syms), node_group, (0, -350))

    # Populate and offset Blender nodes for Y component
    for sym in nodemath_syms:
        sym.offset_y = -500
    outY = scalar_check(funcY(*nodemath_syms), node_group, (0, -500))

    # Populate and offset Blender nodes for Z component
    for sym in nodemath_syms:
        sym.offset_y = -650
    outZ = scalar_check(funcZ(*nodemath_syms), node_group, (0, -650))

    # Link nodes
    if use_mesh:
        node_group.links.new(
            mesh_line_node.outputs['Mesh'], transform_node.inputs['Geometry'])
    else:
        node_group.links.new(
            curve_line_node.outputs['Curve'], resample_curve_node.inputs['Curve'])
        node_group.links.new(
            resample_curve_node.outputs['Curve'], transform_node.inputs['Geometry'])

    node_group.links.new(
        transform_node.outputs['Geometry'], set_position_node.inputs['Geometry'])
    node_group.links.new(
        input_position_node.outputs['Position'], separate_xyz_node.inputs['Vector'])

    node_group.links.new(outX.output, combine_xyz_node.inputs['X'])
    node_group.links.new(outY.output, combine_xyz_node.inputs['Y'])
    node_group.links.new(outZ.output, combine_xyz_node.inputs['Z'])

    node_group.links.new(
        combine_xyz_node.outputs['Vector'], set_position_node.inputs['Position'])
    node_group.links.new(
        set_position_node.outputs['Geometry'], post_transform_node.inputs['Geometry'])
    node_group.links.new(
        post_transform_node.outputs['Geometry'], node_group_out.inputs['Geometry'])


def create_surface(funcX, funcY, funcZ, syms, x_dim, y_dim):
    """
    Function to create a 3D surface from three functions parameterized with two
    variables. F(x, y) -> R^3
    """
    # Create graph
    create_graph("Surface Graph", None, None, 1, 1, x_dim, y_dim,
                 False, False, False, False, None, None, 0, 0, 0, '')
    surface_obj = bpy.context.active_object

    # Get geometry node group from active object
    node_group = surface_obj.modifiers.get("GeometryNodes").node_group
    nodes = node_group.nodes

    # Retrieve existing nodes that need updated links by name
    node_group_in = node_search(nodes, 'Group Input')
    separate_xyz_node = node_search(nodes, 'Separate XYZ')
    separate_xyz_node.location = (-400, -300)
    combine_xyz_node = node_search(nodes, 'Combine XYZ')
    position_node = node_search(nodes, 'Position')
    position_node.location = (-600, -400)

    map_range_x_node = nodes.new("ShaderNodeMapRange")
    map_range_x_node.name = "Surface Range X"
    map_range_x_node.inputs[1].default_value = -0.5
    map_range_x_node.inputs[2].default_value = 0.5
    map_range_x_node.inputs[4].default_value = 6.28319
    map_range_x_node.location = (-200, -100)

    map_range_y_node = nodes.new("ShaderNodeMapRange")
    map_range_y_node.name = "Surface Range Y"
    map_range_y_node.inputs[1].default_value = -0.5
    map_range_y_node.inputs[2].default_value = 0.5
    map_range_y_node.inputs[4].default_value = 6.28319
    map_range_y_node.location = (-200, -350)

    # Instantiate NodeMath objects
    nodemath_syms = []
    for i in range(len(syms)):
        if syms[i] == 'x':
            nodemath_syms.append(
                NodeMath(map_range_x_node.outputs[0], node_group, 0, -100))
        elif syms[i] == 'y':
            nodemath_syms.append(
                NodeMath(map_range_y_node.outputs[0], node_group, 0, -100))
        elif syms[i] == 'z':
            nodemath_syms.append(
                NodeMath(separate_xyz_node.outputs['Z'], node_group, 0, -100))
        else:
            node_group.inputs.new('NodeSocketFloat', f"{syms[i]} variable")
            nodemath_syms.append(
                NodeMath(node_group_in.outputs[f"{syms[i]} variable"], node_group, 0, -100))

    # Populate Blender nodes
    outX = scalar_check(funcX(*nodemath_syms), node_group, (0, -100))

    for sym in nodemath_syms:
        sym.offset_y = -300
    outY = scalar_check(funcY(*nodemath_syms), node_group, (0, -300))

    for sym in nodemath_syms:
        sym.offset_y = -500
    outZ = scalar_check(funcZ(*nodemath_syms), node_group, (0, -500))

    # Link nodes
    node_group.links.new(
        separate_xyz_node.outputs['X'], map_range_x_node.inputs[0])
    node_group.links.new(
        separate_xyz_node.outputs['Y'], map_range_y_node.inputs[0])

    node_group.links.new(outX.output, combine_xyz_node.inputs['X'])
    node_group.links.new(outY.output, combine_xyz_node.inputs['Y'])
    node_group.links.new(outZ.output, combine_xyz_node.inputs['Z'])
