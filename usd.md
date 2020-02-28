# USD Wiki
I've been using Pixar's USD in a CG pipeline for over a year now. Here's some helpful things I've noted.

### C++/Python
Most of these are following are python snippets. The function interface is mostly the same with the C++ API with some noticeable language differences: 

 * Wrap values with `pxr::VtValue(10.0f)`
 * Paths with `pxr::SdfPath("/path")`

### Resources

 * [USD Glossary](https://graphics.pixar.com/usd/docs/USD-Glossary.html)
 * [USD API Documentation](https://graphics.pixar.com/usd/docs/api/index.html)
 * [cgwiki](http://www.tokeru.com/cgwiki/index.php?title=HoudiniLops)

## Stage 

### Creation

|  | Code |
|:-- | -- |
| memory | `stage = Usd.Stage.CreateInMemory()` |
| file | `stage = Usd.Stage.CreateNew("/path/to/stage.usda")` |

### Output

|  | Code | Docs |
|:-- | -- | -- |
| save | `stage.GetRootLayer().Save()` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#adefa2f7ebfc4d8c09f0cd54419aa36c4) |
| save as | `stage.Export( "/path/to/output.usda" )` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#a0185cf581fbcceba34d567c6bc73d351)
| print | `print( stage.ExportToString() )` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#a0cc2dc5d689d2b28e7821db0fb4f4903)

### Traversal

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

## Prims

|  | Code | Docs | Tips |
|:-- | -- | -- | -- |
| define | `stage.DefinePrim("/primpath")` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#a6151ae804f7145e451d9aafdde347730) | Gets or creates prim at primpath. To transform, prim must be an xform (or sub type) |
| exists | `stage.GetPrimAtPath("/primpath")` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_stage.html#a6151ae804f7145e451d9aafdde347730) | Return prim object. Can be invalid (Check with IsValid) |
| valid | `prim.IsValid()` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_object.html#afa8720abaf6972d6dac22a8cd1a67225) | False if not valid (Doesn't exist) |
| attribute | `prim.GetAttribute('attribName')` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_prim.html#a04dca40bb61be7b3779b1eb38002bca2) | Use `.Get()` and `.Set(val)` |
| type *(string)* | `prim.GetTypeName()` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_prim.html#a2e20db2f92fe5f6687b5c7f919277257) |  |
| prim path | `prim.GetPath()` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_object.html#a205aff7879727aeaadd5cf8a3deda408) | Explicitly as C++ String `prim.GetPath().GetString()` |
| prim name | `prim.GetName()` | [docs](https://graphics.pixar.com/usd/docs/api/class_usd_object.html#a806237c0e1ef633b59aee8a42e83d2e2) | Explicitly as C++ String `prim.GetName().GetString()` |

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


## Tips
 * Most API functions are CamelCase.
