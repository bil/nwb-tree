# nwbtree
```nwbtree``` is a small utility that takes the output of [nwbinspector](https://github.com/NeurodataWithoutBorders/nwbinspector) and displays it along the the contents of an NWB file in a color-coded, tree-like format (credit to [h5tree](https://github.com/johnaparker/h5tree) for the tree format). This allows for a more visually guided inspection of a file's compliance with NWB best practices.

To use the utility, simply call ```makeTree()``` and pass in the path to the NWB file. The color scheme of the tree can be adjusted for light or dark display palettes by specifying ````scheme```` as either "light" or "dark".
