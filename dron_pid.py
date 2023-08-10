from simple_pid import PID
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

'''
Dron v.1, 30 jul 2023
Autor: Damián Quijano A.
Versión funcionable. 

Se usa el módulo:simple-pid 2.0.0. Autor:Lundberg,M.(2023).simple-pid 2.0.0. Read the Docs.
Recuperado de: https://simple-pid.readthedocs.io/en/latest/index.html

https://simple-pid.readthedocs.io/en/latest/index.html
https://pypi.org/project/simple-pid/
https://simple-pid.readthedocs.io/en/latest/user_guide.html#user-guide
https://github.com/m-lundberg/simple-pid/blob/master/simple_pid/pid.py
http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/

Objetivos:
1. Entender el funcionamiento y lo que aporta kp,ki y kd por separado y cómo influyen en alcanzar el valor de referencia. Se hacen pruebas
uno a uno para estudiar los resultados.
2. Mostrar el método de buscar los valores de los parámetros kp, ki y kd para alcanzar el valor de referencia.

En resumen se trata de un dron que se quiere elevar hasta una altura de 50 metros y al llegar a dicha altura se mantenga flotando sin subir
ni bajar.
Para mantenerse flotando, debe mantener 100 rpm (revoluciones por minuto en las hélices), si aumenta el rpm  por encima de los 100
empieza a subir, si bajan los rpm por debajo de los 100,empieza a descender. Cada 50 rpm por encima de los 100rpm sube 1 metro
de altura, y al revés, si  por ejemplo el dron marca 50 rpm, cae un 1 metro por debajo de la altura en la que esté.
El motor del dron puede lograr que las hélices alcancen un máximo de 350 rpm. Por tanto, si está en el suelo, debe alcanzar un poco más de
100 rpm para empezar a elevarse.
No puede bajar más de 0 metros (altura negativa)  ni rpm negativos (excepto las diferencias o incrementos).
El pid manda su valor directamente como rpm, como si fuera el motor controlado por el piloto automático. Ese valor se resta a los 100 rpm
de flotación para luego calcular si se incrementa o decrementa la altura. Después de esto, el resultado de la nueva altura nuevamente se
manda al pid.

'''


