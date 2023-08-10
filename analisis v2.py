'''
A a partir de Analisis v.2, 6 ago 2023
Tanque-Análisis
Autor: Damián Quijano A.
Versión con gráfica. Versión funcionable. Final versión anterior v.1
Carga el archivo csv de resultados generado por el simulador tanque para visualizar el comportamiento de las diferentes variables del sistema.
'''
'''
Nota: al ejecutar el script, emergen varias ventanas por separado, cada una contiene 4 gráficos de resultados. Al cerrar las ventanas, el programa permite
ver los valores de todas las variables y dataframes desde la consola, por tanto, en la consola, puede correr instrucciones que permitan visualizar otros
valores además de los mostrados en las ventanas aunque culminó el script. En cambio, su pulsa sobre el botón rojo Stop ubicado en el menú de Thony, se
borrará toda la información de las variables.
'''
'''
Se analizan los gráficos de las siguientes variables:
Nivel de agua
Valor de pid
Cauce de salida: o velocidad del flujo, es la variable de control que el pid aumenta o disminuye (multiplicado por un factor multiplicativo dt2)
Cauce neto: los aumentos o disminuciones del cauce en el momento
El eje x contiene los valores de las iteraciones del 1 hasta el que se llegó en la simulación.

A su vez, se estudian tres tramos para cada variable(valores en el eje Y).
El tramo completo, desde el inicio del proceso.
El tramo de oscilación, explicado más adelante (oscilación 1).
El tramo de la oscilación ajustada o zoom (osclación 2)llamado así porque se ajusta manualmente el punto de inicio de las iteraciones.
'''
'''
Tramo de la oscilación (oscilación 1).
Es el tramo de los resultados que son la oscilación estacionaria alrededor o cerca del setpoint. En este caso el setpoint es 2.5.
Dado que el dataset está ordenado por número de iteración, buscamos la primera iteración en el eje x cuya y es igual o mayor a 2.5,
lo cual nos indica que la oscilación empiezan desde dicha x , por tanto se guardan esos valores de dicho tramo en adelante en un
nuevo dataframe llamado oscilación(oscilación 1).
Esto permitirá calcular el mínimo y máximo valor en dicho intervalo.El mínimo se refiere al valor más bajo por debajo del setpoint y
el máximo es el valor más alto por encima del setpoint, en el tramo o intervalo de la oscilación. Y se calcula y se guarda la iteación
inicial de este tramo que servirá de default para la oscilación ajustada si no le escribimos un valor.
'''
'''
Tramo de la oscilación ajustada o zoom , oscilación estable o estacionaria(oscilación 2). 
El problema de la oscilación 1 es que incluye las oscilaciones inciales que suelen ser muy altas antes que la oscilación se estabilice
y sea la que realmente deseamos conocer sus mínimos y máximos, pues si calculamos los mínimos y máximos con los cilcos iniciales, nos arroja
minimos y máximos y promedio que en realidad no se repiten más en adelante.
Por tanto ,más adelante hay un gráfico que permite se modifique el valor de la iteración desde la que deseamos se genere el tramo, con el fin
de visualizar , a ojo, y despues de ver la oscilación 1, la iteración desde la que pensamos inicia la parte estacionaria o estable con el fin
de calcular el mínimo , máximo y el promedio de los valores de dicho tramo oscilatorio.
El objetivo es enocontrar el inicio de la oscilación estacionaria, o sea, cuyos máximos y mínimos practicamente son iguales a lo largo del
tramo. Eso nos indica que las oscilaciones se estabilizaron y que ya podemos confiar en el intervalo de error con esos valores.
'''
'''
Intervalo de error: caso nivel de agua.
 ( setpoint- mínimo nivel en el tramo de oscilación estable, setpoint más el máximo del tramo de la oscilación estable).


'''

'''
Valores que se deben graduar:
1. El valor del iter o número de iteración  a partir del que inicia el intervalo de oscilación 2.
Se configura en la sección que calcula la oscilación 2, concretamente en la instrucción iniciar_desde=(aque escribe el valor de la iteración desde la que
desea iniciar el tramo oscilación 2). Por default el valor es 
iniciar_desde=iter_oscilacion1 ,valor calculado en el for de arriba al calcular la oscilación 1,que es igual al iter del primer tramo de la oscilación 1,
por tanto, ambos tramos, de oscilación 1 y 2 serán los mismos y la misma gráfica. Lo que se recomienda es correr el script análisis y observar la gráfica
de la oscilación 1, identificar visualmente cuál es la iteración que percibe como el inicio de la oscilación estable, o bien, puede experimentar con otros
valores de inicio en dicho tramo. Luego reemplazar el valor iniciar_desde=iter_oscilacion1 por (por ejemplo) iniciar_desde=150. Es importante que , previo,
se lea el valor iter que se muestra en la parte que muestra los valores iniciales, pues indica la cantidad de iteraciones que ocurrieron al momento de parar
la simulación, por tanto, si hubieron 200 iteraciones, el valor que se coloque en iniciar_desde= valor debe ser menor a las 200 iteraciones, de lo contrario,
el gráfico aparecerá vacío, y los valores mínimos y máximos son Nan .El valor iteraciones ocurridas se conoce en int(df_iniciales.iloc[0][1]).
2. Ajuste de los valores en el eje Y.
Algunas veces se requiere más precisión en la escala de valores en el eje Y y se requiere que se dividan en intervalos más cortos los valores
en dicho eje,por ejemplo, si se visualizan los valores 2.0,2.5 y 3.0, se desea que aparezcan los valores intermedios, o sea, 2.1,2.2..2.6,2.7..., o sea,
intervalos de 0.1 , por tanto, modificaremos el y_ticks, que es el que establece el valor del incremento entre los valores en el eje Y. Además, dado que los
valores en oscilacion 1 y 2 no usan todos los valores del eje Y, se calcula el mínimo y máximo en el eje Y para evitar que se muestre un gráfico con mucho
espacio vacío, es una forma de hacer un aumento o zoom.
Esto solo se aplica en los intervalos oscilacion 1 y oscilacion 2. Por tanto, hay un mínimo y máximo en los ejes Y de oscilación 1 y 2, y luego se ajusta el
tamaño de incremento en los valores de dichos ejes. En el intervalo completo no hay problema, dado que aparecen todos los valores de 0 a 5 (altura del tanque)
para el caso de nivel de agua, y en ese espacio aparece toda la información, por tanto no se manipula el mínimo y máximo ni los incrementos. En cambio, en el
tramo oscilacion 1 los valores útiles no se muestran en todos los valores de Y del tramo completo, entonces se calcula el mínimo y máximo en el eje Y del
tramo oscilacion 1 y luego se calcula el incremento. Igual ocurre para la oscilacion 2, que suele ser más estrecho.

Esto se hace mediante las siguientes instrucciones (previamente se calculó el mínimo y máximo en el eje Y en el tramo oscilacion 1), para el caso tramo
oscilacion 1:
y_increment1 = 0.1 , se establece el incremento, pues nos hemos dado cuenta que es el mejor incremento al ver la gráfica al ser corrida la primera vez.
y_ticks = np.arange(min_oscilacion1_nivel_margen,  max_oscilacion1_nivel_margen, y_increment1) , se generan los valores del eje Y, el mín, máx e incremento.
ax[1,0].set_yticks(y_ticks)# se establecen los valores en el gráfico.
En cambio, en otras ocasiones, se requiere lo contrario, se requiere un incremento mayor, una separación mayor, esto ocurre
a menudo en el tramo de oscilacion 2 para valores muy pequeños como el PID:
y_increment6 = (max_oscilacion2_caudal_salida-min_oscilacion2_caudal_salida) * 50 , se multiplica por 50 en vez de por 0.1(divide), además existe un intento
de automatizar el zoom, o sea, el incremento es 50 veces más el valor producto de la resta del máximo - mínimo en Y en el intervalo oscilacion 2.

Lo que se recomienda es que se corra 2 veces el script análisis, la primera vez es para observar  los valores en eje Y y para identificar el valor iteración
desde el que empiece tramo oscilación 2. Entonces se agregan los ajustes en escala de Y y el iter desde el que inicia oscilacion 2 y se corre de nuevo
el script análisis. Si se observa que alguna ventana demora mucho en mostrar los resultados, es producto de que el ajuste en eje Y, concretamente los
incrementos, están consumiendo mucho cómputo y hay que ir ajustando hasta que la ventana demorada se muestre rápidamente.


'''


