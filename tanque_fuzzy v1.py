'''
Tanque v.2, 6 ago 2023
Autor: Damián Quijano A.
Versión con gráfica. Versión funcionable. Final versión v.1
Se usa el módulo:Fuzzy logic toolbox for Python, scikit-fuzzy 0.4.2 is a fuzzy logic toolbox for SciPy.
Autor: scikit-image team(2019).pythonhosted.
Recuperado de: https://pythonhosted.org/scikit-fuzzy/
https://pypi.org/project/scikit-fuzzy/
https://pythonhosted.org/scikit-fuzzy/
https://github.com/scikit-fuzzy/scikit-fuzzy
https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.membership.html

Los resultados se guardan en archivos csv que se abren y se visualizan en gráficos en el programa
analisis_tanque_fuzzy v1.py

La instrucción  .terms.items permite ver las variables linguísticas asignadas por default cuando usas automf. ejemplo:
x.automf(3) #con la instrucción x.terms.items() verás los términos o variables linguísticas: poor,average,good. Se asignan 3 membresías.
y.automf(5) # con la instrucción y.terms.items() verás los términos o variables linguísticas:'poor', ,'mediocre', 'average','decent',
'good'. Se asignan 5 membresías
z.automf(7) # con la instrucción z.terms.items() verás los términos o variables linguísticas: 'dismal', 'poor','mediocre', 'average',
'decent', 'good','excellent'. Se asignan 7 membresías.
https://python.hotexamples.com/es/examples/skfuzzy.control.controlsystem/Antecedent/automf/python-antecedent-automf-method-examples.html 

Crisp: es el valor llamado nítido , o sea, no difuso. Es la manera de diferenciar los valores usuales, por ejemplo 4.5,8.9, etc de los
valores difusos que son parte de varias funciones. El crisp es el valor que esperamos genere el controlo difuso en su salida.

Tenemos un tanque en forma de cilindro regular al que se aplica la fórmula del volumen en función de radio y altura, de donde se puede calcular
la altura si conocemos el volumnen del agua en un momento dado y y el radio del tanque. O bien, si conocemos el caudal, se puede convertir en medidas
de volumen metros cúbicos, el tema es que teniendo un volumen y las medidas del tanque, podemos calcular el nivel del agua a medida que se modifica el caudal.
Es un tanque que trabaja con gravedad, le alcanza un tubo de agua en la entrada superior del tanque; en esa entrada tenemos una válvula que mantiene de forma
constante un flujo o caudal de entrada al tanque. En la salida del tanque, tenemos una válvula que se puede abrir o cerrar gradualmente y que por tanto permite
controlar el flujo de salida.
El tanque mide 5 metros de altura y 2 metros de radio.
EL cauce de entrada son 2 metros cubicos por segundo,el cauce de salida oscila entre 0 y 4 metros cubicos máximo,  fue calculado a tanteo en una hoja de
cálculo llamada simulartanque.xls buscando valores que logren subir y bajar niveles de agua dentro del tanque que no excedan 30 segundos en el peor de los escenarios.
Se probó con varios valores de entrada para llenar todo el tanque ,estando vacío, en no más de 30 segundos.
Se probó con varios valores de entrada para alcanzar los 2.5m del tanque ,estando vacío, en no más de 15 segundos.
Se probó con varios valores de salida y entrada para vaciar el  tanque ,estando previamente a una altura de 2.5m, en no más de 15 segundos.
Se realizaron los cálculos con una simple fórmula de volumen del cilindro.

En resumen, el proceso calcula el nuevo volumen de agua en el tanque producto del cambio en el cauce_salida y , mediante la fórmula del volumnen de un cilindro
regular, despeja la altura  que es el nuevo nivel del agua. Por tanto, se asume que el tanque es un clindro regular al que se aplica la fórmula del volumen en
función de radio y altura, de donde se puede calcular la altura si conocemos el volumnen del agua en un momento dado y y el radio del tanque.
Se usa la fórmula de volumen de un cilindro.
V=PI*r2*altura, pi por radio al cuadrado por la altura. Al despejar la altura:
Altura= V/(PI*r2), altura= volumen entre( pi por radio al cuadrado).
El flujo o caudal está en metros cubicos por segundo.
El Volumen en metros cúbicos (un metro cubico son 1000 mil litros y pesan 1 tonelada)
La altura está en metros.
Tiempo en segundos.
Cada iteración representa 1 segundo(aunque en realidad el programa lo hace en menos).

Dado que el caudal de entrada es de 2m3/s, se espera que la lograr nivelar en 2.5m, el caudal de salida mantenga ese nivel
estando en 2m3/s también, de tal modo que al estar iguales, no sube ni baja. Ese 2m3/s es el valor EZ con probabilida 1 al momento
de definir la variable de salida que es cauce de salida.

'''

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import os
import sys
import time

