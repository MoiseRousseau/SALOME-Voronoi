#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# Author : Moise Rousseau (2020), email at moise.rousseau@polymtl.ca


import time



def convertForCVTCalculation(context):

  print ("\n\n\n")
  print ("##################################\n")
  print (" Convert to Voronoi Diagram \n")
  print ("     By Moise Rousseau (2020)     \n")
  print ("   \n")
  print ("###################################\n")
  
  
  import Voronoi_GUI
  import Voronoi_utils
  import importlib
  from salome.gui import helper
  from salome.smesh import smeshBuilder
  import SMESH
  import os
  import salome
  from qtsalome import QDialog, QMessageBox, QFileDialog, QTableWidgetItem
  
  importlib.reload(Voronoi_GUI)
  importlib.reload(Voronoi_utils)
  sg = context.sg
  smesh = smeshBuilder.New()
  
  class Voronoi_Dialog(QDialog):
    def __init__(self):
      QDialog.__init__(self)
      # Set up the user interface from Designer.
      self.ui = Voronoi_GUI.Ui_Dialog()
      self.ui.setupUi(self)
      self.show()
      
      self.selectMesh = False
      self.selectSurface = False
      self.mesh = None
      self.surface = None
      
      # Connect up the buttons.
      self.ui.pb_origMeshFile.clicked.connect(self.setMeshInput)
      self.ui.pb_origSurfaceFile.clicked.connect(self.setSurfaceInput)
      
      return
      
    def select(self):
      #sg.getObjectBrowser().selectionChanged.disconnect(self.select)
      objId = salome.sg.getSelected(0)
      if self.selectMesh:
        self._selectMeshInput(objId)
      elif self.selectSurface:
        self._selectSurfaceInput( objId)
      return
      
      
    def _selectMeshInput(self, objId):
      self.mesh = salome.IDToObject(objId)
      if isinstance(self.mesh,salome.smesh.smeshBuilder.meshProxy):
        name = salome.smesh.smeshBuilder.GetName(self.mesh)
      elif isinstance(self.mesh,SMESH._objref_SMESH_Group):
        name = salome.smesh.smeshBuilder.GetName(self.mesh)
      elif isinstance(self.mesh,salome.smesh.smeshBuilder.submeshProxy):
        name = salome.smesh.smeshBuilder.GetName(self.mesh)
      else:
        return
      self.ui.le_origMeshFile.setText(name)
      return
      
      
    def _selectSurfaceInput(self, objId):
      self.surface = salome.IDToObject(objId)
      if isinstance(self.surface,salome.smesh.smeshBuilder.meshProxy):
        name = salome.smesh.smeshBuilder.GetName(self.surface)
      elif isinstance(self.surface,SMESH._objref_SMESH_Group):
        name = salome.smesh.smeshBuilder.GetName(self.surface)
      elif isinstance(self.surface,salome.smesh.smeshBuilder.submeshProxy):
        name = salome.smesh.smeshBuilder.GetName(self.surface)
      else:
        return
      self.ui.le_origSurfaceFile.setText(name)
      return
      
    
    def setMeshInput(self):
      if self.selectMesh == True:
        self.selectMesh = False
        sg.getObjectBrowser().selectionChanged.disconnect(self.select)
      else:
        self.selectSurface = False
        self.ui.pb_origSurfaceFile.setChecked(False)
        self.selectMesh = True
        sg.getObjectBrowser().selectionChanged.connect(self.select)
        self.select()
      return
      
      
    def setSurfaceInput(self):
      if self.selectSurface == True:
        self.selectSurface = False
        sg.getObjectBrowser().selectionChanged.disconnect(self.select)
      else:
        self.selectMesh = False
        self.ui.pb_origMeshFile.setChecked(False)
        self.selectSurface = True
        sg.getObjectBrowser().selectionChanged.connect(self.select)
        self.select()
      return

  window = Voronoi_Dialog()
  #window.setSmeshBuilder(smesh)
  window.exec_()
  result = window.result()
  #compute perm here
  if result:
    t = time.time()
    smesh = salome.smesh.smeshBuilder.New()
    path = '/home/%s/.config/salome/Plugins/Voronoi_converter/' %(os.getlogin())
  
    #get the mesh
    print("\tExport boundary mesh")
    boundary = smesh.Mesh(window.surface)
    out_boundary = path + "boundary.obj"
    Voronoi_utils.exportBoundary(boundary, out_boundary)
  
    #export generator point
    print("\tExport seeds")
    seedsMesh = smesh.Mesh(window.mesh)
    out_point = path + "points.pts"
    Voronoi_utils.exportPoints(seedsMesh, out_point)
    
    #make Voronoi
    #get the custom params
    params = window.ui.le_params.text() #TODO
    output_mesh = path + "out.ovm"
    print("\tCompute the clipped Voronoi Diagram")
    print("")
    Voronoi_utils.vorpalite(out_boundary, output_mesh, out_point, params)
    print("")
    
    #import Voronoi
    print("\tImport the results")
    mainShape = boundary.GetShape()
    Vmesh = smesh.Mesh(mainShape)
    Vmesh.SetName(boundary.GetName()+'_Voronoi')
    Vmesh = Voronoi_utils.importVorpaliteMesh(output_mesh, Vmesh)
    
    if salome.sg.hasDesktop():
      salome.sg.updateObjBrowser()
      
    print ("\tTime elapsed {} s".format(time.time() - t))
      
    print ("    END \n")
    print ("####################\n\n")

  return

