import pygame
import ConfigParser
import random
import pygame
from pygame.locals import *
from history import *
#Contantes globales

# Colores
NEGRO    = (   0,   0,   0)
BLANCO   = ( 255, 255, 255)
AZUL     = (   0,   0, 255)
ROJO     = ( 255,   0,   0)
VERDE    = (   0, 255,   0)

# Dimensiones pantalla
ANCHO = 800
ALTO  = 600

#mapa
archivo = "mapa.map"
class enemigo(pygame.sprite.Sprite):
    def __init__(self, img_sprite):
        pygame.sprite.Sprite.__init__(self)
        self.m=img_sprite
        self.image=self.m[0][2]
        self.rect=self.image.get_rect()
        self.dir=2
        self.i=0
        self.var_x=3
        self.var_y=0
        self.flag=0
        #2 derecha, 1 izquierda

    def update(self):
        if self.var_x !=0 or self.var_y !=0:
            if self.i <2:
                self.i+=1
            else:
                self.i=0
        self.image=self.m[self.i][self.dir]
        #self.rect=self.image.get_rect()

    
        if self.flag==1:
            self.rect.x = random.randrange(ANCHO,ANCHO+50)
            self.rect.y = random.randrange(20,ALTO-120)
        self.dir=1
        self.rect.x-=self.var_x
        self.flag=0
        if self.rect.x < -50:
            self.rect.x = random.randrange(-50,-40)
            self.rect.y = random.randrange(20,ALTO-120)
            self.flag=1


#Jugador
class Jugador(pygame.sprite.Sprite):

    var_x = 0
    var_y = 0
    def __init__(self, m):
        pygame.sprite.Sprite.__init__(self)
        ancho = 40
        alto = 60
        self.m=m
        self.dir=0
        self.image=self.m[self.dir][0]
        self.rect=self.image.get_rect()
        self.var_x=0 #que tantos pixeles se mueve en x
        self.var_y=0 #que tantos pixeles se mueve en y
        self.x=-1 #inicializo con este valor para que la imagen no se quede moviendo
        self.pen=0 #para la pendiente de la ecuacion
        self.inter=0 # calcula el intercepto de la ecuacion
        self.p1=0  #posicion 1 del mouse
        self.p2=0  #posicion 2 del mouse

    def update(self):
        self.rect.x+=self.var_x
        if self.rect.x>=self.p1 and self.var_x==5:
            self.var_x=0
            self.x=-1
        elif self.rect.x<=self.p1 and self.var_x==-5:
            self.var_x=0
            self.x=-1
        if self.x!=-1:
            if self.x<4:
                self.image=self.m[self.dir][self.x] #Me permite visualizar el movimiento de cada img (columna) segun la fila.
                self.x+=1
            else:
                self.x=0
        self.rect.y=int(self.pen*self.rect.x+self.inter)

    def Pendiente(self):
        self.pen=(float(self.rect.y-self.p2))/(float(self.rect.x-self.p1))
        print self.pen
        self.inter=float(self.pen*(-self.p1)+self.p2)


#Recortar mapeo
def matimg(imagen,h,v):
    fondo = pygame.image.load(imagen).convert_alpha()
    info = fondo.get_size()
    img_ancho = info[0]
    img_alto = info[1]

    anc = img_ancho/h
    alt = img_alto/v
    m = []
    for i in range(h):
        fila = []
        for j in range(v):
            cuadro = [i*anc,j*alt,anc,alt]
            recorte = fondo.subsurface(cuadro)#segmento de fondo
            fila.append(recorte)

        m.append(fila)

    return m

