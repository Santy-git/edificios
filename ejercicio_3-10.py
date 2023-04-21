import curses
import time
import signal

def main(screen):
    curses.curs_set(0) # oculta el cursor
    height, width = screen.getmaxyx() # obtiene el tamaño de la ventana
    x, y = 0, height // 2 # posición inicial del texto
    dx = 1 # dirección del movimiento del texto (1 = derecha, -1 = izquierda)

    def handle_signal(signal, frame):
        curses.endwin() # detiene la aplicación curses
        exit(0) # sale del programa

    
    signal.signal(signal.SIGINT, handle_signal) # maneja la señal SIGINT

    while True:
        screen.clear() # limpia la pantalla
        screen.addstr(height-1, 0, "Presione Ctrl + C para salir")
        screen.addstr(y, x, "Gracias por usar mi programa!") # agrega el texto a la pantalla
        screen.refresh() # actualiza la pantalla
        x += dx # mueve el texto en la dirección actual
        if x <= 0: # si llega al borde izquierdo, cambia la dirección del movimiento a la derecha
            dx = 1
        elif x + len("Gracias por usar mi programa!") >= width: # si llega al borde derecho, cambia la dirección del movimiento a la izquierda
            dx = -1
        time.sleep(0.1) # espera un momento
        
deptos = []
pisos = {}
edificio = {}

#cantidad
l = 20              # ladrillos m2 pared
c = 15               # kg cemento m2 pared
L = 20              # largo cm
A = 30              # ancho cm
sup_cer = (L * A) * 0.01
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

class departamento:
    def __init__(self, edificio, piso, nro,  mts, mtspar):
        self.piso = piso
        self.mts = mts
        self.nro = nro
        self.mtspar = mtspar
        self.edificio = edificio

        self.cantidades = {"ladrillo":0, "cemento":0, "ceramico":0,"pegamento":0,
                            "puertas":0, "ventanas":0,
                            "camas":0, "mesas":0, "sillas":0}
        
        self.costos = {"ladrillo":0.0, "cemento":0.0, "ceramico":0.0,"pegamento":0.0,
                        "puertas":0.0, "ventanas":0.0,
                        "camas":0.0, "mesas":0.0, "sillas":0.0}
        
        self.costos_dpto = {"materiales":0.0, "aberturas":0.0, "muebles":0.0, "depto":0.0}
    
    def __str__(self):
        return f"Edificio: {self.edificio}, Piso: {self.piso}, Departamento: {self.nro} [{self.mts}mts de piso y {self.mtspar}mts de pared]"
    
    def calcular(self):
        #cantidad de materiales
        self.cantidades["ladrillo"] = self.mtspar * L                     # unidades de ladrillo
        self.cantidades["cemento"] = (self.mtspar * c) + (self.mts * 2)   # kg cemento en total
        self.cantidades["ceramico"] = self.mts / sup_cer                  # unidades cerámico
        self.cantidades["pegamento"] = ((self.cantidades["ceramico"] * Z) / F)          # kg pegamento
        
        #costos

        self.costos["ladrillo"] = float("{:.2f}".format(self.cantidades["ladrillo"] * PL))                # ladrillo
        self.costos["cemento"] = float("{:.2f}".format(self.cantidades["cemento"] * PC))                  # cemento
        self.costos["ceramico"] = float("{:.2f}".format(self.cantidades["ceramico"] * PCE))               # ceramico
        self.costos["pegamento"] = float("{:.2f}".format(self.cantidades["pegamento"] * PP))              # pegamento

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
        self.costos["puertas"] = float("{:.2f}".format(self.cantidades["puertas"] * PPU)) 
        self.costos["ventanas"] = float("{:.2f}".format(self.cantidades["ventanas"] * PV)) 
    
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
        
        self.costos["camas"] = float("{:.2f}".format(self.cantidades["camas"] * PCA))
        self.costos["mesas"] = float("{:.2f}".format(self.cantidades["mesas"] * PM)) 
        self.costos["sillas"] = float("{:.2f}".format(self.cantidades["sillas"] * PS))    

        #total materiales
        self.costos_dpto["materiales"] = float("{:.2f}".format(self.costos["cemento"] + self.costos["ceramico"] + self.costos["ladrillo"] + self.costos["pegamento"]))

        #total aberturas
        self.costos_dpto["aberturas"] = float("{:.2f}".format(self.costos["ventanas"] + self.costos["puertas"]))

        #total muebles
        self.costos_dpto["muebles"] = float("{:.2f}".format(self.costos["camas"] + self.costos["mesas"] + self.costos["sillas"]))

        #total dpto
        self.costos_dpto["depto"] = float("{:.2f}".format(self.costos_dpto["materiales"] + self.costos_dpto["aberturas"] + self.costos_dpto["muebles"]))

