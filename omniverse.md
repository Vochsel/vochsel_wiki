# Omniverse

Where to start. It's pretty confusing hey. Hugely appreciate NVIDIA pushing USD more into the zeitgeist. But dang, could they have done it a little less confusing??

## Interacting with Omniverse

### From a command line

A lot of pipeline stuff happens headlessly. Haven't found an easy way to do this, but this does _work_.

Don't even both **not** creating a .kit file for configuration... It's annoying you can't just run with the same extensions as create in a headless manner... But whatever

`& ${OMNIVERSE_ROOT}/omni.create.bat --enable omni.kit.asset_converter --exec "${SCRIPT_PATH}" --no-window`
Enable whatever you need. The benefit of using omni.create, is if you have been using Omniverse Create to debug in a gui, this has all the extensions loaded.

### Understanding kit files

See a `${*}` variable in a kit file, the list of them live [here](https://docs.omniverse.nvidia.com/py/kit/docs/guide/tokens.html)
