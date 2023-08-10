#from simple_pid import PID
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl

'''
Dron v.2, 6 ago 2023
Autor: Damián Quijano A.
Versión funcionable. 

Se usa el módulo:Fuzzy logic toolbox for Python, scikit-fuzzy 0.4.2 is a fuzzy logic toolbox for SciPy.
Autor: scikit-image team(2019).pythonhosted.
Recuperado de: https://pythonhosted.org/scikit-fuzzy/
https://pypi.org/project/scikit-fuzzy/
https://pythonhosted.org/scikit-fuzzy/
https://github.com/scikit-fuzzy/scikit-fuzzy
https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.membership.html

La instrucción  .terms.items permite ver las variables linguísticas asignadas por default cuando usas automf. ejemplo:
x.automf(3) #con la instrucción x.terms.items() verás los términos o variables linguísticas: poor,average,good. Se asignan 3 membresías.
y.automf(5) # con la instrucción y.terms.items() verás los términos o variables linguísticas:'poor', ,'mediocre', 'average','decent',
'good'. Se asignan 5 membresías
z.automf(7) # con la instrucción z.terms.items() verás los términos o variables linguísticas: 'dismal', 'poor','mediocre', 'average',
'decent', 'good','excellent'. Se asignan 7 membresías.
https://python.hotexamples.com/es/examples/skfuzzy.control.controlsystem/Antecedent/automf/python-antecedent-automf-method-examples.html 

Crisp: es el valor llamado nítido , o sea, no difuso. Es la manera de diferenciar los valores usuales, por ejemplo 4.5,8.9, etc de los
valores difusos que son parte de varias funciones. El crisp es el valor que esperamos genere el controlo difuso en su salida.

Objetivos:
1. Entender el funcionamiento del control lazo mediante lógica difusa.
2. Mostrar el método de tunear el control hasta encontrar los valors correctos.

En resumen se trata de un dron que se quiere elevar hasta una altura de 50 metros y al llegar a dicha altura se mantenga flotando sin subir
ni bajar.
Para mantenerse flotando, debe mantener 100 rpm (revoluciones por minuto en las hélices), si aumenta el rpm  por encima de los 100
empieza a subir, si bajan los rpm por debajo de los 100,empieza a descender. Cada 50 rpm por encima de los 100rpm sube 1 metro
de altura por segundo, y al revés, si  por ejemplo el dron marca 50 rpm, cae un 1 metro por debajo de la altura en la que esté.
El motor del dron puede lograr que las hélices alcancen un máximo de 350 rpm. Por tanto, si está en el suelo, debe alcanzar un poco más de
100 rpm para empezar a elevarse.
Establecemos lo siguiente(por experimento, especificaciones o de nuestra fantasía):
1 rpm(revoluciones por minuto)de la hélice incrementa 0.02 metros/segundo, o sea, 1 rpm eleva al dron en un segundo: 0.02 metros.
Por tanto, 50 rpm elevan al dron : 50*0.02= 1 metro por segundo, por tanto, en 6 segundos, a 50rpm, se eleva 6 metros a partir de la
altura en la que esté.
Ahora bien, se establece que necesita 100 rpm para flotar, y por encima de los 100 rpm empieza a elevarse, por tanto:
101rpm se eleva : 101-100= 1rpm --> 1rpm*0.02= 0.02 metros por segundo, en 60 segundos (a 1 rpm) sube 1.2 metros a partir de la altura
en que esté.
350rpm se eleva: 350-100=250 rpm--> 250 (no 350) * 0.02= 5 metros, o sea, se eleva 5 metros en un segundo, si pasan 10 segundos, alcanza
los 50 metros a partir de la altura en la que esté.
En cambio, si son menos de 100 rpm, desciende:
60 rpm desciende: 60-100=-40rpm--> -40rpm*0.02=0.8 metros por segundo, en 5 segundos desciende 4 metros a partir de la altura en la que esté.
Por supuesto, si la altura alcanza 0, no se permite disminuir más.
Fórmula: dada una rpm , 1rpm -> 0.02m/s incremento en altura y x segundos de subida (por general 1 segundo)
altura= altura actual+ [((rpm-100)*0.02) * segundos].
El segundo es asumiendo que el control difuso se actualiza del sensor cada 1 segundo, y por tanto, sube o baa cada segundo.

No puede bajar más de 0 metros (altura negativa), va de 0 a 100 metros, ni rpm negativos( va de 10rpm a 350rpm), en cambio los
incrementos de altura e incrementos de rpm pueden ser negativos.

El control fuzzy manda su valor directamente como rpm, como si fuera el motor controlado por el piloto automático. Ese valor se resta a los 100 rpm
de flotación para luego calcular si se incrementa o decrementa la altura. Después de esto, el resultado de la nueva altura nuevamente se
manda al control fyzzy


Consideraciones:
Conocer los Tramos de crecimiento usual del controlador, esto se aprecia en la curva de la varialble de proceso:
Tramo crecimiento: arranca el proceso hasta alcanzar por primera vez la altura de referencia o setpoint. Solo se aplican mínimo de variable de proceso,
por ejemplo altura 0.
Tramo de oscilación caótica: ocurre a partir de llegar por primera vez al setpoint, de allí en adelante ocurren máximos y mínimos de cada
ciclo , esto no son iguales a los siguientes ciclos. Se establece un máximo de la variable de proceso para que no sean excesivas las oscilaciones
dado que pueden provocar daños. Por ejemplo, un máximo es 70 de altura, pues en adelante pierde sustento, no obstante hay procesos que
la fuerza de su acción no es suficiente para que rebase un máximo, tiene un freno natural.
Tramo de oscilación periódica: los mínimos y máximos de esta oscilación se repiten o van en disminución suave.
Tramo estabilización: deja de existir oscilación y se estabiliza el proceso en un setpoint.

Variable del proceso(entrada): altura. Es la que se desea controlar mediante la variable del actuador.
Altura de referencia: 50 metros
Máximo variable de proceso: 25% de altura de referencia= 12.5 metros , redondea a 12 metros. Por tanto máximo= 72 metros. Esto puede
implicar otro dispositivo, además del actuador, para frenar el crecimiento y que se activa al superar el 25%.
Mínimo variable de proceso: 0 metros, puede ser en %, depende del proceso. El dron no puede descender a altura negativas.

Variable del actuador (salida):variable que controla la variable del proceso, en este caso la variable rpm(es el motor).Al aumentar o
disminuir el rpm  afecta al crecimiento o disminución de la altura(variable de proceso).
Constante de referencia de actuador: no en todos los procesos aplica, en este caso se refiere al rpm que mantiene a flote al dron, ni sube
ni baja y es de 100 rpm. Lo ideal es que cuando el dron alcance los 50 metros de altura se estabilice flotando a 100 rpm,los dos indicadores
en esos valores nos indica que alcanzamos el tamo de estabilización buscado.
Mínimo rpm: 10 rpm. , de lo contrario está apagado. El dron en tierra tiene las hélices rotando pero sin despegar.
Máximo rpm: 350 rpm, lo cual representa 5 metros por segundo hacia arriba, el motor no puede dar más.
Para inciar el ascenso desde tierra, debe superar los 100 rpm.

Fórmula del proceso: al subir o bajar el rpm, se calcula el incremento o decremento de rpm con respecto a 100rpm, ese incremento se traduce
en el incremento o decremento de la altura, y el resultado se suma a la altura existente.
Dado un rpm :
incremento o decremento (si es negativo) de  rpm= rpm-100
incremento o decremento (si es negativo) de altura=incremeneto de  rpm * 0.5
altura=altura+incremento de altura
O bien: altura=altura+((rpm-100)*0.5)
Condición:
Si altura <=0 entonces altura=0, esto último es una condición de límite, que en la realidad física no ocurrirá, pero hay que tenerla en
cuanta en la simulación y al momento de establecer los límites de las funciones de membresía.

Se puede observar lo necesario de conocer los indicadores, variables, constantes y condiciones del proceso , esto permite entonces
ajustar los valores de las variables de fuzzy, sus intervalos y las reglas.

Nos faltan tres variables más si tenes esp32:
-Variable del sensor: entrada análoga al esp32. EL sensor mide la altura y la convierte en señal análoga eléctrica y es recibida por el
esp32 y la convierte al valor de una altura, luego compara con el valor de altura de referencia, calcula el error, y esa es la entrada
al componente fuzzy.
-Variable del esp32: salida PWM. La salida del componente fuzzy es un valor que se considera el rpm, se convierte en señal digital
PWM, la cual sale del esp32 y va al actuador, este actuador tiene interfase de recibir la señala PWM y la convierte en el voltaje
que va al componente del motor que aumenta o disminuye el rpm.
-Variable temporal: este es el delay que se agrega después de cada vuelta o iteración en espera de recibir la señal del sensor.
Puede ocurrir que el valor sea de 1 segundo,por tanto, espera 1 segundo antes de aceptar la lectura del sensor(el cual puede estar
haciéndolo mucho más rápido), esto ocurre dentro del while. Puede ocurrir que cada cierto tiempo o al recibir una señal, el delay
se aumente, y luego vuelve al delay usual.


Ajustes al fuzzy:
-Se ajusta la cantidad de variables de entrada: por ejemplo error y su derivada. En este caso fue suficiente solo con la variable error, o sea, una entrada.
-Se ajustan la cantidad(3,5,7) y tipo de funciones(trim,trap,etc) de membresía de cada variable de entrada y salida. Esto se refiere a la
cantidad de variables linguísticas por cada variable de entrada o salida.Por ejemplo , para variable error, por ejemplo: Error Grande Negativo(EGN),
Error Negativo(EN), Error Z(EZ) se refiere el intervalo que incorpora el valor 0 de error y cuya probabilidad dentro de la función es 1, Error Positivo(EP) y
Error Grande Positivo(EGP) y de forma similar para el resto de las variables.
-Ajustar el intervalo de valores para cada variable de entrada y salida.Por ejemplo de 0 a 50, o de -50 a 50, etc...
-Ajustar los intervalos de valores para cada función de membresía de cada variable de entrada y salida. Por ejemplo, los valores de un
triángulo que pretende capturar los valores de EGN, y ver si la salida es la esperada.
-Ajustar las fórmulas de transformación,ver sus factores de multiplicación.
Por ejemplo conversión de PWM a Voltajes
DE Voltajes a RPM
De rpm a alura,etc...
-Ajustar las relaciones o reglas, quitar, poner, etc.

El ajuste implica ir ajustando los diferentes valores, tipos,fórmula del prceoso, etc a medida que se esperan que ocurran unos valores previamente conocidos.
Si esperamos que para la altura -50 el rpm la salida sea de  350rpm, y resulta que es de 250rpm , hay que ajustar el trapecio o el triángulo
para ese intervalo de valores (Mucho error negativo).

'''