# Se queire registrar el tiempo de la simulación, se registra el time inicial
inicio = time.time()
txt_duracion="" # es una variable que en posterior función se llena la duración de la simulación(minutos y segundos) en string para
#conocer si dura mucho

# Dimensiones del tanque
altura_tanque = 5.0  # metros
radio_tanque = 2.0   # metros

# Variables del tanque
nivel_agua = 1.0     # metros, nivel inicial que irá cambiando, pero esta vaiable irá cambiando al modificar el nivel para ajustar
#a otro nivel nivel_agua_inicial = 1.0 , este valor no cambiará
nivel_agua_inicial=1.0

# Caudal de entrada
caudal_entrada = 2  # m3/s,  0.2 metros cúbicos por segundo (flujo de entrada), es constante

caudal_salida_max=4 # 0.4m3/s, o sea, la boca de la válcula permite abrir un tamaño que permite desalojar hasta un
# máximo de 0.4m3/s, más rápida que entrada que son 0.2 m3/s
caudal_salida_min=0 # 0 m3/seg
caudal_salida = 0.0  # 0 m3/s, es el caudal inicial.
caudal_neto=0 # 0 m3/s
volumnenNivelActual=0 # 0m3
volumneCaudalPID=0 # 0m3
volumenNivelNuevo=0 # 0m3

nivel_referencia=2.5 #metros,aqui debe establecer el nivel del agua que desea alcanzar y mantener en el tanque. si cambias a 4,
# funciona



#---Definición de valores iniciales y otras configuracions de variables y valores

minlimite=0
maxlimite=4
registro_datos=[]
cont=0
iteraciones=600

# ------------ Creación y configuración del control Fuzzy---------------------------------

# Antecedentes son las entradas, consecuentes son las salidas.
# A continuación establecemos las variables de entrada y salida y su conjunto universo
v_error = ctrl.Antecedent(np.arange(-2.5, 2.51, 0.1), 'v_error') # -2.5,-2.4,-2.3...-1,-1.1,-1.2,-1.3, 0,0.1,0.2,0.3...1,1.1,1.2,1.3...2,2.1,2.2,2.3,2.4,2.5
#, no incluye 2.51
v_caudal = ctrl.Consequent(np.arange(0, 4.1, 0.1), 'v_caudal') #

# Asignación de variables liguísticas y sus funciones de membresía para cada variable.
v_error['EGN'] = fuzz.trapmf(v_error.universe, [-2.5, -2.5,-2, -1]) # Error grande negativo, está muy por debajo de 50 metros
v_error['EN'] = fuzz.trimf(v_error.universe, [-2, -1, 0]) # Error mediano negativo, está algo por debajo de 50 metros

v_error['EZ'] = fuzz.trimf(v_error.universe, [-1, 0, 1]) # Error cero, está cerca o igual a 50 metros

v_error['EP'] = fuzz.trimf(v_error.universe, [0, 1, 2]) # Error pequeño positivo, está algo por encima de 50 metros
v_error['EGP'] = fuzz.trapmf(v_error.universe, [1, 2, 2.5,2.5]) # Error grande positivo,, está muy por encima de 50 metros**


v_caudal['CMB'] = fuzz.trapmf(v_caudal.universe, [0,0, 1, 1.5]) # Caudal muy bajo de salida, sube mucho nivel
v_caudal['CB'] = fuzz.trimf(v_caudal.universe, [1, 1.5, 2]) # caudal bajo de salida, sube nivel

