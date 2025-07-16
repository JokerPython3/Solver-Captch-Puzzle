import requests # to send request picter url 
import numpy as np  #deal array
import random # create random number
import cv2 as cv #deal video and pictuer

class CaptchSolver:
    def download(self,url1,url2):
        #if you have picter png in your pc don't write this code only return img1,img2
        r1 = requests.get(url1).content
        r2 = requests.get(url2).content
        #response => bayte code
        n1 = np.frombuffer(r1,np.uint8)
        n2 = np.frombuffer(r2,np.uint8)
        #response => array
        img1 = cv.imdecode(n1,cv.IMREAD_COLOR)
        img2 =cv.imdecode(n2,cv.IMREAD_UNCHANGED)
        # cv.imshow("img1",img2)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        #response => image

        return img1,img2
    def officet(self,paice,background): #found a piece of background
        if paice.shape[2] == 4: #if piece have alpha channel 
            alpha = paice[:,:, 3] #get alpha channel
            m = cv.threshold(alpha,127,255,cv.THRESH_BINARY)[1] # get alpha to mask black and white
            pg = cv.cvtColor(paice, cv.COLOR_BGRA2BGR)# remove alpha 
            re = cv.matchTemplate(background,pg,cv.TM_CCOEFF_NORMED,mask=m) #match
        else: # else don't have alpha channel 
            re=cv.matchTemplate(background,paice,cv.TM_CCOEFF_NORMED)  # match
        _,_,_,mx = cv.minMaxLoc(re) # serche the best match 
        return mx[0],mx[1] # return x,y
    def move(self,off,y):# funcion move slide
        pa = [] #move
        for i in range(60): #create 60 poient represent move
            t=int((i / 60) * 1000) + random.randint(-10,10) #create time of moveing
            x = int(self.time((i/60)*off)) + random.randint(-2,2) #get x location
            pa.append({"time":t,"x":x,"y":y+random.randint(-1,1)}) # add points to move
        pa[-1]={"time":1000,"x":off,"y":y} #edit last points 
        return pa #return move
    @staticmethod #No access required self you can Contact Directly from class
    def time(t): # get Normal speed.
        return 1-(1-t)*(1-t) #return Normal speed.
    def solver(self,url1,url2): #solver captcha
        b,p = self.download(url1,url2)#download pictuer
        x,y= self.officet(p,b) # get a correct location of peice(x,y)
        dry = self.move(x,y) # get a correct move 
        h,w = p.shape[:2] #get Height and  offer of peice
        re = b.copy()#get a copy of backgound 
        if p.shape[2] == 4:#if piece have alpha channel 
            alpha = p[:,:, 3] #get alpha channel
            m = cv.threshold(alpha,127,255,cv.THRESH_BINARY)[1] # get alpha to mask black and white
            pg = cv.cvtColor(p, cv.COLOR_BGRA2BGR)# remove alpha 
            ro = re[y:y+w, x:x+h]#selecte location in picuter  for past peice
            np.copyto(ro,pg,where=m[:,:,None].astype(bool))#to merge piece in the pictuer
        else:# else don't have alpha channel 
            re[y:y+w, x:x+h]#to merge piece in the pictuer
        #======[To show pictuer]========
        cv.imshow("solver",re)
        cv.waitKey(0)
        cv.destroyAllWindows()
        #======[To show pictuer]========


#=========[start class] ===========
CaptchSolver().solver("https://p19-rc-captcha-useast2a.tiktokcdn-eu.com/tos-useast2a-i-447w7jt563-euttp/55bca041305f489ebd9439416c41eef0~tplv-447w7jt563-3.webp","https://p19-rc-captcha-useast2a.tiktokcdn-eu.com/tos-useast2a-i-447w7jt563-euttp/873c180cecf64850b45e0a6c151b720a~tplv-447w7jt563-3.webp")
#=========[start class] ===========
#ترجمها اذا ماتعرف بل انكليزي 
#لمام نترو