#Recortar jugador
def Recorte(): # funcion que me retorna una matriz con todos los recortes hechos a una imagen.
    imagen=pygame.image.load('nate.png').convert_alpha()
    ancho_img,alto_img=imagen.get_size()
    sp_fil=4
    sp_col=4
    an_img_recorte=ancho_img/sp_col
    al_img_recorte=alto_img/sp_fil
    matriz = []
    for i in range(sp_fil):
        matriz.append([])
        for j in range(sp_col):
            cuadro=(j*an_img_recorte,i*al_img_recorte,an_img_recorte,al_img_recorte) #posicion del recorte de la imagen
            recorte=imagen.subsurface(cuadro) #me va a tener el recorte de cierta posicion de una imagen
            matriz[i].append(recorte)
    return matriz

def Recortar(archivo, an,al):
    fondo = pygame.image.load(archivo).convert_alpha()

    info=fondo.get_size()
    img_ancho=info[0]
    img_alto=info[1]
    corte_x=img_ancho/an
    corte_y=img_alto/al

    m=[]
    for i in range(an):
        fila=[]
        for j in range(al):
            cuadro=[i*corte_x,j*corte_y,corte_x,corte_y]
            recorte = fondo.subsurface(cuadro)
            fila.append(recorte)
        m.append(fila)

    return m

#-------------------- Menu-----------------------------------------------

class Opcion:

    def __init__(self, fuente, titulo, x, y, paridad, funcion_asignada):
        self.imagen_normal = fuente.render(titulo, 1, (200, 0, 0))
        self.imagen_destacada = fuente.render(titulo, 1, (200, 0, 0))
        self.image = self.imagen_normal
        self.rect = self.image.get_rect()
        self.rect.x = 500 * paridad
        self.rect.y = y
        self.funcion_asignada = funcion_asignada
        self.x = float(self.rect.x)
     

    def actualizar(self):
        destino_x = 52
        self.x += (destino_x - self.x) / 5.0
        self.rect.x = int(self.x)
     

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)

    def destacar(self, estado):
        if estado:
            self.image = self.imagen_destacada
        else:
            self.image = self.imagen_normal

    def activar(self):
        self.funcion_asignada()


class Cursor:

    def __init__(self, x, y, dy):
        self.image = pygame.image.load('cursor.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.y_inicial = y
        self.dy = dy
        self.y = 0
        self.seleccionar(0)

    def actualizar(self):
        self.y += (self.to_y - self.y) / 10.0
        self.rect.y = int(self.y)

    def seleccionar(self, indice):
        self.to_y = self.y_inicial + indice * self.dy

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)


class Menu:
    "Representa un menu con opciones para un juego"
    
    def __init__(self, opciones):
        self.opciones = []
        fuente = pygame.font.Font('dejavu.ttf', 20)
        x = 119
        y = 119
        paridad = 1

        self.cursor = Cursor(x - 30, y, 30)

        for titulo, funcion in opciones:
            self.opciones.append(Opcion(fuente, titulo, x, y, paridad, funcion))
            y += 30
            if paridad == 1:
                paridad = -1
            else:
                paridad = 1

        self.seleccionado = 0
        self.total = len(self.opciones)
        self.mantiene_pulsado = False

    def actualizar(self):
        """Altera el valor de 'self.seleccionado' con los direccionales."""

        k = pygame.key.get_pressed()

        if not self.mantiene_pulsado:
            if k[K_UP]:
                self.seleccionado -= 1
            elif k[K_DOWN]:
                self.seleccionado += 1
            elif k[K_RETURN]:
                # Invoca a la funcion asociada a la opcion.
                self.opciones[self.seleccionado].activar()

        # procura que el cursor este entre las opciones permitidas
        if self.seleccionado < 0:
            self.seleccionado = 0
        elif self.seleccionado > self.total - 1:
            self.seleccionado = self.total - 1
        
        self.cursor.seleccionar(self.seleccionado)

        # indica si el usuario mantiene pulsada alguna tecla.
        self.mantiene_pulsado = k[K_UP] or k[K_DOWN] or k[K_RETURN]

        self.cursor.actualizar()
     
        for o in self.opciones:
            o.actualizar()

    def imprimir(self, screen):
        """Imprime sobre 'screen' el texto de cada opcion del menu."""

        self.cursor.imprimir(screen)

        for opcion in self.opciones:
            opcion.imprimir(screen)
    
    fondom = pygame.image.load("lucifer.png")
    fondo1 = pygame.transform.scale(fondom, (800, 600))  