v_caudal['CZ'] = fuzz.trimf(v_caudal.universe, [1.5, 2, 2.5]) # caudal equlibrado

v_caudal['CA'] = fuzz.trimf(v_caudal.universe, [2, 2.5, 3]) # caudal alto de salida, baja nivel
v_caudal['CMA'] = fuzz.trapmf(v_caudal.universe, [2.5, 3, 4,4]) #  caudal muy alto de salida, baja mucho nivel

#v_error.view(), si lo haces por consola escribe v_error.view(),plt.show()
#v_caudal.view()  v_caudal.view(),plt.show()

# A continuación se construyen las relaciones
rule1 = ctrl.Rule(v_error['EGN'] , v_caudal['CMB'])
rule2 = ctrl.Rule(v_error['EN'], v_caudal['CB'])

rule3 = ctrl.Rule(v_error['EZ'], v_caudal['CZ'])

rule4 = ctrl.Rule(v_error['EP'] , v_caudal['CA'])
rule5 = ctrl.Rule(v_error['EGP'] , v_caudal['CMA'])



fuzzy_control = ctrl.ControlSystem([rule1, rule2, rule3,rule4,rule5])
tanque_control = ctrl.ControlSystemSimulation(fuzzy_control)




def tiempo():
    global inicio
    ahora=time.time()
    duracion=ahora-inicio
    minutos=duracion/60
    segundos=duracion%60
    return(minutos,segundos)

def update():# simulación del proceso
    '''
    En otra función: actualizar_gráfico, se aplica la instrucción caudal_salida= pid(nivel_agua) , el pid modifica el contenido de la variable global caudal_salida
    que controla la apertura o cierre de la válvula (en nuestra imaginación), pues al aumentar el caudal_salida es como si se hubera enviado la orden a la válvula de abrir.
    Ese valor pid o caudal, es leída en esta función update (pudo ser enviada por parámetro) al ser , caudal_salida,  una variable global.
    Al ser caudal_salida una variable global, no hace falta ser enviada como parámetro a esta función update, pues ese valor cambiado se refleja en cualquier parte del programa
    que use dicha variable (u otras que también son globales al ser declaradas al inicio del programa antes de funciones y programa principal).
    La función update, que se podría también llamar Proceso, simula el proceso que se quiere controlar, es una acción matemática que genera una salida , un valor numérico ,que
    calcula la altura o nivel del agua en el tanque.
    En resumen, calcula el nuevo volumen de agua en el tanque producto del cambio en el cauce_salida y , mediante la fórmula del volumnen de un cilindro regular, despeja la altura
    que es el nuevo nivel del agua. Por tanto, se asume que el tanque es un clindro regular al que se aplica la fórmula del volumen en función de radio y altura, de donde se puede
    calcular la altura si conocemos el volumnen del agua en un momento dado y y el radio del tanque.
    Esta función update usa de entrada la variable cauce_salida(la válvula al abrir o cerrar total o parcialmente),calcula el caudal neto al restar al caudal_entrada, que siempre
    es constante, pues tiene una válvula antes de la entrada al tanque que mantiene el caudal fijo. Teniendo el caudal neto, se convierte el caudal en litros por minuto en
    volumnen metros cúbicos, esto representa la nueva canitdad de agua aportada o restada al volumen existente. Luego se calcula el volumnen actual ( la que existe antes de la
    modificación del caudal_saliente).
    Teniendo calculados ambos volúmenes (el actual y el generado por el cauce_neto)  tenemos el nuevo volumen del  tanque de agua después de modificar el cauce_salida.
    Teniendo el volumen del tanque y conocido el radio, podemos despejar la altura de la fórmula y calcular la nueva altura a partir del nuevo volumen, esto nos da el nuevo
    nivel_agua que, posteriormene, el pid tendrá como entrada para comparar con el setpoint y de nuevo aplicar los cambios al cauce_salida.
    Por tanto, esta función es el proceso imaginario cuya salida o resultado es lo que mediriía un sensor y enviaría al pid para que lo proceso.

    '''
    global altura_tanque
    global radio_tanque
    global caudal_entrada
    global caudal_salida
    global caudal_neto
    global nivel_agua
    global volumnenNivelActual
    global volumnenCaudalPID
    global volumenNivelNuevo
    
    print("**************************")
   
    
    # Caudal neto:
    caudal_neto= caudal_entrada-caudal_salida
    print("Update. Nivel agua antes de:",nivel_agua, " Caudal de entrada:",caudal_entrada," Caudal de salida:",caudal_salida," Caudal neto:",caudal_neto)
    
    
    volumnenNivelActual=np.pi * (radio_tanque*radio_tanque) * nivel_agua # volumnen o cantidad de agua en el nivel actual, fórmula del volumen de cilindro.
    volumnenCaudalPID=caudal_neto
    #El dt está explicado al inicio, solo es para acelerar, es un factor multiplicativo.
    volumenNivelNuevo=volumnenNivelActual+volumnenCaudalPID # suma ( o resta) de ambos volúmenes dejando el volumnen total 
    nivel_agua=volumenNivelNuevo/(np.pi*(radio_tanque*radio_tanque)) # con el nuevo volumnen del tanque  se calcula la altura del nuevo nivel de agua del tanque
    print("Update. Nivel agua:",nivel_agua, " Caudal de entrada:",caudal_entrada," Caudal de salida:",caudal_salida," Caudal neto:",caudal_neto) 
    
    # Aseguramos que el nivel del agua no sea negativo y no sobrepase los 5 metros de altura
    nivel_agua = max(0, nivel_agua)
    if nivel_agua>5:
        nivel_agua=5
   
    print("Update. volumnenNivelActual:", volumnenNivelActual, " volumnenCaudalPID:", volumnenCaudalPID," volumenNivelNuevo:", volumenNivelNuevo)
    print("Update. Nivel agua :",nivel_agua)
        
    return nivel_agua

 
