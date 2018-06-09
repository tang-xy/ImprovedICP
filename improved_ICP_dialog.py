# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ImprovedICPDialog
                                 A QGIS plugin
 Grid map fusion Qgis plugin using improved ICP algorithm
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-06-06
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Tang-XY
        email                : 2015302590078@whu.edu.cn
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import sys

import numpy as np
import cv2
#from matplotlib import pyplot as plt

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap,QImage,QColor,QPainter

if __name__ == 'ImprovedICP.improved_ICP_dialog':
    from qgis._core import QgsRasterLayer,QgsRasterViewPort,QgsPointXY,QgsRaster


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'improved_ICP_dialog_base.ui'))
MOOD = "test"


class ImprovedICPDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ImprovedICPDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

    def setupQgisUI(self, iface):
        """动态加载qgis相关配置"""

        self.TMap.setScaledContents(True)
        self.iface = iface

        #获取图层
        canvas = iface.mapCanvas()
        layerList = canvas.layers()

        #清除原有列表
        self.TargetName.clear()
        self.SourceName.clear()

        #添加基础选项中图层下拉菜单
        self.TargetName.addItem('')
        self.SourceName.addItem('')
        for layer in layerList:
            if isinstance(layer,QgsRasterLayer):
                self.TargetName.addItem(layer.name())
                self.SourceName.addItem(layer.name())
    
    def getArrayfromLayer(self,layer):
        extent = layer.extent()
        width = int(extent.width())
        height = int(extent.height())
        res = np.zeros((height, width, layer.bandCount()))
        
        for j in range(width):
            for k in range(height):
                ident = layer.dataProvider().identify(QgsPointXY(extent.xMinimum() + j, extent.yMaximum() - k), QgsRaster.IdentifyFormatValue)
                for i in range(layer.bandCount()):
                    res[k,j,i] = ident.results()[i + 1]
        return res

    def getQimagebyIndex(self, index):
        """通过图层序号获取图层并保存"""
        canvas = self.iface.mapCanvas()
        layerList = canvas.layers()
        extent = layerList[index].extent()
        viewPort = QgsRasterViewPort()
        viewPort.mBottomRightPoint = QgsPointXY(-100,-100)
        viewPort.mTopLeftPoint = QgsPointXY(100,100)
        if MOOD == 'test':
            self.narray = cv2.imread("D:\\Desktop\\TM\\bm.jpg")
            img=cv2.cvtColor(self.narray,cv2.COLOR_BGRA2BGR)
        else:
            self.narray = self.getArrayfromLayer(layerList[index])
            img=self.narray.astype(np.float32)
            img=cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)
        img2=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        _image = QImage(img2[:],img2.shape[1], img2.shape[0],(img2.shape[1]* 3)/4 * 4, QImage.Format_RGB888)
        cv2.imwrite("D:\\Desktop\\bm.jpg",img2)
        return _image

    def on_TargetName_currentIndexChanged(self, layerName):
        """设置其他控件可用性随Targrt变化
           设置选中目标图层后相应
           重绘图片大小
        """
        if type(layerName) == str:
            return
        if layerName > 0:
            self.SourceName.setEnabled(True)
            self.OutputName.setEnabled(True)
            self.SelectOutputPath.setEnabled(True)
            image = self.getQimagebyIndex(layerName - 1)
            self.pixmap  = QPixmap.fromImage(image)
            #self.fitPixmap = pixmap.scaled(50, 50,aspectRatioMode = QtCore.Qt.KeepAspectRatio)#1 = Qtcore.Qt.KeepAspectRatio
            self.TMap.resize(150,self.pixmap.height()/self.pixmap.width()*150)
            self.TMap.move(self.PicBox.width()/2-self.TMap.width()/2,self.PicBox.height()/2-self.TMap.height()/2)
            self.TMap.setPixmap(self.pixmap)
        if layerName == 0:
            self.SourceName.setEnabled(False)
            self.OutputName.setEnabled(False)
            self.SelectOutputPath.setEnabled(False)
            self.OutputName.setText('')
            self.pixmap = QPixmap(0,0)
            self.TMap.setPixmap(self.pixmap)

    def on_SourceName_currentIndexChanged(self, layerName):
        """绘制源图片"""
        if type(layerName) == str:
            return
        if layerName > 0:
            image = self.getQimagebyIndex(layerName - 1)
            self.Spixmap  = QPixmap.fromImage(image)
            #self.fitPixmap = pixmap.scaled(50, 50,aspectRatioMode = QtCore.Qt.KeepAspectRatio)#1 = Qtcore.Qt.KeepAspectRatio
            self.SMap.resize(150,self.pixmap.height()/self.pixmap.width()*150)
            self.SMap.move(self.PicBox.width()/2,self.PicBox.height()/2)
            self.SMap.setPixmap(self.pixmap)
        if layerName == 0:
            self.pixmap = QPixmap(0,0)
            self.TMap.setPixmap(self.pixmap)
            
    
    def on_SelectOutputPath_clicked(self, bol = 2):
        """保存图片"""
        if bol == 2:
            return
        fileName = QFileDialog.getSaveFileName(self,'创建bmp图片并保存',os.path.dirname(__file__),r'bmp(*.bmp)')
        if fileName[0] == ' ':
            pass
        else :
            self.OutputName.setText(fileName[0])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tetris = ImprovedICPDialog()
    narray = cv2.imread("D:\\Desktop\\TM\\bm.jpg")
    #img=img.astype(np.float32)
    #img=cv2.cvtColor(self.narray,cv2.COLOR_BGRA2BGR)
    img2=cv2.cvtColor(narray,cv2.COLOR_BGR2RGB)
    tetris.show()
    
    sys.exit(app.exec_())
