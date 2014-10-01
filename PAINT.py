from pygame import *
from random import *
from collections import deque
#from sets import Set


screen=display.set_mode((1024,768))
running=True

screen.fill((255,255,255))


#tools
t="Tool Icons/"
pencil=image.load(t+"pencil.png")
eyedropper=image.load(t+"eyedropper.png")
rectangle=image.load(t+"rectangle.png")
paintbrush=image.load(t+"paintbrush.png")
eraser=image.load(t+"eraser.png")
line=image.load(t+"linetool.png")
spray=image.load(t+"spraypaint.png")
bucket=image.load(t+"fillbucket.png")
ellipse=image.load(t+"ellipse.png")
gradienttool=image.load(t+"gradient.png")

#background stuff
b="Background/"
stampsmenu=image.load(b+"stampbackground.png")
sizebar=image.load(b+"sizebar.png")
sizecursor=image.load(b+"sizecursor1.png")
saveimage=image.load(b+"saveimage.png")
loadimage=image.load(b+"loadimage.png")
tools=image.load(b+"tools1.png")
toolsclicked=image.load(b+"toolsclicked.png")
stamps=image.load(b+"stamps1.png")
stampsclicked=image.load(b+"stampsclicked.png")
toolbar=image.load(b+"toolbar.png")
toolbar2=image.load(b+"toolbar2.png")

background=image.load(b+"maplestoryback.png")
screen.blit(background,(0,0))

palette=image.load(b+"spectrumPalette.png")

#stamps -lists, for the icon, the transparent icon, and the actual stamp
alishar=[]
papulatus=[]
balrog=[]
mushmom=[]
slime=[]
zombiemush=[]

#loading the stamps faster
for i in range (1,4):
    alishar.append(image.load("Stamps/alishar"+str(i)+".png"))
    papulatus.append(image.load("Stamps/papulatus"+str(i)+".png"))
    balrog.append(image.load("Stamps/jrbalrog"+str(i)+".png"))
    mushmom.append(image.load("Stamps/bluemushmom"+str(i)+".png"))
    slime.append(image.load("Stamps/slime"+str(i)+".png"))
    zombiemush.append(image.load("Stamps/zombiemush"+str(i)+".png"))




canvasRect=Rect(220,117,584,527)
pencilRect = Rect(42,160,60,60)
recttool=Rect(110,160,60,60)
colourselect=Rect(42,230,60,60)
brushtool=Rect(110,230,60,60)
erasertool=Rect(42,300,60,60)
linetool=Rect(110,300,60,60)
spraypaint=Rect(42,370,60,60)
ellipsetool=Rect(110,370,60,60)
fillbucket=Rect(42,440,60,60)
gradientRect=Rect(110,440,60,60)
loadRect=Rect(34,510,70,30)
saveRect=Rect(110,510,70,30)


coloursRect=Rect(860,120,128,32)
paletteRect=Rect(840,160,150,113)
undoRect=Rect(820,300,90,90)
redoRect=Rect(920,300,90,90)
screen.blit(image.load(t+"undo.png"),(820,300))
screen.blit(image.load(t+"redo.png"),(920,300))

menu=0


tool=''

draw.rect(screen,(255,255,255),canvasRect)

#default colours, (colour1=left mouse, colour2=right mouse)
colour1=(0,0,0)
colour2=(255,255,255)

#list used for drawing the recent colour squares
colours=[]
#default colours are white
for i in range (15):
    colours.append((255,255,255))

#size variable
size=1

mx=my=0

instruction='' #text instructions for each tool
instruction2=''

def getName():
    ans = ""                    # final answer will be built one letter at a time.
    arialFont = font.SysFont("Arial", 16)
    back = screen.copy()        # copy screen so we can replace it when done
    textArea = Rect(34,510,146,30) # make changes here.

    typing = True
    while typing:
        for e in event.get():
            if e.type == QUIT:
                event.post(e)   # puts QUIT back in event list so main quits
                return ""
            if e.type == KEYDOWN:
                if e.key == K_BACKSPACE:    # remove last letter
                    if len(ans)>0:
                        ans = ans[:-1]
                elif e.key == K_KP_ENTER or e.key == K_RETURN : 
                    typing = False
                else:
                    ans += chr(e.key)
                    
        txtPic = arialFont.render(ans, True, (0,0,0))   #
        draw.rect(screen,(220,255,220),textArea)        # draw the text window and the text.
        draw.rect(screen,(0,0,0),textArea,2)            #
        screen.blit(txtPic,(textArea.x+3,textArea.y+6))        
        display.flip()
        
    screen.blit(back,(0,0))
    return ans
