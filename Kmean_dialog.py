
import os
import sys
import math
import numpy as np
import cv2
from .kmean import main
#from matplotlib import pyplot as plt

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap,QImage,QColor,QPainter,QPalette

if __name__ == 'ImprovedICP.Kmean_dialog':
    from qgis._core import QgsRasterLayer,QgsRasterViewPort,QgsPointXY,QgsRaster
    from qgis.core import QgsProject


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'K-mean_dialog_base.ui'))
MOOD = "OPENCV"


class KMeanDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(KMeanDialog, self).__init__(parent)
        self.leftPressed = False
        self.rightPressed = False
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.SMap.setScaledContents(True)

    def on_loadPic_clicked(self, bol = 2):
        """load图片"""
        if bol == 2:
            return
        fileName = QFileDialog.getOpenFileName(self,'打开一个png或jpg图片',os.path.dirname(__file__),r'png(*.png);jpg(*.jpg)')
        if fileName[0] == '':
            pass
        else :
            self.img3 = cv2.imread(fileName[0])
            img=cv2.cvtColor(self.img3,cv2.COLOR_BGRA2BGR)
            img2=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            _image = QImage(img2[:],img2.shape[1], img2.shape[0],(img2.shape[1]* 3)/4 * 4, QImage.Format_RGB888)
            self.Spixmap  = QPixmap.fromImage(_image)
            self.SMap.setPixmap(self.Spixmap)
            self.SMap.text = ''
            self.layerName.setEnabled(True)
            #self.pushDown.setEnabled(True)

    def on_layerName_textChanged(self, name):
        if self.layerName.text() == '':
            self.pushButton.setEnabled(False)
        else:
            self.pushButton.setEnabled(True)

    def on_pushButton_clicked(self, name = 's'):
        if name == 's':
            return
        img = self.img3
        if MOOD == "OPENCV":
            #change img(2D) to 1D
            img1 = img.reshape((img.shape[0]*img.shape[1],3))
            img1 = np.float32(img1)
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,10,1.0)
            flags = cv2.KMEANS_RANDOM_CENTERS
            compactness,labels,centers = cv2.kmeans(img1,self.spinBox.value(),None,criteria,10,flags)
        if MOOD == "MY_KMEAN":
            r = img.shape[0]*img.shape[1] / (self.spinBox.value() + 1)
            z = []
            for i in range(self.spinBox.value()):
                z.append(i * r)
            img1 = img.reshape((img.shape[0]*img.shape[1],3))
            img1 = np.float32(img1)
            tree = main(img1, z)
            for i in len(img1):
                img1[i] = tree[i]
        img2 = labels.reshape((img.shape[0],img.shape[1]))
        cv2.imwrite(self.layerName.text(),img2)
        layer = QgsRasterLayer(self.layerName.text(),'result')
        QgsProject.instance().addMapLayer(layer)