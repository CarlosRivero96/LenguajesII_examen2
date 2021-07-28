import sys, operator

instructions = []
instPointer = 0
stack = []
tags = {}
vars = {}

def push(n):
    if (n == "true" or n == "false"):
        stack.append(eval(n.capitalize()))
    else:
        try:
            stack.append(int(n))
        except ValueError:
            print("\033[91mERROR: \033[0mValor no es número entero o literal booleano")

def pop():
    stack.pop()

def arithBinOp(op):
    if (len(stack) < 2):
        print("\033[91mERROR: \033[0mNo hay suficientes elementos en la pila")
    elif (type(stack[-1]) is not int or type(stack[-2]) is not int):
        print("\033[91mERROR: \033[0mvalores en el tope de la pila no son enteros")
    else:
        right = stack.pop()
        left = stack.pop()
        stack.append(op(left, right))
        
def boolBinOp(op):
    if (len(stack) < 2):
        print("\033[91mERROR: \033[0mNo hay suficientes elementos en la pila")
    elif (type(stack[-1]) is not bool or type(stack[-2]) is not bool):
        print("\033[91mERROR: \033[0mValores en el tope de la pila no son booleanos")
    else:
        right = stack.pop()
        left = stack.pop()
        stack.append(op(left, right))

def arithUnOp(op):
    if (len(stack) < 1):
        print("\033[91mERROR: \033[0mNo hay suficientes elementos en la pila")
    elif (type(stack[-1]) is not int):
        print("\033[91mERROR: \033[0mValor en el tope de la pila no es entero")
    else:
        stack.append(op(stack.pop()))

def boolUnOp(op):
    if (len(stack) < 1):
        print("\033[91mERROR: \033[0mNo hay suficientes elementos en la pila")
    elif (type(stack[-1]) is not bool):
        print("\033[91mERROR: \033[0mValor en el tope de la pila no es booleano")
    else:
        stack.append(op(stack.pop()))

def rvalue(id):
    if (id in vars):
        stack.append(vars[id])
    else:
        print(f'\033[91mERROR: \033[0mIdentificador \"{id}\" aún no tiene un valor asignado')

def lvalue(id):
    stack.append("l " + id)

def assign():
    if (len(stack) < 2):
        print("\033[91mERROR: \033[0mNo hay suficientes elementos en la pila")
    elif (type(stack[-1]) is not int and type(stack[-1]) is not bool and len(stack[-1].split()) != 2):
        print("\033[91mERROR: \033[0mEl valor en el tope de la pila no es un l-value")
    elif (type(stack[-2]) is not int and type(stack[-2]) is not bool and len(stack[-2].split()) == 2):
        print("\033[91mERROR: \033[0mNo se le puede asignar un l-value a un l-value")
    else:
        lv = stack.pop().split()[1]
        vars[lv] = stack.pop()

def goto(tag):
    global instPointer
    if (tag not in tags):
        print(f'\033[91mERROR: \033[0mLa etiqueta \"{tag}\" no esta asociada a ninguna instrucción')
        instPointer += 1
    else:
        instPointer = tags[tag]

def goTrue(tag):
    global instPointer
    if (tag not in tags):
        print(f'\033[91mERROR: \033[0mLa etiqueta \"{tag}\" no esta asociada a ninguna instrucción')
    elif(len(stack) < 1):
        print("\033[91mERROR: \033[0mNo hay suficientes elementos en la pila")
    elif (type(stack[-1]) is not bool):
        print("\033[91mERROR: \033[0mValor en el tope de la pila no es booleano")
    elif (stack.pop()):
        instPointer = tags[tag]
        return
    instPointer += 1

def goFalse(tag):
    global instPointer
    if (tag not in tags):
        print(f'\033[91mERROR: \033[0mLa etiqueta \"{tag}\" no esta asociada a ninguna instrucción')
    elif(len(stack) < 1):
        print("\033[91mERROR: \033[0mNo hay suficientes elementos en la pila")
    elif (type(stack[-1]) is not bool):
        print("\033[91mERROR: \033[0mValor en el tope de la pila no es booleano")
    elif (not stack.pop()):
        instPointer = tags[tag]
        return
    instPointer += 1

def read(id):
    v = input(f'Introduzca valor de \"{id}\": ')
    if (v == "true" or v == "false"):
        vars[id] = eval(v.capitalize())
    else:
        try:
            vars[id] = int(v)
        except ValueError:
            print("\033[91mERROR: \033[0mValor no es número entero o literal booleano")

def iprint(id):
    if (id in vars):
        print(vars[id])
    else:
        print(f'\033[91mERROR: \033[0mIdentificador \"{id}\" aún no tiene un valor asignado')

if len(sys.argv) < 2:
    print("\033[91mERROR: \033[0mDebe especificar el archivo")

with open (sys.argv[1]) as f:
    for line in f:
        instructions.append(line)

# Añadir los tags
for line in instructions:
    inst = line.split()

    if (inst[0][-1] == ":"):
        tags[inst.pop(0)[:-1]] = instPointer
    instPointer += 1

instPointer = 0
# Hacer la corrida
while(instPointer < len(instructions)):
    line = instructions[instPointer]
    inst = line.split()

    if (inst[0][-1] == ":"):
        inst.pop(0)

    if (len(inst) == 0):
        pass
    
    elif (inst[0] == "PUSH"):
        push(inst[1])
    elif (inst[0] == "POP"):
        pop()

    elif (inst[0] == "ADD"):
        arithBinOp(operator.add)
    elif (inst[0] == "SUB"):
        arithBinOp(operator.sub)    
    elif (inst[0] == "MUL"):
        arithBinOp(operator.mul)
    elif (inst[0] == "DIV"):
        arithBinOp(operator.floordiv)

    elif (inst[0] == "AND"):
        boolBinOp(operator.and_)
    elif (inst[0] == "OR"):
        boolBinOp(operator.or_)

    elif (inst[0] == "LT"):
        arithBinOp(operator.lt)
    elif (inst[0] == "LE"):
        arithBinOp(operator.le)
    elif (inst[0] == "GT"):
        arithBinOp(operator.gt)
    elif (inst[0] == "GE"):
        arithBinOp(operator.ge)
    elif (inst[0] == "EQ"):
        arithBinOp(operator.eq)
    elif (inst[0] == "NEQ"):
        arithBinOp(operator.ne)

    elif (inst[0] == "UMINUS"):
        arithUnOp(operator.neg)
    elif (inst[0] == "NOT"):
        boolUnOp(operator.not_)

    elif (inst[0] == "RVALUE"):
        rvalue(inst[1])
    elif (inst[0] == "LVALUE"):
        lvalue(inst[1])
    elif (inst[0] == "ASSIGN"):
        assign()

    elif (inst[0] == "GOTO"):
        goto(inst[1])
        continue
    elif (inst[0] == "GOTRUE"):
        goTrue(inst[1])
        continue
    elif (inst[0] == "GOFALSE"):
        goFalse(inst[1])
        continue

    elif (inst[0] == "READ"):
        read(inst[1])
    elif (inst[0] == "PRINT"):
        iprint(inst[1])

    elif (inst[0] == "RESET"):
        stack = []
        vars = {}
        for i in tags:
            if(tags[i] <= instPointer):
                tags.pop(i)
    elif (inst[0] == "EXIT"):
        sys.exit()

    instPointer += 1