#!/usr/bin/python

import sys
import fractions
from time import sleep
from PyQt4 import QtGui, QtCore

sys.setrecursionlimit(10000);
#LCM function used to calculate the optimum size of the box
def lcm1(a,b):
    return abs(a*b)/fractions.gcd(a,b)


#FloodFill Widget Class

class floodFill(QtGui.QWidget):
    global r,c,cd,rd,x,y,qp,ev,flag,speed,tl,ff_arr,m,n,trgxi
    global bndx,bndy,strtx,strty,xbnd,timer,ybnd,xstrt,ystrt,trgx,trgy,xtrg,ytrg
    bndx=[]
    bndy=[]
    xbnd=[]
    ybnd=[]
    xtrg=[]
    ytrg=[]
    trgx=[]
    trgy=[]
    strtx=-1
    strty=-1
    m=-1
    n=-1
    def __init__(self):
        super(floodFill, self).__init__()
        
        self.initUI()
    
#Initialisation
   
    def initUI(self):
	global x,y,r,c,flag,ff_arr,timer,trgxi,speed
	self.timer = QtCore.QTimer()	
	x=0
	y=0
	flag=0
	trgxi=0
	speed=1
	tl=self.sizeCalc()
	self.button(tl)
        self.setWindowTitle('Flood Fill')
        self.show()

#To Calculate The Size of the Entire Widget
   
    def sizeCalc(self):
	global r,c,ff_arr,tl
	ff_arr=[[0]*c for i in range(r)]
        if(r!=c):
            tl=lcm1(r,c)
        else:
            tl=r*2
        tl=tl*10
	return tl

#To Include a Button in the GUI

    def button(self,tl):
        self.nextButton = QtGui.QPushButton("Next")
	self.dial=QtGui.QDial()        
	self.hbox = QtGui.QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.nextButton)
	self.vbox = QtGui.QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)
	self.nextButton.clicked.connect(self.buttonClicked)
	self.setGeometry(300, 300,tl+70, tl+70)
    
#Trigger Function on Button Click

    def buttonClicked(self):
	global flag
	if(flag==0):	
		flag=1
		print "Select Your Starting Point in the GUI "	
	elif(flag==1):
		self.nextButton.setEnabled(False) 		
		flag=2
		print"\n\n\nFlood Filling\n\n\n"
		self.tim()
		self.ff()

#The Entire widget is Repainted Continously by this Function
		   
    def paintEvent(self, e):
	global trgx,trgy,cd,rd,timer,trgxi
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawBoxs(qp,r+1,c+1)
        self.paintBox(qp)        
	qp.end()
	if(flag==2):
	   for i in range(trgxi):		
		qp.begin(self)	
		brush = QtGui.QBrush(QtCore.Qt.red,QtCore.Qt.SolidPattern)
	        qp.setBrush(brush)
		qp.drawRect(trgx[i],trgy[i],cd,rd)
		qp.end()
	   self.tim()
#Timer

    def tim(self):
	global trgxi,speed,trgx
	self.timer.start(speed)
	trgxi=trgxi+1
	self.timer.timeout.connect(self.update)
	
#Function to Convert Virtual Co-Ordinates to Actual Co-ordinates ie.Boundary Values to Co-ordinates

    def convert(self):
	global ff_arr,xbnd,ybnd,r,c
	for i in range(len(xbnd)):
		for m in range(r):
			for n in range(c):
				ff_arr[xbnd[i]-1][ybnd[i]-1]=2
#The Flood Fill Function

    def fld(self,i,j):
	global ff_arr,xtrg,ytrg,xstrt,ystrt
	if(i<0 or j<0 or i>r-1 or j>c-1):
		return	
	if(ff_arr[i][j]!=0):
		return
	ff_arr[i][j]=1
	xtrg.append(j+1)
	ytrg.append(i+1)
	self.update()
	self.fld(i,j-1)
	self.fld(i,j+1)
	self.fld(i-1,j)
	self.fld(i+1,j)
	return

#FloodFill Caller

    def ff(self):
	self.nextButton.setEnabled(False)
	global ff_arr,r,c,xstrt,ystrt
	self.convert()
	self.fld(ystrt-1,xstrt-1)

#Trigger Function on Mouse Click

    def mousePressEvent(self,e):
        global rd,cd,tl,x,y,m,n,ev
	if(flag!=2):
        	x=e.pos().x()
        	y=e.pos().y()
        	m=((x-20)/cd)+1
        	n=((y-20)/rd)+1
		if(x<=tl+20 and y<=tl+20 and x>20 and y>20):
    		 self.update()

#Function Used to Paint all The Colour Boxes in The Widget

    def paintBox(self,qp):
      global rd,cd,m,n,bndx,bndy,ev,r,c,strtx,strty,xstrt,ystrt,xbnd,ybnd,xtrg,ytrg
      mc=m
      nc=n
      if(x<=tl+20 and y<=tl+20 and x>20 and y>20):
	if(flag==0):
        	brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        	qp.setBrush(brush)
	
        m=((m-1)*(cd))+20
	n=((n-1)*(rd))+20
	if(flag==0):
		if (mc<=c and nc<=r):
			bndx.append(m)
			bndy.append(n)
			ybnd.append(mc)
			xbnd.append(nc)
	if(flag==1):
		brush = QtGui.QBrush(QtCore.Qt.red,QtCore.Qt.SolidPattern)
        	qp.setBrush(brush)
		if (mc<=r and nc<=c):
			strtx=m
			strty=n
			xstrt=mc
			ystrt=nc
       		qp.drawRect(strtx,strty,cd,rd)

	brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        qp.setBrush(brush)
	for i in range(len(bndx)):
       		qp.drawRect(bndx[i],bndy[i],cd,rd)

	if(flag==2):
        	brush = QtGui.QBrush(QtCore.Qt.red,QtCore.Qt.SolidPattern)
        	qp.setBrush(brush)
		for i in range(len(xtrg)):
			trgx.append(((xtrg[i]-1)*(cd))+20)
			trgy.append(((ytrg[i]-1)*(rd))+20)

#Function Used to Draw The Basic Grid

    def drawBoxs(self,qp,r,c):
        global rd,cd,x,tl,y,bnd
        pen = QtGui.QPen(QtCore.Qt.black, 0.75, QtCore.Qt.SolidLine)
	qp.setPen(pen)
        r=r-1
        c=c-1
        if(r!=c):
            tl=lcm1(r,c)
        else:
            tl=r*2
        tl=tl*10
        cd=tl/c
        rd=tl/r
        for i in range(0,tl+20,rd):
            qp.drawLine(20,20+i,tl+20,i+20)
        for i in range(0,tl+20,cd):
            qp.drawLine(i+20,20,i+20,tl+20)


#Main Function
        
def main():
    global r,c,x,y
    app = QtGui.QApplication(sys.argv)
    r=input("Max Rows ?")
    c=input("Max Cols ?")
    print "Target Colour: Red,Replacement Colour:White,Boundary Color:Black"
    print "Select the Boundaries"
    ff = floodFill()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
