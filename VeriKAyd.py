import os
try:
    import PyQt5
except:
    command = "pip install PyQt5"
    os.system(command)
try:
    import pandas as pd
except:
    command = "pip install pandas"
    os.system(command)
    import pandas as pd
try:
    import numpy as np
except:
    command = "pip install numpy"
    os.system(command)
    import numpy as np
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import date
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import pandas as pd
import string
import random, pytesseract
from pdf2image import convert_from_path

import json, pathlib,cv2

class ClassWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ClassWidget, self).__init__(parent)
        self.setGeometry(QtCore.QRect(200, 100, 670, 360))
        # image
        self.pdf = QLabel(self)
        

        #self.converter = converter.spot2csv(dir = pdfs_dir)
        #self.id_path = self.converter.id2file_name()

        self.info = info_class()
        
        self.info.index_textbox.textChanged.connect(self.update_image)
        
        self.right_topcon = data_class(type='topcon', side='SAĞ')
        self.left_topcon = data_class(type='topcon', side='SOL')
        self.right_spot = data_class(type='spot', side='SAĞ')
        self.left_spot = data_class(type='spot', side='SOL')
        
        self.button = QPushButton('Kaydet',self)
        self.button.setToolTip('Veriyi Eklemek İçin Tıklaynız!')
        self.button.setCheckable(False)

        self.button.setIcon(QIcon("save.jpg"))
        self.button.setIconSize(QSize(50,50))
        self.button.resize(30,10)

        self.grid = QtWidgets.QGridLayout(self)
        self.grid.addWidget(self.info, 0, 0,1,6)
        self.grid.addWidget(self.pdf, 0, 6,-1,14)
        self.grid.addWidget(self.right_topcon, 1, 0,1,3)
        self.grid.addWidget(self.left_topcon, 1, 3,1,3)
        self.grid.addWidget(self.right_spot, 2, 0,1,3)
        self.grid.addWidget(self.left_spot, 2, 3,1,3)
        self.grid.addWidget(self.button,3,5,-1,1)
        self.button.clicked.connect(self.on_click)
        self.showMaximized()

    def update_image(self):
        id = self.info.index_textbox.text()
        
        if id in self.info.id2name:
            print('-----------------------------')
            print(self.info.info[id])
            print('-----------------------------')
            path = f'./{self.info.id2name[id]}'
            _,_,image = self.info.pdf2image(path)
            image = cv2.resize(image,(750,1000))
            image = image[:600,:500]
            cv2.imwrite('image.jpg',image)
            self.path = f'./image.jpg'
            # Create widget
            self.right_spot.update_values(self.info.info[id]['right'])
            self.left_spot.update_values(self.info.info[id]['left'])
            #self.grid.addWidget(self.right_spot, 2, 0,1,3)
            #self.grid.addWidget(self.left_spot, 2, 3,1,3)
            #self.grid.update()
            pixmap = QPixmap(self.path)
            self.pdf.setPixmap(pixmap)
            self.resize(pixmap.width(),pixmap.height())
            self.show()

    @pyqtSlot()
    def on_click(self): #button clicked
        value_control = [self.right_topcon.ds_text.text().replace(",","."),\
                        self.right_topcon.dc_text.text().replace(",","."),\
                        self.right_topcon.se_text.text().replace(",","."),\
                        self.left_topcon.ds_text.text().replace(",","."),\
                        self.left_topcon.dc_text.text().replace(",","."),\
                        self.left_topcon.se_text.text().replace(",",".")]

        value_control = [(True if (len(_a2_)==0 or 20>float(_a2_)>-20 and float(_a2_)%0.25==0) else False) for _a2_ in value_control]
        
        if not all(value_control)==True:
            
            msgBox4 = QMessageBox.about(self,"DS-DC-SE Veri giriş Hatası","Ds-Dc-Se Değerleri 20 den büyük olamaz ve 0.25 katları olmaldır!")
        else:

            ax_control = [self.left_topcon.ax_text.text(),\
                        self.right_topcon.ax_text.text(),\
                        self.left_spot.ax_text.text(),\
                        self.left_spot.ax_text.text()]
            ax_control = [(True if (len(_a2_)==0 or 180>=float(_a2_)>=0) else False) for _a2_ in ax_control]
            
            if not all(ax_control)==True:
                msgBox3 = QMessageBox.about(self,"AX Veri giriş Hatası","Ax 0 ile 180 arasında olmalıdır!") 
            else:
                    
                if len(str(self.info.index_textbox.text())) == 0 : 
                    msgBox2 = QMessageBox.about(self,"Eksik Veri","Index girişi yapılmadı!")        
                else:
                    msgBox1 = QMessageBox()
                    msgBox1.setIcon(QMessageBox.Question)
                    msgBox1.setText("Veriyi Kaydetmek İstiyormusunuz?")
                    msgBox1.setWindowTitle("Kaydetme")
                    msgBox1.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    

                    returnValue = msgBox1.exec()
                    if returnValue == QMessageBox.Ok:
                        self.data_transfer()
                        
                        msgBox = QMessageBox()
                        msgBox.setIcon(QMessageBox.Question)
                        msgBox.setText("Veri Kaydetme Başarılı! \nTabloyu Temizlemek İstiyormusunuz?")
                        msgBox.setWindowTitle("Temizle")
                        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                        

                        returnValue = msgBox.exec()
                        if returnValue == QMessageBox.Ok:
                            self.info.index_textbox.clear()
                            self.info.yas_textbox.clear()
                            self.info.radio_button_kad.setChecked(False)
                            self.info.radio_button_er.setChecked(False)
                            self.info.radio_button_others.setChecked(False)
                            
                            self.info.yas_textbox.clear()
                            self.info.pam_textbox.clear()
                            #self.lux_textbox.clear()

                            self.left_topcon.ds_text.clear()
                            self.left_topcon.dc_text.clear()
                            self.left_topcon.ax_text.clear()
                            self.left_topcon.se_text.clear()
                            self.left_topcon.pc_text.clear()


                            self.right_topcon.ds_text.clear()
                            self.right_topcon.dc_text.clear()
                            self.right_topcon.ax_text.clear()
                            self.right_topcon.se_text.clear()
                            self.right_topcon.pc_text.clear()

                            self.left_spot.ds_text.clear()
                            self.left_spot.dc_text.clear()
                            self.left_spot.ax_text.clear()
                            self.left_spot.se_text.clear()
                            self.left_spot.pc_text.clear()

                            self.right_spot.ds_text.clear()
                            self.right_spot.dc_text.clear()
                            self.right_spot.ax_text.clear()
                            self.right_spot.se_text.clear()
                            self.right_spot.pc_text.clear()

    def data_transfer(self):
        
        data_csv = pd.read_csv('data.csv',delimiter=",")
        
        #print('Length of Csv:',len(data_csv))
        
        cinsiyet_val = None
        if (self.info.radio_button_er.isChecked() == True):
            cinsiyet_val = 'Erkek'
        elif (self.info.radio_button_kad.isChecked() == True):
            cinsiyet_val = 'Kadin'
        elif (self.info.radio_button_others.isChecked() == True):
            cinsiyet_val = 'Belirsiz'
        
        date_value = str(self.info.date.date()).split("(")[-1][:-1]
        index_top  = 'N'+ str(self.info.index_textbox.text())

        top_r_ds = str(self.right_topcon.ds_text.text())
        top_r_ds = top_r_ds.replace(",",".")

        top_r_dc = str(self.right_topcon.dc_text.text())
        top_r_dc = top_r_dc.replace(",",".")

        top_r_ax = str(self.right_topcon.ax_text.text())
        
        top_r_se = str(self.right_topcon.se_text.text())
        top_r_se = top_r_se.replace(",",".")

        top_r_pc = str(self.right_topcon.pc_text.text())
        top_r_pc = top_r_pc.replace(",",".")
        
        top_l_ds = str(self.left_topcon.ds_text.text())
        top_l_ds = top_l_ds.replace(",",".")

        top_l_dc = str(self.left_topcon.dc_text.text())
        top_l_dc = top_l_dc.replace(",",".")

        top_l_ax = str(self.left_topcon.ax_text.text())
        top_l_ax = top_l_ax.replace(",",".")

        top_l_se = str(self.left_topcon.se_text.text())
        top_l_se = top_l_se.replace(",",".")

        top_l_pc = str(self.left_topcon.pc_text.text())
        top_l_pc = top_l_pc.replace(",",".")

        pam = str(self.info.pam_textbox.text())
        pam = pam.replace(",",".")
        
        new_row = {'Index':index_top,
                    'Cinsiyet':str(cinsiyet_val),
                    'Yas':str(self.info.yas_textbox.text()),
                    'Device':'TOPCON',
                    'Right_DS':top_r_ds,
                    'Right_DC':top_r_dc,
                    'Right_AX':top_r_ax,
                    'Right_SE':top_r_se,
                    'Right_Pupil_Cap':top_r_pc,
                    'Left_DS':top_l_ds,
                    'Left_DC':top_l_dc,
                    'Left_AX':top_l_ax,
                    'Left_SE':top_l_se,
                    'Left_Pupil_Cap':top_l_pc,
                    'Pupil_Arasi_Mesafe':pam,
                    'Luxmetre':str(self.info.lux_textbox.text()),
                    'Tarih':date_value
                    }
        index_spot = 'N' + str(self.info.index_textbox.text())

        spot_r_ds = str(self.right_spot.ds_text.text())
        spot_r_ds = spot_r_ds.replace(",",".")

        spot_r_dc = str(self.right_spot.dc_text.text())
        spot_r_dc = spot_r_dc.replace(",",".")

        spot_r_ax = str(self.right_spot.ax_text.text())
        spot_r_ax = spot_r_ax.replace(",",".")

        spot_r_se = str(self.right_spot.se_text.text())
        spot_r_se = spot_r_se.replace(",",".")

        spot_r_pc = str(self.right_spot.pc_text.text())
        spot_r_pc = spot_r_pc.replace(",",".")

        spot_l_ds = str(self.left_spot.ds_text.text())
        spot_l_ds = spot_l_ds.replace(",",".")

        spot_l_dc = str(self.left_spot.dc_text.text())
        spot_l_dc = spot_l_dc.replace(",",".")

        spot_l_ax = str(self.left_spot.ax_text.text())
        spot_l_ax = spot_l_ax.replace(",",".")

        spot_l_se = str(self.left_spot.se_text.text())
        spot_l_se = spot_l_se.replace(",",".") 

        spot_l_pc = str(self.left_spot.pc_text.text())
        spot_l_pc = spot_l_pc.replace(",",".")

        new_row_spot = {'Index':index_spot,
                    'Cinsiyet':str(cinsiyet_val),
                    'Yas':str(self.info.yas_textbox.text()),
                    'Device':'SPOT',
                    'Right_DS':spot_r_ds,
                    'Right_DC':spot_r_dc,
                    'Right_AX':spot_r_ax,
                    'Right_SE':spot_r_se,
                    'Right_Pupil_Cap':spot_r_pc,
                    'Left_DS':spot_l_ds,
                    'Left_DC':spot_l_dc,
                    'Left_AX':spot_l_ax,
                    'Left_SE':spot_l_se,
                    'Left_Pupil_Cap':spot_l_pc,
                    'Pupil_Arasi_Mesafe':pam,
                    'Luxmetre':str(self.info.lux_textbox.text()),
                    'Tarih':date_value
                    }
        rows = {"Topcon":new_row,"Spot":new_row_spot}
        #saved json
    
        self.entry_saved(rows,index_top)

        data_csv = data_csv.append(new_row, ignore_index=True)
        data_csv = data_csv.append(new_row_spot, ignore_index=True)
        
        try:
            data_csv.to_csv('data.csv',index=False)
        except Exception as e:
            print(e)
        
    def keyPressEvent(self, event):
        #print(event.key())
        if event.key() == Qt.Key_Enter:
            self.on_click()

        elif event.key() == Qt.Key_Escape: #esc
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Gerçekten Kapatmak İstiyormusun?")
            msgBox.setWindowTitle("KAPAT")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                QCoreApplication.instance().quit()
     
    def entry_saved(self,dict_,index):
        data_name = list(os.listdir('Documents/')) 
        if (f'{index}.json') in data_name:
            with open(f'Documents/{index}*.json','a') as json_file:
                json.dump(dict_,json_file)
        else:
            with open(f'Documents/{index}.json','a') as json_file:
                json.dump(dict_,json_file)
    
        json_file.close()
    

