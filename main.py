import os
import sys
from PyQt5 import QtWidgets
from mainWindow import Ui_MainWindow

# matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from skimage import io
from skimage.filters import threshold_local

class Application(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(Application, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # enable drag and drop
        self.setAcceptDrops(True)

        # set matplotlib FigureCanvas
        self.fig = Figure()
        self.FigureCanvas = FigureCanvas(self.fig)
        self.ax1 = self.fig.add_subplot(1,2,1)
        self.ax1.set_axis_off()
        self.ax2 = self.fig.add_subplot(1,2,2)
        self.ax2.set_axis_off()
        self.ui.imageLayout.addWidget(self.FigureCanvas)

        # button
        self.ui.pushButton_exec.clicked.connect(self.onClick_exec)
        self.ui.pushButton_save.clicked.connect(self.onClick_save)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/uri-list'):
            e.accept()
        else:
            e.ignore()
    
    def dropEvent(self, e):
        # ファイルパスを取得する
        urls = e.mimeData().text().split("\n")
        self.filepath = urls[0][8:]
        self.ui.infoLabel.setText("file: " + self.filepath)

        # display image
        self.image = io.imread(self.filepath)
        self.plotImage(self.ax1, self.image, "original image")

        # local thresholding
        self.plotLocalThresholdingImage()
    
    def onClick_exec(self):
        self.plotLocalThresholdingImage()
    
    def plotLocalThresholdingImage(self):
        # local thresholding
        blksize = int(self.ui.spinBox_blocksize.text())
        local_thresh = threshold_local(self.image, blksize)
        self.binimage = self.image > local_thresh
        
        # plot image
        self.plotImage(self.ax2, self.binimage, 'binary image')

    def plotImage(self, axes, image, title='image'):
        axes.clear()
        axes.set_title(title)
        axes.imshow(image, cmap='gray')
        axes.set_axis_off()

        # redraw
        self.FigureCanvas.draw()
    
    def onClick_save(self):
        # show file chooser
        savename = QtWidgets.QFileDialog.getSaveFileName(self, 'save file', os.path.dirname(self.filepath), "PNG Image (*.png)")
        if savename[0]:
            print(savename[0])
            io.imsave(savename[0], self.binimage * 255)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())