import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys
import time
from simple_pid import PID
import numpy as np
import pandas as pd

# datos de cada iteración

# Se abren los archivos de resultados.
carpeta="D:\\Tesis biomedica\\Tanque\\Datos\\"
nombreArchivoDatos='datos_1691439466.2423778.csv'
nombreArchvoIniciales='iniciales_1691439466.2423778.csv'


df=pd.read_csv(carpeta+nombreArchivoDatos)# ['iter', 'nivel_agua' ,  'valor_pid' , 'caudal_salida', 'caudal_neto'])
# max_nivel= df.nivel_agua.max() # esto es para establecer el máximo del eje de la Y en algunos gráficos más adelante, de tal modo que no tenga que
# # ser la altura del tanque, o sea, 5, pues la que sea la máxima que alcanzó es suficiente y el gráfico es más preciso.
# # valores iniciales usados para la simulación con los datos subidos (arriba, anterior a esta línea)
# min_nivel= df.nivel_agua.min() # lo mismo que arriba, esto permite, con los de arriba , hacer un zoom que enfoque aquella parte del gráfico
# # en la que realmente se mueven los datos.

df_iniciales=pd.read_csv(carpeta+nombreArchvoIniciales) # son valores iniciales o constantes
'''Valores iniciales.
0 id del dataset
1 cont  cantidad de iteraciones, se recoje el último cont o contador de iteraciones
2 altura_tanque
3 radio_tanque
4 nivel_agua  inicial
5 caudal_entrada
6 nivel_referencia
7 kp  inicial
8 ki incial
9 kd inicial
10 minlimite
11 maxlimite
12 txt_duracion
'''

iteraciones=int(df_iniciales.iloc[0][1])
nivel_inicial=df_iniciales.iloc[0][4]
radio=df_iniciales.iloc[0][3]
altura=df_iniciales.iloc[0][2]
caudal_entrada=df_iniciales.iloc[0][5]
setpoint=df_iniciales.iloc[0][6]
parametros='kp:'+str(df_iniciales.iloc[0][7])+' ki:' + str(df_iniciales.iloc[0][8])+' kd:'+ str(df_iniciales.iloc[0][9])
min_pid=df_iniciales.iloc[0][10]
max_pid=df_iniciales.iloc[0][11]
txt_duracion=df_iniciales.iloc[0][12]
'''
Se tiene un total de 16 gráficos divididos en 4 pantallas o ventanas  (figures) abiertas simultáneamente.

Ventana 1- nivel de agua: gráfico con los datos generales, gráfico con el tramo total, gráfico de oscilación 1, gráfico de oscilación 2.
Se incluyen los datos: mínimo, máximo, intervalo, promedio.

Ventana 2- valor pid: gráfico con los datos generales, gráfico con el tramo total, gráfico de oscilación 1, gráfico de oscilación 2.
Se incluyen los datos: mínimo, máximo, intervalo, promedio.

Ventana 3- cuadal de salida: gráfico con los datos generales, gráfico con el tramo total, gráfico de oscilación 1, gráfico de oscilación 2.
Se incluyen los datos: mínimo, máximo, intervalo, promedio.

Ventana 4- caudal neto: gráfico con los datos generales, gráfico con el tramo total, gráfico de oscilación 1, gráfico de oscilación 2.
Se incluyen los datos: mínimo, máximo, intervalo, promedio.

Por tanto se calculan los valores de los tramos de oscilación 1 y oscilación 2 y se guardan en datasets.
'''