# 
rpm_flotacion=100 # rpm en que puede quedar flotando, ni sube ni baja, se espera que cuando alcance los 50 metros quede flotando, no apagar el motor.
altura=0 #inicia con 0, está en tierra.
altura_referencia=50 # altura que se espera alcance y quede flotando.
aumenta_1metro= 50 # aumenta 1 metro por cada 50 rpm por encima de los rpm_flotacion, y al revés, disminuye 1 metro por cada 50 rpm por debajo de flotación
iteraciones=50
# El pid controla directamente el rpm del dron.
kp=50
ki=2
kd=0.01
pid = PID(kp, ki, kd, setpoint=altura_referencia)
# En caso solo el uso del proporcional Kp y los otros quedan 0 y 100 iteraciones, resultados para los siguiente kp: 10,15,20,25,30,35,40,45,50  .
# 30->46, 35->47, 50->entre 48 y 51(el mejor),
# 60-> entre 48 y 49 pero tiene saltos a 54. Si 10->39, por general debajo de 30 están por debajo de 46.
# En caso de kp=0,ki=0,kd=0 no hace nada.
# EN caso de Ki solo. Para valores 0.1->No pasa de 28 en altura  y el rpm queda en 27., o sea, se cae el dron. Para 0.5 , ara notar el efecto, subí
# a 500 iteraciones en vez de las 100 usuales para notar la diferencia, las primeras 100 iteraciones casi no se mueve, enpieza a moverse en adelante
# hasta alcanzar los 100 en altura y luego empieza a bajar hasta 0 (aterriza) y luego de nuevo empieza el ciclo lento de subir y luego bajar, quizás
# hay que dejarle más iteraciones hasta estabilizarse. Lo mismo para ki=1, y de alli en adelante manda valores extremadamente grandes y vuelve a 0.
# En el caso de Kd solo, para 100 iteraciones, y valor 10 no hace nada, todo en 0. No importa el valor que se asigne, siempre es 0.
# Al combinar Kp=50,Ki=0.1 y Kd=0.1 alcanza 48 , pero a diferencia de kp=50 solo, la curva se mantiene en el 48, casi no oscila, en cambio para el kp=50 solo
# oscila entre 48 y 51.
# En conclusión, el Kp es el que manda, y los otros dos K solo suavizan y ayudan a estabilizar más finamente, y sus valores son mucho más bajos que el Kp.
# Arriba usé límite mínimo de pid abierto o sea, None, pero lo corregí y puse 0, pues el rpm no puede ser ngativo, el valor
# Kp=50 y los otros en 0 y 500 iteraciones   y otras veces kp=50 y kd=.01estabiliza perfectamente en 48, exactamente en rpm=100, o sea,
#ni se mueve en el aire.
# Entonces , con iteraciones 500 y con kp=50 solo,oscila de forma estacionaria y regular alrededor de 48, por tanto el dron sube y baja
# suavemente alrdedor de la  altura 48, los máximos y mínimos no cambian,es una oscilación estable. Al agregar kd=0.01 se estabiliza el
# dron en la altura 48 , sin subir ni bajar , queda a 100 rpm exactos , flotando, pero mantiene un error estacionario(no cambia) de 2 metros.
# Queremos llegar a 50, por tanto agregamos ki=2 y aumentamos las iteraciones a 3000 para que el Ki tenga tiempo de ir subiendo al dron,
# el ki es lento, y así vaya subiendo poco a poco hasta llegar a 50 metros y a un rpm de 100.
'''
En resumen:
1. Probé primero con el Kp solo, lo fui subiendo desde 10 hasta 70 para comparar, hasta que encontré que con kp=50 ocurre una oscilación
regular estable en los 48, o sea, los mín y máx se repiten, no es una oscilación caótica y cambiante(pero es todavía oscilación), por tanto
tenemos al dron oscilando arriba y abajo en la altitud de 48 metros, por tanto no está fijo en 100 rpm. Por tanto mantiene un error no
estacionario (dado que varía).
2. Luego empecé con el Kd, empecé desde kd=0.01: tuve suerte, el dron quedó en línea sin oscilación en altura 48, el dron
dejó de oscilar y se mantiene fijo en la altura 48. Por tanto el kd ayudó a estabilizar , o sea, mantener 100 rpm, pero en una altura
que no es la 50, por tanto, el dron está estabilizado pero hay un error estacionario de 2 metros por debajo de 50, es error estacionario
porque es constante, no varía. No obstante, la misión de kd es evitar que el dron sobrepase la altura de referencia cuando se acerca
a ella, más adelante ayuda a controlar la ki.
3. Teniendo ya una altura estabilizada y fija sin oscilación(manteniendo kp=50 y kd=0.01) , agregué valores pequeños de Ki ddesde 0.01
en adelante , por ejemplo para 0.01 se puede observar que el dron va subiendo muy poquito a poquito pero de forma constante hacia 50,
por tanto aumenté más la ganancia para ki para que sea más rápida la subida (uniforme y constante), esto implicó aumentar las iteraciones
para que permita al dron alcanzar la altura 50 y verificar que ya no cambia dicha altura. Cada prueba es muy larga dado que el ki hace
las cosas poco a poco.Se puede ver que el dron no baja ni oscila durante su subida hacia 50 (poco a poco), sigue subiendo,en la mayoría de
las veces termina la simulación antes de alcanzar la altura 50, por tanto probé con mayores valores y extendí las iteraciones, hasta
alcanzar el ki=2 con 6000 iteraciones: el sistema se estabilizó perfectamente en 50, sin oscilación y a un rpm perfecto de 100 exactos.
Se puede intentar con un ki mayor a ver si alcanza los 50 estables en menos iteraciones. Hya que señalar que la kd también ayuda a la ki
al momento que esta se acerca a 50 para que no rebase esos 50, la kd coopera en dismunuir los rpm para estabilizar.

Por tanto, el kp ayuda a llegar rápido a las cercanías del valor de referencia pero a pesar de tomar horizontalidad queda en oscilación
regular no caotica, por tanto tendremos un rango de error variante. El kd permite estabilizar sin oscilación pero en la misma altura que
no es la buscada, el error es estacionario, y también coopera con ki para que no sobrepase el alor referencial.. Y el ki permite alcanzar
el valor referenciado pero en forma estabilizada sin oscilación.
Si hiciéramos el orden empezando por ki, demoraría muchísimo en alcanzar las cercanías del valor de referencia, el kp permite "disparar"
el objeto rápidamente, y de allí , y de forma estable, el ki aporta el movimiento pequeño y preciso hasta acoplarse al valor referenciado.

Un ejemplo parecido cuando una nave espacial se acopla a otra en el espacio. Dicha nave, al salir de la Tierra, va con toda la potencia(kp)
y su objetivo es alcanzar una distancia cercana a la otra nave en el espacio, al llegar a una distancia cercana a la otra nave, apaga los
motores potentes y solo usa impulsores pequeños para acercarse poco a poco a la otra nave con el fin de lograr un acopamiento suave (ki).
La kd a su vez son motores más pequeños de ajustes de dirección para que la nave no llegue a rebasar y pegar a la otra nave.
Los motores ki no sirven para lanzar la nave desde la Tierra, y los motores kp no sirven para aproximaciones lentas, suaves y precisas
para acoplar la nave a otra nave. Mientras que kd no son motores, son direccionales de cercanía o aproximación.
'''

