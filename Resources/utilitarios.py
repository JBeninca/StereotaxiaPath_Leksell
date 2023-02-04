# -*- coding: iso-8859-1 -*-
import os
import numpy as np
from __main__ import slicer, vtk


class util():
    def __init__(self):
        pass

    def Inicializa_Escena(self):
        slicer.mrmlScene.Clear(0)       
        modulo = slicer.util.modulePath("StereotaxiaPath")
        
        param = self.Genera_Nodo("vtkMRMLScriptedModuleNode", "Param_data")
        param.SetParameter("modulo", modulo)
        param.SetParameter("rooth_path", slicer.mrmlScene.GetRootDirectory())
        param.SetParameter("modulo_path", os.path.split(modulo)[0])
        param.SetParameter("archivo_path", os.path.split(modulo)[0] + "/Archivo")
        param.SetParameter("escena_path", os.path.split(modulo)[0] + "/Espacio_Marco/_Marco_Escene.mrml#")
        param.SetParameter("verdecito", "background-color:rgb(95, 127, 117)")
        param.SetParameter("rojito", "background-color:rgb(143, 84, 84)")
        param.SetParameter("amarillito", "background-color:rgb(214, 200, 139)")
        param.SetParameter("color_default", "background-color:")

        
    def cambia_window_level(self, widget, window, level):
        # Cambia el color y contraste de la TAC de slice RED
        lay = slicer.app.layoutManager()
        red_logic = lay.sliceWidget(widget).sliceLogic()
        red_cn = red_logic.GetSliceCompositeNode()
        red_volu_ID = red_cn.GetBackgroundVolumeID()
        volu_node = slicer.util.getNode(red_volu_ID)
        display_node = volu_node.GetDisplayNode()
        display_node.AutoWindowLevelOff()
        display_node.SetWindowLevel(window, level)
        print("Establecimiento de window & level a :", window, level)


    def obtiene_lista_volumenes(self):
        volu_nodos = slicer.util.getNodesByClass("vtkMRMLScalarVolumeNode")
        #print(volu_nodos)
        if len(volu_nodos) == 0 :
            texto = "ERROR: no hay volumenes cargados"
            slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
            return False
        else:
            return volu_nodos            


    def centra_nodo_de_widget(self, widget):
        node = slicer.app.layoutManager().sliceWidget(widget)
        node.sliceLogic().FitSliceToAll()
        print("Se ha centrado el nodo: ", widget)


    def modifica_origen_de_volumen(self, volu_nodo, origen):
        volu_nodo.SetOrigin(origen)


    def Genera_Nodo(self, clase, nombre_Nodo):
        self.borra_nodo_si_existe(nombre_Nodo)  # if exists
        nodo = slicer.mrmlScene.CreateNodeByClass(clase)
        nodo.SetName(nombre_Nodo)
        nodo.SetScene(slicer.mrmlScene)
        slicer.mrmlScene.AddNode(nodo)
        print("ha generado nodo =", nombre_Nodo)
        return nodo


    def genera_Markup(self, nombre):    
        self.borra_nodo_si_existe(nombre)  # if exists
        nodo = slicer.mrmlScene.CreateNodeByClass("vtkMRMLMarkupsFiducialNode")
        nodo.SetName(nombre)
        #nodo.SetScene(slicer.mrmlScene)
        slicer.mrmlScene.AddNode(nodo)
        print("ha generado nodo =", nombre)
        
        dnodo = nodo.GetDisplayNode()    # caracteristicas de display   
        dnodo.SetPropertiesLabelVisibility(False)   # no muestra texto
        dnodo.SetPointLabelsVisibility(False)
        dnodo.SetGlyphSize(6)           # valor en mm 
        dnodo.SetUseGlyphScale(False)   # valor absoluto del glyph
        dnodo.SetLineThickness(1)       # 100 % del glyfo
        dnodo.SetColor(0, 1.0, 0)         # color
        dnodo.SetSelectedColor(0, 1.0, 0)
        dnodo.SetActiveColor(0, 1.0, 0)
        
        return nodo    


    def borra_nodo_si_existe(self, nombre):
        try:
            nodo = slicer.util.getNode(nombre)   
            slicer.mrmlScene.RemoveNode(nodo)
            #print("el nodo " + nombre + " esta ya existe")
        except:
            pass


    def Borra_nodos_por_clase(self, clase):
        nodos = slicer.util.getNodesByClass(clase)
        for nodo in nodos:   # borra nodos antiguos
            print("ha borrado nodo =", nodo.GetName())
            slicer.mrmlScene.RemoveNode(nodo)


    def Borra_nodo(self, nombre_Nodo):
        try:
            nodo = slicer.util.getNode(nombre_Nodo)
            slicer.mrmlScene.RemoveNode(nodo)
            print("ha borrado =", nombre_Nodo)
        except:
            print("ha fallado en borrar nodo =", nombre_Nodo)


    def Borra_puntos_fiduciarios(self, nombre_Nodo):
        nodo = slicer.util.getNode(nombre_Nodo)
        nodo.RemoveAllMarkups()
        print("se removieron los markups de: ", nombre_Nodo)


    def Chequea_si_el_nodo_existe(self, nombre_Nodo):
        error = slicer.mrmlScene.GetFirstNodeByName(nombre_Nodo)
        return error


    def Renderiza_3D_Volumen(self, nodo_volu):
        nodo_logic = slicer.modules.volumerendering.logic()
        preset_name = "CT-Cardiac2"
        preset = nodo_logic.GetPresetByName(preset_name)
        #print("Este es logic preset name = ", preset.GetName())
        nodo_preset = slicer.mrmlScene.AddNode(preset)
        nodo_display = nodo_logic.CreateVolumeRenderingDisplayNode()
        slicer.mrmlScene.AddNode(nodo_display)
        nodo_display.UnRegister(nodo_logic)
        nodo_logic.UpdateDisplayNodeFromVolumeNode(nodo_display, nodo_volu, nodo_preset)
        nodo_volu.AddAndObserveDisplayNodeID(nodo_display.GetID())
        nodo_display.SetVisibility(1)


    def Yaw_y_Pitch(self, grados):
        threeDView = slicer.app.layoutManager().threeDWidget(0).threeDView()

        threeDView.setPitchRollYawIncrement(grados)
        threeDView.yawDirection = threeDView.YawRight
        threeDView.yaw()
        threeDView.pitchDirection = threeDView.PitchDown
        #threeDView.pitch()
        #threeDView.setZoomFactor(2.0)
        threeDView.zoomOut()
        threeDView.resetFocalPoint()
    
    def Serializador_de_Parametros(self):
        # TODO  aun incompleto la rutina
        transfe = slicer.util.getNode("Transfe_data")
        l1 = transfe.GetParameterNames()
        print(l1[0])
        print(type(l1))
        name =l1[0]
        print(transfe.GetParameter(name))
        pass


    def obtiene_volu_names(self, nodos):
        names = []
        for nodo in nodos:
            name = nodo.GetName()
            print(name)
            names.append(name)
        return names


    def obtiene_nodo_de_widget(self, widget):
        #print("obtiene nodo de volumen de = '", widget,"'")
        lay = slicer.app.layoutManager()
        logic = lay.sliceWidget(widget).sliceLogic()
        cn = logic.GetSliceCompositeNode()
        volu_ID = cn.GetBackgroundVolumeID()
        if volu_ID is None:
            texto = "ERROR: no hay volumenes cargados"
            print(texto)
            #slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
            return None    
        volu_nodo = slicer.mrmlScene.GetNodeByID(volu_ID)
        return volu_nodo


    def Obtiene_Centro_de_Masa(self, nodo_volu, fidu_nume, fidu_RAS, roi_size, umbral):
        """ calcula, con un filtro sobre la intensidad,
        el centroide de cada fiduciario"""
        
        #print("vino a Centro de Masa")
                
        matri = vtk.vtkMatrix4x4()
        nodo_volu.GetRASToIJKMatrix(matri)
        #print("RAS = ", fidu_RAS)
        IJK_fidu = matri.MultiplyPoint(tuple(fidu_RAS) + (1,))
        IJK_fidu = IJK_fidu[:3]
        # print("IJK_fiduciario =", IJK_fidu)
        # establece un cuadrado ROI
        roi_left = int(round((IJK_fidu[0]-(roi_size/2)), 0))
        roi_up = int(round((IJK_fidu[1]-(roi_size/2)), 0))
        #print("roi bordes: ", roi_left, roi_up)
        # obtencion del array del volumen
        z = int(IJK_fidu[2])

        #array_volumen = slicer.util.array(nodo_volu.GetName())
        array_volumen = slicer.util.arrayFromVolume(nodo_volu)  #3D
        array_plano = array_volumen[z]  # 2D
        #print(array_plano.shape)
        
        # ------------------ filtro -------------------
        
        centroid_x = centroid_y = 0.0
        cuenta = 0
        for x in range(roi_size):  #scann dentro del ROI
            for y in range(roi_size):
                esca = array_plano[roi_up + y, roi_left + x]
                if esca > umbral:   # filtro de intensidad de blanco
                    centroid_x += roi_left + x
                    centroid_y += roi_up + y
                    cuenta += 1
        if cuenta == 0:
            texto=("Error en la marcacion del punto Fiduciario.")
            print(texto)
            slicer.util.warningDisplay(texto, windowTitle="Error !", parent=None, standardButtons=None)
            IJK_corregido = IJK_fidu
            return IJK_corregido
        else:
            centroid_x /= cuenta
            centroid_y /= cuenta
            #print("cuenta punto por encima del umbral (", umbral,") = ", cuenta)
            IJK_corregido = [centroid_x, centroid_y, z]
        
        # transformacion a sistema RAS
        matri2 = vtk.vtkMatrix4x4()
        nodo_volu.GetIJKToRASMatrix(matri2)
        fidu_RAS_correg = matri2.MultiplyPoint(tuple(IJK_corregido) + (1,))
    
        print(self.redondea(fidu_RAS_correg, 2))
        return fidu_RAS_correg


    def impri_layout_markup(self, texto):
        # inscribe en slice
        fidu_node = slicer.util.getNode("Target")
        fidu_node.SetNthMarkupSelected(0, False)
        fidu_node.SetNthMarkupLabel(0, texto)
        #fidu_node.SetNthMarkupDescription(0, str(arg2))


    def impri_layout_2D(self, widget, texto, esquina):
        view=slicer.app.layoutManager().sliceWidget(widget).sliceView()
        # Set text to "Something"
        view.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.UpperLeft, texto)
        # Set color to yellow
        view.cornerAnnotation().GetTextProperty().SetColor(1,1,0)
        # Update the view
        view.forceRender()
        

    def calcula_angulos_con_nodo(self, Target, Entry):
        #import math
        x = Entry[0]-Target[0]
        y = Entry[1]-Target[1]
        z = Entry[2]-Target[2]
        
        alfa = self.Genera_Nodo("vtkMRMLMarkupsAngleNode", "Alfa")
        alfa.SetAngleMeasurementMode(2)
        alfa.SetDisplayVisibility(False)
        puntoA = vtk.vtkVector3d(0, -100, 0)  # eje Y
        puntoB = vtk.vtkVector3d(0, 0, 0)
        puntoC = vtk.vtkVector3d(0, y, z)     # solo 2D
        alfa.AddControlPoint(puntoA)
        alfa.AddControlPoint(puntoB)
        alfa.AddControlPoint(puntoC)
        angulo_Alfa = alfa.GetAngleDegrees()
        
        beta = self.Genera_Nodo("vtkMRMLMarkupsAngleNode", "Beta")
        beta.SetAngleMeasurementMode(0)
        beta.SetDisplayVisibility(False)
        if x >= 0:  
            puntoA = vtk.vtkVector3d(100, 0, 0)  # eje X
        else:
            puntoA = vtk.vtkVector3d(-100, 0, 0)  # eje X
        puntoB = vtk.vtkVector3d(0, 0, 0)
        puntoC = vtk.vtkVector3d(x, 0, z)     # calculo en 2D
        beta.AddControlPoint(puntoA)
        beta.AddControlPoint(puntoB)
        beta.AddControlPoint(puntoC)
        angulo_Beta = beta.GetAngleDegrees()
        
        return angulo_Alfa, angulo_Beta

    def calcula_angulos_con_vtk(self, Target, Entry):
        Target = np.array(Target)
        Entry = np.array(Entry)
        
        #print("calculos con vtk")
        path_vector = (Entry - Target)/np.linalg.norm(Entry - Target)
        ref_Y = np.array([0, -100, 0]) / np.linalg.norm(np.array([0, -100, 0]))
        
        path_Y_Z = np.array([0, path_vector[1], path_vector[2]])
        angRad = vtk.vtkMath.AngleBetweenVectors(path_Y_Z, ref_Y)
        angAlfa = vtk.vtkMath.DegreesFromRadians(angRad)
        
        if path_vector[0] >= 0:  
            ref_X = np.array([100, 0, 0])
        else:
            ref_X = np.array([-100, 0, 0])
                   
        path_X_Z = np.array([path_vector[0], 0, path_vector[2]])
        angRad = vtk.vtkMath.AngleBetweenVectors(path_X_Z, ref_X)
        angBeta = vtk.vtkMath.DegreesFromRadians(angRad)

        #print(angAlfa, angBeta)
        return angAlfa, angBeta        
        

    def calcula_angulos_simple(self, Target, Entry):
        # https://www.geometriaanalitica.info/como-calcular-el-angulo-entre-dos-vectores-ejemplos-ejercicios-resueltos/#:~:text=El%20coseno%20del%20%C3%A1ngulo%20que,m%C3%B3dulos%20de%20los%20dos%20vectores.
        Target = np.array(Target)
        Entry = np.array(Entry)
        #print("calculos de angulos ", Entry-Target)
        path_vector = Entry - Target
        #print(path_vector)

        # cálculo en plano frontal,  y/z, ang Alfa
        if path_vector[0] >= 0:  
            v_1 = [100, 0]
        else:
            v_1 = [-100, 0]
        v_2 = [path_vector[1], path_vector[2]]
        mod1 = np.sqrt(np.square(v_1[0]) + np.square(v_1[1]))
        mod2 = np.sqrt(np.square(v_2[0]) + np.square(v_2[1]))
        #print(v_2, mod1, mod2)
        escalar1 = v_1[0] * v_2[0] + v_1[1] * v_2[1]
        cos_a = escalar1/(mod1 * mod2)
        rad = np.arccos(cos_a)
        angAlfa = np.rad2deg(rad)
        
        # cálculo en plano lateral, x/z, ang Beta
        v_3 = [100, 0]
        v_4 = [path_vector[0], path_vector[2]]
        mod3 = np.sqrt(np.square(v_3[0]) + np.square(v_3[1]))
        mod4 = np.sqrt(np.square(v_4[0]) + np.square(v_4[1]))
        #print(v_4,mod1, mod2)
        escalar2 = v_3[0] * v_4[0] + v_3[1] * v_4[1]
        cos_b = escalar2/(mod3 * mod4)
        rad = np.arccos(cos_b)
        angBeta = np.rad2deg(rad)
        
        #print(angAlfa, angBeta)
        return angAlfa, angBeta        


    def genera_linea(self, Target, Entry):
        nodo_path = self.Genera_Nodo("vtkMRMLMarkupsLineNode", "Path")
       
        nodo_path.AddControlPointWorld(vtk.vtkVector3d(Target))
        nodo_path.AddControlPointWorld(vtk.vtkVector3d(Entry))
        nodo_path.SetNthMarkupLabel(0, "T")
        nodo_path.SetNthMarkupLabel(1, "E")
        
        dnodo = nodo_path.GetDisplayNode()    # caracteristicas de display   
        dnodo.SetPointLabelsVisibility(True)
        dnodo.SetPropertiesLabelVisibility(False)   # no muestra texto
        
        dnodo.SetGlyphType(6)
        dnodo.SetUseGlyphScale(False)     # valor absoluto del glyph
        dnodo.SetLineThickness(0.5)       #  % del glyfo
        dnodo.SetColor(0, 1.0, 0)         # color
        dnodo.SetSelectedColor(0, 1.0, 0)
        dnodo.SetActiveColor(1.0, 1.0, 0)
        dnodo.SetSliceProjection(True)
        dnodo.SetSliceProjectionUseFiducialColor(True)
        dnodo.SetSliceProjectionOpacity(0.2)     

        return nodo_path


    def ubicar_la_punta_en_RPN(self, p_RAS):
        #print("punta =", p_RAS)

        layoutManager = slicer.app.layoutManager()

        rLogic = layoutManager.sliceWidget("Red").sliceLogic()
        rLogic.FitSliceToAll() #https://discourse.slicer.org/t/resize-window-to-fit-data/8563/7
        rLogic.SetSliceOffset(p_RAS[2])     # axial
        
        gLogic = layoutManager.sliceWidget("Green").sliceLogic()
        gLogic.FitSliceToAll()
        gLogic.SetSliceOffset(p_RAS[1])     # lateral
        
        yLogic = layoutManager.sliceWidget("Yellow").sliceLogic()
        yLogic.FitSliceToAll()
        yLogic.SetSliceOffset(p_RAS[0])    # frontal


    def redondea(self, punto, decimales):
        punto_out = []
        for p in punto:
            p_o = round(p, decimales)
            punto_out.append(p_o)
        return punto_out


    def redondea_lista_de_puntos(self, lista_in, decimales):
        from copy import deepcopy
        lista_out = deepcopy(lista_in)
        for punto in lista_out:
            punto[:] = map(lambda x: round(x, decimales), punto)
        return lista_out

    def chequea_errores(param):
        if param["Geometria"] ==  "marco":
            return "no se ha elegido bien el marco"
        else:
            return "ok"
