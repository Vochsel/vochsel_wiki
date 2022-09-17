# Omniverse

Where to start. It's pretty confusing hey. Hugely appreciate NVIDIA pushing USD more into the zeitgeist. But dang, could they have done it a little less confusing??

## Gotchas

### Async python

Doing anything with async or omniverse's task managers? Omniverse makes use of asyncio's event loops quite a lot. 

In order to make your own code synchronous, you should make a new event loop.


```python
import asyncio

async def custom():
  await convert(...)
  
asyncio.new_event_loop().run_until_complete(custom())

```

## Interacting with Omniverse

### From a command line

A lot of pipeline stuff happens headlessly. Haven't found an easy way to do this, but this does _work_.

On windows, this can look like the following: 
```ps1
$OMNI_ROOT = "$Env:LOCALAPPDATA/ov/pkg/create-2022.1.3"
& $OMNI_ROOT/kit/kit.exe --ext-folder $OMNI_ROOT/exts --ext-folder $OMNI_ROOT/extscache --enable omni.kit.asset_converter --exec "C:/yourscript.py" 
```

For very very basic stuff a .kit file isn't needed, but it becomes so hard to maintain it's usually easier to concede and make a kit file to set up your environment.

A basic kit file is pretty simple though:
```
[package]
title = "CLI Convert"

[dependencies]
# tool
"omni.kit.asset_converter" = {}
```

### Understanding kit files

See a `${*}` variable in a kit file, the list of them live [here](https://docs.omniverse.nvidia.com/py/kit/docs/guide/tokens.html)