def fondo(archivo):
    pantalla.blit(archivo, (0,0))

        
       

def comenzar_nuevo_juego():
    Intro() # llamo al metodo intro para que se pueda visualizar la historia
    #antes de entrar a jugar
    
    fondo = matimg('terrenogen.png',32,12)
    #Grupos
    general=pygame.sprite.Group()
    m=Recorte()
    jp=Jugador(m)
    general.add(jp)
    interprete  = ConfigParser.ConfigParser()
    interprete.read(archivo)
    mapa = interprete.get('nivel1','mapa')
    mapa = mapa.split('\n')
    nf = 0
    fila_ejemplo = mapa[1]
    
    
    x,y=[0,0]
    fin=False
    
    while not fin:
        posMouse=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                import sys
                fin = True
                sys.exit()    
            
                
            if event.type==pygame.MOUSEBUTTONDOWN:
                jp.p1,jp.p2=posMouse
                jp.x=0
                if jp.rect.x<jp.p1:  #dependiendo si la pos del mouse esta a la izq o der del sprite, voy a sumar o a restar la pos x.
                    jp.var_x=5
                elif jp.rect.x>jp.p1:
                    jp.var_x=-5
                jp.Pendiente()
        
        

        y = 0
        l = 0
       
        
        for  f  in mapa:

            for e in f:
                interprete.get(e,'x')
                a = interprete.get(e,'x')
                b = interprete.get(e,'y')
                a=int(a)
                b = int(b)
                pantalla.blit(fondo[a+1][b+1],[l,y])
                l += 32
            y += 32
            l= 0
        
       
        
        general.update()
        general.draw(pantalla)
        
        pygame.display.flip()
        reloj.tick(60)
        
    
    

def mostrar_opciones():
    
    salir=False
    screen = pygame.display.set_mode((800,600))
    fondo = pygame.image.load("instruccion.png")
    fondo1 = pygame.transform.scale(fondo, (800, 600))
    while not salir:
        for e in pygame.event.get():
            import sys
            if e.type == QUIT:
                sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    salir = True
            
        screen.blit(fondo1,(0,0))
        pygame.display.flip()
        pygame.time.delay(10)
   
    
    reloj.tick(60)
    
def creditos():
    salir=False
    screen = pygame.display.set_mode((800,600))
    fondo = pygame.image.load("creditos.png")
    fondo1 = pygame.transform.scale(fondo, (800, 600))
    while not salir:
        for e in pygame.event.get():
            import sys
            if e.type == QUIT:
                sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    salir = True
            
        screen.blit(fondo1,(0,0))
        pygame.display.flip()
        pygame.time.delay(10)
   

def salir_del_programa():
    import sys
    print " Gracias por utilizar este programa."
    sys.exit(0)




        

#--------------------principal-------------------------------------

if __name__ == '__main__':
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO,ALTO])
    pygame.display.set_caption("Escaping Hell")
    
    fin=False
    fin1=False
    opciones = [
        ("Jugar", comenzar_nuevo_juego),
        ("Instrucciones", mostrar_opciones),
        ("Creditos", creditos),
        ("Salir", salir_del_programa)
        ]

    
    menu = Menu(opciones)
    reloj=pygame.time.Clock()


    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               
                fin= True
        
        fondom = pygame.image.load("title_box.png")
        fondo1 = pygame.transform.scale(fondom, (800, 600))        
        pantalla.blit(fondo1, (0, 0))

        
        menu.actualizar()
        menu.imprimir(pantalla)
        pygame.display.flip()
        pygame.time.delay(10)


    