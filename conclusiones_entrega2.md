En este caso, para resolver la entrega por IA lo hicimos con Claude y pudimos observar algunos puntos diferentes en comparación a nuestro desarrollo.

Como diferencia más importante o notoria, vimos que la IA realizó una reducción de dominios previa a la ejecución del backtracking, filtrando para las esclusas solo las ubicaciones del borde, para las habitaciones solo las ubicaciones del interior, y excluyendo de cada variable las ubicaciones marcadas como cráteres.

Estos tres puntos en nuestro desarrollo fueron establecidos como restricciones explícitas dentro del CSP. A cambio de eso, aplicamos las heurísticas MRV y LCV, priorizando variables con menos valores disponibles y descartando valores que limiten en mayor medida las opciones de las variables restantes.

Por último, otra diferencia notable es la de sintaxis, ya que el código generado por la IA es más específico y en varios casos más sintetizado.