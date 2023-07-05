# import sys
# import os

# from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
# from PySide6.QtCore import QFile
# from PySide6.QtUiTools import QUiLoader
# from PySide6.QtGui import QPixmap, QImage
# from PySide6.QtCore import QThread, Signal, QDir
# import cv2


# def convertCVImage2QtImage(cv_img):
#     cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
#     height, width, channel = cv_img.shape
#     bytesPerLine = 3 * width
#     qimg = QImage(cv_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
#     return QPixmap.fromImage(qimg)


# class ProcessImage(QThread):
#     signal_show_frame = Signal(object)

#     def __init__(self, fileName):
#         QThread.__init__(self)
#         self.fileName = fileName

#         from detector import Detector
#         self.detector = Detector()

#     def run(self):
#         self.video = cv2.VideoCapture(self.fileName)
#         while True:
#             valid, self.frame = self.video.read()
#             if valid is not True:
#                 break
#             self.frame = self.detector.detect(self.frame)
#             self.signal_show_frame.emit(self.frame)
#             cv2.waitKey(30)
#         self.video.release()

#     def stop(self):
#         try:
#             self.video.release()
#         except:
#             pass


# class show(QThread):
#     signal_show_image = Signal(object)

#     def __init__(self, fileName):
#         QThread.__init__(self)
#         self.fileName = fileName
#         self.video=cv2.VideoCapture(self.fileName)

#     def run(self): 
#         while True:
#             valid, self.frame = self.video.read()
#             if valid is not True:
#                 break
#             self.signal_show_image.emit(self.frame)
#             cv2.waitKey(30)
#         self.video.release()

#     def stop(self):
#         try:
#             self.video.release()
#         except:
#             pass


# class MainWindow(QWidget):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         loader = QUiLoader()
#         self.ui = loader.load("ui/form.ui")
        
#         self.ui.btn_browse.clicked.connect(self.getFile)
#         self.ui.btn_start.clicked.connect(self.predict)

#         self.ui.show()

#     def getFile(self):
#         self.fileName = QFileDialog.getOpenFileName(self,'Single File','C:\'','*.jpg *.mp4 *.jpeg *.png *.avi')[0]
#         self.ui.txt_address.setText(str(self.fileName))
#         self.show=show(self.fileName)
#         self.show.signal_show_image.connect(self.show_input)
#         self.show.start()
        
        
#     def predict(self):
#         self.process_image = ProcessImage(self.fileName)
#         self.process_image.signal_show_frame.connect(self.show_output)
#         self.process_image.start()

#     def show_input(self, image):
#         pixmap = convertCVImage2QtImage(image)
#         self.ui.lbl_input.setPixmap(pixmap)

#     def show_output(self, image):
#         pixmap = convertCVImage2QtImage(image)
#         self.ui.lbl_output.setPixmap(pixmap)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     widget = MainWindow()
#     sys.exit(app.exec())




import sys
import os
import numpy as np
from DataScience.detector import Detector

# from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
# from PySide6.QtCore import QFile
# from PySide6.QtUiTools import QUiLoader
# from PySide6.QtGui import QPixmap, QImage
# from PySide6.QtCore import QThread, Signal, QDir
import cv2
import base64


# def convertCVImage2QtImage(cv_img):
#     cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
#     height, width, channel = cv_img.shape
#     bytesPerLine = 3 * width
#     qimg = QImage(cv_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
#     return QPixmap.fromImage(qimg)


# class ProcessImage(QThread):
#     signal_show_frame = Signal(object)

#     def __init__(self, fileName):
#         QThread.__init__(self)
#         self.fileName = fileName

      
#         self.detector = Detector()

#     def run(self):
#         self.video = cv2.VideoCapture(self.fileName)
#         while True:
#             valid, self.frame = self.video.read()
#             if valid is not True:
#                 break
#             self.frame = self.detector.detect(self.frame)
#             self.signal_show_frame.emit(self.frame)
#             cv2.waitKey(30)
#         self.video.release()

