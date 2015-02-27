___author___ = "Olga Titova"

import copy


class BranchAndBound(object):
    def __init__(self, e=(),c=()):
        n = len(e)
        self.Coef = c
        self.Elem = e
        self.X = 0
        self.C = 0
        self.Adress = [0 for _ in range(n+1)]
        self.Adress[0] = 1
        self.FixedValue = self.X * self.C
        TempValue = 0
        C = sorted(c,reverse=True)
        for x in range(n):
            TempValue += (C[x] * self.Elem[x])
        self.FuncValue = TempValue + self.FixedValue
        self.IfParent = False

    def printbranch(self,array):
        print('------------')
        print("MyTree.C = ", self.C)
        print("MyTree.X = ", self.X)
        print('MyTree.FuncValue = ', self.FuncValue)
        print('MyTree.FixedValue = ', self.FixedValue)
        print('MyTree.Coef = ', self.Coef)
        print('MyTree.Elem = ', self.Elem)
        print('MyTree.Adress = ', self.Adress)
        print('MyTree.Cycle = ', self.ifcycle(array))
        print('------------')

    def getindex(self, Array, Elem):
        return Array.index(Elem)

    def findminimum (self, array):
        return min(array)

    def ifcycle (self,array):
        index = 0
        indexN = 0
        counter = 0
        ifcycle = False
        ifnull = False
        Cycle = False
        if (0 in self.Adress):
            n = self.Adress.index(0)
        else:
            n = len(self.Adress) - 1
        for z in range(1, n):
            counter = 0
            index = z
            indexN = 1 + array.index(self.Adress[z])
            while not ((ifcycle == True)or(ifnull == True)):
                index = indexN
                if  (self.Adress[index] != 0):
                    indexN = 1 + array.index(self.Adress[index])
                else:
                    ifnull = True
                if (indexN == z):
                    ifcycle = True
                counter += 1
            if ((ifcycle == True) and (counter != len(self.Adress)-2)):
                Cycle = True
            if ((ifcycle == True) and (counter == len(self.Adress)-2)):
                break
            ifnull = False
        return(Cycle)

    def generatedaughterbranch(self, InputE):
        n = len(self.Adress) - self.Adress.index(0)
        temp = [copy.deepcopy(self) for _ in range(n)]
        for x in range(n):
            temp[x].C = temp[x].Coef[0]
            temp[x].X = temp[x].Elem[x]
            temp[x].Adress[temp[x].Adress.index(0)] = temp[x].X
            temp[x].Coef.pop(0)
            temp[x].Coef.append(0)
            temp[x].Elem.pop(x)
            temp[x].Elem.append(0)
            temp[x].FixedValue += temp[x].X * temp[x].C
            TempValue = 0
            C = sorted(temp[x].Coef,reverse=True)
            for y in range(n):
              TempValue += (C[y] * temp[x].Elem[y])
            temp[x].FuncValue = TempValue + temp[x].FixedValue
            self.IfParent = True
        return (temp)

    def findcyclemin(self,el):
        counter = 0
        tree = []
        tree.append(copy.deepcopy(self))
        Parent = tree[0]
        n = len(Parent.Adress) - Parent.Adress.index(0)
        while (n > 0):
            daughterarray = Parent.generatedaughterbranch(el)
            temp = []
            for x in range(len(daughterarray)):
                if (daughterarray[x].ifcycle(el) == False):
                    temp.append(copy.deepcopy(daughterarray[x]))
            if (len(temp) > 0):
                Minim = temp[0]
                for y in range(len(temp)):
                    if (Minim.FuncValue>temp[y].FuncValue):
                        Minim = temp[y]
                    tree.append(temp[y])
            elif(len(temp) == 0):
                Minim = tree[0]
            tree.remove(Parent)
            for z in range(len(tree)):
                if ((Minim.FuncValue>tree[z].FuncValue) and (tree[z].ifcycle(el) == False)):
                    Minim = tree[z]
            Parent = Minim
            if (0 in Parent.Adress):
                n = len(Parent.Adress) - Parent.Adress.index(0)
            else:
                n = 0
        return (Minim)

if __name__ == "__main__":
    el = [1, 2, 3]
    co = [6.79877, 6.53333, 9.84568]
    bb = BranchAndBound(el,co)
    #bb.Adress = [1, 4, 1, 2, 3]
    #print(bb.ifcycle(el))
    bb.printbranch(el)
    bbdaughter = bb.findcyclemin(el)
    bbdaughter.printbranch(el)
