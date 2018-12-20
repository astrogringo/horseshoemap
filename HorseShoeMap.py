
import sys, pygame, math
pygame.init()


#function to convert coordinates from x,y to screen x, screen y
def CoordPhysToScreen(inpList,ScreenSizeX,ScreenSizeY):
    "Coordinate conversion x,y to screen"
    
    #this are the corresponding coordinates in physical size
    xmin=-1
    xmax=5
    ymin=-1
    ymax=3

    inpX = [p[0] for p in inpList]
    inpY = [p[1] for p in inpList]

    outX = [ (x - xmin)/(xmax- xmin)*ScreenSizeX for x in inpX]
    outY = [ ScreenSizeY - (y - ymin)/(ymax-ymin)*ScreenSizeY for y in inpY]

    return list(zip(outX,outY))
    


def Transform1(inpList,alpha):
    "Transformation 1: squeeze y coordinates by alpha, unless x<0, if yes, also squeeze x"
    

    outX=[]
    outY=[]



    for x,y in inpList :
        
        resx=x
        resy=y

        if(x<0):
            resx=x*alpha
            resy=y*alpha

        if(x>=0 and x<=1):
            resy=y*alpha
        
        if(x>1):
            resx=1+(x-1)*alpha
            resy=y*alpha


        outX.append(resx)
        outY.append(resy)

    return list(zip(outX,outY))

def EvalForTrans2(x,beta):
    "internal function for Transform 2"

    y=0

    if x >= 0   and x < 1/3 :
        y=beta*x
    
    if x >= 1/3 and x < 2/3 :
        y=x*(beta+(beta-1)*(3*math.pi/4-3/2))+(beta-1)*(1/2-math.pi/4)

    if x >= 2/3 and x < 1   :
        y=beta*x+(beta-1)*(math.pi/4-1/2)
    if x < 0 :
        y=x
    if x >= 1 :
        y=(x-1)+beta+(beta-1)*(math.pi/4-1/2)

    return y

def Transform2(inpList,beta):
    "Transformation 2: stretch in x direction by beta, with some special conditions"
    inpX = [p[0] for p in inpList]
    inpY = [p[1] for p in inpList]

    outX = [ EvalForTrans2(x,beta) for x in inpX]
    outY = [ y for y in inpY]

    return list(zip(outX,outY))


def Transform3(inpList,theta):
    "Transformation 3: turn around point 1, 0.5 by angle theta (0..180)"

    px=1
    py=0.5

    
    outX=[]
    outY=[]



    for x,y in inpList :
        
        resx=x
        resy=y

        #if x<1 do nothing
       
        #if x in middle segment, turn it around until angle theta
        if(x>1 and x <= 1+(math.pi/2)*(theta/180)):
            r=py-y
            alpha=(x-px)*theta/90
            resx=px+r*math.sin(alpha)
            resy=py-r*math.cos(alpha)
        
        if(x> 1+math.pi/2*(theta/180)):

            alpha=math.pi/2*theta/180*theta/90
            r=0.5
            dx=px+r*math.sin(alpha) #-math.pi/2-1
            dy=py-r*math.cos(alpha) #

            #alpha=alpha#+math.pi
            xr=(x-1-math.pi/2*(theta/180))*math.cos(alpha)-y*math.sin(alpha)
            yr=(x-1-math.pi/2*(theta/180))*math.sin(alpha)+y*math.cos(alpha)

            resx=xr+dx
            resy=yr+dy

        outX.append(resx)
        outY.append(resy)


    return list(zip(outX,outY))


size = width, height = 900, 600
speed = [1, 1]
black = 0, 0, 0
white= 255,255,255

screen = pygame.display.set_mode(size)


xPhys=[0,1,1,0,0]
yPhys=[0,0,1,1,0]


xList=[100,100,250,300,400]
yList=[100,200,400,250,150]


#starting points for each side if the square
nPoints=40001
nList=[i/(nPoints-1) for i in range(nPoints)]
nListReversed=nList[::-1]

xList=nList.copy()
xList.extend([1 for i in nList])
xList.extend(nListReversed)
xList.extend([0 for i in nList])

yList=[0 for i in nList]
yList.extend(nList)
yList.extend([1 for i in nList])
yList.extend(nListReversed)

xyList=list(zip(xList,yList))

pList=CoordPhysToScreen(xyList,width,height)


dummy="paolo"

speedFactor=1
dc1=50
dc2=20
dc3=0.5
counter4=0

pygame.font.init() 
myfont = pygame.font.SysFont('Arial', 40)

SqX=[0,1,1,0,0]
SqY=[0,0,1,1,0]
Sq=list(zip(SqX,SqY))

ScreenTransfList=CoordPhysToScreen(Sq,width,height)