minlimite=0 # tampoco existen rpm negativos, el mínimo es 0 cuando se apaga el motor.
maxlimite=350 # máximo rpm que puede alcanzar el dron, por tanro se configura el pid con ese valor para que refleje lo más real al proceso.
'''
Establecer un máximo en la salida del controlador PID es una forma válida de evitar el windup y controlar la salida dentro de los límites
del actuador. Esta técnica es conocida como "saturación de la salida" o "limitación de la salida" y es una forma efectiva de prevenir que
el controlador genere una señal de control que exceda la capacidad del actuador.
En el caso que mencionas, si la hélice de avión tiene un límite máximo de 3000 RPM, puedes configurar el controlador PID para que limite
la salida a 3000 RPM si el valor calculado es mayor. De esta manera, cuando el controlador está generando una señal de control que excede
los 3000 RPM, simplemente se establece la salida en 3000 RPM.

Limitar la salida del controlador a los límites del actuador tiene ventajas importantes:
1. Evita el windup: Al establecer un límite máximo en la salida del controlador, se evita que el integrador siga acumulando error más allá
de los límites del actuador, lo que previene el windup y oscilaciones indeseadas.
2. Protege el actuador: Al mantener la señal de control dentro de los límites del actuador, se protege el sistema físico de operar en
condiciones que puedan causar daños o problemas.
3. Mayor estabilidad: Al evitar que la señal de control se dispare más allá de los límites del actuador, se mantiene la estabilidad del
sistema y se asegura un comportamiento controlado y predecible.

Sin embargo, es importante tener en cuenta que la limitación de la salida puede tener como resultado que el controlador no alcance el
setpoint o referencia deseada si la tarea requiere una salida constante por encima de los límites del actuador. Es un compromiso entre
mantener la estabilidad y evitar daños al actuador versus la capacidad de alcanzar ciertos niveles de referencia. En algunos casos,
es necesario encontrar un equilibrio entre el rendimiento y la seguridad del sistema.

'''



pid.output_limits = (minlimite, maxlimite)
pid.sample_time = 0.01


