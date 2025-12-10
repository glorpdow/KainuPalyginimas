from PySide6.QtWidgets import*
from PySide6.QtGui import*
from PySide6.QtCore import *
from BARBORA_scraper import scrape_barbora
from IKI_scraper import scrape_iki
import sys

class Create_Preke(QWidget):
    def __init__(self,i):
        super().__init__()
        

        #print(i)
        frame1=QFrame()
        frame1.setFrameShape(QFrame.Box)
        frame1.setLineWidth(2)

        layout=QVBoxLayout(frame1)
        

        image_l1=QLabel()
        image_l1.setPixmap(QPixmap("images/spongbub.jpg").scaled(150,150,Qt.KeepAspectRatio))   
        #image_l1.setMaximumHeight(150)

        title_l1=QLabel(i["title"])
        #title_l1=QLabel("textetxextete")
        #title_l1.setStyleSheet("text-font: 10px")
        title_l1.setMaximumWidth(200)
        title_l1.setMinimumHeight(40)
        title_l1.setWordWrap(True)
        

        kaina_l1=QLabel(f'{i["price"]}€') 
        #kaina_l1.setMaximumHeight(40)
        #kaina_l1=QLabel("evro") 
        parde_l1=QLabel()
        parde_l1.setPixmap(QPixmap("images/iki.jpeg").scaled(40,40,Qt.KeepAspectRatio))
        #parde_l1.setMaximumHeight(40)

        kainImg=QHBoxLayout()
        kainImg.addWidget(kaina_l1)
        kainImg.addWidget(parde_l1)
        
        layout.addWidget(image_l1,  alignment = Qt.AlignCenter,)
        layout.addWidget(title_l1)
        layout.addLayout(kainImg)

        #self.setStyleSheet("border: 1px solid #ccc; border-radius: 6px; padding: 8px")
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame1)
        self.setLayout(main_layout)
        

        
