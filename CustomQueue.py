from dataclasses import dataclass


@dataclass
class CustomQueue:
    items: list
    MAXSIZE: int
    x_values = set()

    def xSet(self) -> set:
        if not self.x_values:
            for items in self.items:
                self.x_values.add(items.pos[0])
        return self.x_values
    
    def removeX(self, x):
        if x in self.x_values:
            self.x_values.remove(x)

    def addX(self, x):
        self.x_values.add(x)

    def isEmpty(self) -> bool:
        return len(self.items) == 0
    
    def enqueue(self, item):
        if self.MAXSIZE == len(self.items):
            return 
        
        if not self.isEmpty():
            self.items.append(item)
            self.Sort()
        else: 
            self.items.append(item)

    def dequeue(self):
        if self.isEmpty():
            return 
        item = self.Top()
        self.items.pop(0)
        return item
    
    def Top(self):
        return self.items[0]

    def Sort(self):
        for i in range(len(self.items)):
            idx = i
            for j in range(len(self.items)):
                if self.items[idx].pos[1] < self.items[j].pos[1]:
                    idx = j
            self.items[i], self.items[idx] = self.items[idx], self.items[i]

    def Pop(self, node, add):
        for i in range(len(self.items)):
            if self.items[i].pos == node.pos:
                new = add()
                self.items[i] = new
                return new

    def check(self, height):
        if self.Top().pos[1] >= height and self.Top().maxed:
            return self.dequeue()
        if self.Top().pos[1] >= height and self.Top().next:
            item = self.Top()
            item = item.next
        return None
        


    def UpdateNodes(self, appendFunc):
        for item in self.items:
            node = item
            while node:
                node.pos = (node.pos[0], node.pos[1] + 5)
                node = node.next
        
        for item in self.items:
            node = item
            appendFunc(node)
    
    def Trails(self) -> list:
        return self.items