#     def stop(self):
#         try:
#             self.video.release()
#         except:
#             pass


# class Show(QThread):
#     signal_show_image = Signal(object)

#     def __init__(self, fileName):
#         QThread.__init__(self)
#         self.fileName = fileName
#         self.video = cv2.VideoCapture(self.fileName)

#     def run(self): 
#         while True:
#             valid, self.frame = self.video.read()
#             if valid is not True:
#                 break
#             self.signal_show_image.emit(self.frame)
#             cv2.waitKey(30)
#         self.video.release()

#     def stop(self):
#         try:
#             self.video.release()
#         except:
#             pass


# class MainWindow(QWidget):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         loader = QUiLoader()
#         self.ui = loader.load(QFile("ui/form.ui"))
        
#         self.ui.btn_browse.clicked.connect(self.getFile)
#         self.ui.btn_start.clicked.connect(self.predict)

#         self.ui.show()

#     def getFile(self):
#         self.fileName, _ = QFileDialog.getOpenFileName(self, 'Single File', 'C:\\', '*.jpg *.mp4 *.jpeg *.png *.avi')
#         self.ui.txt_address.setText(str(self.fileName))
#         self.show_thread = Show(self.fileName)
#         self.show_thread.signal_show_image.connect(self.show_input)
#         self.show_thread.start()
        
        
#     def predict(self):
#         self.process_image = ProcessImage(self.fileName)
#         self.process_image.signal_show_frame.connect(self.show_output)
#         self.process_image.start()

#     def show_input(self, image):
#         cv_img = self.convert_image(image)
#         pixmap = convertCVImage2QtImage(cv_img)
#         self.ui.lbl_input.setPixmap(pixmap)

#     def show_output(self, image):
#         cv_img = self.convert_image(image)
#         pixmap = convertCVImage2QtImage(cv_img)
#         self.ui.lbl_output.setPixmap(pixmap)

#     @staticmethod
#     def convert_image(image):
#         if isinstance(image, tuple):
#             return image[0]
#         elif isinstance(image, list):
#             return image[0]
#         elif isinstance(image, np.ndarray):
#             if len(image.shape) == 2:
#                 return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
#             elif len(image.shape) == 3 and image.shape[2] == 3:
#                 return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             elif len(image.shape) == 3 and image.shape[2] == 4:
#                 return cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
#         return image


# class ProcessImage:
#     def __init__(self, fileName):
#         self.fileName = fileName
#         self.detector = Detector()

#     def run(self):
#         image = cv2.imread(self.fileName)
#         print(type(image))
#         if image is not None:
#             processed_image = self.detector.detect(image)
#             return processed_image
#         else:
#             print("Failed to read image")
#             return None


# if __name__ == "__main__":
#     # Prompt the user for the image file path
#     image_path = input("Enter the path of the image file: ")

#     # Create an instance of ProcessImage
#     process_image = ProcessImage(image_path)

#     # Run the image processing
#     # print(type(process_image))
#     processed_image = process_image.run()

#     if processed_image is not None:
#         # Print the results or perform further processing
     
#         for elements in processed_image:
#             print("elements->",elements)






# if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # widget = MainWindow()
    # sys.exit(app.exec())


class ProcessImage:
    
    def __init__(self, base64_string):
        self.base64_string = base64_string

        self.detector = Detector()

    def run(self):
        # Decode the base64 string to bytes
        image_data = base64.b64decode(self.base64_string)
        
        # Convert the bytes to a numpy array
        image_array = np.frombuffer(image_data, np.uint8)
        
        # Decode the numpy array as an image
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        if image is not None:
            processed_image = self.detector.detect(image)
            return processed_image
        else:
            print("Failed to decode image")
            return None

# Prompt the user for the base64 string of the image
# base64_string = input("Enter the base64 string of the image: ")

# # Create an instance of ProcessImage
# process_image = ProcessImage(base64_string)

# # Run the image processing
# processed_image = process_image.run()

# if processed_image is not None:
#     # Print the results or perform further processing
#     for elements in processed_image:
#         print("elements->", elements)