#-----------------------Tramos de oscilación 1 y oscilación 2 -----------------------
# Valores del tramos de oscilación 1.
# ['iter', 'nivel_agua' ,  'valor_pid' , 'caudal_salida', 'caudal_neto'])
#OJO: si la curva se mantiene por debajo del setpoint y ni siquiera hace contacto, no aparecerá el tramo de oscilación 1,pues
# se debe cumplir la condición que alcance y rebase el setpoint.
oscilacion1=[]
iter_oscilacion1=0
grabar="n"
flag=1 # este valor ayuda a que funcione una sola vez el primer if para que capture el iter que inicia la oscilación 1 y no cambie durante el for
for i in df.itertuples():
    if i.nivel_agua>=setpoint and flag==1:# en nuestro caso 2.5 setpoint
        grabar="s"
        iter_oscilacion1=i.iter
        flag=0
    if grabar=="s":
        oscilacion1.append([i.iter,i.nivel_agua,i.valor_pid,i.caudal_salida, i.caudal_neto])
# A continuación se crea el dataframe del tramo de la oscilación      
df_oscilacion1 = pd.DataFrame( oscilacion1,columns=['iter','nivel','valor_pid','caudal_salida', 'caudal_neto'])



# Valores del tramos de oscilación 2. OJO: AQUI CAMBIAS EL AJUSTE O ZOOM DE ESTE INTERVALO.
# Error frecuente: si el máximo de iteraciones son 400 y escribe i.iter>=500, devolverá o registros y NAND
oscilacion2=[]
grabar="n"
iniciar_desde=400 # aquí se escribe un valor, por defecto es= iter_oscilacion1(calculado en el for de arriba al calcuar ka oscilación 1,que es igual al iter
# del primer tramo de la oscilación 1, la idea es que pongas otro iter, pero
# se cambia a otro siempre y cuando esté en el rango entre 0 y el valor iteraciones=int(df_iniciales.iloc[0][1]). Si el tramo completo es entre
# 0 y 620, puede escribir 300, o sea, inciar_desde=300. Lea la explicación al inicio sobre oscilación 2. Lo aconsejable es que inicie con el valor por defecto
# iter_oscilacion1 y después de ver las gráficas e identificar un tramo de interés que considere cubre la oscilación estable, seleccione una iteración y
# cambie el valor y ejecute de nuevo el análisis.


for i in df.itertuples():
    if i.iter>=iniciar_desde:
        grabar="s"
    if grabar=="s":
        oscilacion2.append([i.iter,i.nivel_agua,i.valor_pid,i.caudal_salida, i.caudal_neto])
# A continuación se crea el dataframe del tramo de la oscilación      
df_oscilacion2 = pd.DataFrame( oscilacion2,columns=['iter','nivel','valor_pid','caudal_salida', 'caudal_neto'])




#-------------- Gráficos del nivel del agua ------------------------------
# En el eje X se muestran los números de iteración, en el eje Y se muestra el nivel del agua
# Se calculan los mínimos y máximos de los niveles de todo el tramo y se les agrega un pequeño margen hacia abajo y hacia arriba
max_nivel= df.nivel_agua.max() # esto es para establecer el máximo del eje de la Y en algunos gráficos más adelante, de tal modo que no tenga que
# ser la altura del tanque, o sea, 5, pues la que sea la máxima que alcanzó es suficiente y el gráfico es más preciso.
# valores iniciales usados para la simulación con los datos subidos (arriba, anterior a esta línea)
min_nivel= df.nivel_agua.min() # lo mismo que arriba, esto permite, con los de arriba , hacer un zoom que enfoque aquella parte del gráfico
# en la que realmente se mueven los datos.


# Se calculan los mínimos y máximos de los niveles de oscilación1 y se les agrega un pequeño margen hacia abajo y hacia arriba
'''
Se aplica el absoluto o abs al calcular el margen para garantizar que reste o sume correctamente, por ejemplo, podemos tener los siguientes escenarios:
Si aplicamos el 10 (0.1) de margen que se agrega al máximo y 10(0.1) al mínimo:
Máximo 4  el 10% es 0.4  debería ser 4.4    Sin abs sale 4 + 0.4= 4.4  Al aplicar el abs al margen(0.4), o sea abs(0.4), el resultado es el mismo
Mínimo 2  el 10% es 0.2  debería ser 1.8    Sin abs sale 2 - 0.2= 1.8  Al aplicar el abs al margen(0.2), o sea abs(0.2), el resultado es el mismo

Máximo 4  el 10% es 0.4  debería ser 4.4    Sin abs sale 4 + 0.4= 4.4  Al aplicar el abs al margen(0.4), o sea abs(0.4), el resultado es el mismo
Minimo 0  el 10% es 0.0  debería ser 0.0    Sin abs sale 0 - 0.0= 0.0  Al aplicar el abs al margen(0.0), o sea abs(0.0), el resultado es el mismo

Máximo 4  el 10% es 0.4  debería ser 4.4    Sin abs sale 4 + 0.4= 4.4   Al aplicar el abs al margen(0.4), o sea abs(0.4), el resultado es el mismo
Mínimo -2 el 10% es -0.2  debería ser -2.2  Sin abs sale -2 - (-0.2)= -2+0.2=-1.8 error  Al aplicar el abs al margen(-0.2), o sea abs(-0.2), el resultado
es -2.2, es correcto.

Máximo 0  el 10% es 0.0  debería ser 0.0    Sin abs sale 0 + 0.0= 0.0  Al aplicar el abs al margen(0.0), o sea abs(0.0), el resultado es el mismo
Mínimo -2 el 10% es -0.2  debería ser -2.2  Sin abs sale -2 -(-0.2)= -2+0.2=-1.8 error Al aplicar el abs al margen(-0.2), o sea abs(-0.2), el resultado
es -2.2, es correcto.
Máximo -2 el 10% es -0.2  debería ser -1.8  Sin abs sale -2 +(-0.2)= -2+0.2=-1.8 Al aplicar el abs al margen(-0.2), o sea abs(-0.2), el resultado es el mismo
Mínimo -4 el 10% es 0.4  debería ser -4.4   Sin abs sale -4 -(-0.4)= -4.0+0.4=-3.6 error Al aplicar el abs al margen(-0.4), o sea abs(-0.4), el resultado
es --4.4, es correcto.
Lo de arriba muestra la necesidad de aplicar el absoluto. En el caso de valores 0 , no se aumenta o disminuye, es una decisión mejorable.

'''

