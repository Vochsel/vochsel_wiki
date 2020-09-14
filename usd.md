# USD Wiki
I've been using Pixar's USD in a CG pipeline for over a year now. Here's some helpful things I've noted.

### C++/Python
Most of these are following are python snippets. The function interface is mostly the same with the C++ API with some noticeable language differences: 

 * Wrap values with `pxr::VtValue(10.0f)` `pxr::VtValue("Value")`
 * Paths with `pxr::SdfPath("/path")`

### Resources

 * [USD Glossary](https://graphics.pixar.com/usd/docs/USD-Glossary.html)
 * [USD API Documentation](https://graphics.pixar.com/usd/docs/api/index.html)
 * [Pixar's Presentations](http://graphics.pixar.com/usd/downloads.html)
 * [cgwiki](http://www.tokeru.com/cgwiki/index.php?title=HoudiniLops)

## Stage 

### Creation

|  | Code |
|:-- | -- |
| memory | `stage = Usd.Stage.CreateInMemory()` |
| file | `stage = Usd.Stage.CreateNew("/path/to/stage.usda")` |

### Metadata

|  | Code |
|:-- | -- |
| comment | `stage.SetMetadata('comment', 'This will be the comment')` |
| documentation | `stage.SetMetadata('documentation', 'This will be the documentation')` |
| documentation | `stage.GetPseduoRoot().SetDocumentation('This will be the documentation")` |

### Output

|  | Code | Docs |
|:-- | -- | -- |
| save | `stage.GetRootLayer().Save()` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#adefa2f7ebfc4d8c09f0cd54419aa36c4) |
| save as | `stage.Export( "/path/to/output.usda" )` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#a0185cf581fbcceba34d567c6bc73d351)
| print | `print( stage.ExportToString() )` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#a0cc2dc5d689d2b28e7821db0fb4f4903)

### Traversal

#### Stage

To traverse recursively through every prim:

**Python**
```python
for prim in stage.Traverse():
    print(prim)
```

**C++**
```c++
for (pxr::UsdPrim prim: usd_stage->Traverse()) {
    std::cout << "Prim path: " << prim.GetPath().GetText() << '\n';
}
```
or
```c++
pxr::UsdPrimRange prim_range = usd_stage->Traverse();
for (auto it = prim_range.begin(); it!=prim_range.end(); ++it) {
    std::cout << "Found prim: " << it->GetPath().GetText() << '\n';
    
}
```

#### Children
**C++**
```c++
for (const pxr::UsdPrim &childPrim : prim.GetChildren()) {
    // Do something...
}
```

## Layers
Layers are core part of USD composition. A usd file can have "SubLayers". A Stage can have multiple "Layers". Both "In Memory Layers" and "On Disk Layers".

There is not as nice of an API for layers, and it actaully differs whether in Python or C++. (Link)[https://groups.google.com/g/usd-interest/c/usUeP1USk04/m/ENTOmMsBBwAJ]

|  | Code | Docs | Tips |
|:-- | -- | -- | -- |
| add sublayer | `stage.GetRootLayer().subLayerPaths.append(usd_file)` | (python) |
| get layer stack | `stage.GetLayerStack()` | (python) |


## Prims

|  | Code | Docs | Tips |
|:-- | -- | -- | -- |
| define | `stage.DefinePrim("/primpath")` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#a6151ae804f7145e451d9aafdde347730) | Gets or creates prim at primpath. To transform, prim must be an xform (or sub type) |
| exists | `stage.GetPrimAtPath("/primpath")` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#a5f2d63fdf3b9bb6ac9e3286b70c07551) | Return prim object. Can be invalid (Check with IsValid) |
| valid | `prim.IsValid()` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_object.html#afa8720abaf6972d6dac22a8cd1a67225) | False if not valid (Doesn't exist) |
| attribute | `prim.GetAttribute('attribName')` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_prim.html#a04dca40bb61be7b3779b1eb38002bca2) | Use `.Get()` and `.Set(val)` |
| type *(string)* | `prim.GetTypeName()` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_prim.html#a2e20db2f92fe5f6687b5c7f919277257) |  |
| prim path | `prim.GetPath()` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_object.html#a205aff7879727aeaadd5cf8a3deda408) | Explicitly as C++ String `prim.GetPath().GetString()` |
| prim name | `prim.GetName()` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_object.html#a806237c0e1ef633b59aee8a42e83d2e2) | Explicitly as C++ String `prim.GetName().GetString()` |

## Tokens
USD Tokens are a handle for a registered string. Basically all strings must be tokens. In python these are usually converted automagically.

### Sanitize String

In order to "sanitize" a string to be a valid usd token you can use this function: [docs](https://graphics.pixar.com/usd/docs/api/group__group__tf___string.html#ga68e587cc7f9f5a5dd3ae8f03dcffe15c)

**Python**
```python
from pxr import Tf
token = Tf.MakeValidIdentifier("some.illegal/string") 
```

**C++**
```c++
TfToken token = TfMakeValidIdentifier("some.illegal/string");
``` 

## Attributes

Note:
Value Types for C++: `pxr::SdfValueTypeNames->String`
Value Types for Python: `Sdf.ValueTypeNames.String`

For userProperties, append `userProperties:` to attribute name. 

|  | Code | Docs | Tips |
|:-- | -- | -- | -- |
| create attribute | `prim.CreateAttribute(name, Sdf.ValueTypeNames.Int, isCustom)` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_prim.html#a1e25b831b0e54e1d59ba2da969e165fa) | |
| get attribute | `prim.GetAttribute(name)` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_prim.html#a04dca40bb61be7b3779b1eb38002bca2) | |
| set attribute (value) | `attribute.Set()` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_attribute.html#a5a6164f78a12163010be1b6c3a25187d) | In C++ you need to use the specific template `Set<float>(0.5f)` |
| get attribute (value) | `attribute.Get()` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_attribute.html#adf3eaec3c3d8749ceb86236dcc3d1e9d) | In C++ you need to use a template `Get<float>()` |
| is time varying | `attribute.ValueMightBeTimeVarying()` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_attribute.html#ac059ed4db262b51c18a6c0c28b2fab3f) | Return true if value *might* change. If false, it's __certain__ that this value remains constant. |

## Composition

The idea of composition is one of the key parts of what makes USD so flexible. There are a few core ways to compose a USD stage.

### References

USD References can either be prepended or appended. Combined with this, the reference's order in said list is used in stage composition.

 * (References)[https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-References]

|  | Code | Docs | Tips |
|:-- | -- | -- | -- |
| Add Reference | `prim.GetReferences().AddReference("C:/file/on/disk.usd")` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_references.html#a890b5681714fae1c1f807a8b0f4ab67b) | Adds a reference to back of prepend list|
| Add Reference *(specific)* | `prim.GetReferences().AddReference("C:/file/on/disk.usd", position = Usd.ListPositionFrontOfAppendList)` | [docs](https://graphics.pixar.com/usd/docs/api/common_8h.html#a28349701078995dc76a99331bb60c555a681727d9e5aecd6058825ab1fe888028) | Adds a reference to back of prepend list|
| Get References | `prim.GetPrimStack()` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_prim.html#a0d45421c0488ad9129873e1f8591bfaf) | There is no proper way *yet* to retrieve a list of references. This will return the composed stack, it is not recommended.  |

## Xformables

`from pxr import UsdGeom`

|  | Code | Docs | Tips |
|:-- | -- | -- | -- |
| define xform | `xform = stage.DefinePrim("/primpath", "Xform")` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#a6151ae804f7145e451d9aafdde347730) | Gets or creates an xform prim at primpath. **To transform a prim, it must be an Xform or child type** |
| define xform | `xform = UsdGeom.Xform.Define(stage, "/primpath")` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#a6151ae804f7145e451d9aafdde347730) | Same as above. |
| set position | `UsdGeom.XformCommonAPI(xform).SetTranslate(Gf.Vec3d(x, y, z), timecode)` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_geom_xform_common_a_p_i.html#a4c66e62616adfdaba258e8dfdec1a630) |  |
| set rotation *(euler)* | `UsdGeom.XformCommonAPI(xform).SetRotate(Gf.Vec3d(x, y, z), timecode)` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_geom_xform_common_a_p_i.html#aa1cfa6eb3f9ccf760536e7bf14b60462) | Degrees |
| set rotation *(quaternion)* | `UsdGeom.XformCommonAPI(xform).SetRotate(Gf.Rotation(Gf.Vec3d(x, y, z), w), timecode)` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_geom_xform_common_a_p_i.html#aa1cfa6eb3f9ccf760536e7bf14b60462) |  |
| get transform *(local)* | `UsdGeom.XformCommonAPI(xform).GetXformVectors(timecode)` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_geom_xform_common_a_p_i.html#a9901c2a6ffcdc8c4e7aa4ec07d5efa00) | Returns tuple of (translation, rotation, scale, pivot, rotationOrder) |
| get transform *(world)* | `mat4 = UsdGeom.XformCache(timecode).GetLocalToWorldTransform(prim)` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_geom_xformable.html#a2aa0db10d36cae3d325e930765e54d94) | Returns matrix 4x4 |
| set transform | `xform.AddTransformOp().Set(transform_matrix)` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_geom_xform_common_a_p_i.html#a9901c2a6ffcdc8c4e7aa4ec07d5efa00) | Returns tuple of (translation, rotation, scale, pivot, rotationOrder) |


## Gf
*Graphics Foundations*

`from pxr import Gf`

|  | Code | Docs | Tips |
|:-- | -- | -- | -- |
| define matrix4 | `mat4 = Gf.Matrix4d(2)` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#a6151ae804f7145e451d9aafdde347730) | Creates identity matrix |
| define translate matrix4 | `mat4 = Gf.Matrix4d(2).SetTranslate(Gf.Vec3d(x, y, z))` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#a6151ae804f7145e451d9aafdde347730) | Creates translate matrix |
| define per element matrix4 | `mat4 = Gf.Matrix4d(2).SetTranslate(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#a6151ae804f7145e451d9aafdde347730) | Creates translate matrix |
| get translation | `mat4.ExtractTranslation()` | [docs](https://graphics.pixar.com/usd/docs/api/class_gf_matrix4d.html#a690166f9a9d958ff6c3bc008ebcdeea0) | Get vec3 translation |
| get rotation | `mat4.ExtractRotation()` | [docs](https://graphics.pixar.com/usd/docs/api/class_gf_matrix4d.html#a1fb1e160ed4428d1c94f17180c83b3b7) | Get rotation |
| get scale | `scale = (mat4.GetRow3(0).GetLength(), mat4.GetRow3(1).GetLength(), mat4.GetRow3(2).GetLength())` | | Get all axis scale |


## Lights

`from pxr import UsdLux`

|  | Code | Docs | Tips |
|:-- | -- | -- | -- |
| define light | `light_prim = stage.DefinePrim("/primpath", "DomeLight")` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_lux_dome_light.html) | This will return a prim object, no light methods attached |
| access light | `light = UsdLux.DomeLight(light_prim)` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_lux_dome_light.html) |  |
| set dome texture | `dome_light.CreateTextureFileAttr().Set("/path/to/texture.exr")` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_lux_dome_light.html#a5e1d4f7d42a3bb4957388b2762675aca) |  |


## Shaders

`from pxr import UsdShade`

|  | Code | Docs | Tips |
|:-- | -- | -- | -- |
| get shader from prim | `shader = UsdShade.Shader(prim)` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_shade_shader.html#ad5583e305b62de9e6a2c18302b7d9004) | This will return a shader object |
| get filename | `shader.GetInput("filename").Get()` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_shade_shader.html#a7fa41d67d5a7ca13ae5a544a5ce291d7) | Gets the texture filename string (Has '@' at start and end.  |
| set existing filename | `shader.GetInput("filename").Set("C:/new_path.png")` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_shade_shader.html#a7fa41d67d5a7ca13ae5a544a5ce291d7) | |


## Tips
 * Most API functions are CamelCase.

## USDZip Gotchas

These are somethings that got me when working with USDZips, particularly on iOS quicklook.

* If there are multiple root prims and no default prim, iOS quicklook freaks out. Add a defaultPrim to the stage
* "File size is too large" I've found usdzips work best when small. 
     * Beware large textures. The usdzip can be small but the texture budget could be 100x as much...
 * If a texture path has an invalid path it can bundle in empty 1kb files with no extension
     * Too many (Any?) of these can sometimes cause quicklook to not display it at all
 * Scene size is important, as is the sceneUnits layer property
 * USD Apple Schemas: https://developer.apple.com/documentation/arkit/usdz_schemas_for_ar

     
