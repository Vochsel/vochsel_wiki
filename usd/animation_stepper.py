import math
from pxr import Usd, UsdGeom, Gf

source_stage = Usd.Stage.Open("/content/test_data.usd")
source_stage.Reload()

STEP_AMT = 2

for prim in source_stage.TraverseAll():

  # - Clear xform time samples
  if prim.IsA(UsdGeom.Xform):
    xform = UsdGeom.Xform(prim)

    # For each operator (xform ops can be stacked)
    for op in xform.GetOrderedXformOps():
      op_attr = op.GetAttr()
      
      # Clear moduloed time samples
      for i in op_attr.GetTimeSamples():
        ts = math.floor(i)
        if ts % STEP_AMT != 1:
          op_attr.ClearAtTime(i)

  # - Clear mesh time samples
  if prim.IsA(UsdGeom.Mesh):
    mesh = UsdGeom.Mesh(prim)
    points_attr = mesh.GetPointsAttr()

    # Clear moduloed time samples
    for i in points_attr.GetTimeSamples():
      ts = math.floor(i)
      if ts % STEP_AMT != 1:
        points_attr.ClearAtTime(i)

    # Might want to do this on normals, other data
    # e.g. for pv in mesh.GetPrimvars(): etc

# Optional, not respected in Houdini, linear still used
source_stage.SetInterpolationType(Usd.InterpolationTypeHeld )

# Export new stage
source_stage.Export("/content/stepped_data.usd")