min_oscilacion1_nivel=df_oscilacion1.nivel.min()
min_oscilacion1_nivel_margen=min_oscilacion1_nivel-abs((min_oscilacion1_nivel*0.1))
max_oscilacion1_nivel=df_oscilacion1.nivel.max()
max_oscilacion1_nivel_margen=max_oscilacion1_nivel+abs((max_oscilacion1_nivel*0.1))
# print(min_oscilacion1_nivel_margen," ",  max_oscilacion1_nivel_margen)


# Se calculan los mínimos y máximos de los niveles de la oscilación2 y se les agrega un pequeño margen hacia abajo y hacia arriba
min_oscilacion2_nivel=df_oscilacion2.nivel.min()
min_oscilacion2_nivel_margen=min_oscilacion2_nivel-abs((min_oscilacion2_nivel*0.1))
max_oscilacion2_nivel=df_oscilacion2.nivel.max()
max_oscilacion2_nivel_margen=max_oscilacion2_nivel+abs((max_oscilacion2_nivel*0.1))
# print(min_oscilacion2_nivel_margen," ",  max_oscilacion2_nivel_margen)


figNivel, ax = plt.subplots(2,2) # 0,0  0,1  1,0  1,1


# Gráfico de datos iniciales.

ax[0,0].set_ylim(0,10) 
ax[0,0].set_xlim(0,10)

texto = "Iters:"+ str(iteraciones)
ax[0,0].text(1, 9, texto, fontsize=7)

texto = "nivel_inicial:"+ str(nivel_inicial)
ax[0,0].text(1, 8, texto, fontsize=7)

texto = "radio:"+ str(radio)
ax[0,0].text(1, 7, texto, fontsize=7)

texto = "altura:"+ str(altura)
ax[0,0].text(1, 6, texto, fontsize=7)

texto = "caudal_entrada:"+ str(caudal_entrada)
ax[0,0].text(1, 5, texto, fontsize=7)

texto = "setpoint:"+ str(setpoint)
ax[0,0].text(1, 4, texto, fontsize=7)

texto = "parametros:"+ str(parametros)
ax[0,0].text(1, 2, texto, fontsize=7)

texto = "min_pid:"+ str(min_pid)
ax[0,0].text(4, 9, texto, fontsize=7)

texto = "max_pid:"+ str(max_pid)
ax[0,0].text(4, 8, texto, fontsize=7)

ax[0,0].text(4, 7, txt_duracion, fontsize=7)





ax[0,0].set_title("Valores iniciales y constantes usados para la simulación.")

# Gráfico de tramo completo de la variación del nivel de agua.
ax[0,1].plot(df.iter, df.nivel_agua, linewidth=2.0)
ax[0,1].set_ylim(min_nivel- (min_nivel*0.1),max_nivel+ (max_nivel*0.1))# (max_nivel*0.1) agrega un 10%, (max_nivel*0.1) restas un 10%
ax[0,1].set_xlabel('Iteraciones')
ax[0,1].set_ylabel('Altura del agua (m)')
ax[0,1].axhline(y=setpoint,linewidth=1, color='r')
ax[0,1].grid()
ax[0,1].set_title("Variación del nivel tanque. Setpoint: "+str(setpoint))

# Gráfico de la oscilación 1 de la variación del nivel de agua.
y_increment1 = 0.1# divide el eje Y en unidades decimalaes pequeñas,se observa el valor max y min y se establece la división en el eje Y que se desea.
y_ticks = np.arange(min_oscilacion1_nivel_margen,  max_oscilacion1_nivel_margen, y_increment1) # para que se vean estos incrementos debes abrir toda la pantalla de la gráfica, muestras en eje y los valores desde 2 hasta 3 de 0.1
ax[1,0].set_yticks(y_ticks)# divide el eje Y en unidades decimalaes pequeñas
ax[1,0].plot(df_oscilacion1.iter, df_oscilacion1.nivel, linewidth=2.0)
ax[1,0].set_ylim(min_oscilacion1_nivel_margen, max_oscilacion1_nivel_margen)
ax[1,0].set_xlabel('Iteraciones')
ax[1,0].set_ylabel('Altura del agua (m)')
ax[1,0].axhline(y=setpoint,linewidth=1, color='r')
ax[1,0].grid()
ax[1,0].set_title("Tramo de la oscilación 1 alrededor del setpoint")

textMinMaxoscilacion1 = "Mín:"+ str(round(min_oscilacion1_nivel,3))+" Máx:"+ str(round(max_oscilacion1_nivel_margen,3))
ax[1,0].text(0.6, 0.9, textMinMaxoscilacion1, transform = ax[1,0].transAxes, fontsize=10)  #0.6 y 0.9 son % que se desplaza hacia derecha y hacia arriba
# del gráfico. Si es 0.9 y 0.9 es la esquina superior derecha, si escribes a partir de allí, el texto inicia desde ese punto y continúa hacia la derecha
# y se saldrá, por tanto hay que iniciar más hacia la izquierda, por ejemplo desde 0.6 que es casi la mitad en el ehe horizontal.
# 0,0 es la esquina inferior izquierda, 0.9 , 0 es la esquina inferior derecha, 0, 0.9 es la esquina superior izquierda, 0.5,0.5 es el centro del gráfico.
# Para identificar que nos referimos a la posición relativo, o sea , porcentual, se usa la instrucción transform = ax[1,0].transAxes.

izquierdaError=round(setpoint,3)-round(min_oscilacion1_nivel,3)
derechaError=round(max_oscilacion1_nivel,3)- round(setpoint,3)
textIntervaloError = "("+ str(round(izquierdaError,3))+" , "+ str(round(setpoint,3))+" , "+ str(round(derechaError,3))+")"
ax[1,0].text(0.6, 0.8, textIntervaloError, transform = ax[1,0].transAxes, fontsize=10) 

