# SALOME-Voronoi

Interface between Salome and Vorpalite from the [Geogram](http://alice.loria.fr/index.php/software/4-library/75-geogram.html) programming library for polyhedral mesh generation. Note the Vorpalite program has many features (such as parallel tetrahedral meshing among other), but this script is primary intented for Centroidal Voronoi diagram computation.


## Getting started

Below instructions were tested using Ubuntu 20.04 and Salome 9.4. However, it should work for other Linux distributions without so much modifications.

### Compiling Vorpalite program

1. Download the Geogram library source [here](https://gforge.inria.fr/frs/?group_id=5833) and unzip the archive.

2. Install Boost, CGAL and others library header required: `sudo apt install libboost-dev libcgal-dev libglu1-mesa-dev libxxf86vm-dev libxtst-dev`. You may have to install other if error during compiling occur below.

3. Open a terminal in the unzipped Geogram folder and run in the terminal:
```
./configure.sh
cd build/Linux64-gcc-dynamic-Release
make -j4
```
The Vorpalite program is now compiled and can be find in `$GEOGRAM/build/Linux64-gcc-dynamic-Release/bin/` folder.

4. Copy the file `vorpalite` of the repository in the folder `~/.local/bin/` to create a command for Vorpalite to be called from anywhere in the terminal. You may have to change the file with the path to Vorpalite. Then open a terminal and make the script executable with `chmod +x vorpalite`.


### Salome plugin installation

1. Clone this repository inside your Salome plugin directory (Typically, `~/.config/salome/Plugins/`)

2. Add the following line to the `smesh_plugin.py` file:

```
import sys
path = "~/.config/salome/Plugins/" #or change by your Salome plugin directory 
sys.path.append(path + 'SALOME-Voronoi')
salome_pluginsmanager.AddFunction('Voronoi/Convert to Voronoi', ' ',
                                  convertToVoronoi.convertForCVTCalculation)
```

3. Your plugin is operational. You can now start converting meshes with `Mesh/Plugins/Voronoi/Convert to Voronoi`.


## Use the plugin

0. Plugins GUI is launch with `Mesh/Plugins/Voronoi/Convert to Voronoi`.

1. (Mandatory) Select the boundary mesh. This mesh will define the boundary of the Voronoi diagram. Only the 2D elements will be used.

2. (Optional) Select the seeds mesh. This mesh will define the seeds from where the Voronoi cell will be computed. Only the node will be used. If no mesh is specified, Vorpalite will create and optimize the seeds and their locations to create a Centroidal Voronoi Diagram.

3. Type the parameter to pass to Vorpalite. By default, Vorpalite is set to polygonal meshing mode (`profile=poly`), generate unique ids for the vertices (`generate_ids=true`) and will merge the boundary the with same normal (`simplify=tets_voronoi_boundary`). If no seeds mesh is specified, you should add the command `nb_pts=X` to create X seeds. A description of available parameter can be found by running in a terminal `vorpalite -h`

4. Click OK to launch the Voronoi Diagram computation.

## Mesh generation application

To be completed

* Voronoi diagram made from NETGEN 3D-2D-1D algorithm was found to be quite centroidal.

## Authors

* **Moïse Rousseau** - *Initial work*

## Know issues

No known issues for instance! :)

## Getting involved

Feel free to contact me if you have problems or comments, it will help me to improve the plugin.

## Further reading

* https://link.springer.com/chapter/10.1007%2F978-3-030-23436-2_3
* http://alice.loria.fr/
* http://alice.loria.fr/index.php/erc-vorpaline.html

## License

File in this repository are licensed under the GPL version 3 License - see the [LICENSE.md](LICENSE.md) file for details. About the Vorpalite program and Geogram library, please see this [page](http://alice.loria.fr/software/geogram/doc/html/geogram_license.html).