class info_class(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(info_class, self).__init__(parent)
        ##
        self.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Normal, italic=False))
        #
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(True)
        # ------------------ index ------------------
        # label
        index = QtWidgets.QLabel("index: ")
        index.setSizePolicy(sizePolicy)
        # N
        seri = QLabel(' N',self)
        seri.setAlignment(Qt.AlignRight)
        seri.setSizePolicy(sizePolicy)
        # index text
        self.index_textbox = QLineEdit()
        self.index_textbox.setValidator(QDoubleValidator())
        
        # ------------------ yaş ------------------
        # label
        yas = QtWidgets.QLabel("Yaş: ")
        # yas
        self.yas_textbox = QLineEdit()
        self.yas_textbox.setValidator(QDoubleValidator())
        # ------------------ lux ------------------
        # label
        lux = QtWidgets.QLabel("Luxmetre: ")
        # lux
        self.lux_textbox = QLineEdit()
        self.lux_textbox.setValidator(QDoubleValidator())
        # ------------------ cinsiyet ------------------
        # label
        cinsiyet = QtWidgets.QLabel("cinsiyet: ")
        # cinsiyet
        self.radio_button_er = QRadioButton()
        self.radio_button_er.setText("Erkek")
        self.radio_button_er.setChecked(True)

        self.radio_button_kad = QRadioButton()
        self.radio_button_kad.setText("Kadın")

        self.radio_button_others = QRadioButton()
        self.radio_button_others.setText("Diğer")
        # ------------------ Date ------------------
        # label
        date_label = QtWidgets.QLabel('Tarih')
        # date
        self.date = QDateEdit()
        today = date.today()
        d = QDate(today)
        self.date.setDate(d)
        # ------------ Pupil_Arası_Mesafe ------------
        # label
        pam_label = QLabel('Pupil Arası\nMesafe:')
        # pam
        self.pam_textbox = QLineEdit()
        self.pam_textbox.setValidator(QDoubleValidator())
        # progress bar
        # creating progress bar
        self.pbar = QProgressBar(self)
        self.btn = QPushButton('pdfleri oku', self)
        self.btn.clicked.connect(self.id2file_name)
        # =========== widgets ===========
        self.hbox = QtWidgets.QHBoxLayout()
        #index
        self.hbox.addWidget(index)
        self.hbox.addWidget(seri)
        self.hbox.addWidget(self.index_textbox)
        #yas
        self.hbox.addWidget(yas)
        self.hbox.addWidget(self.yas_textbox)
        #luxmeter
        self.hbox.addWidget(lux)
        self.hbox.addWidget(self.lux_textbox)
        #cinsiyet
        self.hbox2 = QtWidgets.QHBoxLayout()
        self.hbox2.addWidget(cinsiyet)
        self.hbox2.addWidget(self.radio_button_er)
        self.hbox2.addWidget(self.radio_button_kad)
        self.hbox2.addWidget(self.radio_button_others)
        # pam
        self.hbox2.addWidget(pam_label)
        self.hbox2.addWidget(self.pam_textbox)
        # date
        self.hbox2.addWidget(date_label)
        self.hbox2.addWidget(self.date)

        # ------------------- pdf stuff --------------------
        self.hbox3 = QtWidgets.QHBoxLayout()
        self.hbox3.addWidget(self.pbar)
        self.hbox3.addWidget(self.btn)
        # ------------------ layout and groupBox ------------------
        self.vlay = QtWidgets.QVBoxLayout()
        self.vlay.addLayout(self.hbox3)
        self.vlay.addLayout(self.hbox)
        self.vlay.addLayout(self.hbox2)
        self.vlay.addStretch()

        Concrete_Group = QtWidgets.QGroupBox()
        Concrete_Group.setTitle("&Bilgiler")
        Concrete_Group.setLayout(self.vlay)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(Concrete_Group)
    
    def id2file_name(self):
        dir = pathlib.Path('./spot_pdfs')
        pdfs = list(dir.glob('*.pdf'))
        self.id2name = {}
        self.info = {}

        for p,pdf in enumerate(pdfs):
            i = int(round(100*p/len(pdfs)))
            self.pbar.setValue(i)
            roi, id_region, image = self.pdf2image(str(pdf))
            id = self.fetch_id(id_region)

            img_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            se = self.fetch_SE(img_rgb)
            ds = self.fetch_ds(img_rgb)
            dc = self.fetch_dc(img_rgb)
            ax = self.fetch_ax(img_rgb)
            pc = self.fetch_pc(image)
            self.id2name[id]=str(pdf)

            self.info[id]={'left':{'ds': ds['left'],'dc': dc['left'], 'ax':ax['left'], 'se':se['left'],'pc':pc['left']}, 
                            'right':{'ds': ds['right'],'dc': dc['right'], 'ax':ax['right'], 'se':se['right'],'pc':pc['right']}}
        print(self.id2name)
        self.pbar.setValue(100)
    
    def pdf2image(self,path):
        pages = convert_from_path(path, 500)
        for i,page in enumerate(pages):
            page = np.array(page)
        h,w,c = page.shape
        return page[int(h/2)+20:int(h/2)+250,650:-1900,:],page[1100:1200,750:1050,:], page
    
    def fetch_id(self,image):
        return pytesseract.image_to_string(image).strip()

    def fetch_info(self,image):
        se = self.fetch_SE(image)
        ds = self.fetch_ds(image)
        dc = self.fetch_dc(image)
        ax = self.fetch_ax(image)
        pc = self.fetch_pc(image)
        return {'ds':ds, 'dc':dc, 'ax':ax}
    def fetch_ax(self, image):
        region = image[150:,500:,:]
        
        try:
            right  = region[:,30:275,:]
            txt = pytesseract.image_to_string(right).strip()
            if len(txt)==0:
                r = ''
            else:
                r = float(txt.strip().replace('@','').replace('°','').replace('|','').strip())
        except:
            r = ''
        try:
            left  = region[:,-250:-30,:]
            txt=pytesseract.image_to_string(left).strip()
            if len(txt)==0:
                l = ''
            else:
                l = float(txt.strip().replace('@','').replace('°','').replace('|','').strip())
        except:
            l=''
        return {'right':r,'left':l}
        
    def fetch_dc(self, image):
        region = image[150:,300:-230,:]
        

        try:
            right  = region[:,:200,:]
            txt = pytesseract.image_to_string(right).strip()
            if len(txt)==0:
                r=''
            else:
                r = float(txt.replace(',','').replace('|','').strip())
                r = self.check_sign(r)
        except:
            r=''
        try:
            left  = region[:,-300:,:]
            txt = pytesseract.image_to_string(left).strip()
            if len(txt)==0:
                l=''
            else:
                l = float(txt.replace(',','').replace('|','').strip())
                l = self.check_sign(l)
        except:
            l=''
        return {'right':r,'left':l}
    
    def check_sign(self,r):
        if r>30:
            if str(r)[0]=='4': 
                return float(str(r)[1:])
        return r
    
    def fetch_ds(self, image):
        region = image[150:,:-200,:]
        try:
            right  = region[:,:300,:]
            h,w,c = right.shape
            txt = pytesseract.image_to_string(right).strip()
            if len(txt)==0:
                r = ''
            else:
                r = float(txt.replace(',','').replace('|','').strip())
                r = self.check_sign(r)
        except:
            r =''
        try:
            left  = region[:,-530:-300,:]
            txt = pytesseract.image_to_string(left).strip()
            if len(txt)==0:
                l = ''
            else:
                l = float(txt.replace(',','').replace('|','').strip())
                l = self.check_sign(l)
        except:
            l=''
        return {'right':r,'left':l}
    
    def fetch_SE(self,image):
        region = image[20:100,250:-200,:]
        try:
            right  = region[:,:300,:]
            txt=pytesseract.image_to_string(right).strip()
            if len(txt)==0:
                r=''
            else:
                r = float(txt.replace(',','').replace('|','').strip())
                r = self.check_sign(r)
        except:
            r=''
        try:
            left  = region[:,-300:,:]
            txt = pytesseract.image_to_string(left).strip()
            if len(txt)==0:
                l=''
            else:
                l = float(txt.replace(',','').replace('|','').strip())
                l = self.check_sign(l)
        except:
            l=''
        return {'right':r,'left':l}

    def fetch_pc(self,page):
        h,w,c = page.shape
        region = page[int(h/2)-380:int(h/2)-280,300:-1500,:]
        try:
            right = region[:,100:300,:]
            txt=pytesseract.image_to_string(right).strip()
            if len(txt)==0:
                r=''
            else:
                try:
                    r = float(txt.replace(',','').replace('|','').strip())
                except:
                    r = ''
        except:
            r=''
        try:
            left = region[:,-350:-200,:]
            txt=pytesseract.image_to_string(left).strip()
            if len(txt)==0:
                l=''
            else:
                try:
                    l = float(txt.replace(',','').replace('|','').strip())
                except:
                    l=''
        except:
            l=''

        return {'right':r, 'left':l}