# Gráfico oscilación 2 de la variación del nivel de agua.
y_increment2 = 0.1 # se observa el valor max y min y se establece la división en el eje Y que se desea.
# print(min_oscilacion2_nivel_margen," ",  max_oscilacion2_nivel_margen," ", y_increment2)
y_ticks2 = np.arange(min_oscilacion2_nivel_margen,  max_oscilacion2_nivel_margen, y_increment2) # divide el eje Y en unidades decimalaes pequeñas
ax[1,1].set_yticks(y_ticks2)# divide el eje Y en unidades decimalaes pequeñas
ax[1,1].plot(df_oscilacion2.iter, df_oscilacion2.nivel, linewidth=2.0)
ax[1,1].set_ylim(min_oscilacion2_nivel_margen, max_oscilacion2_nivel_margen)
ax[1,1].set_xlabel('Iteraciones')
ax[1,1].set_ylabel('Altura del agua (m)')
ax[1,1].axhline(y=setpoint,linewidth=1, color='r')
ax[1,1].grid()
ax[1,1].set_title("Tramo de la oscilación2 alrededor del setpoint")

textMinMaxoscilacion2 = "Mín:"+ str(round(min_oscilacion2_nivel,3))+" Máx:"+ str(round(max_oscilacion2_nivel,3))
ax[1,1].text(0.7, 0.9, textMinMaxoscilacion2, transform = ax[1,1].transAxes, fontsize=10) # 

izquierdaError=round(setpoint,3)-round(min_oscilacion2_nivel,3)
derechaError=round(max_oscilacion2_nivel,3)- round(setpoint,3)
textIntervaloError = "("+ str(round(izquierdaError,3))+" , "+ str(round(setpoint,3))+" , "+ str(round(derechaError,3))+")"
ax[1,1].text(0.7, 0.8, textIntervaloError, transform = ax[1,1].transAxes, fontsize=10) 



figNivel.tight_layout() # esto separa las gráficas para que no se superpongan los labels 
# Personalizar el título de la ventana de la figura


#-------------- Gráficos del valor pid ------------------------------

# En el eje X se muestran los números de iteración, en el eje Y se muestra el valor del pid.

# Se calculan los mínimos y máximos de la variación del pid en todo e tramo y se les agrega un pequeño margen hacia abajo y hacia arriba

min_pid=df.valor_pid.min() 
min_pid_margen=min_pid-abs((min_pid*0.1))
max_pid=df.valor_pid.max()
max_pid_margen=max_pid+abs((max_pid*0.1))# (max_pid*0.1) agrega un 10%, (min_pid*0.1) restas un 10%
# print(min_pid,max_pid)


# Se calculan los mínimos y máximos de la variación del pid en la oscilación1 y se les agrega un pequeño margen hacia abajo y hacia arriba
min_oscilacion1_pid=df_oscilacion1.valor_pid.min()
min_oscilacion1_pid_margen=min_oscilacion1_pid-abs((min_oscilacion1_pid*0.1))
max_oscilacion1_pid=df_oscilacion1.valor_pid.max()
max_oscilacion1_pid_margen=max_oscilacion1_pid+abs((max_oscilacion1_pid*0.1))
# print(min_oscilacion,max_oscilacion,min_oscilacion_margen,max_oscilacion_margen)


# Se calculan los mínimos y máximos de la variación del pid en la oscilación1 y se les agrega un pequeño margen hacia abajo y hacia arriba
min_oscilacion2_pid=df_oscilacion2.valor_pid.min()
min_oscilacion2_pid_margen=min_oscilacion2_pid-abs((min_oscilacion2_pid*0.1))
max_oscilacion2_pid=df_oscilacion2.valor_pid.max()
max_oscilacion2_pid_margen=max_oscilacion2_pid+abs((max_oscilacion2_pid*0.1))



figPid, ax = plt.subplots(2,2) # 0,0  0,1  1,0  1,1

# Gráfico de datos iniciales.

ax[0,0].set_ylim(0,10) 
ax[0,0].set_xlim(0,10)

texto = "Iters:"+ str(iteraciones)
ax[0,0].text(1, 9, texto, fontsize=7)

texto = "nivel_inicial:"+ str(nivel_inicial)
ax[0,0].text(1, 8, texto, fontsize=7)

texto = "radio:"+ str(radio)
ax[0,0].text(1, 7, texto, fontsize=7)

texto = "altura:"+ str(altura)
ax[0,0].text(1, 6, texto, fontsize=7)

texto = "caudal_entrada:"+ str(caudal_entrada)
ax[0,0].text(1, 5, texto, fontsize=7)

texto = "setpoint:"+ str(setpoint)
ax[0,0].text(1, 4, texto, fontsize=7)

texto = "parametros:"+ str(parametros)
ax[0,0].text(1, 2, texto, fontsize=7)

texto = "min_pid:"+ str(min_pid)
ax[0,0].text(4, 9, texto, fontsize=7)

texto = "max_pid:"+ str(max_pid)
ax[0,0].text(4, 8, texto, fontsize=7)

ax[0,0].text(4, 7, txt_duracion, fontsize=7)

ax[0,0].set_title("Valores iniciales y constantes usados para la simulación.")

# Gráfico de tramo completo.
ax[0,1].plot(df.iter, df.valor_pid, linewidth=2.0)
ax[0,1].set_ylim(min_pid_margen,max_pid_margen)
ax[0,1].set_xlabel('Iteraciones')
ax[0,1].set_ylabel('Valor PID')
# ax[0,1].axhline(y=setpoint,linewidth=1, color='r')
ax[0,1].grid()
ax[0,1].set_title("Variación del valor pid en todo el tramo")

# Gráfico de la oscilación 1
y_increment3 = 0.5# divide el eje Y en unidades decimales pequeñas,se observa el valor max y min y se establece la división en el eje Y que se desea.
# Si el gráfico se ve muy saturado en el eje Y, debes aumentar, por ejemplo de 0.1 pasar a 0.5 o a 1, aumentar, y viceversa.
y_ticks = np.arange(min_oscilacion1_pid_margen,  max_oscilacion1_pid_margen, y_increment3) # para que se vean estos incrementos debes abrir toda la pantalla de la gráfica, muestras en eje y los valores desde 2 hasta 3 de 0.1
ax[1,0].set_yticks(y_ticks)# divide el eje Y en unidades decimalaes pequeñas
ax[1,0].plot(df_oscilacion1.iter, df_oscilacion1.valor_pid, linewidth=2.0)
ax[1,0].set_ylim(min_oscilacion1_pid_margen, max_oscilacion1_pid_margen)
ax[1,0].set_xlabel('Iteraciones')
ax[1,0].set_ylabel('Valores PID')
# ax[1,0].axhline(y=setpoint,linewidth=1, color='r')
ax[1,0].grid()
ax[1,0].set_title("Variación del valor pid en el tramo oscilación 1")

