# Houdini Wiki
Here are a mix of Python and Vex snippets that have served me well.

## HDAs/OTLs

### Internal Callback Function
When writing HDAs you can put your python code under Scripts tab, and then create a `Python Module` event handler.
To call this function from a parameter callback script you can use `hou.pwd().hm().function_name(kwargs, hou.pwd())`. 
`hou.pwd().hm()` effectively becomes your module.

## LOPS

### Primitive selection

The primitive field on lop nodes act like SOPs groups. You can selectively filter what this node will effect.

Spaces separate primitive paths.

These can be set via dropdown in any Primitive field on any node. Put here for convinience:

All Meshes: `` `lopinputprims('.', 0)\` { usd_istype(0, @primpath, "Mesh") }``

All Components: `{ usd_kind(0, @primpath) == "component" }`

For more info: [Houdini Docs: Primitive Matching Patterns](https://www.sidefx.com/docs/houdini/solaris/pattern.html)

### Set subdiv attribute

In an attribute wrangle set the string attribute `@subdivisionScheme` to be a token of your choice: `catmullClark`, `loop`, `bilinear`, `none`.

```c
s@subdivisionScheme = "catmullClark";
s@subdivisionScheme = "loop";
s@subdivisionScheme = "bilinear";
```

![lops subdiv attribute](https://github.com/Vochsel/vochsel_wiki/blob/master/houdini/lops_subdiv_wrangle.png)

### LOP Lights -> Mantra/OBJ Lights

This script is a barebones conversion of a USD Stage to Mantra/OBJ level lights. There's bugs, it doesn't work on all cases, but might be of interest.

Source:
[houdini/lop_import_lights.py](houdini/lop_import_lights.py)

## External Links
 * [kiryha python-snippets](https://github.com/kiryha/Houdini/wiki/python-snippets)

*Disclaimer; This is not in any way a competitor to [CGWiki](http://www.tokeru.com/cgwiki/index.php?title=Main_Page)*