for j in range(100):
    screen.fill(white)
    res=pygame.draw.lines(screen, (0,0,0), False, ScreenTransfList, 1)

    textsurface = myfont.render("Start with a Square", True, (0, 0, 0))                
    screen.blit(textsurface,(100,50))

    pygame.display.flip()
    counter4=counter4+1
    pygame.image.save(screen, "C:\Temp\screenshot"+str(counter4).zfill(4)+".png")
        


for i in range(5):
    
    counter1=0
    counter2=0
    counter3=0
   
      

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


       
        
        
        
        screen.fill(white)

        #draw grid
        for ox in range(12):
            for oy in range(8):
                x=[ox/2-1,ox/2-1]
                y=[-1,3]
                g=list(zip(x,y))
               # ScreenTransfList=CoordPhysToScreen(g,width,height)
               # res=pygame.draw.lines(screen, (255,0,0), False, ScreenTransfList, 1)
                x=[-1,5]
                y=[oy/2-1,oy/2-1]
                g=list(zip(x,y))
               # ScreenTransfList=CoordPhysToScreen(g,width,height)
               # res=pygame.draw.lines(screen, (255,0,0), False, ScreenTransfList, 1)
              
  
        counter1=counter1+1
        alpha=1-counter1/dc1

        #step 1
        if (alpha >= 0.5) : 
            if (counter1 % speedFactor ) == 0  : 

                PhysTransfList=Transform1(xyList,alpha)
                ScreenTransfList=CoordPhysToScreen(PhysTransfList,width,height)

                res=pygame.draw.lines(screen, (0,0,0), False, ScreenTransfList, 1)
                #res=pygame.draw.polygon(screen, (0,0,0), ScreenTransfList, 0)


                textsurface = myfont.render("Loop "+str(i+1)+": Shrink Phase", True, (0, 0, 0))                
                screen.blit(textsurface,(100,50))

                pygame.display.flip()
                counter4=counter4+1
                pygame.image.save(screen, "C:\Temp\screenshot"+str(counter4).zfill(4)+".png")
        
            finalAlpha=alpha
            continue


        #step 2 
        counter2=counter2+1
        beta=1+counter2/dc2

        if (beta <= 3) :
            if (counter2 % speedFactor ) == 0  : 
                PhysTransfList1=Transform1(xyList,finalAlpha)
                PhysTransfList2=Transform2(PhysTransfList1,beta)
                ScreenTransfList=CoordPhysToScreen(PhysTransfList2,width,height)

                res=pygame.draw.lines(screen, (0,0,0), False, ScreenTransfList, 1)
                #res=pygame.draw.polygon(screen, (0,0,0), ScreenTransfList, 0)


                textsurface = myfont.render("Loop "+str(i+1)+": Stretch Phase", True, (0, 0, 0))                
                screen.blit(textsurface,(100,50))

                    #screen.blit(ball, ballrect)
                pygame.display.flip()
                counter4=counter4+1
                pygame.image.save(screen, "C:\Temp\screenshot"+str(counter4).zfill(4)+".png")

            finalBeta=beta
            continue

        #step 3 
        counter3=counter3+1
        theta=counter3/dc3

        if(theta <= 180) :
            if (counter3 % speedFactor ) == 0  : 
                PhysTransfList1=Transform1(xyList,finalAlpha)
                PhysTransfList2=Transform2(PhysTransfList1,finalBeta)
                PhysTransfList3=Transform3(PhysTransfList2,theta)
         
                ScreenTransfList=CoordPhysToScreen(PhysTransfList3,width,height)

                res=pygame.draw.lines(screen, (0,0,0), False, ScreenTransfList, 1)
                #res=pygame.draw.polygon(screen, (0,0,0), ScreenTransfList, 0)


                textsurface = myfont.render("Loop "+str(i+1)+": Fold Phase", True, (0, 0, 0))                
                screen.blit(textsurface,(100,50))



                pygame.display.flip()
                counter4=counter4+1
                pygame.image.save(screen, "C:\Temp\screenshot"+str(counter4).zfill(4)+".png")


                finalTheta=theta
                continue


            #go back to start 6 times
        else :
            xyList=PhysTransfList3
            break


for j in range(100):

    screen.fill(white)
    res=pygame.draw.lines(screen, (0,0,0), False, ScreenTransfList, 1)
                    #res=pygame.draw.polygon(screen, (0,0,0), ScreenTransfList, 0)


    textsurface = myfont.render("Final Result", True, (0, 0, 0))                
    screen.blit(textsurface,(100,50))



    pygame.display.flip()
    counter4=counter4+1
    pygame.image.save(screen, "C:\Temp\screenshot"+str(counter4).zfill(4)+".png")

