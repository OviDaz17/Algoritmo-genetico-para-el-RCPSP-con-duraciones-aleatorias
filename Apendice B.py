import random
import copy
from numpy.random import choice
from future.utils import iteritems
from scipy import stats
from timeit import default_timer
from os import system
#########################################################################
compensacion_inicial = 18 #inicio de desplazamiento (compesación inicial)
compensacion_final = 32 + 4 #compensación de orden (compesación final)
compesacion_recurso = 89 #Recurso de compensación (Compensacion de recurso)
n_tareas = 32 #numero de tareas 
tareas = [] #lista de tareas
disponibilidad_de_recursos	= {} #Disponibilidad de recursos
uso_de_recursos = {'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0} #uso de recursos
#Borrar la línea y enumerarla
def clearLine(e): 

	te = len(e) #captura el tamaño de la línea
	i = 0
	v = []
	flag = 0 #bandera
	word = '' #Palabra
#Capturando los valores que son de interés para la ejecución del algoritmo.
	while i < te:
		if e[i] == ' ':
			if flag == 1:
				#Insertando los valores en el vector
				v.append(int(word))
				word = ''
				flag = 0
				i = i + 1
			else:		
				i = i + 1
		else:
			#concatenando la palabra
			word = word + e[i]
			flag = 1
			i = i + 1
	#Agregando el último valor de línea en el vector	
	if word:		
		v.append(int(word))

	return v

def es_predecesor(t, pt):
	
	try:
		i = pt['Sucessors'].index(t['NR'])
	except ValueError:	
		return -1
	else:
		return 1

def generando_predecesores():#generar predecesores

	pred = []
	i = 0
	while i < n_tareas:
		for t2 in tareas:
			if es_predecesor(tareas[i], t2) == 1:
				pred.append(t2['NR'])
		tareas[i]['Predecessors'] = pred
		pred = []		
		i = i + 1
#Cargando el archivo para alimentar el algoritmo
def load (nombre_archivo):
	
	
	archivo = open(nombre_archivo, 'r') #nombre del archivo
	text = archivo.read(); #leyendo todo el archivo e ingresandolo a memoria
	lineas = text.split('\n') #Separando las lineas por \n
	nt = 0

	while nt < n_tareas:
		#Seleccionando parte de los datos del archivo que son de interés para el algoritmo
		e1 = lineas[compensacion_inicial + nt]
		e2 = lineas[compensacion_inicial + compensacion_final  + nt]

		#Limpiando líneas y guardanndo datos en el vector
		l1 = clearLine(e1)
		l2 = clearLine(e2)

		h1 = len(l1)
		h2 = len(l2)
			   #[Tarea NR, Sucesores, Recursos, Tiempo de duracion de la tarea]
		tareas.append({'NR':l1[0], 'Predecessors':[], 'Sucessors':l1[3:h1],'R1': l2[3], 'R2': l2[4], 'R3': l2[5], 'R4':l2[6], 'TimeDuration':l2[2]}) 

		#print task

		nt = nt + 1

	#Capturando la cantidad de recurso	
	e3 = lineas[compesacion_recurso]
	l3 = clearLine(e3)
	disponibilidad_de_recursos['R1'] = l3[0]
	disponibilidad_de_recursos['R2'] = l3[1]
	disponibilidad_de_recursos['R3'] = l3[2]
	disponibilidad_de_recursos['R4'] = l3[3]
	
	generando_predecesores()
#############################################################################################################################################################
def riesgos():
    binario = [0,1]
    print("desea someter a dos tipos de riesgo a 10 actividades?")
    respuesta = str(input())
    print("responda si o no")
    if respuesta == "si":
        actividades_al_riesgo=[]
        actividades_con_mas_duracion=[]
        print("escriba 1 para ingresar el numero de las actividades (de 1 a 31)","\nescriba 2 para crearlas pseudo-aleatoriamente","\nescriba 3 para utilizar las guardadas en memoria")
        respuesta2=int(input())
        if respuesta2==1:
            print("ingrese uno a uno el numero de la actividad a la que le desea aplicar el riesgo")
            for i in range (10):
                print("actidad",i)
                actividades_al_riesgo.append(int(input())-1)
                system("pause")
            print(f"las actividades elegidas son: {actividades_al_riesgo}")
        if respuesta2==2:
            actividades_al_riesgo= random.sample(range(1,31),10)
            print(f"las actividades elegidas son: {actividades_al_riesgo} ")
        if respuesta2==3:
            actividades_al_riesgo= [2,3,4,7,8,15,16,21,28,17]
            print(f"las actividades elegidas son: {actividades_al_riesgo} ")
        aplicacion_del_riesgo1 = [1,1,0,1,1,0,1,0,1,0]
        aplicacion_del_riesgo2 = [0,1,1,0,1,1,1,1,1,1]
        n=0
        for i in actividades_al_riesgo:
            tareas[i]["TimeDuration"] += int(aplicacion_del_riesgo1[n]*tareas[i]["TimeDuration"]*0.5) +  int(aplicacion_del_riesgo2[n]*tareas[i]["TimeDuration"]*0.5)
            if  aplicacion_del_riesgo1[n] == 1:
                print(f"ocurrió el riesgo 1 para la actividad: {i}")
                actividades_con_mas_duracion.append(i)
            if  aplicacion_del_riesgo2[n] == 1:
                print(f"ocurrió el riesgo 2 para la actividad: {i}")
            n+=1
    else:
        if respuesta != "si":
            print("sin riesgo")
            system("pause")
########################################################################################################################################################################
def rutaCritica(T):
    z=[]
    def Actividades1():
        for i in range(len(T)):
            z.append(T[i]["NR"])
    Actividades1()
    y=[]
    def Predecesores():
        for i in range(len(T)):
            y.append(T[i]["Predecessors"])
    Predecesores()
    x=[]
    def duracion():
        for i in range(len(T)):
            x.append(T[i]["TimeDuration"])
    duracion()
    t=[]
    def Sucesores():
        for i in range(len(T)):
            t.append(T[i]["Sucessors"])
    Sucesores()
    class Actividades:
        def __init__(self,nombre,duracion,precedencia, inicio_cercano, inicio_lejano, termino_cercano, termino_lejano,sucesores):
            self.nombre = nombre
            self.duracion = duracion
            self.precedencia = precedencia
            self. holgura = 0
            self.inicio_cercano = inicio_cercano
            self.inicio_lejano = inicio_lejano
            self.termino_cercano =  termino_cercano
            self.termino_lejano = termino_lejano
            self.sucesores = sucesores
    Z=[]
    for i in range(len(z)):#se llena la lista Z de objetos de la clase actividad (se llenan los parametros de entrada)
        actividadesCNDPP = Actividades(i+1,x[i],y[i],0,0,0,0,t[i])
        Z.append(actividadesCNDPP)
    p1=[]
    p2=[]
    q1=[]
    q2=[]
    for j in range(len(z)):      
        if j > 0: 
            p1 = Z[j].precedencia
            if len(p1)<=1: 
                for k in p1:
                    p2.append(Z[k-1].termino_cercano)
                for xp in p1:   
                    Z[j].inicio_cercano=Z[xp-1].termino_cercano
                    Z[j].termino_cercano=Z[j].inicio_cercano + Z[j].duracion
                for bp in p2[:]:
                    p2.remove(bp)
            else:
                for k in p1:
                    p2.append(Z[k-1].termino_cercano)
                mayor=p2[0]
                posicion = 0
                for ficti in range(len(p2)):
                    if p2[ficti]>=mayor:
                        mayor=p2[ficti]
                        posicion=ficti
                W=p1[posicion]
                Z[j].inicio_cercano=Z[W-1].termino_cercano 
                Z[j].termino_cercano=Z[j].inicio_cercano + Z[j].duracion
            for bp in p2[:]:
                p2.remove(bp)
            posicion=0
            if len(z)==Z[j].nombre:
                Z[len(Z)-1].termino_lejano=Z[len(Z)-1].termino_cercano
                Z[len(Z)-1].inicio_lejano=Z[len(Z)-1].termino_cercano
    for J in range(len(Z)-1,0,-1):
        if len(Z[J].sucesores)<=1: # se pregunta cuantos sucesores tiene la actividad
            if Z[J].precedencia != [1]:
                q1 = Z[J].precedencia #si es un solo sucesor entonces se toma las precedencias para calcularles sus indices ls lf 
                for k in q1:
                    q2.append(Z[k-1].inicio_lejano)
                if Z[J].inicio_lejano!=0:
                    for xp in q1:    
                        Z[xp-1].termino_lejano=Z[J].inicio_lejano
                        Z[xp-1].inicio_lejano=Z[xp-1].termino_lejano - Z[xp-1].duracion
                    for bp in q2[:]:# se limpia la lista P 
                        q2.remove(bp)
                else:
                    Z[J].termino_lejano=Z[Z[J].sucesores[0]-1].inicio_lejano
                    Z[J].inicio_lejano=Z[Z[J].sucesores[0]-1].inicio_lejano-Z[J].duracion
                    for xp in q1:    
                        Z[xp-1].termino_lejano=Z[J].inicio_lejano
                        Z[xp-1].inicio_lejano=Z[xp-1].termino_lejano - Z[xp-1].duracion
                    for bp in q2[:]:# se limpia la lista P 
                        q2.remove(bp)
                    posicion=0
        else:
            q1 = Z[J].sucesores 
            for T in q1:
                q2.append(Z[T-1].inicio_lejano)        
            menor=q2[0]
            posicion = 0
            for ficti in range(len(q2)):
                if q2[ficti]<=menor:
                    menor=q2[ficti]
                    posicion=ficti
            W=q1[posicion]
            Z[J].termino_lejano=Z[W-1].inicio_lejano
            Z[J].inicio_lejano=Z[J].termino_lejano - Z[J].duracion
            for bp in q2[:]:
                q2.remove(bp)
            posicion=0
        if len(Z[J].sucesores)==1 and len(Z[J].precedencia)==1:
            q1 = Z[J].sucesores #si es un solo sucesor entonces se toma las precedencias para calcularles sus indices ls lf 
            for k in q1:
                w=Z[k-1].inicio_lejano
            for xp in q1:    
                Z[J].termino_lejano=w
                Z[J].inicio_lejano=Z[J].termino_lejano - Z[J].duracion
            for bp in q2[:]:# se limpia la lista P 
                q2.remove(bp)
            posicion=0
    return Z
############################################################################
L=[]
G=[]
for o1 in range(len(rutaCritica(tareas))):
    rutaCritica(tareas)[o1].holgura = rutaCritica(tareas)[o1].termino_lejano - rutaCritica(tareas)[o1].termino_cercano
    if rutaCritica(tareas)[o1].holgura==0:
        L.append(rutaCritica(tareas)[o1].nombre)
    else:
        G.append(rutaCritica(tareas)[o1].nombre)
def primer_individuo1():
    o =[]
    oo=[]
    for i1 in L:
        k1=rutaCritica(tareas)[i1-1].precedencia
        for xx in k1:
            o.append(xx)
            o = list(dict.fromkeys(o))
        o.append(i1)
    wqw=o
    while len(wqw)<len(G)+len(L):
        for ixi in wqw:
            g1g=rutaCritica(tareas)[ixi-1].precedencia
            for iix in g1g:
                oo.append(iix)
                oo = list(dict.fromkeys(oo))
            oo.append(ixi)
        wqw=oo
        oo=[]
    perreco = {"Cromosoma": wqw,"Mks":rutaCritica(tareas)[31].termino_lejano}
    Ascl=[]
    for i in wqw:
        Ascl.append(rutaCritica(tareas)[i-1].termino_lejano)
    Ncapturado=[perreco,Ascl]       
    return Ncapturado
###############################################################################################################################################################################################
#se procede aplicarle distribucion de probabilidad a la duracion media

def cambio_duracion():
        for i in range(len(tareas)):
            if i != 0 and i != 31:
                tareas[i]["TimeDuration"] = int(round(stats.beta.rvs(2,5,(tareas[i]["TimeDuration"])*11/20,23/8*(tareas[i]["TimeDuration"]))))

def obtener_actividad(num):
    for ativ in tareas:  #actividad en tareas
        if ativ['NR'] == num:
            return ativ

def verificando_que_los_predecesores_ya_estan_programados(predecessors, s):  #verificar los predecesores ya programados
    for p in predecessors:
        try:
            i = s.index(
                p
            )  #Intenta recuperar la posición de la actividad anterior ya programada
        except ValueError:
            return -1
        else:
            pass  #la sentencia requiere ser llenada pero el programa no requiere ninguna acción

    return 1

def ordenando_actividades(Dg, asc):

    popElitist = sorted(Dg, key=lambda k: k['TimeDuration'])

    if asc:
        return popElitist
    else:
        popElitist.reverse()
        return popElitist

#Recuperando el último predecesor en terminar
def obteniendo_el_predecesor_mas_temprano(j, et):  #obtener el predecesor final más temprano_se utiliza en SGS serial
    pft = {'NR': 0, 'TimeEnd': 0}
    for p in j['Predecessors']:
        for a in et:
            if p == a['NR']:
                if a['TimeEnd'] > pft['TimeEnd']:
                    pft = a
    return pft['TimeEnd']

#Crea la lista de predecesores.
def seleccionando_actividades_elegibles(s, d, t):  # se utiliza en el SGS
    longitud = len(t)
    contador = 0
    listpop = []
    #iterando sobre un cojunto de actidades para ser procesadas
    while contador < longitud:  #for a in t:
        cp = 0
        #iterando sobre el conjunto de predecesores de las actividades
        for p in t[contador]['Predecessors']:
            try:
                i = s.index(p)  #Intentos de recuperar la posición de la actividad predecesora ya programada
            except ValueError:
                break
            else:
                cp = cp + 1
        #Verificando si la actividad ya no es elegible. Si es así, agregue al conjunto d
        if cp == len(t[contador]['Predecessors']):
            d.append(t[contador])  #Insertar en la lista de elegibles
            listpop.append(t[contador])  #Guardando la referencia del objeto para eliminarla más tarde
        contador = contador + 1
    #Eliminar actividades de la lista de actividades a procesar
    for pop in listpop:
        t.remove(pop)

def Fruleta(lista):
    valoresPJN = []
    for i3 in lista:
        valoresPJN.append(i3/sum(lista))
    ruleta1=[]
    for i4 in range(len(valoresPJN)):
        if i4==0:
            ruleta1.append(range(round(valoresPJN[i4]*100)+1))
        else:
            ruleta1.append(range(round(sum(valoresPJN[:i4])*100+1),round(sum(valoresPJN[:i4+1])*100+1)))    
    ruletagrande=[]
    for I1 in range(len(ruleta1)):
        for I2 in ruleta1[I1]:
            ruletagrande.append(I2)     
    el_elegido=random.choice(ruletagrande)
    sisas=0
    for i5 in range(len(valoresPJN)):
        if i5==0:    
            if el_elegido <= round((valoresPJN[i5]*100)):
                sisas=i5
        else:
            if el_elegido > round(valoresPJN[i5]*100) and el_elegido <= round(sum(valoresPJN[:i5+1]*100)):
                sisas=i5
                break
    return sisas

def obteniendo_actividades_elegibles_al_azar(d):  #SGS
    if not d:
        return -1
    else:
        pseudoaleatorio = random.random()
        if pseudoaleatorio > 0.5:
            def GPRW(X1):
                Elegibles = []
                if sum(Elegibles) != len(tareas) and len(Elegibles) == 1:
                    for I1 in range(len(X1)):  #importado era d
                        Elegibles.append(X1[I1]["NR"])
                    sucesores1 = []
                    for i2 in Elegibles:
                        sucesores1.append(rutaCritica(tareas)[i2 - 1].sucesores)
                    duraciones = []
                    for I3 in range(len(sucesores1)):
                        duracionesi = []
                        for I4 in sucesores1[I3]:
                            duracionesi.append(
                                rutaCritica(tareas)[I4 - 1].duracion)
                            if len(sucesores1[I3]) == len(duracionesi):
                                duraciones.append(sum(duracionesi))
                    qk=0
                    for i6 in range(len(X1)):
                        if X1[i6]["NR"]==Elegibles[Fruleta(duraciones)]:
                            qk=i6
                else:
                    qk=0
                return X1[qk]
            ra = GPRW(d)
            d.remove(ra)
        if pseudoaleatorio < 0.5:
            def LFT(X):
                Elegibles = []
                for i1 in range(len(X)):  #importado era d
                    Elegibles.append(X[i1]["NR"])
                TerminosLejanos = []
                for i2 in Elegibles:
                    TerminosLejanos.append(
                        rutaCritica(tareas)[i2 - 1].termino_lejano)
                qk = 0
                for i6 in range(len(X)):
                    if X[i6]["NR"] == Elegibles[Fruleta(TerminosLejanos)]:
                        qk = i6
                return X[qk]
            ra = LFT(d)
            d.remove(ra)
    return ra
def obteniendo_la_actividad_elegible_mas_corta(d):
    ordenando_actividades_elegibles = ordenando_actividades(d, 1)
    activ = ordenando_actividades_elegibles.pop()
    for a in d:
        if activ['NR'] == a['NR']:
            try:
                i = d.index(a)  #Intentos de recuperar la posición de la actividad predecesora ya programada
            except ValueError:
                break
            else:
                pass
            act = d.pop(i)
            return act
    return -1

#Actualización de la cantidad de recursos en tiempo inst
def actualizando_el_uso_de_los_recursos_en_el_tiempo(demanda,tiempo_de_uso_de_recursos,inst):  #SGS
    for resource, amount in iteritems(tiempo_de_uso_de_recursos[inst]):
        if resource in demanda:
            tiempo_de_uso_de_recursos[inst][resource] = tiempo_de_uso_de_recursos[inst][
                    resource] + demanda[resource]

#Comprobación de la cantidad de recursos disponibles en el momento de la instalación
def verificar_la_disponibilidad_de_recursos(demanda, tiempo_de_uso_de_recursos,inst):
    for resource, amount in iteritems(tiempo_de_uso_de_recursos[inst]):  #SGS
        if resource in demanda:
            if tiempo_de_uso_de_recursos[inst][resource] + demanda[
                    resource] > disponibilidad_de_recursos[resource]:
                return -1
    return 1

#Agregando recursos en uso en el momento T
def asignación_de_actividad_en_la_línea_de_tiempo(j, tiempo_de_uso_de_recurso,inst): #SGS
    esta_programado = False
    tiempo_de_inicio = inst
    reservar_recurso_a_tiempo = []
    contando_tiempo = 0
    tiempo_de_finalizacion = 0
    limite = 0
    #print 'Time inst: ', inst, 'NR: ', j['NR'], 'TimeDuration: ', j['TimeDuration']
    #Buscando el instante en el que se puede programar la actividad
    while esta_programado == False:
        limite = tiempo_de_inicio + j['TimeDuration']
        contando_tiempo = tiempo_de_inicio
        #Comprobando si es posible destinar todos los recursos necesarios para el tiempo de ejecución de la actividad
        for t in range(int(tiempo_de_inicio), int(limite)):
            #Si no existe en el tiempo de uso del recurso, significa que a partir de ahora no hay más recursos asignados.
            if t not in tiempo_de_uso_de_recurso:
                #print 't: ', t
                tiempo_de_uso_de_recurso[t] = {'R1': 0,'R2': 0,'R3': 0,'R4': 0}
                actualizando_el_uso_de_los_recursos_en_el_tiempo(j, tiempo_de_uso_de_recurso, t)
                contando_tiempo = contando_tiempo + 1
            #Verifique la disponibilidad de recursos para ese momento en particular,
            #si está disponible, insértelo en la lista de asignación
            elif verificar_la_disponibilidad_de_recursos(
                    j, tiempo_de_uso_de_recurso, t) == 1:
                #print 't in verify: ', t
                reservar_recurso_a_tiempo.append(t)
                contando_tiempo = contando_tiempo + 1
            else:
                break
        #print 'countTime: ', countTime, 'TimeEnd: ', timeStart + j['TimeDuration']
        #Actualizar el uso de recursos a lo largo del tiempo
        if contando_tiempo == limite:
            for t in reservar_recurso_a_tiempo:
                actualizando_el_uso_de_los_recursos_en_el_tiempo(
                    j, tiempo_de_uso_de_recurso, t)
            esta_programado = True
            tiempo_de_finalizacion = tiempo_de_inicio + j['TimeDuration']
        else:
            contando_tiempo = 0
            tiempo_de_inicio = tiempo_de_inicio + 1

    return tiempo_de_finalizacion
#Serial Schedule Generation Scheme
def SGS():
    q=[]
    for i in range(len(tareas)):
        if i != 0 and i != 31:
            q.append(tareas[i]["TimeDuration"])
    cambio_duracion()
    tp = []  #conjunto de tareas a procesar
    Dg = []  #Conjunto de actividades a elegir
    Sg = []  #Conjunto de actividades elegido
    F = []  #Hora de finalización de las actividades
    g = len(tareas)  #Número de actividades del proyecto
    et = []  #Tiempo de término
    #etc = []
    tiempo_de_uso_de_recursos = {}  #Cronología del uso de recursos
    individual = {}  #Individuo generado en ejecución
    tp = copy.deepcopy(tareas)

    #Procesando la primera actividad
    tarea = tp.pop(0)
    et.append({'NR': tarea['NR'], 'TimeEnd': 0})
    Sg.append(tarea['NR'])
    F.append(1)
    tiempo_de_uso_de_recursos[0] = {'R1': 0,'R2': 0,'R3': 0,'R4': 0}  #Inserindo uso dos recursos no instante 0
    i = 1
    while i < g:

        #función de selección de actividades elegibles
        seleccionando_actividades_elegibles(Sg, Dg, tp)
        #Seleccionar una actividad al azar
        j = obteniendo_actividades_elegibles_al_azar(Dg)
        #Crea la función de consumo de recursos
        #Determinar la hora de finalización anticipada de la actividad j, ignorando la disponibilidad de recursos
        #etc.append({'NR': j['NR'], 'TimeMaxPredecessor': getEarliestEndingPredecessor(j, et)})
        ese = obteniendo_el_predecesor_mas_temprano(j, et)
        #Agregar la hora de finalización de la actividad en ejecución j y actualizar los recursos.
        minJ = asignación_de_actividad_en_la_línea_de_tiempo(j, tiempo_de_uso_de_recursos, ese)
        et.append({'NR': j['NR'], 'TimeEnd': minJ})
        #Calcular el tiempo del conjunto  final
        F.append(et[-1])
        #Insertar en la lista de actividades ya programadas
        Sg.append(j['NR'])
        i = i + 1
    individual['Cromosoma'] = Sg
    individual['Mks'] = F[-1]['TimeEnd']
    truco = [individual, F]
    def normaliza_la_duracion():
        n=0
        for i in range(len(tareas)):
            if i != 0 and i != 31:
                tareas[i]["TimeDuration"] = q[n]
                n=n+1
        return
    normaliza_la_duracion()
    return truco
#######################################################################################################################################################
def SGS_P(ingreso):
    import numpy as np
    import copy
    if ingreso !=[]:
        Ascl=[0]
        for iwi in range(1,31+1):
            Ascl.append(ingreso[1][iwi]['TimeEnd'])
    #actividad inicial y final son ficticias: act 1 y act n+2 .  i inicia en 2 (actividad 2 que realmente es la 1, 3 que es la 2 y asi sucesivamente hasta que y termina en: numero actividades reales + 2 osea 9, por eso i=8 es realmente actividad 7 y i=9 es la ficticia final)
    Capturado =  copy.deepcopy(SGS())
    ka = list(range(1,32+1))
    i = ka[1:32]
    #k inicia en 1 (actividad 1 que es la actividad inicial ficticia, sigue en 2 que es la 1, 3 que es la 2 y asi sucesivamente hasta que y termina en: numero actividades reales + 1 osea 8, por eso k=8 es realmente actividad 7)
    #recursos 
    #recurso renovables -> r 7
    R = [1,2,3,4]
    #b maxima cantidad de recurso disponible por periodo de tiempo en orden
    B=[disponibilidad_de_recursos["R1"],disponibilidad_de_recursos["R2"],disponibilidad_de_recursos["R3"],disponibilidad_de_recursos["R4"]]
    #relacion de precedencia cuando actividad k precede a actividad i
    #tabla de precedencias
    def p(k,i):
        precedencia = 0
        for I1 in tareas[i-1]["Predecessors"]:
            if I1==k:
                precedencia = 1
            if precedencia==1:
                break
        return  precedencia
    #table u(k,r)  recurso renovable r que requiere la actividad k por periodo de tiempo 
    u=np.array([[tareas[0]["R1"],tareas[0]["R2"],tareas[0]["R3"],tareas[0]["R4"]],[tareas[1]["R1"],tareas[1]["R2"],tareas[1]["R3"],tareas[1]["R4"]],[tareas[2]["R1"],tareas[2]["R2"],tareas[2]["R3"],tareas[2]["R4"]],[tareas[3]["R1"],tareas[3]["R2"],tareas[3]["R3"],tareas[3]["R4"]],[tareas[4]["R1"],tareas[4]["R2"],tareas[4]["R3"],tareas[4]["R4"]],[tareas[5]["R1"],tareas[5]["R2"],tareas[5]["R3"],tareas[5]["R4"]],[tareas[6]["R1"],tareas[6]["R2"],tareas[6]["R3"],tareas[6]["R4"]],[tareas[7]["R1"],tareas[7]["R2"],tareas[7]["R3"],tareas[7]["R4"]],[tareas[8]["R1"],tareas[8]["R2"],tareas[8]["R3"],tareas[8]["R4"]],[tareas[9]["R1"],tareas[9]["R2"],tareas[9]["R3"],tareas[9]["R4"]],[tareas[10]["R1"],tareas[10]["R2"],tareas[10]["R3"],tareas[10]["R4"]],[tareas[11]["R1"],tareas[11]["R2"],tareas[11]["R3"],tareas[11]["R4"]],[tareas[12]["R1"],tareas[12]["R2"],tareas[12]["R3"],tareas[12]["R4"]],[tareas[13]["R1"],tareas[13]["R2"],tareas[13]["R3"],tareas[13]["R4"]],[tareas[14]["R1"],tareas[14]["R2"],tareas[14]["R3"],tareas[14]["R4"]],[tareas[15]["R1"],tareas[15]["R2"],tareas[15]["R3"],tareas[15]["R4"]],[tareas[16]["R1"],tareas[16]["R2"],tareas[16]["R3"],tareas[16]["R4"]],[tareas[17]["R1"],tareas[17]["R2"],tareas[17]["R3"],tareas[17]["R4"]],[tareas[18]["R1"],tareas[18]["R2"],tareas[18]["R3"],tareas[18]["R4"]],[tareas[19]["R1"],tareas[19]["R2"],tareas[19]["R3"],tareas[19]["R4"]],[tareas[20]["R1"],tareas[20]["R2"],tareas[20]["R3"],tareas[20]["R4"]],[tareas[21]["R1"],tareas[21]["R2"],tareas[21]["R3"],tareas[21]["R4"]],[tareas[22]["R1"],tareas[22]["R2"],tareas[22]["R3"],tareas[22]["R4"]],[tareas[23]["R1"],tareas[23]["R2"],tareas[23]["R3"],tareas[23]["R4"]],[tareas[24]["R1"],tareas[24]["R2"],tareas[24]["R3"],tareas[24]["R4"]],[tareas[25]["R1"],tareas[25]["R2"],tareas[25]["R3"],tareas[25]["R4"]],[tareas[26]["R1"],tareas[26]["R2"],tareas[26]["R3"],tareas[26]["R4"]],[tareas[27]["R1"],tareas[27]["R2"],tareas[27]["R3"],tareas[27]["R4"]],[tareas[28]["R1"],tareas[28]["R2"],tareas[28]["R3"],tareas[28]["R4"]],[tareas[29]["R1"],tareas[29]["R2"],tareas[29]["R3"],tareas[29]["R4"]],[tareas[30]["R1"],tareas[30]["R2"],tareas[30]["R3"],tareas[30]["R4"]],[tareas[31]["R1"],tareas[31]["R2"],tareas[31]["R3"],tareas[31]["R4"]]])
    # n = nuemero de actividades con fictiacias #pensar en una forma distinta de escribir esto 
    n = len(ka)
    #tiempos de inicio segun la linea base
    Ascl=[0]
    for iwi in range(1,31+1):
        Ascl.append(Capturado[1][iwi]['TimeEnd'])
    #ObjAscl es el Makespan generado por la linea base en la programacion proactiva, que tambien es igual a Asc(k) de la actividad 28 en este caso la ultima actividad
    #robustez de la solucion
    RobustezAscl=0
    #robustez de la calidad
    ROBAscl = 0
    # tiempo de duracion de cada actividad
    d=[0]*len(ka)
    #Creacion lista de actividades
    # z(k) prioridad de cada actividad segun la programacion proactiva
    def Z():
        qq = n
        con = 0
        ya = []
        ya1=[]
        jj = 0
        for xk in ka:
            for xi in i:
                if Ascl[xk-1]<Ascl[xi-1]:
                        qq=qq-1
            ya.append(qq)
            qq = n                                   
        for xk in ka:
            for xi in i:  
                if ya[xk-1] == ya[xi-1]:
                    con = con + 1
            if con>0:
                ya[xk-1] = ya[xk-1] - con
            if jj>0:
                ya[xk-1] = ya[xk-1] + 1       
            jj = jj + 1
            con=0
            ya1.append(ya[xk-1])
        return ya1
    z = Z()
    #********************PARA EL PROCEDIMINETO ASCL ...... SGS 
    # # Escenarios - programacion reactiva - SGS paralelo
    # print("¡Hola!"," ingrese la cantidad de escenarios")
    x = 50
    xx=x
    e = list(range(1,x+1))
    #tiempo donde inicia cada actividad segun sgs
    # Smc es el tiempo de inicio en programación reactiva despues de aplicar SGS 
    #obj(e) es el makespan en programación reactiva despues de aplicar SGS para cada actividad k en cada escenario e
    SMC=[]
    toi=[]
    TOID=[]
    ii=[0]*len(ka)
    for xe in e:    
        #actividades completadas en el SGS en un momento dado Tg 
        c = [0]*len(ka)
        #numero total de precendencias de cada actividad
        np = [0,len(tareas[1]["Predecessors"]),len(tareas[2]["Predecessors"]),len(tareas[3]["Predecessors"]),len(tareas[4]["Predecessors"]),len(tareas[5]["Predecessors"]),len(tareas[6]["Predecessors"]),len(tareas[7]["Predecessors"]),len(tareas[8]["Predecessors"]),len(tareas[9]["Predecessors"]),len(tareas[10]["Predecessors"]),len(tareas[11]["Predecessors"]),len(tareas[12]["Predecessors"]),len(tareas[13]["Predecessors"]),len(tareas[14]["Predecessors"]),len(tareas[15]["Predecessors"]),len(tareas[16]["Predecessors"]),len(tareas[17]["Predecessors"]),len(tareas[18]["Predecessors"]),len(tareas[19]["Predecessors"]),len(tareas[20]["Predecessors"]),len(tareas[21]["Predecessors"]),len(tareas[22]["Predecessors"]),len(tareas[23]["Predecessors"]),len(tareas[24]["Predecessors"]),len(tareas[25]["Predecessors"]),len(tareas[26]["Predecessors"]),len(tareas[27]["Predecessors"]),len(tareas[28]["Predecessors"]),len(tareas[29]["Predecessors"]),len(tareas[30]["Predecessors"]),len(tareas[31]["Predecessors"])]#aqui puedo poner la suma de predecesores de cada actividad 
        #total de actividades finalizadas para la tarea k en la etapa g
        To= [1]+[0]*31
        #tiempo de finalización de actividades activas
        af= [0]*len(ka)
        #actividades elegibles en la etapa g
        eleg=[0]*len(ka)
        #tiempo donde finaliza cada actividad
        f=[0]*len(ka)
        # orden de las actividaddes elegibles en la etapa g
        w=[0]*len(ka)
        # actividades activas en el momento Tg
        act=[1]+[0]*31
        #tiempo o momento que corresponde a la etapa g (Variable auxiliar)
        H =20000
        #etapa
        g = 0  
        #tiempo o momento que corresponde a la etapa g (Variable principal) - tiempo transcurrido en la etapa g 
        Tg = 0
        #contador 
        y = 1
        m = 0
        cont = 0
        ww = 0
        vw = 0
        while y<=n-1:
            g=g+1
            for xk in range(len(ka)):
                af[xk] = (act[xk])*(f[xk])
            if g>1:
                H=20000
                for xk in range(len(ka)):
                    if af[xk]>0:
                        if af[xk]<=H:
                            H=af[xk]
                for xk in range(len(ka)): 
                    if af[xk]==H:
                        for RR in range(len(R)):
                            B[RR]=B[RR]+u[xk][RR]
            else:
                H=0
            Tg=H
            for xk in range(len(ka)):
                if f[xk]==Tg:
                    if c[xk]==0:
                        c[xk] = c[xk] + act[xk]
                        act[xk] = act[xk] - c[xk]
            for xi in i: 
                for xk in ka:
                    toi.append(c[xk-1]*p(xk,xi))
            T=0
            for Rs in list(range(32,992+1,32)):#992=(32*32)-32
                TOID.append(sum(toi[T:Rs]))
                T=Rs
            for xp in range(len(i)):
                To[xp+1]=TOID[xp]
            for x in toi[:]:
                toi.remove(x)
            for xs in TOID[:]:
                TOID.remove(xs)
            for xk in range(len(ka)):
                if To[xk]==np[xk]:
                    eleg[xk] = 1-c[xk]-act[xk]
                else:
                    eleg[xk]=0
            for xk in range(len(ka)): 
                w[xk]= eleg[xk]*z[xk]
            m=1
            ww=0
            for xk in range(len(ka)):
                ww=ww+w[xk]
            while ww>0:
                for xk in range(len(ka)):
                    if w[xk]==m:
                        if u[xk][0]<=B[0]:
                            cont = cont + 1
                        if u[xk][1]<=B[1]:
                            cont = cont + 1
                        if u[xk][2]<=B[2]:
                            cont = cont + 1
                        if u[xk][3]<=B[3]:
                            cont = cont + 1
                        if cont==4:
                            act[xk]=1
                            eleg[xk]=0
                            for wiw in range(1,32+1):
                                if ka[xk]==1 and wiw==1:
                                    d[xk]=0
                                    break
                                elif ka[xk]==32 and wiw==32:
                                    d[xk]=0
                                else:   
                                    if ka[xk]==wiw:
                                        d[xk]=int(round(stats.beta.rvs(2,5,(tareas[xk]["TimeDuration"])*11/20,(tareas[xk]["TimeDuration"])*23/8)))#asignacion de la duracion.
                            f[xk]=Tg+d[xk]
                            y=y+1
                            for xr in range(len(R)):
                                B[xr]= B[xr]- u[xk][xr]
                        else:
                            eleg[xk]=0
                            act[xk]=0
                    cont=0
                m=m+1
                for xk in range(len(ka)):
                    w[xk]=eleg[xk]*z[xk]
                vw=0
                for xk in range(len(ka)):
                    vw=vw+w[xk]
                ww=vw
        for xk in range(len(ka)):
            ii[xk]=0
            ii[xk] = f[xk]-d[xk]
            SMC.append(ii[xk])
    obj=[]
    for xe in list(range(31,(xx*32),32)):
        obj.append(abs(SMC[xe]))
    promedio = int(sum(obj)/50)
    Capturado.pop(1)
    Capturado[0]["Mks"] = promedio
    if ingreso !=[]:
            ingreso.pop(1)
            ingreso[0]["Mks"] = promedio
            return ingreso[0]
    return Capturado[0]
#######################################################################################################################################################################################
#Incío dos códigos dos operadores genéticos
def generando_poblacion(n):
	popu = []
	i = 0
	individual = {}

	while i < n:
		individual = SGS_P([])
		if existe_cromosoma(individual, popu) == 1:#Comprueba si el cromosoma ya existe 
			#print 'Chromossome igual'
			individual = {}
		else:	
			popu.append(SGS_P([]))
			i = i + 1
	return popu

#Función para garantizar que no haya cromosomas iguales en la población. 
def existe_cromosoma(cromosoma, poblacion):
	
	for ind in poblacion:
		if cromosoma['Cromosoma'] == ind['Cromosoma']: 
			return 1

	return -1 	

#Ordena la población por el menor costo de tiempo de ejecución
def clasificando_candidatos(pop):

	popElitist = sorted(pop, key=lambda k: k['Mks'])
	return popElitist

def selecciona_a_los_mejores_padres(pop, txSlection):

	poplength = len(pop)
	popCondidates = clasificando_candidatos(pop)
	Selecciona_la_cantidad = int(((poplength*txSlection)/100))

	elit = popCondidates[0:Selecciona_la_cantidad]

	return elit

def crossover(ind1, ind2, candidates, qp):


	puntero = 0
	limite = 0
	Cromosoma1 = []
	Cromosoma2 = []
	hijo1 = {}
	hijo2 = {}
	lenInd1 = len(ind1['Cromosoma']) 
	lenInd2 = len(ind2['Cromosoma'])
	listrandom = []
	offset = int(lenInd1/(qp+1))#compesación
	residual = int(lenInd1%(qp+1))
	set = 0
	listrandom = range(0,lenInd1)
	puntero=random.choice(listrandom)
	#listrandom = range(0,lenInd1)
	#puntero =  random.choice(listrandom)

	if lenInd1 == lenInd2:
		#generando hijos
		for i in range(1,qp+2):
			#print 'i: ', i, 'offset: ', offset, 'puntero: ' , puntero

			limite = (i*offset)
 
			if (i%2) == 1:
				Cromosoma1 += ind1['Cromosoma'][puntero:limite]
				Cromosoma2 += ind2['Cromosoma'][puntero:limite]
				puntero = limite
			else:
				Cromosoma1 += ind2['Cromosoma'][puntero:limite]
				Cromosoma2 += ind1['Cromosoma'][puntero:limite]
				puntero = limite
		
		if residual > 0:
			if ((limite + residual)%2) == 1:
				Cromosoma1 += ind1['Cromosoma'][puntero:limite+residual]
				Cromosoma2 += ind2['Cromosoma'][puntero:limite+residual]
			else:
				Cromosoma1 += ind2['Cromosoma'][puntero:limite+residual]
				Cromosoma2 += ind1['Cromosoma'][puntero:limite+residual]
	else:
		print ('Pais com tamanho de gene diferente!')
		exit(1)

	hijo1['Cromosoma'] = Cromosoma1	
	hijo2['Cromosoma'] = Cromosoma2
	
	candidates.append(hijo1)
	candidates.append(hijo2)

def cruce_con_los_mejores_padres(mejorP, pop, candidatos, qp):

	i = 1
	j = 0
	lengthBP = len(mejorP)
	lengthPOP = len(pop)

	while i < lengthBP - 1:
		j = 1
		while j < lengthPOP - 2:
			crossover(mejorP[i], pop[j], candidatos, qp)
			j = j + 1
		i = i + 1	

def cruce_de_la_poblacion(pop, candidatos, qp):

	i = 1
	j = 0
	length = len(pop)

	while i < length - 1:
		j = 1
		while j < length - 2:
			crossover(pop[i], pop[j], candidatos, qp)
			j = j + 1
		i = i + 1	

def mutacion(individual, candidatos, probabilidad):

	mutant =  copy.deepcopy(individual)
	length = len(mutant['Cromosoma'])
	aux = 0
	candidate = {}

	i = 1 #Asegura que no intentarás realizar una mutación en la actividad 1, ya que no importa porque es ficticia
	while i < length - 2: #Asegura que no intentará hacer una mutación en la actividad 32, ya que no importa porque es ficticia
		if choice(2, p = [1-probabilidad, probabilidad]):
			#chromossome.vect[x] = random_integers(1, Solution.solution_size)
			print ('Mutación')
			print('Gen1: ', mutant['Cromosoma'][i])
			print('Gen2: ', mutant['Cromosoma'][i+1]) 
			aux = mutant['Cromosoma'][i+1]
			mutant['Cromosoma'][i+1] = mutant['Cromosoma'][i]			
			mutant['Cromosoma'][i] = aux
			print (mutant['Cromosoma'])

		i = i + 1
	
	candidate['Cromosoma'] = mutant['Cromosoma'] 

	candidatos.append(candidate)

def mutacion_de_poblacion(pop, candidatos, probabilidad):

	for ind	in pop:
		mutacion(ind, candidatos, probabilidad)

def tiene_un_gen_repetido(Cromosoma):

	#print Cromosoma

	for gen in Cromosoma['Cromosoma']:
		if Cromosoma['Cromosoma'].count(gen) > 1:
			return 1

	else:
		return -1

def candidato_de_evaluación(candidato):

	if tiene_un_gen_repetido(candidato) == 1:
		return None

	Sg = [] #Conjunto de actividades elegido
	F = []	#Hora de finalización de las actividades
	g = 32 #Número de actividades del proyecto
	et = [] #Hora de finalización
	tiempo_de_uso_de_recursos = {} #Timeline de uso dos recursos
	individual = {} #Individuo generado en ejecución
	
	
	#Procesando la primera actividad
	tarea = obtener_actividad(candidato['Cromosoma'][0])
	et.append({'NR':tarea['NR'], 'TimeEnd':0})
	Sg.append(tarea['NR'])
	F.append(1)
	tiempo_de_uso_de_recursos[0] ={'R1' : 0, 'R2' : 0, 'R3' : 0, 'R4' : 0} #Inserindo uso dos recursos no instante 0


	i = 1
	while i < g:

		#función de selección de actividades elegibles
		#seleccionar actividades elegibles(Sg, Dg, tp)
		#Seleccionar una actividad al azar
		j = obtener_actividad(candidato['Cromosoma'][i])
		if verificando_que_los_predecesores_ya_estan_programados(j['Predecessors'], Sg) == -1:
			return None

		#Crea la función de consumo de recursos
		
		#Determinar la hora de finalización anticipada de la actividad j, ignorando la disponibilidad de recursos 
		#etc.append({'NR': j['NR'], 'TimeMaxPredecessor': getEarliestEndingPredecessor(j, et)})

		ES = obteniendo_el_predecesor_mas_temprano(j, et)

		#Agregar la hora de finalización de la actividad en ejecución j y actualizar los recursos 
		minJ = asignación_de_actividad_en_la_línea_de_tiempo(j,tiempo_de_uso_de_recursos,ES) #utiliza la duracion media de la actividad 

		
		et.append({'NR':j['NR'], 'TimeEnd': minJ}) 

		#Calculando el tiempo final del conjunto
		F.append(et[-1])

		#Insertar en la lista de actividades ya programadas	
		Sg.append(j['NR'])

		i = i + 1

	individual['Cromosoma'] = Sg
	individual['Mks'] = F[-1]['TimeEnd']
	truco = [individual, F]
	pepe=SGS_P(truco)
	return pepe

def selectsCandidates(candidatesFit, numberpopulation):
	
	classifiedList = clasificando_candidatos(candidatesFit)

	selectedCandidates = classifiedList[0:numberpopulation]

	return selectedCandidates


#def candidatos a evaluación(newGeneration):
#############################################################################################################################################
#Inicio de la ejecución del código

print("¡Hola!"," ingrese el tamaño de la población")
numberpopulation = int(input())
print("¡Hola!"," ingrese la cantidad de puntos de cruce")
numberpoints = int(input())
print("¡Hola!"," ingrese la cantidad de mejores padres a seleccionar de la población anterior")
print("Nota: el anterior parametro es un tasa dependiente del tamaño de la poblacion ejemplo: un valor de 50 tomara la mitad de la poblacion anterior")
txSlection = int(input())
print("¡Hola!","ingrese el numero de generaciones")
numberInteration = int(input())
print("¡Hola!","Hola ingrese la ubicacion del archivo-instancia")
instancia = str(input())
load(instancia)
riesgos()
txMutation = 0.1 #tasa de mutacion del 10% 
Generations = []
numberGeneration = 0
population = generando_poblacion(numberpopulation)
Generation = [{'NrGeneration' : numberGeneration, 'Population' : population}] 
bestParents = selecciona_a_los_mejores_padres(population, txSlection)
newGeneration = []
candidates = []
candidatesFit = []
counterIteration = 0
bestFitness = bestParents[0]['Mks']
Cromosoma=0
print(bestParents[0])
bestFitnessNow = 0

#Inicio del algoritmo genetico
timeBegin = default_timer()
while counterIteration <= numberInteration:

	numberGeneration = numberGeneration + 1
	bestParents = selecciona_a_los_mejores_padres(population, txSlection) #Recuperando los mejores individuos de la población anterior
	population = generando_poblacion(numberpopulation - len(bestParents)) #Generando una nueva población
	population = population + bestParents #Uniendo los mejores de la población anterior con los de la nueva población
	#población cruzada(population, candidates, numberpoints)

	cruce_con_los_mejores_padres(bestParents, population, candidates, numberpoints)
	mutacion_de_poblacion(population, candidates, txMutation)

	#Seleccionar candidatos adecuados
	for ind in candidates:
		candidate = candidato_de_evaluación(ind)
		if candidate == None:
			pass
		else:
			candidatesFit.append(candidate)

	newGeneration = selectsCandidates(candidatesFit, numberpopulation+1)

	bestFitnessNow = newGeneration[0]['Mks']
	Cromosoma = newGeneration[0]["Cromosoma"]
    
	#print contar iteración
	print("generación:",counterIteration, "\n poblacion:",population, "\n Mejores padres:",bestParents)

	if bestFitnessNow >= bestFitness:
		counterIteration = counterIteration + 1    
	else:
		timeEnd = default_timer()
		deltaTime = timeEnd - timeBegin
		print ('Generacion: ', numberGeneration, '\n  Antiguo: ' , bestFitness, '\n  Nuevo: ', bestFitnessNow, ' Cromosoma', Cromosoma, '\nTiempo de ejecución:' , deltaTime)
		bestFitness = bestFitnessNow
		bestParents[-1]["Cromosoma"]= Cromosoma
		bestParents[-1]["Mks"]= bestFitnessNow
		clasificando_candidatos(bestParents)
	if counterIteration == 25:
		timeEnd = default_timer()
		deltaTime = timeEnd - timeBegin
		system("pause")
		print(instancia)
	if counterIteration == 50:
		timeEnd = default_timer()
		deltaTime = timeEnd - timeBegin
		system("pause")
		print(instancia)         
timeEnd = default_timer()
deltaTime = timeEnd - timeBegin
print("###############################################################################")
print ("Mejor padre:",bestParents[0],'\nTiempo de ejecución:' , deltaTime, "\nCandidates",len(candidates))
print(instancia)
system("pause")