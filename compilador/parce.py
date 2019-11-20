from rply import ParserGenerator
from abs_syn_tree import *


def int_to_hex_16(value):
    value=value%256
    if len(hex(value)[2:]) < 2:
        return "0"+hex(value)[2:].upper()
    else:
        return hex(value)[2:].upper()
    
class Parser():
    def __init__(self, dic_variables, dic_etiquetas):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['LODD','STOD','ADDD','SUBD','JPOS','JZER','JUMP','LOCO','LODL','STOL','ADDL','SUBL','JNEG','JNZE','CALL','PUSHI','POPI','PUSH','POP','RETN','SWAP','INSP','DESP','INPAC', 'OUTAC','HALT','DIRECCION', 'NUMERO', 'VARIABLE', 'ETIQUETA']
        )
        self.dic_variables=dic_variables
        self.dic_etiquetas=dic_etiquetas
        
    def parse(self):
    
        @self.pg.production('expression : LODD expression')
        @self.pg.production('expression : STOD expression')
        @self.pg.production('expression : ADDD expression')
        @self.pg.production('expression : SUBD expression')
        @self.pg.production('expression : JPOS expression')
        @self.pg.production('expression : JZER expression')
        @self.pg.production('expression : JUMP expression')
        @self.pg.production('expression : LOCO expression')
        @self.pg.production('expression : LODL expression')
        @self.pg.production('expression : STOL expression')
        @self.pg.production('expression : ADDL expression')
        @self.pg.production('expression : SUBL expression')
        @self.pg.production('expression : JNEG expression')
        @self.pg.production('expression : JNZE expression')
        @self.pg.production('expression : CALL expression')
        @self.pg.production('expression : INSP expression')
        @self.pg.production('expression : DESP expression')
        def expression(p):
            if p[0].gettokentype() == 'LODD':
                return Lodd(p[1])
            elif p[0].gettokentype() == 'STOD':
                return Stod(p[1])
            elif p[0].gettokentype() == 'ADDD':
                return Addd(p[1])
            elif p[0].gettokentype() == 'SUBD':
                return Subd(p[1])
            elif p[0].gettokentype() == 'JPOS':
                return Jpos(p[1])
            elif p[0].gettokentype() == 'JZER':
                return Jzer(p[1])
            elif p[0].gettokentype() == 'JUMP':
                return Jump(p[1])
            elif p[0].gettokentype() == 'LOCO':
                return Loco(p[1])
            elif p[0].gettokentype() == 'LODL':
                return Lodl(p[1])
            elif p[0].gettokentype() == 'STOL':
                return Stol(p[1])
            elif p[0].gettokentype() == 'ADDL':
                return Addl(p[1])
            elif p[0].gettokentype() == 'SUBL':
                return Subl(p[1])
            elif p[0].gettokentype() == 'JNEG':
                return Jneg(p[1])
            elif p[0].gettokentype() == 'JNZE':
                return Jnze(p[1])
            elif p[0].gettokentype() == 'CALL':
                return Call(p[1])
            elif p[0].gettokentype() == 'INSP':
                return Insp(p[1])
            elif p[0].gettokentype() == 'DESP':
                return Desp(p[1])
        
        @self.pg.production('expression : PUSHI')
        @self.pg.production('expression : POPI')
        @self.pg.production('expression : PUSH')
        @self.pg.production('expression : POP')
        @self.pg.production('expression : RETN')
        @self.pg.production('expression : SWAP')
        @self.pg.production('expression : INPAC')
        @self.pg.production('expression : OUTAC')
        @self.pg.production('expression : HALT')
        def expression(p):
            if p[0].gettokentype() == 'PUSHI':
                return Pushi()
            elif p[0].gettokentype() == 'POPI':
                return Popi()
            elif p[0].gettokentype() == 'PUSH':
                return Push()
            elif p[0].gettokentype() == 'POP':
                return Pop()
            elif p[0].gettokentype() == 'RETN':
                return Retn()
            elif p[0].gettokentype() == 'SWAP':
                return Swap()
            elif p[0].gettokentype() == 'INPAC':
                return Inpac()
            elif p[0].gettokentype() == 'OUTAC':
                return Outac()
            elif p[0].gettokentype() == 'HALT':
                return Halt()
        
                  
        @self.pg.production('expression : DIRECCION')
        def expression(p):
            return Direccion(p[0])
            
        @self.pg.production('expression : VARIABLE')    
        def expression(p):
            return Variable(p[0].value, self.dic_variables)
            
        @self.pg.production('expression : NUMERO') 
        def expression(p):
            return NumeroUnsigned(p[0].value)
            
        @self.pg.production('expression : ETIQUETA expression')
        def expression(p):
            return Etiqueta_Inicial(p[1])
            
        @self.pg.production('expression : ETIQUETA')
        def expression(p):
            return Etiqueta(p[0].value, self.dic_etiquetas)
        
        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()