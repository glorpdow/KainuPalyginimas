from PySide6.QtWidgets import*
from PySide6.QtGui import*
from PySide6.QtCore import *
from PySide6.QtNetwork import*
from Scraper import scrape_all_stores

# pip install -r recomended.txt; python -m playwright install

class Create_Preke(QWidget):

    def __init__(self,i):
        super().__init__()
        
        self.internet = QNetworkAccessManager()
        self.setFixedWidth(200)
        

        frame1=QFrame()
        frame1.setFrameShape(QFrame.Box)
        frame1.setLineWidth(2)

        layout=QVBoxLayout(frame1)
        

        self.image_l1=QLabel()
        self.image_l1.setPixmap(QPixmap(f"images/{i['shop']}.png").scaled(150,150,Qt.KeepAspectRatio))   
        
        

        title_l1=QLabel(i["title"])
        title_l1.setMaximumWidth(250)
        title_l1.setMinimumHeight(40)
        title_l1.setWordWrap(True)
        

        kaina_l1=QLabel(f'{i["price"]}€') 
        #kaina_l1.setMaximumHeight(40)
        #kaina_l1=QLabel("evro") 
        kaina_l1.setStyleSheet('font-size: 16px; font-weight: bold')
        parde_l1=QLabel()
        parde_l1.setPixmap(QPixmap(f"images/{i['shop']}.png").scaled(40,40,Qt.KeepAspectRatio))
        #parde_l1.setMaximumHeight(40)

        kainImg=QHBoxLayout()
        kainImg.addWidget(kaina_l1)
        kainImg.addWidget(parde_l1,alignment = Qt.AlignRight)
        
        layout.addWidget(self.image_l1,  alignment = Qt.AlignCenter,)
        layout.addWidget(title_l1)
        layout.addLayout(kainImg)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(frame1)
        #self.setLayout(main_layout)


        if(i['image']!=None):
            self.LoadImage(i['image'])
       
    def LoadImage(self,url):

        request = QNetworkRequest(QUrl(url))
        atsakims = self.internet.get(request)
        atsakims.finished.connect(lambda a=atsakims: self.ImageUpload(a))

    def ImageUpload(self,atsakims):
        if atsakims.error() == QNetworkReply.NoError:
            img_data=atsakims.readAll()
            pixmap=QPixmap()
            pixmap.loadFromData(img_data)
            self.image_l1.setPixmap(pixmap.scaled(150,150,Qt.KeepAspectRatio))
        atsakims.deleteLater()



        
class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kaina25")
        
        ### grn top juosta
        virsus=QHBoxLayout()

        virsus_l1=QLabel("Kaina25")
        virsus_l1.setStyleSheet("font-size: 22px; font-weight: bold")
        virsus_l1.setAlignment(Qt.AlignLeft)
        virsus_l1.setMaximumWidth(200)
        
        virsus_search=QLineEdit()
        virsus_search.setPlaceholderText("Kokios prekės ieškote?")
        virsus_search.setMaximumWidth(500)
        virsus_search.setMinimumWidth(300)
        virsus_search.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)

        virsus_search.returnPressed.connect(lambda: self.Search(virsus_search.text()))


        virsus.addWidget(virsus_l1,2, alignment=Qt.AlignLeft)
        virsus.addWidget(virsus_search,5, alignment=Qt.AlignLeft)
        
        
        ### grn filtrai visi jei bus isvis

        side_scroll = QScrollArea()
        side_scroll.setWidgetResizable(True)
        side_scroll_layout=QWidget()
 
        sideFilter=QVBoxLayout(side_scroll_layout)
        side_scroll.setWidget(side_scroll_layout)

        side_l1=QLabel("Pardavėjai:")
        side_l1.setStyleSheet("font-size: 13px; font-weight: bold ")
        side_l2=QLabel("Kaina:")
        side_l2.setStyleSheet("font-size: 13px; font-weight: bold ")
        
        iki=QCheckBox("Iki")
        barbora=QCheckBox("Barbora")
        iki.setChecked(True)
        barbora.setChecked(True)
        
        self.pard_list = []

        iki.toggled.connect(lambda checked: self.PardList('iki',checked))
        barbora.toggled.connect(lambda checked: self.PardList('barbora',checked))

        side_b1= QPushButton("Filtruoti")
        side_b1.clicked.connect(self.add_prekes)


        sideFilter.addWidget(side_l1)
        sideFilter.addWidget(iki)
        sideFilter.addWidget(barbora)
     
        sideFilter.addWidget(side_l2)

        self.side_kainafilter = QCheckBox("Filtruoti pagal kainą")


        sideFilter.addWidget(self.side_kainafilter)
        sideFilter.addWidget(side_b1)


        sideFilter.addStretch()

        
        ### Prekes menu tas
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        scroll_layout=QWidget()
        self.mainPrekes=QGridLayout(scroll_layout)

        self.scroll.setWidget(scroll_layout)



        miniLayout=QHBoxLayout()
        miniLayout.addWidget(side_scroll,1)
        miniLayout.addWidget(self.scroll,4)

        MainLayout=QVBoxLayout()
        MainLayout.addLayout(virsus)
        MainLayout.addLayout(miniLayout)

        self.setLayout(MainLayout)

        self.original_main_results=[]
        self.colmax=1

    
    def PardList(self,pard,checked):
       
        if(checked == False):
            self.pard_list.append(pard)
        else:
            self.pard_list.remove(pard)


    def Search(self,query):
        
        self.original_main_results = scrape_all_stores(query)
        self.filtered_main_results = sorted(self.original_main_results, key=lambda x: float(x.get('price') or 0))
        
        self.add_prekes()
        
    
    def add_prekes(self):
        row=0
        col=0

        while self.mainPrekes.count():
          
            widgets = self.mainPrekes.takeAt(0)
            if widgets.widget():
                widgets.widget().setParent(None)


        if(self.side_kainafilter.isChecked()):
            main_results=self.filtered_main_results
        else:
            main_results=self.original_main_results
        for i in main_results:
            if(i['title']==None or i['price']==None or i['shop'] in self.pard_list):
                continue

            preke=Create_Preke(i)
            preke.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
                
            self.mainPrekes.addWidget(preke,row,col)

            col+=1
            if col>=self.colmax:
                col=0
                row+=1

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.mainPrekes.addItem(spacer, row+1, 0)

    def resizeEvent(self,event):
        
        width=self.scroll.viewport().width()
        preke_width=200
        colnow=max(1,width//preke_width)
        if(colnow!=self.colmax):
            self.colmax=colnow
            self.add_prekes()
            
        super().resizeEvent(event)



app=QApplication()

langs=Main()
langs.resize(1000,700)
langs.show()

app.exec()
