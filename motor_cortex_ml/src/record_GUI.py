#!/usr/bin/env python

from tkinter import *
import time
import rospy
class Movementgui():
    def __init__(self):
        root=Tk()
        self.canvas = Canvas(root, width = 300, height = 100)
        self.img = PhotoImage(file="/home/jingyan/Pictures/24_2_c.png")
        self.imgArea = self.canvas.create_image(0, 0, anchor = NW, image = self.img)
        self.canvas.pack()
        # self.but1 = Button(root, text="press me", command=lambda: self.changeImg())
        # self.but1.place(x=10, y=500)
        # root.after(2000,self.changeImg)

    def callback(self,flag):
        if flag==-1:
            self.leftimg()
        elif flag==0:
            self.crossimg()
        elif flag==1:
            self.rightimg()
        else: pass

    def leftimg(self):
        self.img = PhotoImage(file="/home/jingyan/Pictures/Ps_lab1.png")
        self.canvas.itemconfig(self.imgArea, image = self.img)
    def rightimg(self):
        self.img = PhotoImage(file="/home/jingyan/Pictures/Ps_lab1.png")
        self.canvas.itemconfig(self.imgArea, image = self.img)
    def crossimg(self):
        self.img = PhotoImage(file="/home/jingyan/Pictures/Ps_lab1.png")
        self.canvas.itemconfig(self.imgArea, image = self.img)

def main():
    rospy.init_node("mindwave_moter_trainning_record",anonymous=True)
    
    try:
       
        
        app = Movementgui()
        root.mainloop()        
    except rospy.ROSInterruptException: pass

    rospy.spin()
    
if __name__ == '__main__':
	main()
