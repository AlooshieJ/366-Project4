class Testing:
    def __init__(self, first, last):
        self.first = first
        self.last = last
    def printName(self):
        print("Hello" +" "+ self.first +" "+ self.last)
Name = Testing("Luis","Schaad")
Name.printName()

