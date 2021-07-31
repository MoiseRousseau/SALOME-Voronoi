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

import SMESH
import subprocess
import numpy as np
#import time

### 
### PREPROCESSING
###

def exportPoints(meshToExport, output):
  """
  Export the mesh vertice as seed for computing the Voronoi diagram using
  Vorpalite
  """
  #open outputfile
  out = open(output, 'w')
  #export source points
  n_nodes = meshToExport.NbNodes()
  for x in range(1,1+n_nodes):
    X,Y,Z = meshToExport.GetNodeXYZ(x)
    out.write('v %s %s %s\n' %(X, Y, Z))
  out.close()
  return
  

def exportBoundary(meshToExport, output):
  #open outputfile
  out = open(output, 'w')
  #export nodes
  n_nodes = meshToExport.NbNodes()
  for x in range(1,1+n_nodes):
    X,Y,Z = meshToExport.GetNodeXYZ(x)
    out.write('v %s %s %s\n' %(X, Y, Z))
  #export facets
  Ids = meshToExport.GetElementsByType(SMESH.FACE)
  for Id in Ids:
    nodes = meshToExport.GetElemNodes(Id)
    out.write('f'+''.join([' '+str(x) for x in nodes]) + '\n')
  out.close()
  return
  


###
### CONVERSION
###

def vorpalite(input_boundary, output_mesh = None, input_points = None, params = None):
  #prepare command to call
  cmd = ["vorpalite"]
  #params
  if params:
    if isinstance(params, str): params = params.split()
    cmd += params
  else:
    cmd += ["profile=poly","generate_ids=true","simplify=tets_voronoi_boundary"]
  #add input point or check for nb_pts
  if input_points:
    cmd += ["points_file="+input_points]
  else:
    #check if nb_pts defined
    pass
  #add mesh to convert
  cmd += [input_boundary]
  #output
  if output_mesh:
    cmd += [output_mesh]
  #call command
  res = subprocess.call(cmd)
  return res



###
### IMPORTER
###