# Abajo, en la función actualizar_grafico, está el Control PID que devuelve el valor del cauce de salida ,la función también actualiza el gráfico de la simulación
# Desde esta función se llama también a la función update() o del proceso.
def actualizar_grafico(frames):
    global altura_tanque 
    global radio_tanque
    global nivel_agua
    global caudal_salida
    global caudal_entrada
    global registro_datos
    global cont
    global txt_duracion
    print()
    print("------------------------------------------")
    print("1. Modulo pid(antes de pid).Caudal salida:",caudal_salida," Nivel de agua:",nivel_agua)
    nivel_ant=nivel_agua
    caudal_salida_ant=caudal_salida
    cont=cont+1
    
    
    #------------------------- Ciclo de control y realimentación--------------------------------
    # Abajo el control fuzzy recibe (de un supuesto sensor) el valor actual del nivel del tanque, el pid lo comparar con el setpoint, calcula
    # el error y da la salida que será el cauce_saida que recibirá la válvula de salida para controlar el flujo del agua en la salida.
    
    # Compute error
    error=nivel_agua-nivel_referencia # aquí altura sigue siendo la anterior, la nueva se calcula en controlled_update
    tanque_control.input['v_error'] = error
    tanque_control.compute()
    caudal_salida=tanque_control.output['v_caudal']
        
    # Dado que la válcula tiene un mínimo y máximo de lo que puede abrir y cerrar, esto se controla de la siguiente manera.
    if caudal_salida > caudal_salida_max:
        caudal_salida= caudal_salida_max
    if caudal_salida < 0:
        caudal_salida= 0
       
    print("2. Módulo pid(después de pid).Caudal salida return pid:",caudal_salida, "Nivel de agua:",nivel_agua)
    
    # ***************Abajo se llama al proceso en base al nuevo valor del caudal_salida , se calcula el nuevo nivel de agua.**************************
    nivel_agua=update()
    print("3. Módulo pid. Enviado a update. Caudal salida despues de update:",caudal_salida," Nivel de agua:",nivel_agua," Dif:",nivel_agua - nivel_ant)
    print()
    #-------------------------------------------------------------------------------------------------------------------------------------
    
    # -------------------------Graficación de los resultados de cada iteración. La iteración la hace el animation.FuncAnimation--------------
    eje.clear()
    eje.set_title('Simulación del tanque de agua')
    eje.set_xlabel('Radio del tanque (m)')
    eje.set_ylabel('Altura del agua (m)')
    eje.set_xlim(0, 2*radio_tanque)
    eje.set_ylim(0, altura_tanque)
     # Establecer las marcas del eje y
    y_increment = 0.1
    y_ticks = np.arange(2, 3 + y_increment, y_increment) # para que se vean estos incrementos debes abrir toda la pantalla de la gráfica, muestras en eje y los valores desde 2 hasta 3 de 0.1
    eje.set_yticks(y_ticks)
   
    
    # Horizontal line at y=2.5 that spans the xrange.
    eje.axhline(y=nivel_referencia,linewidth=1, color='r') # 2.5 e el setpoint
    mcolor='blue'

    
    # Se agrega informacióin de interés al gráfico
    # https://python-charts.com/matplotlib/texts/
    minutos,segs=tiempo()
    txt_duracion="Min:"+str(round(minutos,2))+" Segs:"+str(round(segs,2))
    eje.text(0.1, 0.85, txt_duracion,transform = eje.transAxes, fontsize=12)
    txt_iteraciones = "Iter:"+ str(round(cont))
    eje.text(0.1, 0.80, txt_iteraciones, transform = eje.transAxes, fontsize=10) # 
    txt_nivel = "Nivel(m):"+ str(round(nivel_agua,3))
    eje.text(0.1, 0.9, txt_nivel,transform = eje.transAxes, fontsize=12)
    txt_cauce_salida = "Cauce Salida(m3/s)="+ str(round(caudal_salida,3))
    eje.text(0.6, 0.9, txt_cauce_salida,transform = eje.transAxes, fontsize=8)
        
    
    # Listo todo lo de arriba se procede a construir todos los datos del gráfico con los nuevos valores en esta iteración.
    eje.bar(0, nivel_agua, width=4*radio_tanque , bottom=0, alpha=0.8, color=mcolor, edgecolor='black')
    
    # Registros de los datos para su posterior graficación 
    registro_datos.append([cont, nivel_agua,caudal_salida,  caudal_neto])
    