class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kaina24")
        
        ### grn top juosta
        virsus=QHBoxLayout()

        virsus_l1=QLabel("Kaina24.lt")
        virsus_l1.setStyleSheet("font-size: 22px; font-weight: bold")
        
        virsus_search=QLineEdit()
        virsus_search.setPlaceholderText("Kokios prekės ieškote?")

        
        self.virsus_kategorijos=QComboBox()
        self.virsus_kategorijos.setPlaceholderText("Kategorijos")
        self.virsus_kategorijos.currentIndexChanged.connect(self.KategorijosTransparent) 

        self.virsus_kategorijos.addItems([
            "Maistas ir gerimai",
            "Telefonai",
            "Kompiuterine technika",
            "Vaizdo, garso technika",
            "Foto ir video",
            "Namu ir sporto prekes"
        ])
        self.idx=-1
        


        virsus.addWidget(virsus_l1,2)
        virsus.addWidget(virsus_search,5)
        virsus.addWidget(self.virsus_kategorijos,2)

        ### cia poto kad sufiltruotu or sum
        #b1=QPushButton("get values")
        #b1.clicked.connect(self.B1)

        '''hlayout=QVBoxLayout()
        hlayout.addLayout(virsus)
        hlayout.addWidget(b1)

        self.setLayout(hlayout)'''
        #self.setLayout(virsus)
        
        
        ### grn filtrai visi jei bus veiks isvis

        side_scroll = QScrollArea()
        side_scroll.setWidgetResizable(True)
        side_scroll_layout=QWidget()
 
        sideFilter=QVBoxLayout(side_scroll_layout)
        side_scroll.setWidget(side_scroll_layout)
        #side_scroll_layout.setStyleSheet("border: 1px")
        #side_scroll.setStyleSheet("border: 1px")

        side_l1=QLabel("Pardavėjai:")
        side_l1.setStyleSheet("font-size: 13px; font-weight: bold ")
        side_l2=QLabel("Kaina:")
        side_l2.setStyleSheet("font-size: 13px; font-weight: bold ")
        
        maxima=QCheckBox("Maxima")
        iki=QCheckBox("Iki")
        rimi=QCheckBox("Rimi")
        norfa=QCheckBox("Norfa")
        barbora=QCheckBox("Barbora")
        sum=QCheckBox("sum other shit idk")

        sideFilter.addWidget(side_l1)
        sideFilter.addWidget(maxima)
        sideFilter.addWidget(iki)
        sideFilter.addWidget(rimi)
        sideFilter.addWidget(norfa)
        sideFilter.addWidget(barbora)
        sideFilter.addWidget(sum)
        sideFilter.addWidget(side_l2)

        sideFilter.addStretch()

        
        ### Prekes menu tas
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        scroll_layout=QWidget()
        self.mainPrekes=QGridLayout(scroll_layout)

        self.scroll.setWidget(scroll_layout)
        self.add_prekes()
        
        #scroll_layout.setStyleSheet("border: 1px solid #ccc; border-radius: 6px; padding: 8px")
        #self.scroll.setStyleSheet("border: 1px solid #ccc; border-radius: 6px; padding: 8px")

        


        miniLayout=QHBoxLayout()
        miniLayout.addWidget(side_scroll,1)
        miniLayout.addWidget(self.scroll,4)

        MainLayout=QVBoxLayout()
        MainLayout.addLayout(virsus)
        MainLayout.addLayout(miniLayout)

        self.setLayout(MainLayout)

        self.prekes_rebuild()



    
    def add_prekes(self):
        row=0
        col=0
        self.main_results=[]
        #self.barbora_result = scrape_barbora("duona")
        barbora_result=scrape_barbora("duona")
        #self.iki_result= scrape_iki("pienas")
        iki_result= scrape_iki("pienas")
        self.main_results.append(barbora_result)
        self.main_results.append(iki_result)
        

        #for i in range(100):
        for j in self.main_results:
            for i in j:
                if(i['title']==None or i['price']==None):
                    #print("bazinga")
                    continue

                preke=Create_Preke(i)
                preke.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
                #preke.setStyleSheet("border: 1px solid #ccc; border-radius: 6px; padding: 8px")
                self.mainPrekes.addWidget(preke,row,col)

                col+=1
                if col>=6:
                    col=0
                    row+=1

        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.mainPrekes.addItem(spacer, row+1, 0)

######### ↓↓↓ ASILAS KRW ↓↓↓ KODEL NER NIEKS KAS NORMALIAI PAAISKINTU ############
    def KategorijosTransparent(self):
        #print(self.idx)
        if(self.idx!=-1):
            self.idx.setEnabled(True)
        self.idx=self.virsus_kategorijos.model().item(self.virsus_kategorijos.currentIndex())
        #print(self.idx)
        #self.virsus_kategorijos.setItemData(1,False, idx)
        #idx=self.virsus_kategorijos.model().item(index)
        self.idx.setEnabled(False)

    def resizeEvent(self, event):
        self.prekes_rebuild()
        super().resizeEvent(event)
    
    def prekes_rebuild(self):
        #sk=1
        while self.mainPrekes.count():
            #print(sk)
            #sk+=1
            widgets = self.mainPrekes.takeAt(0)
            if widgets.widget():
                widgets.widget().setParent(None)

        
        width=self.scroll.viewport().width()
        #print(width)    
        preke_width=200
        colmax=max(1,width//preke_width)

        row=0
        col=0
        #for i in range(100):
        for j in self.main_results:
            for i in j:
                if(i['title']==None or i['price']==None):
                    #print("bazinga")
                    continue
                preke=Create_Preke(i)
                preke.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
                #preke.setStyleSheet("border: 1px solid #ccc; border-radius: 6px; padding: 8px")
                self.mainPrekes.addWidget(preke,row,col)

                col+=1
                if col>=colmax:
                    col=0
                    row+=1

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.mainPrekes.addItem(spacer, row+1, 0)





app=QApplication(sys.argv)

langs=Main()
langs.resize(1000,700)
langs.show()

app.exec()

#result=scrape_barbora("duona")

#for i in result:
#    print(i)
#    print(i['title'])