def controlled_update(pid_control,altura):
    
    # se supone el pid calcula el error
    rpm=pid_control
    inc_rpm=rpm-rpm_flotacion # se necestia saber el incremeneto o disminución de rpm con respecto al rpm de flotacion que es 100rpm
    inc_dec_altura=inc_rpm/aumenta_1metro # se calcula el incremento o decremento en altura que genera el incremento o decremento de los rpm,diferencia
    nueva_altura=altura + inc_dec_altura # se calcula la altura en la que queda al restar o sumar la diferencia de altura a la altura anterior
    if nueva_altura <=0: # no puede haber una altura negativa , pero puede haber una diferencia de altura negativa que reste a la altura.
        nueva_altura=0
    return nueva_altura,rpm,inc_rpm
#Programa principal    
cont=0
registro_datos=[]
while cont<iteraciones:
    cont=cont+1
    antes=altura
    # Compute new output from the PID according to the systems current value
    pid_control = pid(altura)

    # Feed the PID output to the system and get its current value, rpm es el pid directamente
    altura,rpm,inc_rpm = controlled_update(pid_control,altura)
    print("Iter:",cont," Altura antes:",antes," pid:",pid_control," RPM:",rpm, "inc_rpm:",inc_rpm," Altura nueva:",altura)
    registro_datos.append([cont, altura,pid_control,rpm,inc_rpm])
    
# Los resultados muestran que alcanza , con Kp=30 altura de casi 47 metros, y los rpm casi en los 100rpm, lo cual muestra que el modelo es correcto,
# pues se deben cumplir ambas cosas, que alcance casi 50 metros y casi los 100 rpm , o sea, queda flotando. Lo que no debe ocurrir es que se estabilice
# en una altura y el rpm está por debajo o por encima de 100 rpm, pues se supone que por debajo o por encima cae o sube, pero no queda flotando manteniendo
# una altura.

# Algo importante es entender el proceso y sus límites y variables que afectan al activador. En este caso, al observar que el pid genera valores
# que sirven para controlar directamente los rpm sin agregar transformadores(factores de multiplicación, o resta, que encajen con los valores que el
# activador usualmente usa) entonces hay que asegurarse que el pid no arroje valores que el motor o el generador de rpm acepte, por tanto, al saber
# que el dron no supera los 350rpm, hay que asegurarse que el Kp o pid no sobrepase esa cifra, tampoco debería bajar de 0.

# Se hicieron pruebas con varios valores Kp (dejando los otros pids en 0)

df = pd.DataFrame( registro_datos,columns=['cont', 'altura' ,  'pid_control' , 'rpm', 'inc_rpm'])

# Data for plotting
t = np.linspace(0.0, cont,cont)

fig, ax = plt.subplots()
ax.plot(t,df.altura)
# Cinco últimos valores.
a1=str(round(df.altura.tail().iloc[0],2))
a2=str(round(df.altura.tail().iloc[1],2))
a3=str(round(df.altura.tail().iloc[2],2))
a4=str(round(df.altura.tail().iloc[3],2))
a5=str(round(df.altura.tail().iloc[4],2))

txtref="Alt ref:"+str(altura_referencia)+"ms"
txtiters="Iteraciones:"+str(cont)
txtKs="Kp:"+str(kp)+" Ki:"+str(ki)+" Kd:"+str(kd)

ax.text(0.8, 0.3, "Últimas 5 alturas", transform = ax.transAxes, fontsize=10)
ax.text(0.8, 0.25, a1, transform = ax.transAxes, fontsize=10)
ax.text(0.8, 0.20, a2, transform = ax.transAxes, fontsize=10)
ax.text(0.8, 0.15, a3, transform = ax.transAxes, fontsize=10)
ax.text(0.8, 0.10, a4, transform = ax.transAxes, fontsize=10)
ax.text(0.8, 0.05, a5, transform = ax.transAxes, fontsize=10)
ax.text(0.8, 0.98, txtref, transform = ax.transAxes, fontsize=10)
ax.text(0.8, 0.96, txtiters, transform = ax.transAxes, fontsize=10)
ax.text(0.8, 0.94, txtKs, transform = ax.transAxes, fontsize=10)

ax.set(xlabel='iteraciones', ylabel='Altura(m)',
title='Simulación Dron')
ax.axhline(y=altura_referencia,linewidth=1, color='r')
ax.grid()


plt.show()