textstr3 = "Mín:"+ str(round(min_oscilacion1_pid,3))+" Máx:"+ str(round(max_oscilacion1_pid,3))
ax[1,0].text(0.6, 0.9, textstr3, transform = ax[1,0].transAxes, fontsize=10) # 

# Gráfico oscilación 2
y_increment4 =0.1 # se observa el valor max y min y se establece la división en el eje Y que se desea.
# Si el gráfico se ve muy saturado en el eje Y, debes aumentar, por ejemplo de 0.1 pasar a 0.5 o a 1, aumentar, y viceversa.
y_ticks2 = np.arange(min_oscilacion2_pid_margen,  max_oscilacion2_pid_margen, y_increment4) # divide el eje Y en unidades decimalaes pequeñas
ax[1,1].set_yticks(y_ticks2)# divide el eje Y en unidades decimalaes pequeñas
ax[1,1].plot(df_oscilacion2.iter, df_oscilacion2.valor_pid, linewidth=2.0)
ax[1,1].set_ylim(min_oscilacion2_pid_margen,  max_oscilacion2_pid_margen)
ax[1,1].set_xlabel('Iteraciones')
ax[1,1].set_ylabel('Valores PID')
ax[1,1].axhline(y=setpoint,linewidth=1, color='r')
ax[1,1].grid()
ax[1,1].set_title("Variación del valor pid en el tramo oscilación 2")

textstr3 = "Mín:"+ str(round(min_oscilacion2_pid,3))+" Máx:"+ str(round(max_oscilacion2_pid,3))
ax[1,1].text(0.6, 0.9, textstr3, transform = ax[1,1].transAxes, fontsize=10) # 


figPid.tight_layout() # esto separa las gráficas para que no se superpongan los labels 
# plt.show()

#-------------- Gráficos del valor caudal salida ------------------------------

# En el eje X se muestran los números de iteración, en el eje Y se muestra el valor del caudal de salida

# Se calculan los mínimos y máximos de la variación del caudal de salida en todo e tramo y se les agrega un pequeño margen hacia abajo y hacia arriba
min_caudal_salida=df.caudal_salida.min() 
min_caudal_salida_margen=min_caudal_salida-abs((min_caudal_salida*0.1))
max_caudal_salida=df.caudal_salida.max()
max_caudal_salida_margen=max_caudal_salida+abs((max_caudal_salida*0.1))# (max_pid*0.1) agrega un 10%, (min_pid*0.1) restas un 10%
# print(min_pid,max_pid)


# Se calculan los mínimos y máximos de la variación del caudal de salida en la oscilación1 y se les agrega un pequeño margen hacia abajo y hacia arriba
min_oscilacion1_caudal_salida=df_oscilacion1.caudal_salida.min()
min_oscilacion1_caudal_salida_margen=min_oscilacion1_caudal_salida-abs((min_oscilacion1_caudal_salida*0.1))
max_oscilacion1_caudal_salida=df_oscilacion1.caudal_salida.max()
max_oscilacion1_caudal_salida_margen=max_oscilacion1_caudal_salida+abs((max_oscilacion1_caudal_salida*0.1))



# Se calculan los mínimos y máximos de la variación del caudal de salida en la oscilación1 y se les agrega un pequeño margen hacia abajo y hacia arriba
min_oscilacion2_caudal_salida=df_oscilacion2.caudal_salida.min()
min_oscilacion2_caudal_salida_margen=min_oscilacion2_caudal_salida-abs((min_oscilacion2_caudal_salida*0.1))
max_oscilacion2_caudal_salida=df_oscilacion2.caudal_salida.max()
max_oscilacion2_caudal_salida_margen=max_oscilacion2_caudal_salida+abs((max_oscilacion2_caudal_salida*0.1))



figcaudal_salida, ax = plt.subplots(2,2) # 0,0  0,1  1,0  1,1

# Gráfico de datos iniciales.

ax[0,0].set_ylim(0,10) 
ax[0,0].set_xlim(0,10)

texto = "Iters:"+ str(iteraciones)
ax[0,0].text(1, 9, texto, fontsize=7)

texto = "nivel_inicial:"+ str(nivel_inicial)
ax[0,0].text(1, 8, texto, fontsize=7)

texto = "radio:"+ str(radio)
ax[0,0].text(1, 7, texto, fontsize=7)

texto = "altura:"+ str(altura)
ax[0,0].text(1, 6, texto, fontsize=7)

texto = "caudal_entrada:"+ str(caudal_entrada)
ax[0,0].text(1, 5, texto, fontsize=7)

texto = "setpoint:"+ str(setpoint)
ax[0,0].text(1, 4, texto, fontsize=7)

texto = "parametros:"+ str(parametros)
ax[0,0].text(1, 2, texto, fontsize=7)

texto = "min_pid:"+ str(min_pid)
ax[0,0].text(4, 9, texto, fontsize=7)

texto = "max_pid:"+ str(max_pid)
ax[0,0].text(4, 8, texto, fontsize=7)

ax[0,0].text(4, 7, txt_duracion, fontsize=7)

ax[0,0].set_title("Valores iniciales y constantes usados para la simulación.")

# Gráfico de tramo completo.
ax[0,1].plot(df.iter, df.caudal_salida, linewidth=2.0)
ax[0,1].set_ylim(min_caudal_salida_margen,max_caudal_salida_margen)
ax[0,1].set_xlabel('Iteraciones')
ax[0,1].set_ylabel('caudal_salida')

ax[0,1].grid()
ax[0,1].set_title("Variación del valor caudal_salida en todo el tramo")