print("_"*100)
print("{:.^20}".format("Bienvendio al gestor de costos"))
while True:
    print("\n")
    print("Ingrese la opción que desea realizar: ")
    print("_"*100)
    print("[1] - Ingresar departamento")
    print("[2] - Mostrar departamentos")
    print("[3] - Mostrar pisos")
    print("[4] - Mostrar edificios")
    print("_"*100)
    print("[0] - Salir del programa")

    while True:
        print("_"*100)
        opcion = input("Ingrese la opción: ")
        print("_"*100)
        try:
            int(opcion)
        except ValueError:
            print("Solo se aceptan valores numéricos, reintente")
        else:
            opcion = int(opcion)
            if 4 >= opcion >= 0:
                break
            else:
                print(f"{opcion} no es una opción válida, reintente")

    # salir
    if opcion == 0:
        if __name__ == "__main__":
            curses.wrapper(main)
        

    # ingresar depto
    if opcion == 1:
        print("_"*100)
        ban = True
        while ban:
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
            
            #nro
            while True:
                try:
                    nro = int(input("Ingrese el departamento: "))
                except ValueError:
                    print("Se admiten solo valores numéricos, reintente")
                else:
                    if nro <= 0:
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
                        xd = False


                        for i in range(len(deptos)):
                            if ed == deptos[i].edificio and pi == deptos[i].piso and nro == deptos[i].nro:
                                print("El departamento ya ha sido ingresado, reintente")
                                xd = True
                                break

                        if not xd:
                            # ------- HAGO LOS CALCULOS ----------
                            # ----------- depto -----------------
                            # agrego a la lista de deptos el depto ingresado
                            depto = departamento(ed, pi, nro, mts, mtspar)
                            depto.calcular()
                            deptos.append(depto)

                            # calculo todo

                            # ----------- piso -----------------
                            x = ["materiales", "aberturas", "muebles", "depto"]
                            code = str(depto.edificio) + "." + str(depto.piso)  # clave para identificar en el diccionario

                            if code in pisos:
                                aux = {}
                                i = 0
                                for j in pisos[code]:
                                    num = pisos[code][j] + depto.costos_dpto[x[i]]
                                    aux[x[i]] = num
                                    i += 1
                                pisos[code] = aux
                            # si no existe crea un par clave-valor nuevo
                            else:
                                pisos[code] = depto.costos_dpto

                            # -------------- edificio ---------
                            costo_edi = depto.costos_dpto
                            

                            key = depto.edificio
                            if key in edificio:
                                aux = {}
                                i = 0
                                for piso in edificio[key]:
                                    num = edificio[key][piso] + costo_edi[x[i]]
                                    aux[x[i]] = num
                                    i += 1
                                edificio[key] = aux
                            # si no existe crea un par clave-valor nuevo
                            else:
                                edificio[key] = costo_edi

                            x = input("0 - Salir || 1 - Continuar: ")

                            if x == '0':
                                ban = False
                                break

                            else:
                                ban = True
                                break
                        
                        else:
                            break
    
    # mostrar depto
    if opcion == 2:
        if len(deptos) > 0:
            for i in range(len(deptos)):
                dto = deptos[i]
                # materiales, aberturas, muebles, todo
                print("_"*100)
                print(dto)
                print("_"*50)
                print("Materiales: {:>25,.2f} \nAberturas: {:>25,.2f} \nMuebles: {:>27,.2f} \n{} \nTotal: {:>30,.2f}".format(dto.costos_dpto["materiales"], dto.costos_dpto["aberturas"], dto.costos_dpto["muebles"], "-"*50, dto.costos_dpto["depto"]))
        else:
            print("Ingrese un departamento primero")
    # mostar piso
    if opcion == 3:
        if len(pisos) > 0:
            for clave, valor in pisos.items():
                print("_"*100)
                print(f"Edificio-Piso: {clave}")
                print("_"*50)
                print("Materiales: {:>25,.2f} \nAberturas: {:>25,.2f} \nMuebles: {:>27,.2f} \n{} \nTotal: {:>30,.2f}".format(valor["materiales"], valor["aberturas"], valor["muebles"], "-"*50, valor["depto"]))
        
        else:
            print("Ingrese un departamento primero")

    # mostrar edificio
    if opcion == 4:
        if len(edificio) > 0:
            for clave, valor in edificio.items():
                print("_"*100)
                print(f"Edificio: {clave}")
                print("_"*50)
                print("Materiales: {:>25,.2f} \nAberturas: {:>25,.2f} \nMuebles: {:>27,.2f} \n{} \nTotal: {:>30,.2f}".format(valor["materiales"], valor["aberturas"], valor["muebles"], "-"*50, valor["depto"]))
        else:
            print("Ingrese un departamento primero")