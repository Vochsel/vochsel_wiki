# These two lines are for Houdini LOP Python Script compat.
node = hou.pwd()
stage = node.editableStage()

from pxr import Usd, UsdGeom, Gf

# Get global bbox cache
bboxCache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), includedPurposes=[UsdGeom.Tokens.default_])

# Get Prim, at arbitrary path
prim = stage.GetPrimAtPath("/unified")
xform = UsdGeom.Xform(prim)

# Get bbox
bb = bboxCache.ComputeWorldBound(prim)

# Get center for translate offset
center = bb.ComputeCentroid()

# Get min and max vecs
minr = bb.GetRange().GetMin() 
maxr = bb.GetRange().GetMax()

# Find abs min and max vec components
amin = abs(min(minr[0], min(minr[1], minr[2])))
amax = abs(max(maxr[0], max(maxr[1], maxr[2])))

radius = (amin + amax) / 2.0
s = 1.0/radius

# Apply scale and translate offsets
xform.AddScaleOp().Set(Gf.Vec3f(s,s,s), 0.0)
xform.AddTranslateOp().Set(-center)
