# Houdini Wiki
Here are a mix of Python and Vex snippets that have served me well.

## HDAs/OTLs

### Internal Callback Function
When writing HDAs you can put your python code under Scripts tab, and then create a `Python Module` event handler.
To call this function from a parameter callback script you can use `hou.pwd().hm().function_name(kwargs, hou.pwd())`. 
`hou.pwd().hm()` effectively becomes your module.

## LOPS

### LOP Lights -> Mantra/OBJ Lights

This script is a barebones conversion of a USD Stage to Mantra/OBJ level lights. There's bugs, it doesn't work on all cases, but might be of interest.

Source:
[houdini/lop_import_lights.py](houdini/lop_import_lights.py)

## External Links
 * [kiryha python-snippets](https://github.com/kiryha/Houdini/wiki/python-snippets)

*Disclaimer; This is not in any way a competitor to [CGWiki](http://www.tokeru.com/cgwiki/index.php?title=Main_Page)*
