import sys
import os
import salome_pluginsmanager

try:
  pathVoronoi = os.getenv("HOME") + "/.config/salome/Plugins/SALOME-Voronoi"
  if not pathVoronoi in sys.path:
      sys.path.append(pathVoronoi)
 
  import Voronoi_converter

  salome_pluginsmanager.AddFunction('Voronoi/Convert to Voronoi', '', Voronoi_converter.convertForCVTCalculation)
  
except Exception as e:

  print("Failed to import SALOME-Voronoi plugin:", e)

