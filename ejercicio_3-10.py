
deptos = []
pisos = {}
edificio = {}

#cantidad
l = 20              # ladrillos m2 pared
c = 15               # kg cemento m2 pared
L = 20              # largo cm
A = 30              # ancho cm
sup_cer = L * A
F = 10              # f cerámicos
Z = 1               # z kg pegamento
X = 5               # kg cemento m2 piso

V = 1              # ventanas primer piso
P = 3              # puertas primer piso

# costos
PL = 100            # cada ladrillo
PC = 40             # cemento por kg
PCE = 3700          # ceramico cada uno
PP = 1000           # pegamento por kg
PPU = 90000         # puerta
PV = 30000          # ventana
PCA = 150000        # cama
PS = 30000          # silla
PM = 100000         # mesa

ban = False

class depto:
    def __init__(self, piso, mts, mtspar, edificio):
        self.piso = piso
        self.mts = mts
        self.mtspar = mtspar
        self.edificio = edificio
    
    def __str__(self):
        return f"Piso {self.piso}, con {self.mts}mts de piso y {self.mtspar}mts de pared"
    
    def calcular(self):
        #cantidad de materiales
        self.cemento = (self.mtspar * c) + (self.mts * 2)   # kg cemento en total
        self.ladrillo = self.mtspar * L                     # unidades de ladrillo
        self.ceramico = self.mts / sup_cer                  # unidades cerámico
        self.pegamento = ((self.ceramico * Z) / F)          # kg pegamento
        
        #costos
        self.pladrillo = self.ladrillo * PL                 # ladrillo
        self.pcemento = self.cemento * PC                   # cemento
        self.pceram = self.ceramico * PCE                   # ceramico
        self.ppegame = self.pegamento * PP                  # pegamento

        if (self.ceramico * sup_cer) > 500:                 # si el dpto tiene mas de 500mt2
            self.pceram = self.pceram * 0.9
            self.ppegame = self.ppegame * 0.9

        #cantidad
        if self.piso == 1:              # puertas y ventanas piso 1
            self.puertas = P
            self.ventanas = V
        
        if self.mts > 80:               # si los mts2 son mayores a 80
            self.puertas = P + 3
            self.ventanas = V + 3
        
        elif self.mts < 80:             # si los mts2 son mayores a 80
            self.puertas = P + 1
            self.ventanas = V - 2

        #costos
        self.ppuertas = self.puertas * PPU
        self.pventanas = self.ventanas * PV
    
        #cantidad
        if self.mts < 50:           # si los mts2 son menores a 50
            self.cama = 1
            self.mesa = 1
            self.sillas = 4

        else:                       # si los mts2 son menores a 50
            self.cama = 3
            self.mesa = 1
            self.sillas = 6

        #costo
        self.pcama = self.cama * PCA
        self.pmesa = self.mesa * PM
        self.psillas = self.sillas * PS        

        #total materiales
        self.costo_mat = self.pcemento + self.pceram + self.pladrillo + self.ppegame
        self.cant_mat = self.ladrillo + self.ceramico + self.cemento + self.pegamento

        #total aberturas
        self.costo_aber = self.pventanas + self.ppuertas

        #total muebles
        self.costo_mueb = self.pcama + self.pmesa + self.psillas

        #total dpto
        self.costo_dpto = self.costo_mat + self.costo_aber + self.costo_mueb


#validar que no se pueda ingresar el mismo
while True:
    #edificio
    while True:
        try:
            ed = int(input("Ingrese el edificio: "))
        except ValueError:
            print("Se admiten solo valores numéricos, reintente")
        else:
            if ed <= 0:
                print("Solo se admiten valores superiores a 0")
            else:
                break
    
    #piso
    while True:        
        try:
            pi = int(input("Ingrese el piso: "))
        except ValueError:
            print("Se admiten solo valores numéricos, reintente")
        else:
            if pi <= 0:
                print("Solo se admiten valores superiores a 0")
            else:
                break

    #metros2 de depto
    while True:
        try:
            mts = int(input("Ingrese mts: "))
        except ValueError:
            print("Se admiten solo valores numéricos, reintente")
        else:
            if mts <= 0:
                print("Solo se admiten valores superiores a 0")
            else:
                break
    
    #mts2 pared depto
    while True:
        try:
            mtspar = int(input("Ingrese mts pared: "))
        except ValueError:
            print("Se admiten solo valores numéricos, reintente")
        else:
            if mts <= 0:
                print("Solo se admiten valores superiores a 0")
            else:
                deptos.append([pi, mts, mtspar, ed])
                x = input("0 - Salir || ABC - Continuar: ")
                if x == str(0):
                   ban = True
                   break

                else:
                    ban = False
                    break
    
    if ban == True:
        break

#recorro la lista "deptos" para crear los objetos y remplazarlos 
for i in range(len(deptos)):
    #creo el objeto depto
    deptos[i] = depto(deptos[i][0], deptos[i][1], deptos[i][2], deptos[i][3])
    #uso los "metodos" que cree en la clase
    deptos[i].calcular()

    # ----------- piso -----------------

    # lo usamos despues en el for de edificio
    costo_edi = []

    #agrego los valores de los pisos en el diccionario
    costos = [deptos[i].costo_dpto, deptos[i].costo_mat, deptos[i].cant_mat, deptos[i].costo_aber, deptos[i].costo_mueb]    # lista costos con todos los costos del piso
    code = str(deptos[i].edificio) + "." + str(deptos[i].piso)  # clave para identificar en el diccionario

    # si existe el piso le agrega los costos
    if code in pisos:
        c = 0
        aux = []
        for departamentos in pisos[code]:
            aux.append(departamentos + costos[c])
            costo_edi.append(departamentos + costos[c])
            c += 1
        pisos[code] = aux

    # si no existe crea un par clave-valor nuevo
    else:
        pisos[code] = costos


    # -------------- edificio ------

    key = deptos[i].edificio

    if key in edificio:
        c = 0
        aux = []
        for piso in edificio[key]:
            aux.append(piso + costo_edi[c])
            c += 1
        edificio[key] = aux

    # si no existe crea un par clave-valor nuevo
    else:
        edificio[key] = costos

print("Ladrillos: {:.2f} unidades. {:>20}".format(deptos[i].ladrillo, deptos[i].pladrillo))

# print(f"Edificio: {edificio}")
# print(f"Piso: {pisos}")
