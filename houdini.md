# Houdini Wiki
Here are a mix of Python and Vex snippets that have served me well.

## LOPS

### LOP Lights -> Mantra/OBJ Lights

This script is a barebones conversion of a USD Stage to Mantra/OBJ level lights. There's bugs, it doesn't work on all cases, but might be of interest.

```
def update_node(kwargs, cd):
    from pxr import Usd, UsdGeom, UsdLux

    node = kwargs['node']
    
    # Remove old nodes
    
    for child in node.children():
        child.destroy()
    
    lop_node = node.parm('lop_node').evalAsNode()
    
    supported_types = [
        "spherelight",
        "distantlight",
        "rectlight",
        "cylinderlight",
    ]

    # Traverse stage and create mantra lights
    try:
        stage = lop_node.stage()
    except:
        return
        
    for prim in stage.Traverse():

        prim_type = prim.GetTypeName().lower()

        if prim_type not in supported_types:
            continue

        if 'light' in prim_type:
            light = node.createNode('hlight')
            light.setName(prim.GetName())
            light.parm('light_intensity').set(prim.GetAttribute('intensity').Get())
            
            mat = UsdGeom.XformCache(0).GetLocalToWorldTransform(prim)

            pos = mat.ExtractTranslation()

            rot = mat.ExtractRotation().GetQuaternion()
            rot = hou.Quaternion(rot.GetImaginary()[0], rot.GetImaginary()[1], rot.GetImaginary()[2], rot.GetReal()).extractEulerRotates() 
            
            light.parm('tx').set(pos[0])
            light.parm('ty').set(pos[1])
            light.parm('tz').set(pos[2])
            
            light.parm('rx').set(rot[0])
            light.parm('ry').set(rot[1])
            light.parm('rz').set(rot[2])

            col = prim.GetAttribute('color').Get()
            
            light.parm('light_colorr').set(col[0])
            light.parm('light_colorg').set(col[1])
            light.parm('light_colorb').set(col[2])
            
            try:
                light.parm('coneenable').set(1)
                angle = UsdLux.ShapingAPI(prim).GetShapingConeAngleAttr().Get()
                softness = UsdLux.ShapingAPI(prim).GetShapingConeSoftnessAttr().Get()

                light.parm('coneangle').set(angle)
            except:
                print('Couldnt set angle')
            
            if prim_type == 'spherelight':
                light.parm('light_type').set(4)
                light.parm('areasize1').set(prim.GetAttribute('radius').Get())
                light.parm('areasize2').set(prim.GetAttribute('radius').Get())
    
            elif prim_type == 'distantlight':
                light.parm('light_type').set(7)
    
            elif prim_type == 'rectlight':
                light.parm('light_type').set(2)
                light.parm('areasize1').set(prim.GetAttribute('width').Get())
                light.parm('areasize2').set(prim.GetAttribute('height').Get())
                
    node.layoutChildren()
    
```

## External Links
 * [kiryha python-snippets](https://github.com/kiryha/Houdini/wiki/python-snippets)

*Disclaimer; This is not in any way a competitor to [CGWiki](http://www.tokeru.com/cgwiki/index.php?title=Main_Page)*