"""def flood (x,y,newClr,oldClr):
    #first point to check
    vs_queue = deque ( [(x,y)] );
   
    #a set of visited points, empty because nothing has been checked yet
    vs = Set()
   
    #looks at the surrounding points
    surround = [(-1,0),(+1,0),(0,-1),(0,+1)]
   
    #while there are still points left to visit
    while vs_queue:
        #gets the next point to visit
        pt = vs_queue.popleft()
       
        #if the colour of the point is the current colour and the point has not been visited
        if screen.get_at(pt) == oldClr and pt not in vs and canvasRect.collidepoint(pt):
            #change the colour
            screen.set_at(pt, newClr)
           
            #set point as visited (add that point to the visited set)
            vs.add(pt)
   
            #looks at surrounding points adds them to the to-be-visited list
            for s in surround:
                vs_queue.append ((pt[0]+s[0],pt[1]+s[1]))
"""
vs=[]
def gradient (cmx,cmy,mx,my,firstclr,oldclr,r,g,b):
    #same set up as the floodfill
    vs_queue = deque ([(cmx+1,cmy+1)]);
    
    surround = [(+1,0),(0,+1),(-1,0),(0,-1)]

    #distance from the x coordinates of the gradient line (path of the gradient)
    length=mx-cmx
    
    #finding the r,g,b values of the first colour
    r1=firstclr[0]
    g1=firstclr[1]
    b1=firstclr[2]

    x=max(cmx,umx)
    x2=min(cmx,umx)
    y=max(cmy,umy)
    y2=min(cmy,umy)

    while vs_queue:
        pt= vs_queue.popleft()
        
        #distance from the point being checked to the x-coordinate of the gradient line 
        dist=pt[0]-cmx

        # if the point is the old colour or it satsifies the equation of the gradient line
        if (screen.get_at(pt)==oldclr or (pt[0]*(cmy-my)+pt[1]*(mx-cmx)+(cmx*my-cmy*mx)!=0 and pt[0]>=x2 and pt[0]<=x and pt[1]>=y2 and pt[1]<=y)) and pt not in vs and canvasRect.collidepoint(pt):
            #if length greater than 0, if the line is drawn from left to right
            if length>0:
                #if the point is not greater than the x coordinate of the rightmost point of the line, it will be coloured as the 2nd colour
                if pt[0]>=x:
                    screen.set_at(pt,(r1-r,g1-g,b1-b))
                    
                #if the point is not greater than the x coordinate of the leftmost point of the line, it will be coloured as the first colour    
                elif pt[0]<=x2:
                    screen.set_at(pt,firstclr)
                    
                #if the point is on the within the range of the line, it will be coloured depending on how far away it is from the gradient line's beginning point
                elif dist!=0:
                    screen.set_at(pt,(int(r1-dist*(r/float(length))),int(g1-dist*(g/float(length))),int(b1-dist*(b/float(length)))))

            #if length is less than 0
            if length<0:
                #similar situation as before
                if pt[0]>=x:    #the firstclr is used because the line is draw from right to left
                    screen.set_at(pt,firstclr)
                elif pt[0]<=x2:
                    screen.set_at(pt,(r1-r,g1-g,b1-b))
                elif dist!=0:
                    screen.set_at(pt,(int(r1-dist*(r/float(length))),int(g1-dist*(g/float(length))),int(b1-dist*(b/float(length)))))
            vs.append(pt)  #adds the point to the set
            for s in surround:
                vs_queue.append ((pt[0]+s[0],pt[1]+s[1]))

                 
    

font.init()                                

smx=50

#loading fonts
comic = font.SysFont("Comic Sans MS", 14)
comic2 = font.SysFont("Comic Sans MS", 12)

screen.blit(sizecursor,(50,542))

display.set_caption("Maplestory Paint")

