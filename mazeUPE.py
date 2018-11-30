import requests
import sys

up=1
down=2
left=3
right=4
row=0
col=0
def getStates(token):
    result=requests.get("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token)
    return result.json()

def main():
    global row
    global col
    myID = {"uid":"504933797"}
    r = requests.post("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session", data=myID)
    response = r.json()
    print (response)
    token = response['token']
    for i in range(5):
        currentStates=getStates(token)
        print(currentStates)
        if currentStates["status"]=="FINISHED":
            return 0
        sizeX, sizeY = currentStates['maze_size'][0], currentStates['maze_size'][1]
        col=sizeX
        row=sizeY
        curx=currentStates['current_location'][0]
        cury = currentStates['current_location'][1]
        solveMaze(token,curx,cury)


def reverse(dir):
    if dir=="UP":
        return "DOWN"
    if dir =="DOWN":
        return "UP"
    if dir=="LEFT":
        return "RIGHT"
    if dir=="RIGHT":
        return "LEFT"

def outOfBound(dir,currentX,currentY):
    global row
    global col
    if dir == "UP":
        return (currentY-1)<0
    if dir =="DOWN":
        return (currentY+1)>=row
    if dir=="LEFT":
        return (currentX - 1) <0
    if dir=="RIGHT":
        return (currentX +1) >=col

def solveMaze(token,x,y):
    found_or_wall =[]
    found_or_wall.append([x,y])
    moveaStep(x,y,token,found_or_wall)



def moveaStep(currentX,currentY,token,found_or_wall):
    x=currentX
    y=currentY
    dict={"UP":[x,(y-1)],"DOWN":[x,(y+1)],"LEFT":[(x-1),y],"RIGHT":[(x+1),y]}
    for i,cod in dict.items():
        if (not outOfBound(i,x,y)and ([cod[0],cod[1]] not in found_or_wall)):
            result1=requests.post("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token,{"action":i}).json()
            print(result1)
            if result1["result"]=="WALL":
                found_or_wall.append([cod[0],cod[1]])
            elif  result1["result"]=="END":
                return True
            elif result1["result"]=="SUCCESS":
                found_or_wall.append([cod[0],cod[1]])
                if(moveaStep(cod[0],cod[1],token,found_or_wall)):
                    return True
                else :
                    r=requests.post("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token,{"action":reverse(i)}).json()


    return False





main()