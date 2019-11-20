class UnaryOp():
    def __init__(self, derecha):
        self.derecha= derecha
class Lodd(UnaryOp):
    def eval(self):
        return "00"+self.derecha.eval()
class Stod(UnaryOp):
    def eval(self):
        return "10"+self.derecha.eval()
class Addd(UnaryOp):
    def eval(self):
        return "20"+self.derecha.eval()
class Subd(UnaryOp):
    def eval(self):
        return "30"+self.derecha.eval()
class Jpos(UnaryOp):
    def eval(self):
        return "40"+self.derecha.eval()
class Jzer(UnaryOp):
    def eval(self):
        return "50"+self.derecha.eval()
class Jump(UnaryOp):
    def eval(self):
        return "60"+self.derecha.eval()
class Loco(UnaryOp):
    def eval(self):
        return "70"+self.derecha.eval()
class Lodl(UnaryOp):
    def eval(self):
        return "80"+self.derecha.eval()
class Stol(UnaryOp):
    def eval(self):
        return "90"+self.derecha.eval()
class Addl(UnaryOp):
    def eval(self):
        return "A0"+self.derecha.eval()
class Subl(UnaryOp):
    def eval(self):
        return "B0"+self.derecha.eval()
class Jneg(UnaryOp):
    def eval(self):
        return "C0"+self.derecha.eval()
class Jnze(UnaryOp):
    def eval(self):
        return "D0"+self.derecha.eval()
class Call(UnaryOp):
    def eval(self):
        return "E0"+self.derecha.eval()
class Pushi():
    def eval(self):
        return "F000"
class Popi():
    def eval(self):
        return "F100"
class Push():
    def eval(self):
        return "F200"
class Pop():
    def eval(self):
        return "F300"
class Retn():
    def eval(self):
        return "F400"
class Swap():
    def eval(self):
        return "F500"
class Insp(UnaryOp):
    def eval(self):
        return "F6"+self.derecha.eval()
class Desp(UnaryOp):
    def eval(self):
        return "F7"+self.derecha.eval()
class Inpac():
    def eval(self):
        return "F800"
class Outac():
    def eval(self):
        return "F900"
class Halt():
    def eval(self):
        return "FA00"

class NumeroUnsigned():
    def __init__(self, value):
        self.value = value

    def eval(self):
        j= int(self.value)%256
        if len(hex(j)[2:]) < 2:
            return "0"+hex(j)[2:].upper()
        else:
            return hex(j)[2:].upper()

class Direccion():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value[2:]
        
class Etiqueta():
    def __init__(self, value, dic_etiquetas):
        self.value = value
        self.dic_etiquetas= dic_etiquetas

    def eval(self): #Devuelve la dirección donde se encuentra la etiqueta
        return self.dic_etiquetas[self.value]
        
class Etiqueta_Inicial(UnaryOp):
    def eval(self):
        return self.derecha.eval()
        
        
class Variable():
    def __init__(self,value, dic_variables):
        self.value = value
        self.dic_variables=dic_variables

    def eval(self):
        return self.dic_variables[self.value]