class data_class(QtWidgets.QWidget):
    def __init__(self, side,type,parent=None):
        super(data_class, self).__init__(parent)
        self.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Normal, italic=False))
        
        

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(False)

        self.tbox = QtWidgets.QHBoxLayout()
        # ------------------ ds ------------------
        # label
        ds = QtWidgets.QLabel("ds: ")
        ds.setSizePolicy(sizePolicy)
        # ds text
        self.ds_text = QLineEdit()
        self.ds_text.setSizePolicy(sizePolicy)
        self.ds_text.setValidator(QDoubleValidator())

        # ------------------ dc ------------------
        # label
        dc = QtWidgets.QLabel("dc: ")
        dc.setSizePolicy(sizePolicy)
        # ds text
        self.dc_text = QLineEdit()
        self.dc_text.setSizePolicy(sizePolicy)
        self.dc_text.setValidator(QDoubleValidator())
        # ------------------ ax ------------------
        # label
        ax = QtWidgets.QLabel("Axis: ")
        ax.setSizePolicy(sizePolicy)
        # ds text
        self.ax_text = QLineEdit()
        self.ax_text.setSizePolicy(sizePolicy)
        self.ax_text.setValidator(QDoubleValidator())            
        # ------------------ pç ------------------
        # label
        #if type in ['spot', 'SPOT']:
        pc = QtWidgets.QLabel("pupil çapı: ")
        pc.setSizePolicy(sizePolicy)
        # pç text
        self.pc_text = QLineEdit()
        self.pc_text.setSizePolicy(sizePolicy)
        self.pc_text.setValidator(QDoubleValidator())
        # ------------------ se ------------------
        # label
        se = QtWidgets.QLabel("se: ")
        se.setSizePolicy(sizePolicy)
        # se text
        self.se_text = QLineEdit()
        self.se_text.setSizePolicy(sizePolicy)
        self.se_text.setValidator(QDoubleValidator())
        
        # ============ widgets =============
        box = QtWidgets.QVBoxLayout()
        box.addWidget(ds)
        box.addWidget(self.ds_text)
        box.addWidget(dc)
        box.addWidget(self.dc_text)
        box.addWidget(ax)
        box.addWidget(self.ax_text)
        box.addWidget(se)
        box.addWidget(self.se_text)
        if type in ['spot', 'SPOT']:
            box.addWidget(pc)
            box.addWidget(self.pc_text)

        self.grid = QtWidgets.QGridLayout()
        self.grid.addLayout(box, 0, 0, 1, 2)

        Environment_Group = QtWidgets.QGroupBox()
        Environment_Group.setTitle(f"&{side} ({type})")
        Environment_Group.setLayout(self.grid)

        vlay = QtWidgets.QVBoxLayout(self)
        vlay.addWidget(Environment_Group)
    def update_values(self,info):
        
        self.ds_text.setText(str(info['ds']))
        self.dc_text.setText(str(info['dc']))
        self.ax_text.setText(str(info['ax']))
        self.se_text.setText(str(info['se']))
        self.pc_text.setText(str(info['pc']))
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = ClassWidget()
    w.show()
    sys.exit(app.exec_())