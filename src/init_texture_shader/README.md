# Purpose
Create a basic texture shader setup faster.

Creates nodes for any or all of the following: Base Color/Albedo, Ambient Occlusion, Roughness, and Normal, and connects them to an aiStandardSurfaceShader. Note that you cannot have an AO file node without an Albedo node. The roughness and metallic maps will be routed through remapValue nodes in case you want to scale the values in them. `aiImage` is used for the normal map solely because aiNormalMap is also used.

# Result
![expected result of running the script](./images/basic_texture_nodes_outcome.png "Basic Texture Node Setup")