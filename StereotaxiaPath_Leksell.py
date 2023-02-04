# -*- coding: utf-8 -*-
# StereotaxiaPath version 22.0809
from __main__ import qt, ctk, slicer, vtk
from slicer.ScriptedLoadableModule import *

import os
import numpy as np
import logging
import time
import ast   # para eval seguras
import json
import importlib

from Recursos import Maquina_Russell_Brown
from Recursos import utilitarios 
from Recursos import gestion_Fiduciarios 

importlib.reload(Maquina_Russell_Brown)
importlib.reload(utilitarios)
importlib.reload(gestion_Fiduciarios)

class StereotaxiaPath_Leksell(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class"""
    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "StereotaxiaPath_Leksell"
        self.parent.categories = ["Stereotaxia"]
        self.parent.dependencies = []
        self.parent.contributors = ["Dr. Jorge Beninca; Dr. Dante Lovey; Dr. Lucas Vera; Dra. Elena Zema; Dra. Anabella Gatti."]
        self.parent.helpText = "Esta es la Version 23.0130"
        self.parent.acknowledgementText = "Este modulo calcula en un corte tomografico, los 9 fiduciarios, realiza la registración con las ecuaciones de Russel Brown para la determinacion 3D de un sistema de localizadores N de un marco Estereotáxico "

class StereotaxiaPath_LeksellWidget(ScriptedLoadableModuleWidget):
    """Uses ScriptedLoadableModuleWidget base class"""    
    def __init__(self, parent=None):
        ScriptedLoadableModuleWidget.__init__(self, parent)
        self.utiles = utilitarios.util()
        self.gest = gestion_Fiduciarios.gestion()
        self.maqui = Maquina_Russell_Brown.calculus()
        

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)
        self.Registracion_Bton = ctk.ctkCollapsibleButton()
        self.Registracion_Bton.text = "Registración y cálculo del Target"
        self.Registracion_Bton.collapsed = False
        self.layout.addWidget(self.Registracion_Bton)
        self.Grilla1 = qt.QGridLayout(self.Registracion_Bton)
        self.Layout_Bton = ctk.ctkCollapsibleButton()
        self.Layout_Bton.text = "Gráfica"
        self.Layout_Bton.collapsed = False
        self.layout.addWidget(self.Layout_Bton)
        self.Grilla2 = qt.QGridLayout(self.Layout_Bton)
        self.Resultados_Bton = ctk.ctkCollapsibleButton()
        self.Resultados_Bton.text = "Resultados"
        self.Resultados_Bton.collapsed = False
        self.layout.addWidget(self.Resultados_Bton)
        self.Grilla3 = qt.QGridLayout(self.Resultados_Bton)
        
        #self.Bton1 = qt.QPushButton("Inicializa")
        self.Bton2= qt.QPushButton("abre Archivo Dicom")
        self.Bton3 = qt.QPushButton("Registración ")
        #self.Bton4 = qt.QPushButton("Traza path")
        self.Bton5 = qt.QPushButton("Target / Entry")
        #self.Bton6 = qt.QPushButton("Entry")
        self.Bton7 = qt.QPushButton("Dieño MPR")
        self.Bton8 = qt.QPushButton("Diseño tabulado")
        self.Bton9 = qt.QPushButton("Guarda la Sesión")
        self.Bton20 = qt.QPushButton("prueba 1")
        self.Bton21 = qt.QPushButton("prueba 2")
        
        self.Combo1 = qt.QComboBox()
        self.Combo1.setEditable(True)
        self.Combo1.lineEdit().setAlignment(qt.Qt.AlignCenter)
        self.Combo1.addItems(['LEKSELL'])
        self.Combo2 = qt.QComboBox()
        self.Combo2.setEditable(True)
        self.Combo2.lineEdit().setAlignment(qt.Qt.AlignCenter)
        self.Combo2.addItems(['UPWARD'])
      
        self.Lbl0 = qt.QLabel("")

        #self.textEdit = qt.QTextEdit("")
        #self.textEdit.setMaximumSize(500, 200)
        self.lbl0 = qt.QLabel("Geometría :")
        self.lbl0.setAlignment(qt.Qt.AlignCenter)
        
        self.Grilla1.addWidget(self.Bton2, 1, 0, 1, 0)
        self.Grilla1.addWidget(self.lbl0, 2, 0)
        self.Grilla1.addWidget(self.Combo1, 2, 1)
        self.Grilla1.addWidget(self.Combo2, 2, 2)
        self.Grilla1.addWidget(self.Bton3, 3, 0, 1, 0)
        #self.Grilla1.addWidget(self.Bton4, 4, 0)
        #self.Grilla1.addWidget(self.Bton6, 5, 1)
        self.Grilla1.addWidget(self.Lbl0, 6, 0, 1, 0)
        #self.Grilla1.addWidget(self.Bton5, 7, 2)
        self.Grilla1.addWidget(self.Bton9, 9, 0, 1, 0)
        #self.Grilla1.addWidget(self.Bton20, 10, 0 )
        #self.Grilla1.addWidget(self.Bton21, 10, 1 )
  

        #self.Grilla2.setMaximunSize(200, 200)
        self.Grilla2.addWidget(self.Bton5, 5, 2)
        self.Grilla2.addWidget(self.Bton7, 5, 0)
        self.Grilla2.addWidget(self.Bton8, 5, 1)
        
        #self.Grilla3.addWidget(self.textEdit, 13, 0)
        #self.textEdit = qt.QTextEdit()
        #self.textEdit.setMaximumSize(500, 200)
        #self.Grilla3.addWidget(self.textEdit, 13, 0)
        
        self.lbl1 = qt.QLabel("Marco :")
        self.ledt1 = qt.QLineEdit()
        self.lbl2 = qt.QLabel("Fiduciarios :")
        self.ledt2 = qt.QLineEdit()
        self.lbl3 = qt.QLabel("Target :")
        self.ledt3 = qt.QLineEdit()
        self.lbl4 = qt.QLabel("Entry :")
        self.ledt4 = qt.QLineEdit()
        self.lbl5 = qt.QLabel("Trayectoria :")
        self.ledt5 = qt.QLineEdit()
        #self.lbl6 = qt.QLabel("ang Alfa :")
        #self.ledt6 = qt.QLineEdit()
        #self.lbl7 = qt.QLabel("ang Beta :")
        #self.ledt7 = qt.QLineEdit()
        self.lbl9 = qt.QLabel(" ")

        self.Grilla3.addWidget(self.lbl1, 1, 0)
        self.Grilla3.addWidget(self.ledt1, 1, 1)
        self.Grilla3.addWidget(self.lbl2, 1, 2)
        self.Grilla3.addWidget(self.ledt2, 1, 3)
        self.Grilla3.addWidget(self.lbl3, 3, 0)
        self.Grilla3.addWidget(self.ledt3, 3, 1)
        self.Grilla3.addWidget(self.lbl4, 3, 2)
        self.Grilla3.addWidget(self.ledt4, 3, 3)
        self.Grilla3.addWidget(self.lbl5, 4, 0)
        self.Grilla3.addWidget(self.ledt5, 4, 1)
        self.Grilla3.addWidget(self.lbl5, 5, 0)
        self.Grilla3.addWidget(self.ledt5, 5, 1)
        #self.Grilla3.addWidget(self.lbl6, 6, 0)
        #self.Grilla3.addWidget(self.ledt6, 6, 1)
        #self.Grilla3.addWidget(self.lbl7, 6, 2)
        #self.Grilla3.addWidget(self.ledt7, 6, 3)

        self.Grilla3.addWidget(self.lbl9, 8, 0, 1, 0)
        self.Grilla3.addWidget(self.Bton9, 9, 0, 1, 0)

        self.layout.addStretch(1)   # Add vertical spacer
        
        # conecciones con las clases logicas
        #
        #self.Bton1.clicked.connect(lambda: self.selectora_botones("Inicializa"))
        self.Bton2.clicked.connect(lambda: self.selectora_botones("Dicom"))
        self.Bton3.clicked.connect(lambda: self.selectora_botones("Registracion"))
        self.Bton5.clicked.connect(lambda: self.selectora_botones("Target/Entry"))
        self.Bton9.clicked.connect(lambda: self.selectora_botones("Guarda"))
        self.Bton7.clicked.connect(lambda: self.selectora_botones("MPR"))
        self.Bton8.clicked.connect(lambda: self.selectora_botones("Tabulado"))
        self.Bton20.clicked.connect(lambda: self.selectora_botones("Prueba1"))
        self.Bton21.clicked.connect(lambda: self.selectora_botones("Prueba2"))
        
        self.Combo1.currentTextChanged.connect(self.on_combo1_changed)
        self.Combo2.currentTextChanged.connect(self.on_combo2_changed)
     
        ######################  Incio de la actividad del widget ##############
        self.utiles.Inicializa_Escena()
        self.param = slicer.util.getNode("Param_data")
        
        #######################################################################
 
    def selectora_botones(self, modo):
        if modo == "Dicom":
            self.Setup_Escena()
            #slicer.util.selectModule("DICOM")
            slicer.util.loadVolume(self.param.GetParameter("modulo_path") + "/Paciente_Leksell_10_grados.nrrd")
            #slicer.util.loadVolume(self.param.GetParameter("modulo_path") + "/Paciente_Leksell.nrrd")
            #slicer.util.loadVolume(self.param.GetParameter("modulo_path") + "/Paciente_Leksell_rotado.nrrd")
            #slicer.util.loadVolume(self.param.GetParameter("modulo_path") + "/Paciente.nrrd")
            
        elif modo == "Registracion":
            nodo_volu = self.utiles.obtiene_nodo_de_widget("Red")
            if nodo_volu == None:
                texto = "ERROR: no hay paciente cargados !!!"
                slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
                return
            """if self.Combo1.currentText == "Marco" or self.Combo2.currentText == "Fiduciarios":
                texto = "ERROR: No se ha elegido correctamente el Marco !!!  "
                slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
                self.Bton3.setStyleSheet(self.param.GetParameter("rojito")) 
                return        
            if self.Combo1.currentText == "LEKSELL":
                if self.Combo2.currentText == "DOWNWARD":
                    texto = "ERROR: Leksell no tiene marcadores DownWard !!!  "
                    slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
                    self.Bton3.setStyleSheet(self.param.GetParameter("rojito")) 
                return
            """
            slicer.app.layoutManager().setLayout(6)  # red panel
            name = nodo_volu.GetName()
            self.param.SetParameter("Paciente", name)
            self.Bton2.setText("Paciente: " + name)
            self.Bton3.setStyleSheet(self.param.GetParameter("amarillito"))
            self.ledt1.setText(self.Combo1.currentText)
            self.ledt2.setText(self.Combo2.currentText)
            self.utiles.centra_nodo_de_widget("Red")
            self.utiles.cambia_window_level("Red", 100, 50)
            self.Obtiene_9_Fiduciarios_f()
            self.utiles.Renderiza_3D_Volumen(nodo_volu)     # Renderiza el volumen en uso
            self.utiles.Yaw_y_Pitch(20)                     # gira hacia abajo y a la derecha el volumen 
            
        elif modo == "Target/Entry":
            if self.E_T_flag == 0:
                self.E_T_flag = 1
                self.utiles.impri_layout_2D("Red", "Target", None)
            else:
                self.E_T_flag = 0
                self.utiles.impri_layout_2D("Red", "Entry", None)
            nodo_path = slicer.util.getNode("Path")
            self.funcion_mueve_path(nodo_path, None)        
            
        elif modo == "MPR":
            slicer.app.layoutManager().setLayout(3)  # 3d panel   
            print("cambia layout a 4-UPp")        
            
        elif modo == "Tabulado":
            slicer.app.layoutManager().setLayout(10)  # tabulado    
            print("cambia layout a tabulado")                   
            
        elif modo == "Guarda":
            self.guarda()
            

 
    def Setup_Escena(self):
        slicer.app.layoutManager().setLayout(6)  # red panel
        self.utiles.Genera_Nodo("vtkMRMLLinearTransformNode", "Transformada_Correctora_del_Volumen")
        self.utiles.Genera_Nodo("vtkMRMLMarkupsFiducialNode", "f")
        self.utiles.Genera_Nodo("vtkMRMLMarkupsLineNode", "Path")
        self.limpia_widget()         
        self.E_T_flag = 0       # flag señalando la activacion el punto Target
        self.param.SetParameter("Marco", self.Combo1.currentText)
        self.param.SetParameter("Fiduciarios", self.Combo2.currentText)
        self.Bton3.setStyleSheet(self.param.GetParameter("rojito"))
       

    def on_combo1_changed(self, value):
        nodo_volu = self.utiles.obtiene_nodo_de_widget("Red")
        if nodo_volu == None:
            texto = "ERROR: no hay paciente cargados !!!"
            slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
            return
        self.param.SetParameter("Marco", self.Combo1.currentText)
        self.ledt1.setText(self.Combo1.currentText)
        print("Cambia la geometria: ", self.Combo1.currentText)
        

    def on_combo2_changed(self, value):
        nodo_volu = self.utiles.obtiene_nodo_de_widget("Red")
        if nodo_volu == None:
            texto = "ERROR: no hay paciente cargados !!!"
            slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
            return
        self.param.SetParameter("Fiduciarios", self.Combo2.currentText)
        self.ledt2.setText(self.Combo2.currentText)
        print("Cambia la geometria: ", self.Combo2.currentText)
        

    def Obtiene_9_Fiduciarios_f(self):
        print("Vino a marcacion de 9 fiduciarios")
        nodo_volu = self.utiles.obtiene_nodo_de_widget("Red")
        print("El volumen con que se trabaja es = ", nodo_volu.GetName())
        print("El origen del volumen es =", nodo_volu.GetOrigin())
        self.utiles.modifica_origen_de_volumen(nodo_volu, [100,100,-100])
        self.utiles.centra_nodo_de_widget("Red")
                
        nodo_fidu = self.gest.Inicializa_nodo("f")

        dnodo_fidu = nodo_fidu.GetDisplayNode()
        dnodo_fidu.SetGlyphType(1)
        dnodo_fidu.SetSelectedColor(0.0, 1.0, 0.0)
        dnodo_fidu.SetActiveColor(1.0, 0.0, 0.0)
        
        transformada = slicer.util.getNode("Transformada_Correctora_del_Volumen")
        #transformada = self.utiles.Genera_Nodo("vtkMRMLLinearTransformNode", "Transformada_Correctora_del_Volumen")
        nodo_volu.SetAndObserveTransformNodeID(transformada.GetID())
        nodo_fidu.SetAndObserveTransformNodeID(transformada.GetID())
        
        self.param.SetParameter("Nombre_del_Paciente", nodo_volu.GetName())
        
        self.mixObservador_1 = slicer.util.VTKObservationMixin()
        self.mixObservador_1.addObserver(nodo_fidu, vtk.vtkCommand.UserEvent, self.calculos_para_registracion)
        
        self.gest.Marcacion_Fiduciarios("f", 9)
        #self.calculos_para_registracion(None, None)
        

    def calculos_para_registracion(self, caller, event):   # funcion principal MAIN del procesamiento de fiduciarios
        print("vino a callback calculos desde :", type(caller), event)
        self.mixObservador_1.removeObservers()      
        #
        #-----------------procedimiento de REGISTRACION--------------------
        #
        nodo_fidu = slicer.util.getNode("f")
        nodo_fidu.SetDisplayVisibility(False)

        fiduciarios_TAC = self.gest.Lectura_Fiduciarios(nodo_fidu)
        #fiduciarios_TAC=  [[75.62618255615234, -83.13968658447266, -23.0], [75.73440551757812, -12.635770797729492, -23.0], [75.93955993652344, 35.749839782714844, -23.0], [39.508262634277344, 92.31975555419922, -23.0], [-32.29926681518555, 92.12418365478516, -23.0], [-79.90154266357422, 91.85201263427734, -23.0], [-115.97569274902344, 38.367767333984375, -23.0], [-116.44105529785156, -10.668255805969238, -23.0], [-116.53287506103516, -83.57567596435547, -23.0]]
        print("fiduciarios TAC= ", fiduciarios_TAC)
        
        geometria = self.param.GetParameter("Marco") + "_" + self.param.GetParameter("Fiduciarios")
        matriz_RB = self.maqui.Ecuaciones_Russell_Brown(fiduciarios_TAC, geometria)
        if matriz_RB == None:
            texto = "ATENCION: hay un error en el Marco y/o Fiduciarios !!!"
            slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
            self.Bton3.setStyleSheet(self.param.GetParameter("rojito")) # rojito
            return        

        array_M_RB = slicer.util.arrayFromVTKMatrix(matriz_RB).tolist()
        fiduciarios_3D = self.maqui.Multiplica_lista_de_puntos(fiduciarios_TAC, matriz_RB)
        
        matriz_4x4  = self.maqui.Analisis_por_ICP(fiduciarios_TAC, fiduciarios_3D)
        array_M_3D = slicer.util.arrayFromVTKMatrix(matriz_RB).tolist()
        
        transformada = vtk.vtkTransform()
        transformada.SetMatrix(matriz_4x4)
        nodo_transfo = slicer.util.getNode("Transformada_Correctora_del_Volumen")
        nodo_transfo.SetAndObserveTransformToParent(transformada)

        self.utiles.centra_nodo_de_widget("Red")
        slicer.app.layoutManager().setLayout(3)  # 4 up


        if self.param.GetParameter("Marco") == "LEKSELL":
            Target = np.array([100.0, 100.0, 60.0])
            Entry = np.array([160.0, 160.0, 130.0])
        else:
            Target = np.array([0.0, 0.0, 60.0])
            Entry = np.array([60.0, 60.0, 130.0])
        
        self.inicia_path(Target, Entry)    
        
        self.param.SetParameter("Fiduciarios_TAC", str(self.utiles.redondea_lista_de_puntos(fiduciarios_TAC, 2)))
        self.param.SetParameter("Array_Matrix_RB", str(array_M_RB))
        self.param.SetParameter("Fiduciarios_3D", str(self.utiles.redondea_lista_de_puntos(fiduciarios_3D, 2)))
        self.param.SetParameter("Array_Matrix_3D", str(array_M_3D))
        self.param.SetParameter("Target", str(Target[0])+ ", " + str(Target[1]) +", " + str(Target[2]))
        self.param.SetParameter("Entry" , str(Entry[0])+ ", " + str(Entry[1]) +", " + str(Entry[2]))
        self.param.SetParameter("Transformada_Position", str(self.utiles.redondea(transformada.GetPosition(), 2)))
        self.param.SetParameter("Transformada_Orientation", str(self.utiles.redondea(transformada.GetOrientation(), 2)))
        self.param.SetParameter("Registered_flag", "True")
        
        self.actualiza_widget()       
        self.Bton3.setStyleSheet(self.param.GetParameter("verdecito")) # verde


    def inicia_path(self, Target, Entry):        
        nodo_path = self.utiles.genera_linea(Target, Entry)
        # inicia observador
        self.mixObservador_5 = slicer.util.VTKObservationMixin()
        self.mixObservador_5.addObserver(nodo_path, nodo_path.PointEndInteractionEvent, self.funcion_mueve_path)
        self.funcion_mueve_path(nodo_path, None)               
        
    
    def funcion_mueve_path(self, nodo, ev):
        print("vino a mueve path")
        p_RAS = slicer.util.arrayFromMarkupsControlPoints(nodo, True)
        self.utiles.ubicar_la_punta_en_RPN(p_RAS[self.E_T_flag])
        
        Target = self.utiles.redondea((p_RAS[0]), 1)
        Entry = self.utiles.redondea((p_RAS[1]), 1)
        
        Alfa, Beta = self.utiles.calcula_angulos_con_vtk(Target, Entry)
        print("Alfa, Beta con vtk =", Alfa, Beta)
        Alfa, Beta = self.utiles.calcula_angulos_simple(Target, Entry)
        print("Alfa, Beta con formula simple =", Alfa, Beta)
         
        if (Entry[0]>=0) != (Target[0]>=0):   #(a>0) == (b>0)   #### ojo con leksell
            texto = "ATENCION: el PATH atraviesa la línea media !  "
            slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
        
        if Entry[0] >= 0:
            self.param.SetParameter("Target_Izq_Der_flag", str(True))
        else:
            self.param.SetParameter("Target_Izq_Der_flag", str(False))

        self.param.SetParameter("Target", str(Target[0])+ ", " + str(Target[1]) +", "+ str(Target[2]))
        self.param.SetParameter("Entry" , str(Entry[0])+ ", " + str(Entry[1]) +", "+ str(Entry[2]))
        largo_path = nodo.GetLineLengthWorld()
        self.param.SetParameter("Path_length", str(round(largo_path, 2)) +"  mm.")
        self.param.SetParameter("Target_Angulo_Alfa", str(round(Alfa, 2)) + "  grados")
        self.param.SetParameter("Target_Angulo_Beta", str(round(Beta, 2)) + "  grados")

        self.actualiza_widget()
    

    def limpia_widget(self):
        #self.ledt1.setText("")
        #self.ledt2.setText("")
        self.ledt3.setText("")
        self.ledt4.setText("")
        self.ledt5.setText("")
        #self.ledt6.setText("")
        #self.ledt7.setText("")    
        pass


    def actualiza_widget(self):
        print("vino a actualiza widget.-")
        self.ledt1.setText(self.param.GetParameter("Marco"))
        self.ledt2.setText(self.param.GetParameter("Fiduciarios"))
        self.ledt3.setText(self.param.GetParameter("Target"))
        self.ledt4.setText(self.param.GetParameter("Entry"))
        self.ledt5.setText(self.param.GetParameter("Path_length"))
        #self.ledt6.setText(param.GetParameter("Target_Angulo_Alfa"))
        #self.ledt7.setText(param.GetParameter("Target_Angulo_Beta"))    
                

    def guarda(self):
        print("vino a guardar la Escena")
        # Create a new directory where the scene will be saved into
        ref_time = time.strftime("%Y%m%d-%H%M%S")
        sceneSaveDirectory = self.param.GetParameter("modulo_path") + "/Archivo/Escena_" + ref_time
        if not os.access(sceneSaveDirectory, os.F_OK):
            os.makedirs(sceneSaveDirectory)
        # Save the scene
        if slicer.app.applicationLogic().SaveSceneToSlicerDataBundleDirectory(sceneSaveDirectory, None):
            logging.info("Escena guardada en: {0}".format(sceneSaveDirectory))
        else:
            logging.error("Escena guardar falló")
        
        # Guarda los parametros
        self.param.SetParameter("Referencia_tiempo_guarda", ref_time)
        dictio = {}
        for item in self.param.GetParameterNames():
            dictio[item] = self.param.GetParameter(item)
        js = json.dumps(dictio)
        fp = open(sceneSaveDirectory + "/Parametros_" + ref_time + ".json", 'a')
        fp.write(js)
        fp.close()

 