'''

Vamos a crear un sistema de control difuso que modele la elevación o descenso de un dron que intenta alcanzar una altura de 50 metros
y mantenerse flotando en dicha altura, inicia el ascenso en vertical y desde tierra. 
El control podríamos estructurarlo como tal:

Antecedentes (Entradas)
 error
   
Consecuencias (Salidas)
 rpm
   

Reglas
    

Uso
 

'''

#-----------------Configuración de valores inciales y constantes--------------------
rpm_flotacion=100 # rpm en que puede quedar flotando, ni sube ni baja, se espera que cuando alcance los 50 metros quede flotando, no apagar el motor.
altura=0 #inicia con 0, está en tierra.
altura_referencia=50 # altura que se espera alcance y quede flotando.
aumenta_1metro= 0.02 # es como dividir 1/50, aumenta 1 metro por cada 50 rpm por encima de los rpm_flotacion, y al revés, disminuye
#1 metro por cada 50 rpm por debajo de flotación.
iteraciones=100

minlimite=0 # tampoco existen rpm negativos, el mínimo es 0 cuando se apaga el motor.
maxlimite=350 # máximo rpm que puede alcanzar el dron, por tanro se configura el pid con ese valor para que refleje lo más real al proceso.


# ------------ Creación y configuración del control Fuzzy---------------------------------