# Gráfico de la oscilación 1
y_increment5 = (max_oscilacion1_caudal_salida-min_oscilacion1_caudal_salida) * 0.1# divide el eje Y en unidades decimalaes pequeñas
# lo de arriba e sun intento mejorable de calcular d eforma automática la mejor división en Y, pero hay que mejorar.
# se observa el valor max y min y se establece la división en el eje Y que se desea.
y_ticks = np.arange(min_oscilacion1_caudal_salida_margen,  max_oscilacion1_caudal_salida_margen, y_increment5) # para que se vean estos incrementos debes abrir toda la pantalla de la gráfica, muestras en eje y los valores desde 2 hasta 3 de 0.1
ax[1,0].set_yticks(y_ticks)# divide el eje Y en unidades decimalaes pequeñas
ax[1,0].plot(df_oscilacion1.iter, df_oscilacion1.caudal_salida, linewidth=2.0)
ax[1,0].set_ylim(min_oscilacion1_caudal_salida_margen, max_oscilacion1_caudal_salida_margen)
ax[1,0].set_xlabel('Iteraciones')
ax[1,0].set_ylabel('Valores caudal_salida')
ax[1,0].grid()
ax[1,0].set_title("Variación del valor caudal_salida en el tramo oscilación 1")

textstr3 = "Mín:"+ str(round(min_oscilacion1_caudal_salida,3))+" Máx:"+ str(round(max_oscilacion1_caudal_salida,3))
ax[1,0].text(0.4, 0.95, textstr3, transform = ax[1,0].transAxes, fontsize=10) # 


# Gráfico de la oscilación 2
y_increment6 = (max_oscilacion2_caudal_salida-min_oscilacion2_caudal_salida) * 20 #OJO, en este caso si se pone 0.1 la gráfica demora mucho en aparecer
# y genera miles de divisiones, hay que probar con diferentes, a medida que aparece más rápido la gráfica la división en Y es más correcta.
y_ticks6 = np.arange(min_oscilacion2_caudal_salida_margen,  max_oscilacion2_caudal_salida_margen, y_increment6) # para que se vean estos incrementos debes abrir toda la pantalla de la gráfica, muestras en eje y los valores desde 2 hasta 3 de 0.1
ax[1,1].set_yticks(y_ticks6)# divide el eje Y en unidades decimalaes pequeñas
ax[1,1].plot(df_oscilacion2.iter, df_oscilacion2.caudal_salida, linewidth=2.0)
ax[1,1].set_ylim(min_oscilacion2_caudal_salida_margen, max_oscilacion2_caudal_salida_margen)
ax[1,1].set_xlabel('Iteraciones')
ax[1,1].set_ylabel('Valores caudal_salida')
ax[1,1].grid()
ax[1,1].set_title("Variación del valor caudal_salida en el tramo oscilación 2")

textstr4 = "Mín:"+ str(round(min_oscilacion2_caudal_salida,3))+" Máx:"+ str(round(max_oscilacion2_caudal_salida,3))
ax[1,1].text(0.4, 0.95, textstr4, transform = ax[1,1].transAxes, fontsize=10) # 


figcaudal_salida.tight_layout()

#-------------- Gráficos del valor caudal neto ------------------------------

# En el eje X se muestran los números de iteración, en el eje Y se muestra el valor del caudal neto


# Se calculan los mínimos y máximos de la variación del caudal neto en todo e tramo y se les agrega un pequeño margen hacia abajo y hacia arriba
'''
Se aplica el absoluto o abs al calcular el margen para garantizar que reste o sume correctamente, por ejemplo, podemos tener los siguientes escenarios:
Si aplicamos el 10 (0.1) de margen que se agrega al máximo y 10(0.1) al mínimo:
Máximo 4  el 10% es 0.4  debería ser 4.4    Sin abs sale 4 + 0.4= 4.4  Al aplicar el abs al margen(0.4), o sea abs(0.4), el resultado es el mismo
Mínimo 2  el 10% es 0.2  debería ser 1.8    Sin abs sale 2 - 0.2= 1.8  Al aplicar el abs al margen(0.2), o sea abs(0.2), el resultado es el mismo

Máximo 4  el 10% es 0.4  debería ser 4.4    Sin abs sale 4 + 0.4= 4.4  Al aplicar el abs al margen(0.4), o sea abs(0.4), el resultado es el mismo
Minimo 0  el 10% es 0.0  debería ser 0.0    Sin abs sale 0 - 0.0= 0.0  Al aplicar el abs al margen(0.0), o sea abs(0.0), el resultado es el mismo

Máximo 4  el 10% es 0.4  debería ser 4.4    Sin abs sale 4 + 0.4= 4.4   Al aplicar el abs al margen(0.4), o sea abs(0.4), el resultado es el mismo
Mínimo -2 el 10% es -0.2  debería ser -2.2  Sin abs sale -2 - (-0.2)= -2+0.2=-1.8 error  Al aplicar el abs al margen(-0.2), o sea abs(-0.2), el resultado
es -2.2, es correcto.

Máximo 0  el 10% es 0.0  debería ser 0.0    Sin abs sale 0 + 0.0= 0.0  Al aplicar el abs al margen(0.0), o sea abs(0.0), el resultado es el mismo
Mínimo -2 el 10% es -0.2  debería ser -2.2  Sin abs sale -2 -(-0.2)= -2+0.2=-1.8 error Al aplicar el abs al margen(-0.2), o sea abs(-0.2), el resultado
es -2.2, es correcto.
Máximo -2 el 10% es -0.2  debería ser -1.8  Sin abs sale -2 +(-0.2)= -2+0.2=-1.8 Al aplicar el abs al margen(-0.2), o sea abs(-0.2), el resultado es el mismo
Mínimo -4 el 10% es 0.4  debería ser -4.4   Sin abs sale -4 -(-0.4)= -4.0+0.4=-3.6 error Al aplicar el abs al margen(-0.4), o sea abs(-0.4), el resultado
es --4.4, es correcto.
Lo de arriba muestra la necesidad de aplicar el absoluto. En el caso de valores 0 , no se aumenta o disminuye, es una decisión mejorable.

'''
min_caudal_neto=df.caudal_neto.min() 
min_caudal_neto_margen=min_caudal_neto-abs((min_caudal_neto*0.1))
max_caudal_neto=df.caudal_neto.max()
max_caudal_neto_margen=max_caudal_neto+abs((max_caudal_neto*0.1))# (max_pid*0.1) agrega un 10%, (min_pid*0.1) restas un 10%
# print(min_pid,max_pid)