#cursor for the spraypaint"
spraypaint_strings=("           ####         ",
"############..#         ",
"########   ####         ",
"######      ##          ",
"#####     ######        ",
"####    ##########      ",
"###   ##############    ",
"##    #............#    ",
"#     #............#    ",
"      #............#    ",
"      #............#    ",
"      #............#    ",
"      #...######...#    ",
"      #..##....##..#    ",
"      #..##........#    ",
"      #...######...#    ",
"      #........##..#    ",
"      #..##....##..#    ",
"      #...######...#    ",
"      #............#    ",
"      #............#    ",
"      #............#    ",
"      #............#    ",
"      ##############    ")

#compile the strings into a cursor
datatuple, masktuple = cursors.compile(spraypaint_strings,black='.',white='#', xor='o' )

select=0

#undo/redo lists
undolist=[]
redolist=[]
#blank canvas added
a_1=screen.subsurface(canvasRect).copy()
undolist.append(a_1)

mb=''

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==MOUSEBUTTONDOWN:
            cmx,cmy = evt.pos
            a=screen.copy()
            if evt.button==1:
                if paletteRect.collidepoint(mx,my): #changing the colour
                    del colours [0] #first colour is deleted
                    colours.append(colour1) #new colour is added to list to be displayed in the recent colour squares
                elif tool=="eyedropper" and canvasRect.collidepoint(mx,my): #selecting a colour from the canvas
                    del colours [0]
                    colours.append(colour1)
            if evt.button==3:
                a=screen.copy()
            #scrolling to change size    
            if evt.button == 4:
                if size<101:
                   size += 1
            if evt.button == 5:
                if size>1:
                   size -= 1
               
        if evt.type == MOUSEBUTTONUP:
            mouse.set_visible(True)
            umx,umy=mouse.get_pos()
        if evt.type == MOUSEBUTTONUP:
            #once the mouse is up, the screen is copied for undo/redo
            if canvasRect.collidepoint(mx,my) and (evt.button==1 or evt.button==3):
                edit = screen.subsurface(canvasRect).copy()
                undolist.append(edit)
        if evt.type==MOUSEBUTTONDOWN and evt.button==1:
            if undoRect.collidepoint(mx,my):
                if len(undolist) > 1:
                    redolist.append(undolist[-1]) #redo gets the most recent picture in the undo list
                    undolist.remove(undolist[-1]) #undo gets rid of the most recent picture
                    screen.blit(undolist[-1],(220,117)) # blits the 2nd most recent picture
            if redoRect.collidepoint(mx,my):
                if len(redolist) > 0:
                    screen.blit(redolist[-1],(220,117)) #redo first blits the picture
                    undolist.append(redolist[-1])       #undo gets the picture
                    redolist.remove(redolist[-1])       #redo gets rid of the picture
            

    omx,omy=mx,my

    
    keys=key.get_pressed()

    mx,my=mouse.get_pos()
    omb=mb
    mb=mouse.get_pressed()

    screen.blit(toolbar2,(816,110))
    
    draw.rect(screen,colour2,(842,128,24,24))
    draw.rect(screen,colour1,(834,120,24,24))
    
    #draws the recent colour squares, colour depends on position in the list
    for x in range (1,8):
        draw.rect(screen,colours[-x],(852+18*x,120,15,15))
        draw.rect(screen,colours[-x-7],(852+18*x,137,15,15))
           
                            
    screen.blit(palette,(834,160))

    draw.rect(screen,(119,187,68),(220,650,580,40))
    draw.rect(screen,(0,0,0),(220,650,580,40),2)

    if menu==0: #if the tool menu is selected
            
        screen.blit(toolbar,(20,109))
        screen.blit(sizebar,(54,550))
        
        #size cursor blits depending on what the size is
        #the size can be changed by click somewhere on the sizebar or dragging the sizecursor or scrolling
        screen.blit(sizecursor,(size+42,542))
        if mx>=50 and mx<=150 and my>=550 and my<=557 and mb[0]==1:
            size=mx-49
        screen.blit(tools,(29,73))
        screen.blit(stampsclicked,(110,73))
        screen.blit(pencil,(42,161))
        screen.blit(eyedropper,(43,231))
        screen.blit(rectangle,(110,160))
        screen.blit(paintbrush,(110,230))
        screen.blit(eraser,(42,300))
        screen.blit(line,(110,300))
        screen.blit(spray,(43,371))
        screen.blit(bucket,(42,440))
        screen.blit(ellipse,(110,370))
        screen.blit(gradienttool,(111,440))
        draw.rect(screen,(0,255,0),pencilRect,2)
        draw.rect(screen,(0,255,0),recttool,2)
        draw.rect(screen,(0,255,0),colourselect,2)
        draw.rect(screen,(0,255,0),brushtool,2)
        draw.rect(screen,(0,255,0),erasertool,2)
        draw.rect(screen,(0,255,0),linetool,2)
        draw.rect(screen,(0,255,0),spraypaint,2)
        draw.rect(screen,(0,255,0),ellipsetool,2)
        draw.rect(screen,(0,255,0),fillbucket,2)
        draw.rect(screen,(0,255,0),gradientRect,2)
        screen.blit(saveimage,(110,510))
        screen.blit(loadimage,(34,510))
        
        #displays tool name and any other instructions
        toolname = comic.render("TOOL: "+ tool.upper()+instruction.upper(), True, (0,0,0))
        instructions=comic.render(instruction2.upper(),True,(0,0,0))
        screen.blit(toolname,(225,650))
        screen.blit(instructions, (360,668))

        