# Antecedentes son las entradas, consecuentes son las salidas.
# A continuación establecemos las variables de entrada y salida y su conjunto universo
v_error = ctrl.Antecedent(np.arange(-50, 50, 1), 'v_error') # incluye valores enteros desde -50 hasta 50 de 1 en 1.
v_rpm = ctrl.Consequent(np.arange(10, 350, 1), 'v_rpm') ## genera valores enteros desde 10 hasta 350 de 1 en 1

# Asignación de variables liguísticas y sus funciones de membresía para cada variable.
v_error['EGN'] = fuzz.trapmf(v_error.universe, [-50, -50,-36, -24]) # Errror grande negativo, está muy por debajo de 50 metros
v_error['EN'] = fuzz.trimf(v_error.universe, [-36, -12, 0]) # Error mediano negativo, está algo por debajo de 50 metros

v_error['EZ'] = fuzz.trimf(v_error.universe, [-12, 0, 12]) # Error cero, está cerca o igual a 50 metros

v_error['EP'] = fuzz.trimf(v_error.universe, [0, 24, 36]) # Error pequeño positivo, está algo por encima de 50 metros
v_error['EGP'] = fuzz.trapmf(v_error.universe, [24, 36, 50,50]) # Error grande positivo,, está muy por encima de 50 metros**


