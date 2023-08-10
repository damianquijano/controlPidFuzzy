# controlPidFuzzy
Programas simuladores en los que se aplican controles PID y Fuzzy  
Los programas dron_pid y dron_fuzzy v2 son iguales pero se aplican técnicas de control de lazo diferentes, el primero usa el control PID y el segundo la lógica borrosa o Fuzzy.  
Luego tenemos los programas tanque_pid v2 y tanque_fuzzy v1 , simuladores más complejos , uno funciona con el control PID y el otro con el control Fuzzy. Ambos programas guardan los resultados de su corrida en dos archivos csv cada uno, que luego deben ser abiertos en los programas analisis v2 para el caso de tanque_pid v2 y analisis_tanque_fuzzy v1 para el caso tanque_fuzzy v1 .  
El objetivo es mostrar la forma de reemplazar un control por otro dentro del cuerpo del simulador conservando los mismos parámetros y cuerpo de programación.  
Desarrollado con el lenguaje python, editor Tony.  
