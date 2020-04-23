# Unreal Engine 4

Collection of console commands, python calls, etc. That I've found helpful

## Camera

### Clip Planes

Currently the UE4 USD Importer doesn't respect near clip planes. This can be set in the Project Settings but this requires a restart.

To set it at runtime, run this command in the editor with the `~` key.

`r.SetNearClipPlane 30`

## RTX

### Path Tracing

Instanced meshes get culled by default. Set to 0 to disable.

`r.RayTracing.InstancedStaticMeshes.Culling [0|1]`

[Source](https://devblogs.nvidia.com/ray-tracing-in-ue4-23/)
