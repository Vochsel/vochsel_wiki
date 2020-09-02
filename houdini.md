# Houdini Wiki
Here are a mix of Python and Vex snippets that have served me well.

## Python

Layout node: `node.moveToGoodPosition()`

Flags:
* `node.setDisplayFlag(True)`
* `node.setRenderFlag(True)`

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

![lops subdiv attribute](https://github.com/Vochsel/vochsel_wiki/raw/master/houdini/lops_subdiv_wrangle.png)

### Bulk override attributes

This will change all filename attributes from backslashes to forward, but can be adjusted to suit your needs.

```python
node = hou.pwd()
stage = node.editableStage()
# Add code to modify the stage.
# Use drop down menu to select examples.
import os
from pxr import UsdShade
for prim in stage.Traverse():
    try:
        s = UsdShade.Shader(prim)
        i = s.GetInput("filename")
        p = i.Get()
        if p:
            p = str(p)
            p = p[1:-1]
            p = p.replace('\\\\', '/')
            i.Set(p)
    except:
        pass
```

### GeomSubsets

USD uses [USDGeomSubsets](https://graphics.pixar.com/usd/docs/api/class_usd_geom_subset.html) to allow for multiple materials assigned to one mesh. These work well. But additional care should be taken when modifying LOPs via SOPs. When going back and forth between LOPs and SOPs, an important mesh attribute to keep an eye on is `subsetFamily:materialBind:familyType`. If this is set to `nonOverlapping` then the additional geometry from SOPs will not properly interpolate or set the GeomSubsets. 

One fix is to set your mesh attribute to `s@subsetFamily:materialBind:familyType = "unrestricted";` via an Attribute Wrangle in LOPs. 

Another fix is to create groups for the geom subsets.Add a primitive wrangle in SOPs after unpacking polys from USD. Add the following VEX to the prim wrangle.

```c
string s@materialBind;
setprimgroup(0, s, @primnum, 1);
```

And then enable **Subset Groups**, under **Import Data**, in LOPs, and set the groups to either `*` or the specific groups created per subface.


### LOP Lights -> Mantra/OBJ Lights

This script is a barebones conversion of a USD Stage to Mantra/OBJ level lights. There's bugs, it doesn't work on all cases, but might be of interest.

Source:
[houdini/lop_import_lights.py](houdini/lop_import_lights.py)

## C++

### HBoost

When linking against HBoost, you need to ensure these three steps:

1. Change references to the boost namespace to `hboost` instead.
2. Change references to `BOOST_*` preprocessor variables to `HBOOST_*` instead. (This one got me)
3. Change `<boost/...>` header includes to `<hboost/...>` instad.

## External Links
 * [kiryha python-snippets](https://github.com/kiryha/Houdini/wiki/python-snippets)

*Disclaimer; This is not in any way a competitor to [CGWiki](http://www.tokeru.com/cgwiki/index.php?title=Main_Page)*