#when the tool is clicked, the rectangle around the icon turns red
        
        if pencilRect.collidepoint(mx,my) and mb[0]==1:    
            draw.rect(screen,(255,0,0),pencilRect,2)
            tool="pencil"
            instruction=''

        if recttool.collidepoint(mx,my) and mb[0]==1:    
            draw.rect(screen,(255,0,0),recttool,2)
            tool="rectangle"
            instruction=" ---> hold down ctrl to draw a filled rectangle"

        if colourselect.collidepoint(mx,my) and mb[0]==1:    
            draw.rect(screen,(255,0,0),colourselect,2)
            tool="eyedropper"
            instruction=" ---> pick a colour from the colour palette"

        if brushtool.collidepoint(mx,my) and mb[0]==1:    
            draw.rect(screen,(255,0,0),brushtool,2)
            tool="brush"
            instruction=''

        if erasertool.collidepoint(mx,my) and mb[0]==1:    
            draw.rect(screen,(255,0,0),erasertool,2)
            tool="eraser"
            instruction=''

        if linetool.collidepoint(mx,my) and mb[0]==1:
            draw.rect(screen,(255,0,0),linetool,2)
            tool="line"
            instruction=''

        if spraypaint.collidepoint(mx,my) and mb[0]==1:
            draw.rect(screen,(255,0,0),spraypaint,2)
            tool="spray paint"
            size=20
            instruction=''

        if ellipsetool.collidepoint(mx,my) and mb[0]==1:
            draw.rect(screen,(255,0,0),ellipsetool,2)
            tool="ellipse"
            instruction=" ---> hold down ctrl to draw a filled ellipse"
            instruction2="hold down shift to draw a circle"

        if tool!="ellipse":
            instruction2=""

        if fillbucket.collidepoint(mx,my) and mb[0]==1:
            draw.rect(screen,(255,0,0),fillbucket,2)
            tool="paint bucket"
            instruction=" ---> click in a closed area to fill"

        if gradientRect.collidepoint(mx,my) and mb[0]==1:
            draw.rect(screen,(255,0,0),gradientRect,2)
            tool="gradient"
            instruction=" ---> draw a line inside a closed area"

        if tool=="eyedropper":
            draw.rect(screen,(255,0,0),colourselect,2)
                           
        if tool=="rectangle":
            draw.rect(screen,(255,0,0),recttool,2)
        if tool=="pencil":
            draw.rect(screen,(255,0,0),pencilRect,2)
        if tool=="brush":
            draw.rect(screen,(255,0,0),brushtool,2)
        if tool=="eraser":
            draw.rect(screen,(255,0,0),erasertool,2)
        if tool=="line":
            draw.rect(screen,(255,0,0),linetool,2)
        if tool=="spray paint":
            draw.rect(screen,(255,0,0),spraypaint,2)
        if tool=="ellipse":
            draw.rect(screen,(255,0,0),ellipsetool,2)
        if tool=="paint bucket":
            draw.rect(screen,(255,0,0),fillbucket,2)
        if tool=="gradient" or tool=="Gradient":
            draw.rect(screen,(255,0,0),gradientRect,2)
            
            

    if menu==1: #if the stamps menu is selected
        screen.blit(stamps,(110,73))
        screen.blit(toolbar,(20,109))
        screen.blit(toolsclicked,(29,73))
        screen.blit(loadimage,(34,510))
        screen.blit(saveimage,(110,510))

        #blits the transparent version of the icon if the tool is selected
        if tool!="alishar":
            screen.blit(alishar[0], (32,150))
        else:
            screen.blit(alishar[1], (32,150))
        if tool!="papulatus":
            screen.blit(papulatus[0], (108,148))
        else:
            screen.blit(papulatus[1], (108,148))
        if tool!="jr balrog":
            screen.blit(balrog[0], (32,238))
        else:
            screen.blit(balrog[1], (32,238))
        if tool!="blue mushmom":
            screen.blit(mushmom[0], (108,238))
        else:
            screen.blit(mushmom[1], (108,238))
        if tool!="slime":
            screen.blit(slime[0], (32,328))
        else:
            screen.blit(slime[1], (32,328))
        if tool!="zombie mushroom":
            screen.blit(zombiemush[0], (114,328))
        else:
            screen.blit(zombiemush[1], (114,328))

        # if the mouse is clicking on the stamp icon
        if mb[0]==1:
            if mx>=32 and mx<=100 and my>=150 and my<=223:
                tool="alishar"
                screen.blit(alishar[1], (30,150))
            if mx>=108 and mx<=175 and my>=148 and my<=227:
                tool="papulatus"
                screen.blit(papulatus[1], (106,148))
            if mx>=32 and mx<=100 and my>=238 and my <=304:
                tool="jr balrog"
                screen.blit(balrog[1], (30,238))
            if mx>=108 and mx<=176 and my>=238 and my<=301:
                tool="blue mushmom"
                screen.blit(mushmom[1], (106,238))
            if mx>=32 and mx<=96 and my>=328 and my<=377:
                tool="slime"
                screen.blit(slime[1], (30,328))
            if mx>=114 and mx<=170 and my>=328 and my<=380:
                tool="zombie mushroom"
                screen.blit(zombiemush[1], (112,328))
            
        stampname = comic.render("STAMP: "+ tool.upper(), True, (0,0,0))
        screen.blit(stampname,(225,650))

                
