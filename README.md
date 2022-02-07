# Graph

## About
 Graph is a Blender 3D addon that adds graphing capabilities to Blender using geometry nodes. Sympy is used to accept an expression as a string. The string is parsed and the function is then programmatically populated as geometry nodes. 

## Features
 - Parameterized curve graphs c(t) -> R³
 - Parameterized surface graphs r(u, v) -> R³
 - Vector fields v(x, y, z) -> R³
 - Scatter plot/scalar output graphs f(x, y, z) -> R
 - Gradient fields
 - Visualize gradient descent/ascent
 - Controllable settings/dynamic graphs
 - Natural function style (ex: 5x+9y rather than 5\*x+9\*y)
 - x y z variables are mapped to blender vertice position x y z
 - Add controllable parameters (ex: mx+b; m and b can be controlled with value sliders/input)
 - Nodes are defined programmatically

## Requirements
 - sympy python package

## Setup
 1. Install requirements for your Blender's python

 2. Download the latest release of the addon from the releases page/section.

 3. Install in blender by going to preferences > addons and then select the .zip file.

*Pdf documentation coming soon
**Questions/suggestions/bugs - labounty3d@gmail.com
