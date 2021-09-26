from iop import *
class Console():
    def __init__(self,width,heigh):
        self.width = width
        self.heigh = heigh
        self.content = ""
   

    def __str__(self) -> str:
        return list(self.mass).__str__()
    def get(self):
        mass=[""]
        ofset = 0
        mindex=0
        for t in range(len(self.content)):#1-9

            if self.content[t]=="\n":
                mindex+=1
                mass.append('')
                ofset = 0
            else:
                if ofset==self.width:
                    mindex+=1
                    mass.append('')
                    ofset = 1
                else:
                    ofset +=1
                mass[mindex]+=(self.content[t])
        return mass
            
    def draw(self,x,y):
        mass = self.get()
        #move(x,y)
        for f in mass:
            print(f)
            movehor(x)