# Se calculan los mínimos y máximos de la variación del caudal neto en la oscilación1 y se les agrega un pequeño margen hacia abajo y hacia arriba
min_oscilacion1_caudal_neto=df_oscilacion1.caudal_neto.min()
min_oscilacion1_caudal_neto_margen=min_oscilacion1_caudal_neto-abs((min_oscilacion1_caudal_neto*0.15))
max_oscilacion1_caudal_neto=df_oscilacion1.caudal_neto.max()
max_oscilacion1_caudal_neto_margen=max_oscilacion1_caudal_neto+abs((max_oscilacion1_caudal_neto*0.15))



# Se calculan los mínimos y máximos de la variación del caudal neto en la oscilación1 y se les agrega un pequeño margen hacia abajo y hacia arriba
min_oscilacion2_caudal_neto=df_oscilacion2.caudal_neto.min()
min_oscilacion2_caudal_neto_margen=min_oscilacion2_caudal_neto-abs((min_oscilacion2_caudal_neto*0.15))
max_oscilacion2_caudal_neto=df_oscilacion2.caudal_neto.max()
max_oscilacion2_caudal_neto_margen=max_oscilacion2_caudal_neto+abs((max_oscilacion2_caudal_neto*0.15))



figcaudal_neto, ax = plt.subplots(2,2) # 0,0  0,1  1,0  1,1

# Gráfico de datos iniciales.

ax[0,0].set_ylim(0,10) 
ax[0,0].set_xlim(0,10)

texto = "Iters:"+ str(iteraciones)
ax[0,0].text(1, 9, texto, fontsize=7)

texto = "nivel_inicial:"+ str(nivel_inicial)
ax[0,0].text(1, 8, texto, fontsize=7)

texto = "radio:"+ str(radio)
ax[0,0].text(1, 7, texto, fontsize=7)

texto = "altura:"+ str(altura)
ax[0,0].text(1, 6, texto, fontsize=7)

texto = "caudal_entrada:"+ str(caudal_entrada)
ax[0,0].text(1, 5, texto, fontsize=7)

texto = "setpoint:"+ str(setpoint)
ax[0,0].text(1, 4, texto, fontsize=7)

texto = "parametros:"+ str(parametros)
ax[0,0].text(1, 2, texto, fontsize=7)

texto = "min_pid:"+ str(min_pid)
ax[0,0].text(4, 9, texto, fontsize=7)

texto = "max_pid:"+ str(max_pid)
ax[0,0].text(4, 8, texto, fontsize=7)

ax[0,0].text(4, 7, txt_duracion, fontsize=7)

ax[0,0].set_title("Valores iniciales y constantes usados para la simulación.")

# Gráfico de tramo completo.
ax[0,1].plot(df.iter, df.caudal_neto, linewidth=2.0)
ax[0,1].set_ylim(min_caudal_neto_margen,max_caudal_neto_margen)
ax[0,1].set_xlabel('Iteraciones')
ax[0,1].set_ylabel('caudal_neto')

ax[0,1].grid()
ax[0,1].set_title("Variación del valor caudal_neto en todo el tramo")


# Gráfico de la oscilación 1
y_increment8 = (max_oscilacion1_caudal_neto-min_oscilacion1_caudal_neto) * 0.1# divide el eje Y en unidades decimalaes pequeñas
# lo de arriba e sun intento mejorable de calcular d eforma automática la mejor división en Y, pero hay que mejorar.
# se observa el valor max y min y se establece la división en el eje Y que se desea.
y_ticks8 = np.arange(min_oscilacion1_caudal_neto_margen,  max_oscilacion1_caudal_neto_margen, y_increment8) # para que se vean estos incrementos debes abrir toda la pantalla de la gráfica, muestras en eje y los valores desde 2 hasta 3 de 0.1
ax[1,0].set_yticks(y_ticks8)# divide el eje Y en unidades decimalaes pequeñas
ax[1,0].plot(df_oscilacion1.iter, df_oscilacion1.caudal_neto, linewidth=2.0)
ax[1,0].set_ylim(min_oscilacion1_caudal_neto_margen, max_oscilacion1_caudal_neto_margen)
ax[1,0].set_xlabel('Iteraciones')
ax[1,0].set_ylabel('Valores caudal_neto')
ax[1,0].grid()
ax[1,0].set_title("Variación del valor caudal_neto en el tramo oscilación 1")

textMinMaxNeto = "Mín:"+ str(round(min_oscilacion1_caudal_neto,3))+" Máx:"+ str(round(max_oscilacion1_caudal_neto,3))
ax[1,0].text(0.4, 0.95, textMinMaxNeto, transform = ax[1,0].transAxes, fontsize=10) # 


# Gráfico de la oscilación 2
y_increment9 = (max_oscilacion2_caudal_neto-min_oscilacion2_caudal_neto) * 0.1 #OJO, en este caso si se pone 0.1 la gráfica demora mucho en aparecer
# y genera miles de divisiones, hay que probar con diferentes, a medida que aparece más rápido la gráfica la división en Y es más correcta.
y_ticks9 = np.arange(min_oscilacion2_caudal_neto_margen,  max_oscilacion2_caudal_neto_margen, y_increment9) # para que se vean estos incrementos debes abrir toda la pantalla de la gráfica, muestras en eje y los valores desde 2 hasta 3 de 0.1
ax[1,1].set_yticks(y_ticks9)# divide el eje Y en unidades decimalaes pequeñas
ax[1,1].plot(df_oscilacion2.iter, df_oscilacion2.caudal_neto, linewidth=2.0)
ax[1,1].set_ylim(min_oscilacion2_caudal_neto_margen, max_oscilacion2_caudal_neto_margen)
ax[1,1].set_xlabel('Iteraciones')
ax[1,1].set_ylabel('Valores caudal_neto')
ax[1,1].grid()
ax[1,1].set_title("Variación del valor caudal_neto en el tramo oscilación 2")

textMinMaxNeto2 = "Mín:"+ str(round(min_oscilacion2_caudal_neto,3))+" Máx:"+ str(round(max_oscilacion2_caudal_neto,3))
ax[1,1].text(0.4, 0.95, textMinMaxNeto2, transform = ax[1,1].transAxes, fontsize=10) # 


figcaudal_neto.tight_layout()


# ---------------------Se activan las 4 ventanas-------------------------------
plt.show()