#-----------------------------Porgrama principal------------------------------
# Configuramos el gráfico
fig, eje = plt.subplots()

# Abajo tenemos la función de graficación animada FuncAnimation, esta función llamada a la función actualizar_grafico de forma iterativa, de manera infinita y a una velocidad establceida
# en el parámetro interval. A su vez, actualizar_grafico llamada las funcones pid y upadte que calculan los valores necesarios para graficar.
ani = animation.FuncAnimation(fig, actualizar_grafico, interval=100)

# Mostramos la animación
plt.show()

df = pd.DataFrame( registro_datos,columns=['iter', 'nivel_agua', 'caudal_salida', 'caudal_neto'])

# No hace faltsa dt ni dt2, esto se quitará en otra versión.
iniciales=[[cont,altura_tanque, radio_tanque, nivel_agua_inicial, caudal_entrada, nivel_referencia,txt_duracion]]
iniciales_cols=['cont','altura_tanque', 'radio_tanque', 'nivel_agua', 'caudal_entrada', 'nivel_referencia','txt_duracion']
df_iniciales=pd.DataFrame(iniciales,columns=iniciales_cols)

# Guardar los datos y los valores iniciales
carpeta="D:\\Tesis biomedica\\Tanque\\Datos\\"
time_archivo=start_time = time.time()

# Si no se desea guardar los archivos de los resultados de la simulación, se deben comentar.
df.to_csv(carpeta+'datos_'+str(time_archivo)+'.csv') # se comenta cuando no se quiere grabar
df_iniciales.to_csv(carpeta+'iniciales_'+str(time_archivo)+'.csv') # se comenta cuando no se quiere grabar


print('Nombre del archivo de datos guardado: datos_'+str(time_archivo)+'.csv')
print('Nombre del archivo de valores iniciales: inicales_'+str(time_archivo)+'.csv')
print()
pd.set_option('display.max_columns', None)
print(df_iniciales)
print("Final.")




