# CMake

CMake is one of those languages I use a lot for a short period of time, and then not for a looong time. These are little refreshers that I've found I use a lot. 

## Paths

### Windows Separators

Got a windows path in an environment variable that has the wrong separators?

`file(TO_CMAKE_PATH $ENV{MyLib_DIR} MyLib_DIR)`

_Note: It's important that this environment variable exists..._

[Source](https://stackoverflow.com/questions/28070810/cmake-generate-error-on-windows-as-it-uses-as-escape-seq)

## Lists

### Filter 

If you have a cmake list you can filter it to only contain a certain file type by using the following:

`list(FILTER LIST_VAR INCLUDE REGEX ".*h$")`

That will only keep header files. The regex is a weird format but necessary.

## Debugging 

### Log Verbosity

For command line:
`cmake -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON $path_to_project_source;`

[Source](https://bytefreaks.net/programming-2/make-building-with-cmake-verbose)