v_rpm['GD'] = fuzz.trapmf(v_rpm.universe, [10,10, 25, 50]) # gran descenso
v_rpm['PD'] = fuzz.trimf(v_rpm.universe, [25, 50, 100]) # poco descenso

v_rpm['E'] = fuzz.trimf(v_rpm.universe, [50, 100, 150]) # equlibrado

v_rpm['PA'] = fuzz.trimf(v_rpm.universe, [100, 150, 300]) # poco ascenso
v_rpm['GA'] = fuzz.trapmf(v_rpm.universe, [150, 300, 350,350]) #  gran ascenso



#v_error.view(), si lo haces por consola escribe v_error.view(),plt.show()
#v_rpm.view(),plt.show()

# A continuación se construyen las relaciones
rule1 = ctrl.Rule(v_error['EGN'] , v_rpm['GA'])
rule2 = ctrl.Rule(v_error['EN'], v_rpm['PA'])

rule3 = ctrl.Rule(v_error['EZ'], v_rpm['E'])

rule4 = ctrl.Rule(v_error['EP'] , v_rpm['PD'])
rule5 = ctrl.Rule(v_error['EGP'] , v_rpm['GD'])



fuzzy_control = ctrl.ControlSystem([rule1, rule2, rule3,rule4,rule5])
dron_control = ctrl.ControlSystemSimulation(fuzzy_control)


#-----------Función del proceso-----------------

# Función que simula el proceso dron , recibe los rpm producto de la acción del control fuzzy, ajusta  la altura y devuelve la nueva altura
def controlled_update(rpm_fuz,altura,rpm_flot):
    # altura es la altura anterior al update, rpm_fuz valor que computa el fuzzy , rpm_float es de flotación=100 rpm, referencia es la
    # altura 50 que se busca
     
    inc_rpm=rpm_fuz-rpm_flot # se necestia saber el incremento o disminución de rpm con respecto al rpm de flotacion que es 100rpm
    inc_dec_altura=inc_rpm*0.02 # se calcula el incremento o decremento en altura que genera el incremento o decremento de los rpm,
   
    nueva_altura=altura + inc_dec_altura # se calcula la altura en la que queda al restar o sumar la diferencia de altura a la altura anterior
    if nueva_altura <=0: # no puede haber una altura negativa , pero puede haber una diferencia de altura negativa que reste a la altura.
        nueva_altura=0
    return nueva_altura

