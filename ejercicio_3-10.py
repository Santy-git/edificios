
deptos = []
pisos = {}
edificio = {}

#cantidad
l = 20              # ladrillos m2 pared
c = 15               # kg cemento m2 pared
L = 20              # largo cm
A = 30              # ancho cm
sup_cer = L * A * 0.01
F = 10              # f cerámicos
Z = 1               # z kg pegamento
X = 5               # kg cemento m2 piso

V = 3              # ventanas primer piso
P = 1              # puertas primer piso

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

cantidades = {"ladrillo":0, "cemento":0, "ceramico":0,"pegamento":0,
                "puertas":0, "ventanas":0,
                "camas":0, "mesas":0, "sillas":0}

costos = {"ladrillo":0, "cemento":0, "ceramico":0,"pegamento":0,
            "puertas":0, "ventanas":0,
            "camas":0, "mesas":0, "sillas":0}

costos_dpto = {"materiales":0, "aberturas":0, "muebles":0, "depto":0}

ban = False

class depto:
    def __init__(self, piso, mts, mtspar, edificio):
        self.piso = piso
        self.mts = mts
        self.mtspar = mtspar
        self.edificio = edificio

        self.cantidades = cantidades
        self.costos = costos
        self.costos_dpto = costos_dpto
    
    def __str__(self):
        return f"Piso {self.piso}, con {self.mts}mts de piso y {self.mtspar}mts de pared"
    
    def calcular(self):
        #cantidad de materiales
        self.cantidades["ladrillo"] = self.mtspar * L                     # unidades de ladrillo
        self.cantidades["cemento"] = (self.mtspar * c) + (self.mts * 2)   # kg cemento en total
        self.cantidades["ceramico"] = self.mts / sup_cer                  # unidades cerámico
        self.cantidades["pegamento"] = ((self.cantidades["ceramico"] * Z) / F)          # kg pegamento
        
        #costos
        self.costos["ladrillo"] = self.cantidades["ladrillo"] * PL                 # ladrillo
        self.costos["cemento"] = self.cantidades["cemento"] * PC                   # cemento
        self.costos["ceramico"] = self.cantidades["ceramico"] * PCE                   # ceramico
        self.costos["pegamento"] = self.cantidades["pegamento"] * PP                  # pegamento

        if (self.cantidades["ceramico"] * sup_cer) > 500:                 # si el dpto tiene mas de 500mt2
            self.costos["ceramico"] *= 0.9
            self.costos["pegamento"] *= 0.9

        #cantidad
        if self.piso == 1 or self.mts == 80:              # puertas y ventanas piso 1
            self.cantidades["puertas"] = P
            self.cantidades["ventanas"] = V

        else:
            if self.mts > 80:               # si los mts2 son mayores a 80
                self.cantidades["puertas"] = P + 3
                self.cantidades["ventanas"] = V + 3
            
            elif self.mts < 80:             # si los mts2 son menores a 80
                self.cantidades["puertas"] = P + 1
                self.cantidades["ventanas"] = V - 2

        self.cantidades["ventanas"]

        #costos
        self.costos["puertas"] = self.cantidades["puertas"] * PPU
        self.costos["ventanas"] = self.cantidades["ventanas"] * PV
    
        #cantidad
        if self.mts < 50:           # si los mts2 son menores a 50
            self.cantidades["camas"] = 1
            self.cantidades["mesas"] = 1
            self.cantidades["sillas"] = 4

        else:                       # si los mts2 son menores a 50
            self.cantidades["camas"] = 3
            self.cantidades["mesas"] = 1
            self.cantidades["sillas"] = 6

        #costo
        self.costos["camas"] = self.cantidades["camas"] * PCA
        self.costos["mesas"] = self.cantidades["mesas"] * PM
        self.costos["sillas"] = self.cantidades["sillas"] * PS        

        #total materiales
        self.costos_dpto["materiales"] = self.costos["cemento"] + self.costos["ceramico"] + self.costos["ladrillo"] + self.costos["pegamento"]

        #total aberturas
        self.costos_dpto["aberturas"] = self.costos["ventanas"] + self.costos["puertas"]

        #total muebles
        self.costos_dpto["muebles"] = self.costos["camas"] + self.costos["mesas"] + self.costos["sillas"]

        #total dpto
        self.costos_dpto["depto"] = self.costos_dpto["materiales"] + self.costos_dpto["aberturas"] + self.costos_dpto["muebles"]

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
    costo_edi = deptos[i].costos_dpto

    code = str(deptos[i].edificio) + "." + str(deptos[i].piso)  # clave para identificar en el diccionario

    # si no existe crea un par clave-valor nuevo
    pisos[code] = deptos[i].costos_dpto

    # -------------- edificio ------

    x = ["materiales", "aberturas", "muebles", "depto"]

    key = deptos[i].edificio
    if key in edificio:
        aux = []
        i = 0
        for piso in edificio[key]:
            aux.append(piso + costo_edi[[x][i]])
            i += 1
        edificio[key] = aux

    # si no existe crea un par clave-valor nuevo
    else:
        edificio[key] = costos

    print(deptos[i].cantidades)
    print(deptos[i].costos)
    print(deptos[i].costos_dpto)