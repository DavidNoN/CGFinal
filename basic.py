import pygame
import ConfigParser
#tragame tierra, y arrojame en una isla
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



if __name__ == '__main__':
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO,ALTO])
    pygame.display.set_caption("Juego basico")
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


    reloj=pygame.time.Clock()



    while not fin:
        posMouse=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True

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
