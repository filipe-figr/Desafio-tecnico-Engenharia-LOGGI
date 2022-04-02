import os
from asyncio.windows_events import NULL
from numpy import isin

# chamando system
os.system("")

# Classe para mudar cor do texto
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

#processar qual será o item com base no código, se não exitir ele retorna um None
def processarItem(codigo) -> str:
    newCode = codigo[6:9]
    if newCode == "001":
        return "Jóias"
    elif newCode == "111":
        return "Livros"
    elif newCode == "333":
        return "Eletrônicos"
    elif newCode == "555":
        return "Bebidas"
    elif newCode == "888":
        return "Brinquedos"
    else:
        return None

#processar qual será a cidade com base no código, se não exitir ele retorna um None
def processarCidade(codigo) -> str:

    if int(codigo) >= 1 and int(codigo) <= 99:
        return "Sudeste"
    elif int(codigo) >= 100 and int(codigo) <= 199:
        return "Sul"
    elif int(codigo) >= 201 and int(codigo) <= 299:
        return "Centro-Oeste"
    elif int(codigo) >= 300 and int(codigo) <= 399:
        return "Nordeste"
    elif int(codigo) >= 400 and int(codigo) <= 499:
        return "Norte"
    else:
        return "Invalido"
        
#valida o código
def isValid(codigo) -> bool:
    if len(codigo) < 15:
        return False
    if processarCidade(codigo) == None:
        return False
    if processarItem(codigo) == None:
        return False
    if processarItem(codigo) == "Jóia" and processarCidadeDeOrigem(codigo) == "Centro-Oeste":
        return False
    if codigoVendedor(codigo) == "367":
        return False
    
#verifica sem destino pro Sul e com produto Brinquedo
def isDestinoSulComBrinquedo(codigo) -> bool:
    newCodigo = codigo[:3]
    if processarCidade(newCodigo) == "Sul" and processarItem(codigo) == "Brinquedo":
        return True
    return False

def processarCidadeDeOrigem(codigo)-> str:
    newCodigo = codigo[:3]
    return processarCidade(newCodigo)

def processarCidadeDestino(codigo)-> str:
    newCodigo = codigo[3:6]
    return processarCidade(newCodigo)

#retorna o código do vendedor
def codigoVendedor(codigo): return codigo[9:12]

def pacotesPorVendedor(codigo):
    vendedor = codigoVendedor(codigo)
    if vendedor in vendedores:
        vendedores[vendedor] += 1
    else:
        vendedores[vendedor] = 1
        


codigos = ["288355555123888", "335333555584333", "223343555124001", "002111555874555", "111188555654777", "111333555123333", "432055555123888", "079333555584333", "155333555124001", "333188555584333", "555288555123001", "111388555123555", "288000555367333", "066311555874001", "110333555123555", "333488555584333", "455448555123001", "022388555123555", "432044555845333", "034311555874001"]

#quantidade de pacotes por região, caso o código seja invalido ele vai para a key "Invalido"
qtdPacotesPorRegiaoDestino = {'Centro-Oeste': 0, 'Nordeste': 0, 'Norte': 0, 'Sudeste': 0, 'Sul': 0, 'Invalido': 0}

pacotesPorRegiaoDestino = {'Centro-Oeste': {'Jóias':[], 'Livros':[], 'Eletrônicos':[], 'Bebidas':[], 'Brinquedo':[]},
                        'Nordeste': {'Jóias':[], 'Livros':[], 'Eletrônicos':[], 'Bebidas':[], 'Brinquedo':[]},
                        'Norte':{'Jóias':[], 'Livros':[], 'Eletrônicos':[], 'Bebidas':[], 'Brinquedo':[]},
                        'Sudeste': {'Jóias':[], 'Livros':[], 'Eletrônicos':[], 'Bebidas':[], 'Brinquedo':[]},
                        'Sul': {'Jóias':[], 'Livros':[], 'Eletrônicos':[], 'Bebidas':[], 'Brinquedo':[]}}
vendedores = {}
pacotesOrigemSul = []
pacotesInvalidos = []

#intera sobre os codigos 
for codigo in codigos:
    cidadeDestino = processarCidadeDestino(codigo)
    tipoDeProduto = processarItem(codigo)
    qtdPacotesPorRegiaoDestino[cidadeDestino] += 1 #soma a quantidade de pacotes por região

    #verifica se o código é válido 
    if isValid(codigo) == False: 
        pacotesInvalidos.append(codigo)
        continue

    #Se brinquedo tem como Destino o Sul e é um Brinquedo então ele é add a lista 'pacotesOrigemSul'
    if isDestinoSulComBrinquedo == True: pacotesOrigemSul.append(codigo) 

    #adicionamos o produto a 'pacotesPorRegiao' com base na regiao e no tipo
    pacotesPorRegiaoDestino[cidadeDestino][tipoDeProduto].append(codigo)

    pacotesPorVendedor(codigo) #verificar de qual vendedor é o produto e adiciona + 1 a sua quantidade de produtos vendidos em 'vendedores'



print("############################ PACOTES VALIDOS POR DESTINO #############################")

for destino, tipos in pacotesPorRegiaoDestino.items():
    print(f"Pacotes destino {destino} - Total: {qtdPacotesPorRegiaoDestino[destino]}")
    for tipo in tipos:
        for i in pacotesPorRegiaoDestino[destino][tipo]:
            print(f"{style.GREEN}{i}{style.RESET}") #style é a mudança da linha no print
        

print("\n############################ PACOTES VALIDOS POR DESTINO E TIPO #######################")

for destino, tipos in pacotesPorRegiaoDestino.items():
    print(f"Pacotes válidos destino {destino}")
    for tipo in tipos:
        print(f"{tipo}:")
        if not pacotesPorRegiaoDestino[destino][tipo]:
            print(f"{style.RED}Sem pacotes deste tipo para esse destino{style.RESET}")
        for i in pacotesPorRegiaoDestino[destino][tipo]:
            print(f"{style.GREEN}{i}{style.RESET}")
        print("")
    print("-----------------------------------------")
   
print("\n############################ RELATÓRIO DE PACOTES PARA CADA VENDEDOR #####################")
for vendedor, pacotes in vendedores.items():
    print(f"Quantidade de pacotes para o vendedor {vendedor}: {style.GREEN}{vendedores[vendedor]}{style.RESET}")
    print("")


print("\n######### PACOTES QUE SERÃO DESPACHADOS NO CENTRO-OESTE DO CAMINHÃO SENTIDO NORTE ########")

for x in pacotesPorRegiaoDestino["Centro-Oeste"]:
    for i in pacotesPorRegiaoDestino["Centro-Oeste"][x]:
        print(f"{style.GREEN}{i}{style.RESET}")


print("\n######### PACOTES EM FILA QUE IRÃO PARA O NORTE PASSANDO PELO CENTRO-OESTE ################")

for destino,tipos in pacotesPorRegiaoDestino.items():
    if destino == "Centro-Oeste" or destino == "Norte":
        for tipo in tipos:
            for i in tipos[tipo]:
                print(f"{style.GREEN}{i}{style.RESET}", end=" → ")

print("TODOS OS PACOTES FORAM ENTREGUES")

print("\n############################ RELATÓRIO DE PACOTES INVÁLIDOS ###############################")
print(f"Pacotes Inválidos: Total: {qtdPacotesPorRegiaoDestino['Invalido']}")
for codigo in pacotesInvalidos:
    print(f"{style.RED}{codigo}{style.RESET}")
print("")
