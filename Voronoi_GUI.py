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
# Author : Moise Rousseau (2019), email at moise.rousseau@polymtl.ca


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):

  def setupUi(self, Dialog):
    Dialog.setObjectName("Dialog")
    Dialog.resize(600, 180)
    Dialog.setSizeGripEnabled(False)
    print('set')
    
    #principal layout
    self.gridLayout_main = QtWidgets.QGridLayout(Dialog)
    self.gridLayout_main.setObjectName("gridLayout_main")
    
    #mesh/surface/output selection
    self.gridLayout_MSO = QtWidgets.QGridLayout(Dialog)
    self.gridLayout_MSO.setObjectName("gridLayout_MSO")
    #mesh
    self.label_mesh = QtWidgets.QLabel(Dialog)
    self.label_mesh.setObjectName("label_mesh")
    self.pb_origMeshFile = QtWidgets.QPushButton(Dialog)
    self.pb_origMeshFile.setObjectName("origMeshFile")
    self.pb_origMeshFile.setCheckable(True)
    self.le_origMeshFile = QtWidgets.QLineEdit(Dialog)
    self.le_origMeshFile.setObjectName("le_origMeshFile")
    self.le_origMeshFile.setReadOnly(True)
    self.gridLayout_MSO.addWidget(self.label_mesh, 2, 0)
    self.gridLayout_MSO.addWidget(self.pb_origMeshFile, 3, 0)
    self.gridLayout_MSO.addWidget(self.le_origMeshFile, 3, 1)
    #surface
    self.label_surface = QtWidgets.QLabel(Dialog)
    self.label_surface.setObjectName("label_surface")
    self.pb_origSurfaceFile = QtWidgets.QPushButton(Dialog)
    self.pb_origSurfaceFile.setObjectName("origSurfaceFile")
    self.pb_origSurfaceFile.setCheckable(True)
    self.le_origSurfaceFile = QtWidgets.QLineEdit(Dialog)
    self.le_origSurfaceFile.setObjectName("le_origSurfaceFile")
    self.le_origSurfaceFile.setReadOnly(True)
    self.gridLayout_MSO.addWidget(self.label_surface, 0, 0)
    self.gridLayout_MSO.addWidget(self.pb_origSurfaceFile, 1, 0)
    self.gridLayout_MSO.addWidget(self.le_origSurfaceFile, 1, 1)
    #surface
    self.label_params = QtWidgets.QLabel(Dialog)
    self.label_params.setObjectName("label_params")
    self.le_params = QtWidgets.QLineEdit(Dialog)
    self.le_params.setObjectName("le_params")
    self.gridLayout_MSO.addWidget(self.label_params, 4, 0)
    self.gridLayout_MSO.addWidget(self.le_params, 5, 0)
    #checkbox for adding 0d center
    self.label_addCenter0D = QtWidgets.QLabel(Dialog)
    self.label_addCenter0D.setObjectName("label_addcenter0D")
    self.gridLayout_MSO.addWidget(self.label_addCenter0D, 6, 1)
    self.cb_enableAddCenter0D = QtWidgets.QCheckBox(Dialog)
    self.cb_enableAddCenter0D.setObjectName("cb_enableAddCenter0D")
    self.gridLayout_MSO.addWidget(self.cb_enableAddCenter0D, 6, 0)
    #add layout
    self.gridLayout_main.addLayout(self.gridLayout_MSO, 0, 0)
    
    #ok and cancel button
    self.splitter = QtWidgets.QSplitter(Dialog)
    self.splitter.setOrientation(QtCore.Qt.Horizontal)
    self.splitter.setObjectName("splitter")
    self.pb_okCancel = QtWidgets.QDialogButtonBox(self.splitter)
    self.pb_okCancel.setOrientation(QtCore.Qt.Horizontal)
    self.pb_okCancel.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
    self.pb_okCancel.setObjectName("pb_okCancel")
    self.gridLayout_main.addWidget(self.splitter, 1, 0)
    self.pb_okCancel.accepted.connect(Dialog.accept)
    self.pb_okCancel.rejected.connect(Dialog.reject)
    
    self.retranslateUi(Dialog)
    
    
  def retranslateUi(self, Dialog):
    _translate = QtCore.QCoreApplication.translate
    Dialog.setWindowTitle(_translate("Dialog", "Convert to Voronoi"))
    #MSO
    self.pb_origMeshFile.setText(_translate("Dialog", "Select"))
    self.label_mesh.setText(_translate("Dialog", "Seeds location (optional):"))
    self.pb_origSurfaceFile.setText(_translate("Dialog", "Select"))
    self.label_surface.setText(_translate("Dialog", "Boundary mesh (mandatory):"))
    self.label_params.setText(_translate("Dialog", "Parameters to pass to Vorpalite:"))
    self.le_params.setText("profile=poly generate_ids=true simplify=tets_voronoi_boundary")
    self.label_addCenter0D.setText(_translate("Dialog", "Add center to result as 0D elements"))
    
    return
    
    