#STAMPS------------------------------------------------

    #click for stamps 
    if canvasRect.collidepoint(mx,my):
        screen.set_clip(canvasRect)
        
        if tool=="alishar":
            if evt.type==MOUSEBUTTONDOWN or mb[0]==1:
                screen.blit(a,(0,0))
                screen.blit(alishar[2],(mx-124,my-132))
        
        if tool=="papulatus":
            if evt.type==MOUSEBUTTONDOWN or mb[0]==1:
                screen.blit(a,(0,0))
                screen.blit(papulatus[2],(mx-117,my-137))

        if tool=="jr balrog":
            if evt.type==MOUSEBUTTONDOWN or mb[0]==1:
                screen.blit(a,(0,0))
                screen.blit(balrog[2],(mx-80,my-78))

        if tool=="blue mushmom":
            if evt.type==MOUSEBUTTONDOWN or mb[0]==1:
                screen.blit(a,(0,0))
                screen.blit(mushmom[2],(mx-59,my-55))

        if tool=="slime":
            if evt.type==MOUSEBUTTONDOWN or mb[0]==1:
                screen.blit(a,(0,0))
                screen.blit(slime[2],(mx-32,my-24))

        if tool=="zombie mushroom":
            if evt.type==MOUSEBUTTONDOWN or mb[0]==1:
                screen.blit(a,(0,0))
                screen.blit(zombiemush[2],(mx-31,my-29))
        screen.set_clip(None)