def importVorpaliteMesh(mesh, Vmesh):
  """
  Import a OVM mesh created with Vorpalite
  Args:
  - mesh: path to the ovm file created by Vorpalite
  - Vmesh: Salome mesh instance to import the mesh
  """
  #OVM file format particularity
  # edge are oriented: i.e. (i,j) = from i to j
  # in faces: even edge are the normally oriented edge
  #           but odd mean reversed edge!
  #           for example, face (2,4,8,7) = edge1, edge2, edge4 but edge3 in reverse!
  # for poly ??
  
  #check mesh format
  if mesh.split('.')[-1] != 'ovm':
    print("Only meshes in OVM format are supported")
  src = open(mesh, 'r')
  line = src.readline() #pass header
  
  print("Add point")
  line = src.readline() #Vertices
  nb_vertices = int(src.readline())
  for i in range(nb_vertices):
    X,Y,Z = [float(x) for x in src.readline().split()]
    Vmesh.AddNode(X,Y,Z)
    
  #delete double point
  print("Merge coincident node")
  double = Vmesh.FindCoincidentNodes(1e-6) #in salome, so start from 1!
  Vmesh.MergeNodes(double)
  if 0:
    uniqueIds = {}
    for Ids in double:
      for Id in Ids:
        uniqueIds[Id] = Ids[0]
  uniqueIds = {x:ids[0] for ids in double for x in ids}
  if len(uniqueIds) != Vmesh.NbNodes():
    #it lacks some element
    for i in range(1,nb_vertices+1):
      if i not in uniqueIds.keys(): uniqueIds[i] = i
  
  print("Build half-edges")
  line = src.readline() #Edges
  nb_edges = int(src.readline())
  #edges = np.array((2*nb_edges,2), dtype='i8')
  edges = [[0,0]]*2*nb_edges #make the structure according to salome numbering
  valid_edges = [True]*2*nb_edges
  for i in range(nb_edges):
    I,J = [uniqueIds[int(x)+1] for x in src.readline().split()]
    edges[2*i] = [I,J]
    edges[2*i+1] = [J,I]
    if I == J:
      valid_edges[2*i] = False
      valid_edges[2*i+1] = False
  
  print("Build half-faces")
  line = src.readline() #Faces
  nb_faces = int(src.readline())
  faces = [[]] * 2 * nb_faces
  valid_faces = [True] * 2 * nb_faces
  for i in range(nb_faces):
    #do something with the edges
    face_elem = [int(x) for x in src.readline().split()[1:]]
    face_nodes = [edges[x][0] for x in face_elem if valid_edges[x]]
    faces[2*i] = face_nodes
    face_nodes.reverse()
    faces[2*i+1] = face_nodes
    if len(face_nodes) < 3:
      valid_faces[2*i] = False
      valid_faces[2*i+1] = False
  
  print("Build polyhedrons")
  line = src.readline() #Poly
  nb_poly = int(src.readline())
  for i in range(nb_poly):
    line = src.readline().split()
    poly_face = [int(x) for x in line[1:]]
    poly_nodes = []
    quantities = []
    for faceid in poly_face:
      if valid_faces[faceid]:
        for x in faces[faceid]:
          poly_nodes.append(x)
        quantities.append(len(faces[faceid]))
    #t = time.time()
    #poly_nodes = orient_faces_slow(poly_nodes, quantities, Vmesh)
    #print("compute face orientation: {} µs".format((time.time()-t)*1e6))
    Vmesh.AddPolyhedralVolume(poly_nodes, quantities)
  #orient face
  Vmesh.ReorientObject(Vmesh)
  volId = Vmesh.GetElementsByType(SMESH.VOLUME)[0]
  if Vmesh.GetVolume(volId) < 0.:
    Vmesh.ReorientObject(Vmesh)
  return


def createGroupsFromNodes(seedsMesh, Vmesh):
  """
  Create a groups of Voronoi mesh volume corresponding to some mesh node group
  """
  nodesGroups = seedsMesh.GetGroups(SMESH.NODE)
  if not nodesGroups: return
  for group in nodesGroups:
    nodes = group.GetNodeIDs()
    volIds = set()
    newGrp = Vmesh.CreateEmptyGroup(SMESH.VOLUME, group.GetName())
    for node in nodes:
      X,Y,Z = seedsMesh.GetNodeXYZ(node)
      volId = Vmesh.FindElementsByPoint(X,Y,Z,SMESH.VOLUME)
      newGrp.Add(volId)
  return

def orient_faces_slow(nodes, quantities, Vmesh):
  #approximatively 1.5 ms per polyhedra
  #so for 10000 polyhedra = 15s
  #t = time.time()
  #compute center
  Xc,Yc,Zc = 0,0,0
  for x in nodes:
    X,Y,Z = Vmesh.GetNodeXYZ(x)
    Xc += X; Yc += Y; Zc += Z
  Xc /= len(nodes); Yc /= len(nodes); Zc /= len(nodes)
  center = np.array([Xc,Yc,Zc])
  #print("compute center: {} µs".format((time.time()-t)*1e6))
  #check face orientation
  index = 0
  out = []
  for nb_nodes in quantities:
    face_nodes = nodes[index:nb_nodes+index]
    A = np.array(Vmesh.GetNodeXYZ(face_nodes[1]))
    u = A - np.array(Vmesh.GetNodeXYZ(face_nodes[0]))
    v = np.array(Vmesh.GetNodeXYZ(face_nodes[2])) - A
    n = np.cross(u,v)
    test = center - A
    if np.dot(test,n) > 0.:
      face_nodes.reverse()
    out += face_nodes
    index += nb_nodes
    #print("compute face: {} µs".format((time.time()-t)*1e6))
  return out
  

