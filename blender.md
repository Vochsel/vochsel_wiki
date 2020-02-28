# Blender Wiki
Blender snippets. 

## C++

### Debug Output
```C++
#include "WM_api.h"
#include "WM_types.h"

WM_reportf(RPT_WARNING, "Output: %s", var);
```

### Node Traversal

```c++
#include "BKE_node.h"

for (bNode *node = (bNode*)nodetree->nodes.first; node; node = node->next) {
   WM_reportf(RPT_WARNING, "Found node: %s", node->name);
}
```