#---------------Programa principal----------------------------
cont=1
registro_datos=[]
registro_datos.append([cont,10,0])# valores al arrancar el motor el dron.10 rpm y altura=0
print("Iter Inicial:",cont," Altura antes:",0," RPM_fuzzy:",10,"Altura nueva:",0)
while cont<iteraciones:
    cont=cont+1
    antes=altura # altura anterior (actual, antes de fuzzy)
    # Compute error
    error=altura-altura_referencia # aquí altura sigue siendo la anterior, la nueva se calcula en controlled_update
    print("Error:",error)

    dron_control.input['v_error'] = error
    dron_control.compute()
    rpm_fuzzy=dron_control.output['v_rpm']
    #print(rpm_fuzzy,altura,rpm_flotacion)
    
    # Feed the PID output to the system and get its current value, rpm es el pid directamente
    altura = controlled_update(rpm_fuzzy,altura,rpm_flotacion) # aquí altura sigue siendo la anterior, la nueva se calcula en controlled_update
    print("Iter:",cont," Altura antes:",antes," RPM_fuzzy:",rpm_fuzzy,"Altura nueva:",altura)
    registro_datos.append([cont,rpm_fuzzy,altura]) # se registran los datos para su posterior graficación
    
# Los resultados muestran que alcanza el objetivo, con   , y los rpm casi en los 100rpm, lo cual muestra que el modelo es correcto,
# pues se deben cumplir ambas cosas, que alcance casi 50 metros y casi los 100 rpm , o sea, queda flotando. Lo que no debe ocurrir es que se
# estabilice en una altura y el rpm está por debajo o por encima de 100 rpm, pues se supone que por debajo o por encima cae o sube, pero no
# queda flotando manteniendo una altura.

#--------- Graficación -----------------------

df = pd.DataFrame( registro_datos,columns=['cont', 'rpm','altura'])

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
#txt_dronControl="Dron_control:"+str(dron_control)

ax.text(0.8, 0.3, "Últimas 5 alturas", transform = ax.transAxes, fontsize=10)
ax.text(0.8, 0.25, a1, transform = ax.transAxes, fontsize=10)
ax.text(0.8, 0.20, a2, transform = ax.transAxes, fontsize=10)
ax.text(0.8, 0.15, a3, transform = ax.transAxes, fontsize=10)
ax.text(0.8, 0.10, a4, transform = ax.transAxes, fontsize=10)
ax.text(0.8, 0.05, a5, transform = ax.transAxes, fontsize=10)
ax.text(0.8, 0.98, txtref, transform = ax.transAxes, fontsize=10)
ax.text(0.8, 0.96, txtiters, transform = ax.transAxes, fontsize=10)
#ax.text(0.8, 0.94, txt_dronControl, transform = ax.transAxes, fontsize=10)

ax.set_ylim(0, 60)
ax.set(xlabel='iteraciones', ylabel='Altura(m)',
title='Simulación Dron')
ax.axhline(y=altura_referencia,linewidth=1, color='r')
ax.grid()


plt.show()


'''
ValueError: Crisp output cannot be calculated, likely because the system is too sparse. Check to make sure this set of input
values will activate at least one connected Term in each Antecedent via the current set of Rules.
Esto es porque al introducir el input -50 es también el límite izquierdo de la membresía, debes agrandar el intervalo de la membresía,
por ejemplo a -100 sabiendo que durante el lazo de control no recibirá errores menores a -50.
'''














