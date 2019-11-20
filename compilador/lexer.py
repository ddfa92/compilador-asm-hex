from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # LODD
        self.lexer.add('LODD', r'(?<!\w)LODD(?!\w)')
        # STOD
        self.lexer.add('STOD', r'(?<!\w)STOD(?!\w)')
        # ADDD
        self.lexer.add('ADDD', r'(?<!\w)ADDD(?!\w)')
        # SUBD
        self.lexer.add('SUBD', r'(?<!\w)SUBD(?!\w)')
        # JPOS
        self.lexer.add('JPOS', r'(?<!\w)JPOS(?!\w)')
        # JZER
        self.lexer.add('JZER', r'(?<!\w)JZER(?!\w)')
        # JUMP
        self.lexer.add('JUMP', r'(?<!\w)JUMP(?!\w)')
        # LOCO
        self.lexer.add('LOCO', r'(?<!\w)LOCO(?!\w)')
        # LODL
        self.lexer.add('LODL', r'(?<!\w)LODL(?!\w)')
        # STOL
        self.lexer.add('STOL', r'(?<!\w)STOL(?!\w)')
        # ADDL
        self.lexer.add('ADDL', r'(?<!\w)ADDL(?!\w)')
        # SUBL
        self.lexer.add('SUBL', r'(?<!\w)SUBL(?!\w)')
        # JNEG
        self.lexer.add('JNEG', r'(?<!\w)JNEG(?!\w)')
        # JNZE
        self.lexer.add('JNZE', r'(?<!\w)JNZE(?!\w)')
        # CALL
        self.lexer.add('CALL', r'(?<!\w)CALL(?!\w)')
        # PUSHI
        self.lexer.add('PUSHI', r'(?<!\w)PUSHI(?!\w)')
        # POPI
        self.lexer.add('POPI', r'(?<!\w)POPI(?!\w)')
        # PUSH
        self.lexer.add('PUSH', r'(?<!\w)PUSH(?!\w)')
        # POP
        self.lexer.add('POP', r'(?<!\w)POP(?!\w)')
        # RETN
        self.lexer.add('RETN', r'(?<!\w)RETN(?!\w)')
        # SWAP
        self.lexer.add('SWAP', r'(?<!\w)SWAP(?!\w)')
        # INSP
        self.lexer.add('INSP', r'(?<!\w)INSP(?!\w)')
        # DESP
        self.lexer.add('DESP', r'(?<!\w)DESP(?!\w)')
        # INPAC
        self.lexer.add('INPAC', r'(?<!\w)INPAC(?!\w)')
        # OUTAC
        self.lexer.add('OUTAC', r'(?<!\w)OUTAC(?!\w)')
        # HALT
        self.lexer.add('HALT', r'(?<!\w)HALT(?!\w)')
        # ETIQUETA
        self.lexer.add('ETIQUETA', r'\@[A-Za-z]\w*')
        # VARIABLE
        self.lexer.add('VARIABLE', r'(?<!\w)[A-Za-z]\w*')
        # DIRECCION
        self.lexer.add('DIRECCION', r'(?<!\w)0x[A-F0-9][A-F0-9](?!\w)')
        # Numero
        self.lexer.add('NUMERO', r'(?<![A-Za-z])\d+(?![A-Za-z])')
        # Ignore spaces
        self.lexer.ignore('\s+')
        self.lexer.ignore('\%.*')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()