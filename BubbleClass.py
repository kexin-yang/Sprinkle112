import random
import hearWords
class Bubble():
    # define bubble
    def __init__(self,cx,cy,r,color,direction,word):
        # a bubble has a position, size, color and a word in it
        self.cx = cx
        self.cy = cy
        self.r = r
        self.color = color
        self.direction = direction
        self.word = word

    # cite from hw5,15112, line 15-18
    def draw(self, canvas):
        # draw the bubbles on canvas
        canvas.create_oval(self.cx-self.r,self.cy-self.r,self.cx+self.r, self.cy+self.r, fill= self.color)
        canvas.create_text(self.cx,self.cy,text = self.word)
    def moveBubble(self):
        # make the bubble move
        self.cx += self.direction[0]
        self.cy += self.direction[1]

    def collideWithBorder(self,height,width):
        # see if the bubble collide with border
        return self.cx-self.r <= 0 or self.cx+self.r>= width or self.cy-self.r <= 0 or self.cy+self.r>= height

    def touchOtherBubble(self,other):
        # see if the bubble touches other bubble
        if isinstance(other,Bubble) and distance(other.cx,other.cy, self.cx,self.cy)<other.r+self.r:
            return True
        else:
            return False

    def reactToBorderHit(self,width, height):
        if (self.cx-self.r) < 0 or (self.cx+ self.r>width):
            self.direction[0] = ((-1)*self.direction[0])
        elif (self.cy-self.r) < 0 or (self.cy+self.r)> height:
            self.direction[1] = ((-1)*self.direction[1])

# Graphic function
from tkinter import *
def generateWords():
    # this function provide a pool of words that can make senteces, and randomly choose from them
    wordPool = (["he","really","likes","apples"],["i","can","play","football"],["they","enjoy","having","dinner","together"])
    word = random.choice(wordPool)
    return word

def init(data):
    data.score = 0
    data.bubbles = []
    data.words = generateWords()
    data.time = 0
    data.hearMessage = ""
    data.heardWord = ""
    data.speakingInstruction = "Say a word in the bubble!"
def mouthPressed(event,data):
    pass
def keyPressed(event,data):
    pass
def timerFired(data):
    data.time += 1
    print("instruction",data.speakingInstruction)
    print("hearMessage:",data.hearMessage)
    for bubble in reversed(data.bubbles):
        if bubble.word == data.heardWord:
            data.bubbles = []
    if data.time % 5 == 0:
        putBubble(data)
    if data.time % 8 == 0:
        checkIfHeard(data)

def checkIfHeard(data):
    # this function check if we hear any words in the bubble
    data.speakingInstruction = "Say a word in the bubble!"
    spoken = hearWords.recognizeWords()
    print("spoken",spoken)
    if spoken == None:
        data.hearMessage = "We didn't hear what you say, try again!"
        #data.speakingInstruction = ""
        print(data.hearMessage)
    elif spoken in data.words:
        data.hearMessage = "You spoke '%s' correctly!" % spoken
        #data.speakingInstruction = ""
        data.heardWord = spoken
        data.words.remove(spoken)
        print(data.words)
        bubbleBurst(data)
    else:
        data.hearMessage = "Did you said '%s'? \n Try again by saying words in the bubble!" % spoken
        #data.speakingInstruction = ""
        print(data.hearMessage)

def bubbleBurst(data):
    pass

def putBubble(data):
    # this function places bubble in the data
    for i in range(len(data.words)):
        print(i)
        speedLow, speedHigh = 8,12
        cx =  (1/(len(data.words)+1))*data.width * (i+1)
        cy = 0.25 * data.height
        r = 30
        #!! r can change later
        color = random.choice(["cyan","pink","yellow","green","gold","white"])
        #!! can change later
        direction = random.choice([[0, 1], [0, -1], [1, 1], [1, -1], [1, 0], [-1, 0], [-1, -1], [-1, 1]])
        speed = random.randint(speedLow,speedHigh)
        bubble = Bubble(cx,cy,r,color,direction,data.words[i])
        data.bubbles.append(bubble)

def redrawAll(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height,fill = "lightblue")
    for bubble in data.bubbles:
        bubble.draw(canvas)
    canvas.create_text(data.width/2, data.height, anchor="s", fill="yellow",
                       font="Arial 24 bold", text="Score: " + str(data.score))
    canvas.create_text(data.width, 0.8* data.height, anchor="e", fill="brown",
                       font="Arial 30 bold", text=data.hearMessage)
    canvas.create_text(data.width, 0.5 * data.height, anchor="e", fill="brown",
                       font="Arial 30 bold", text=data.speakingInstruction)


#################################################################
# cited from course note: the run function- line 128-169
#################################################################

def runBubbles(width=600, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")



