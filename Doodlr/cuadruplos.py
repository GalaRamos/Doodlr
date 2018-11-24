class cuadruplo:
    def __init__(self, ind, estatuto, var1, var2, var3):
        self.ind = ind
        self.estatuto = estatuto
        self.var1 = var1
        self.var2 = var2
        self.var3 = var3
    def __str__(self):
    	return str(self.ind) + "\t" + str(self.estatuto) + "\t" + str(self.var1) + "\t" + str(self.var2) + "\t" + str(self.var3)