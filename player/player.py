from math import sqrt, exp

from classes.entity import Entity
from classes.weapon import Weapon
from .inventory import Inventory

class Player(Entity):
    def __init__(self, name, id=None):
        super().__init__(id=id)
        self.name: str = name
        self.blood: int = 100
        self.pneuma: int = 100
        self.hunger: int = 0
        self.stamina: int = 100
        self.pdr: int = 0
        self.bloodLoss: int = 0
        self.tiredLvl: int = 0
        self.cdims = {'ímpeto':0,'agilidade':0,'precisão':0,'defesa':0}
        self.cdimsTot: int = 6
        self.cdimsRsvd = {'ímpeto':0,'agilidade':0,'precisão':0,'defesa':0}
        self.weapon: Weapon = None
        self.sleeping: bool = False
        
        self.inventory = Inventory(self.id)
         
    def setCdim(self, cdimName, cdimVal):
        if(cdimVal < self.cdimsRsvd[cdimName]):
            print(f'Failed to assign value {cdimVal} to {cdimName}: smaller than reserved. Min allowed is {self.cdimsRsvd[cdimName]}.')
            return
        
        sum = cdimVal
        for k,v in self.cdims.items():
            if(k != cdimName):
                sum += v
        
        if(sum > self.cdimsTot):
            excess = sum - self.cdimsTot
            print(f'Failed to assign value {cdimVal} to {cdimName}: total cdims overshoot. Max allowed is {cdimVal - excess}.')
            return
        
        self.cdims[cdimName] = cdimVal
        
    def loadFromFile(self):
        pass
    
    def massCurCarrying(self):
        mass = 0.0
        for item in self.invtry:
            if(item.isContainer):
                for subItem in item.storedItems:
                    mass += subItem.kgs
            mass += item.kgs
        return mass
     
    def calcActDelay(self, act):
        delay = 0.0
        if(act == 'step'):
            mass = self.massCurCarrying()
            delay = mass*0.02 - 0.00004*self.cdims['precisão']*(mass**2) + 0.1/(self.cdims['agilidade']+1) + 0.3
        
        elif(act == 'roll'):
            mass = self.massCurCarrying()
            delay = 0.2/(self.cdims['precisão']+1)*mass - 0.000004*(self.cdims['precisão']**2)*(mass**2) + 1/(self.cdims['agilidade']**2+1) + 1.3
        
        elif(act == 'jump'):
            mass = self.massCurCarrying()
            delay = 0.02*mass - 0.000004*(self.cdims['precisão']**2)*(mass**2) + 0.1/(self.cdims['agilidade']+1) + 0.8
        
        elif(act == 'strike'):
            if(self.wpn is None):
                mass = 0.2
            else:
                mass = self.wpn.kgs
            delay = exp(-1*self.cdims['agilidade']/mass) + 0.1*mass/(self.cdims['ímpeto']+1) + 1/sqrt(self.cdims['agilidade']*self.cdims['ímpeto']+1)
        
        elif(act == 'interact'):
            print("Well, it's complicated. What are you interacting with?")
        
        elif(act == 'block'):
            pass

        else:
            print(f'Action {act} not recognized.')
        
        return delay

    def calcDmg(self, enemy, tgt):
        pass
    
    def wearItem(self, item):
        pass
    
    def takeBloodHit(self, dmg):
        self.blood -= dmg
    
    def takePDRHit(self, dmg):
        self.pdr -= dmg

    def takeStmHit(self, dmg):
        self.stamina -= dmg

    def eatFood(self, food):
        pass
    
    def printState(self):
        ret = ''
        ret += 'blood ' + str(self.blood) + '\n'
        ret += 'bloodLoss ' + str(self.bloodLoss) + '\n'
        ret += 'pneuma ' + str(self.pneuma) + '\n'
        ret += 'pdr ' + str(self.pdr) + '\n'
        ret += 'stamina ' + str(self.stamina) + '\n'
        ret += 'tiredLvl ' + str(self.tiredLvl) + '\n'
        ret += 'hungerPts ' + str(self.hunger) + '\n'
        return ret

    def addHunger(self, points: int):
        if not self.sleeping:
            self.hunger += points
    
    def goToSleep(self):
        self.sleeping = True
        self.pdr += 3
        self.pdr -= self.hunger

    def wakeUp(self):
        self.sleeping = False
        self.pneuma += self.pdr