#TOOLS-----------------------------------------------
    if tool=="spray paint" and canvasRect.collidepoint(mx,my): 
        mouse.set_cursor((24,24),(0,0),datatuple,masktuple) #if tool is spraypaint, change to spraypaint cursor
    else: mouse.set_cursor(*cursors.arrow) # change back to regular cursor
    if canvasRect.collidepoint(mx,my):
        if mb[0]==1:
            colour=colour1 #colour1 for left mouse button
        if mb[2]==1:
            colour=colour2 #colour2 for right mouse button

        if mb[0]==1 or mb[2]==1:
            screen.set_clip(canvasRect)
            
            if tool=="eyedropper":
                if mb[0]==1:
                    colour1=screen.get_at((mx,my)) 
                if mb[2]==1:
                    colour2=screen.get_at((mx,my))

            if tool=="gradient":
                tool="Gradient"
                select=1
                #perpendicular=-(mx-cmx)/(my-cmy)                
                #x(cmy-my)+y(mx-cmx)+(cmx*my-cmy*mx)=0
                
            if tool=="Gradient": #tool is changed to Gradient to run only after drawing the line
                if mb[0]==1:
                    instruction=" ---> draw a line inside a closed area"
                    select=1
                    screen.blit(a,(0,0))
                    draw.line(screen,(0,0,0),(cmx,cmy),(mx,my),1)
                       
            if tool=="paint bucket":
                c=screen.get_at((mx,my))
                if c!=colour:   #only runs if the fill colour is not the colour already inside
                    flood(mx,my,colour,c)
            if tool=="ellipse":
                if keys[K_LSHIFT]==1 or keys[K_RSHIFT]==1: #changes to circle tool
                    screen.blit(a,(0,0))
                    radius=min(abs(cmx-mx),abs(cmy-my)) #takes the shorter distance
                    if radius/2>=size:  #if the radius/2 is bigger than size, it won't crash
                        draw.circle(screen,colour,((mx+cmx)/2,(my+cmy)/2),radius/2,size)
                        
                elif keys[K_LCTRL]==1 or keys[K_RCTRL]==1: #draws a filled ellipse
                    if abs(cmx-mx)>size*2 and abs(cmy-my)>size*2:

                        #finds minimum to set as the corner
                        x=min(cmx,mx)
                        x_2=max(cmx,mx)
                        y=min(cmy,my)
                        y_2=max(cmy,my)

                        screen.blit(a,(0,0))
                        draw.ellipse(screen,colour,(x,y,x_2-x,y_2-y)) #draws from the upperleft most corner

                else:   #draws a regular ellipse
                    if abs(cmx-mx)>size*2 and abs(cmy-my)>size*2: 
                        
                        #finding the max is not really necessary
                        x=min(cmx,mx)
                        x_2=max(cmx,mx)
                        y=min(cmy,my)
                        y_2=max(cmy,my)

                        screen.blit(a,(0,0))
                        draw.ellipse(screen,colour,(x,y,x_2-x,y_2-y),size)
                        
            if tool=="spray paint":
                for i in range (int(size**1.5)): #the speed of the spraypaint is exponential because it is colouring an area (squared units)
                    sx=randint(mx-size,mx+size) #takes random points in a square
                    sy=randint(my-size,my+size)
                    if ((mx-sx)**2+(my-sy)**2)**0.5 <= size: #only draws the point if the distance is less than or equal to the radius
                        draw.line(screen,colour,(sx,sy),(sx,sy))
                        
            if tool=="pencil":
                draw.aaline(screen, colour,(omx,omy),(mx,my),1) #aaline for clearer lines

            if tool=="brush":
                dist=((my-omy)**2+(mx-omx)**2)**0.5
                if dist!=0:
                    #takes the ratio of delta x over distance
                    bx=(mx-omx)/dist 
                    by=(my-omy)/dist
                    for i in range (int(dist)+1):
                        draw.circle(screen,colour,(int(omx+bx*i),int(omy+by*i)),size//2) #draws circles along the line in increments of bx and by

            if tool=="rectangle":
                screen.blit(a,(0,0))
                if keys[K_LCTRL]==1 or keys[K_RCTRL]==1: #draws filled
                    draw.rect(screen,colour,(cmx,cmy,mx-cmx,my-cmy))
                    
                else:
                    if mx>=cmx:
                        if size%2==0:
                            #this drawing method makes the rectangle more smooth as the size gets bigger
                            draw.line(screen,colour,(cmx-size/2+1,cmy),(mx+size/2,cmy),size)
                            draw.line(screen,colour,(cmx,cmy-size/2+1),(cmx,my+size/2),size)
                            draw.line(screen,colour,(mx,cmy-size/2+1),(mx,my+size/2),size)
                            draw.line(screen,colour,(cmx-size/2+1,my),(mx+size/2,my),size)
                        if size%2==1:
                            #a bit different from the first case because the size value is odd
                            draw.line(screen,colour,(cmx-size/2+1,cmy),(mx+size/2,cmy),size)
                            draw.line(screen,colour,(cmx,cmy-size/2),(cmx,my+size/2),size)
                            draw.line(screen,colour,(mx,cmy-size/2),(mx,my+size/2),size)
                            draw.line(screen,colour,(cmx-size/2+1,my),(mx+size/2,my),size)
                            
                    if mx<cmx:  #drawing the other direction
                        draw.line(screen,colour,(cmx+size/2,cmy),(mx-size/2,cmy),size)
                        draw.line(screen,colour,(cmx,cmy+size/2),(cmx,my-size/2),size)
                        draw.line(screen,colour,(mx,cmy+size/2),(mx,my-size/2),size)
                        draw.line(screen,colour,(cmx+size/2,my),(mx-size/2,my),size)

            if tool=="eraser":
                draw.line(screen,(255,255,255),(omx,omy),(mx,my),size)

            if tool=="line":
                screen.blit(a,(0,0))
                draw.line(screen, colour, (cmx,cmy),(mx,my),size)

            screen.set_clip(None)

        else:
            select=0


    if canvasRect.collidepoint(mx,my) and tool=="Gradient" and select==0: #when the tool is Gradient and the mouse has just been released
        screen.set_clip(canvasRect)
        #finds r,g,b values of the first colour and the 2nd colour
        r1=colour1[0] 
        g1=colour1[1]
        b1=colour1[2]
        r2=colour2[0]
        g2=colour2[1]
        b2=colour2[2]
        
        #finds the change in the r,g,b values
        r_c=r1-r2
        g_c=g1-g2
        b_c=b1-b2

        #finds the colour of the area that gradient is applied to
        #makes sure that the point is not on the line by checking one point over
        if mx>cmx:
            c=screen.get_at((mx+1,my))
        if mx<cmx:
            c=screen.get_at((mx-1,my))

        gradient(cmx,cmy,umx,umy,colour1,c,r_c,g_c,b_c)
        screen.set_clip(None)
        tool="gradient"

#-----------------------------------------------------
    if keys[K_SPACE]==1:    #screen clear
        screen.subsurface(canvasRect).fill((255,255,255))

    #getting a colour from the palette
    if mb[0]==1:
        if paletteRect.collidepoint(mx,my) or coloursRect.collidepoint(mx,my):
            colour1=screen.get_at((mx,my))
    if mb[2]==1:
        if paletteRect.collidepoint(mx,my) or coloursRect.collidepoint(mx,my):
            colour2=screen.get_at((mx,my))

        
    
                    
#-----------------------------------------------------
    if mb[0]==1:
        if saveRect.collidepoint((mx,my)):
            display.set_caption("Type in the save file name, saves as a jpg file")
            txt=getName()   #gets filename from user
            if txt!="": #dont save if the filename is blank
                image.save(screen.subsurface(canvasRect), txt+".jpg")
            display.set_caption("Maplestory Paint")
        
        #load
        if loadRect.collidepoint((mx,my)):            
            display.set_caption("Type in the name of the file you want to load")
            txt=getName()   #runs same function as save
            if txt!="":
                screen.blit(image.load(txt),(220,117))  #blits into the corner of canvas
            display.set_caption("Maplestory Paint")
            
        if mx>=110 and mx<=184 and my>=73 and my<=108:  #if the stamps icon is clicked
            if menu!=1:
                menu=1
                tool=""
                
    
        if mx>=29 and mx<=101 and my>=73 and my<=108:   #if the tools icon is clicked
            if menu!=0:
                menu=0
                tool=""

            
            
            
    display.flip()

font.quit()
quit()

    
    

    
