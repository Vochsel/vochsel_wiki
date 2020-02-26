# Blender Wiki
Blender snippets. 

## C++

### Debug Output
```C++
WM_reportf(RPT_WARNING, "Output: %s", var);
```

### Node Traversal

```c++
for (bNode *node = (bNode*)nodetree->nodes.first; node; node = node->next) {
   WM_reportf(RPT_WARNING, "Found node: %s", node->name);
}
```
