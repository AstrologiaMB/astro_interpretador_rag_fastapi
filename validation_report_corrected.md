# Validación de Títulos vs Datos JSON Ejemplo (Corregida v2)

Esta tabla compara los títulos requeridos en la versión más reciente de `Títulos Numerados tropico.md` con los datos encontrados en `data/carta_natal_tropical_Maria_Blaquier_Buenos_Aires_3-11-1967.json`. La lógica para evaluar aspectos compuestos ha sido corregida.

*   **OK:** El dato correspondiente a este título se encontró o calculó a partir del JSON. Para títulos de aspectos compuestos (ej: conjunción o cuadratura), 'OK' significa que **al menos uno** de los aspectos específicos fue encontrado.
*   **NO OK:** El dato correspondiente a este título NO se encontró o calculó a partir del JSON. Para títulos de aspectos compuestos, 'NO OK' significa que **ninguno** de los aspectos específicos fue encontrado.
*   **REQUIERE LÓGICA ADICIONAL:** Este título implica condiciones complejas (marcadas con 'y' o descripciones) o cálculos (como planetas en el Ascendente) que el script actual no realiza.

```markdown
| Título Requerido (Títulos Numerados tropico.md - Actualizado) | Estado (Basado en JSON Ejemplo) |
|---|---|
| Sol en Aries (0° a 29° 59’) | NO OK |
| Sol en Tauro (30° a 59°59’) | NO OK |
| Sol en Géminis (60° a 89°59’) | NO OK |
| Sol en Cáncer (90° a 119°59’) | NO OK |
| Sol en Leo (120° a 149°59’) | NO OK |
| Sol en Virgo (150° a 179°59’) | NO OK |
| Sol en Libra (180° a 209°59’) | NO OK |
| Sol en Escorpio (210° a 239°59’) | OK |
| Sol en Sagitario (240° a 269°59’) | NO OK |
| Sol en Capricornio (270° a 299°59’) | NO OK |
| Sol en Acuario (300° a 329°59’) | NO OK |
| Sol en Piscis (330° a 359°59’) | NO OK |
| Sol en Casa 1 | NO OK |
| Sol en Casa 2 | NO OK |
| Sol en Casa 3 | NO OK |
| Sol en Casa 4 | NO OK |
| Sol en Casa 5 | NO OK |
| Sol en Casa 6 | NO OK |
| Sol en Casa 7 | NO OK |
| Sol en Casa 8 | NO OK |
| Sol en Casa 9 | OK |
| Sol en Casa 10 | NO OK |
| Sol en Casa 11 | NO OK |
| Sol en Casa 12 | NO OK |
| Aspecto Sol sextil a Venus | NO OK |
| Aspecto Sol conjunción a Venus | NO OK |
| Aspecto Sol conjunción a Marte | NO OK |
| Aspecto Sol sextil a Marte | OK |
| Aspecto Sol trígono a Marte | NO OK |
| Aspecto Sol trígono a Júpiter | NO OK |
| Aspecto Sol sextil a Júpiter | NO OK |
| Aspecto Sol cuadratura u oposición a Júpiter | NO OK |
| Aspecto Sol en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en casa 1, 4, 7 o 10. | REQUIERE LÓGICA ADICIONAL |
| Aspecto Sol en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en conjunción al Sol, la Luna, Mercurio, Venus o Marte. | REQUIERE LÓGICA ADICIONAL |
| Aspecto Sol en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en cuadratura al Sol, la Luna, Mercurio, Venus o Marte. | REQUIERE LÓGICA ADICIONAL |
| Aspecto Sol en conjunción, cuadratura u oposición a Júpiter y hay conjunción, cuadratura u oposición entre Saturno y Plutón. | REQUIERE LÓGICA ADICIONAL |
| Aspecto Sol sextil o trígono a Saturno | NO OK |
| Aspecto Sol conjunción o cuadratura u oposición a Saturno | NO OK |
| Aspecto Sol conjunción o cuadratura u oposición a Urano | NO OK |
| Aspecto Sol sextil o trígono a Urano | NO OK |
| Aspecto Sol conjunción o cuadratura u oposición a Neptuno | NO OK |
| Aspecto Sol conjunción o cuadratura u oposición a Plutón | NO OK |
| Luna en Aries (0° a 29° 59’) | NO OK |
| Luna en Tauro (30° a 59° 59’) | NO OK |
| Luna en Géminis (60° a 89° 59’) | NO OK |
| Luna en Cáncer (90° a 119° 59’) | NO OK |
| Luna en Leo (120° a 149° 59’) | NO OK |
| Luna en Virgo (149° a 179° 59’) | NO OK |
| Luna en Libra (180° a 209° 59’) | NO OK |
| Luna en Escorpio (210° a 239° 59’) | NO OK |
| Luna en Sagitario (240° a 269° 59’) | OK |
| Luna en Capricornio (270° a 299° 59’) | NO OK |
| Luna en Acuario (300° a 329° 59’) | NO OK |
| Luna en Piscis (330° a 359° 59’) | NO OK |
| Luna en casa 1 | NO OK |
| Luna en casa 2 | NO OK |
| Luna en casa 3 | NO OK |
| Luna en casa 4 | NO OK |
| Luna en casa 5 | NO OK |
| Luna en casa 6 | NO OK |
| Luna en casa 7 | NO OK |
| Luna en casa 8 | NO OK |
| Luna en casa 9 | OK |
| Luna en casa 10 | NO OK |
| Luna en casa 11 | NO OK |
| Luna en casa 12 | NO OK |
| Aspecto Luna conjunción a Mercurio | NO OK |
| Aspecto Luna sextil o trígono a Mercurio | NO OK |
| Aspecto Luna cuadratura u oposición a Mercurio | NO OK |
| Aspecto Luna conjunción a Venus | NO OK |
| Aspecto Luna conjunción a Marte | NO OK |
| Aspecto Luna cuadratura u oposición a Marte | NO OK |
| Aspecto Luna sextil o trígono a Marte | NO OK |
| Aspecto Luna conjunción o sextil o trígono a Júpiter | NO OK |
| Aspecto Luna cuadratura u oposición a Júpiter | OK |
| Aspecto Luna en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en casa 1, 4, 7 o 10. | REQUIERE LÓGICA ADICIONAL |
| Aspecto Luna en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en conjunción al Sol, la Luna, Mercurio, Venus o Marte. | REQUIERE LÓGICA ADICIONAL |
| Aspecto Luna en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en cuadratura al Sol, la Luna, Mercurio, Venus o Marte. | REQUIERE LÓGICA ADICIONAL |
| Aspecto Luna en conjunción, cuadratura u oposición a Júpiter y hay conjunción, cuadratura u oposición entre Saturno y Plutón. | REQUIERE LÓGICA ADICIONAL |
| Aspecto Luna conjunción, cuadratura u oposición Saturno | NO OK |
| Aspecto Luna sextil o trígono a Saturno | OK |
| Aspecto Luna conjunción o cuadratura u oposición a Urano | OK |
| Aspecto Luna en conjunción, cuadratura u oposición a Urano y Saturno está en casa 1, 4, 7 o 10. | REQUIERE LÓGICA ADICIONAL |
| Aspecto Luna en conjunción, cuadratura u oposición a Urano y Saturno está en conjunción al Sol, la Luna, Mercurio, Venus o Marte. | REQUIERE LÓGICA ADICIONAL |
| Aspecto Luna en conjunción, cuadratura u oposición a Urano y Saturno está en cuadratura al Sol, la Luna, Mercurio, Venus o Marte. | REQUIERE LÓGICA ADICIONAL |
| Aspecto Luna conjunción, cuadratura u oposición a Neptuno | OK |
| Aspecto Luna conjunción o cuadratura u oposición a Plutón | NO OK |
| Nodo en Aries (0° a 29° 59’) | OK |
| Nodo en Tauro (30° a 59° 59’) | NO OK |
| Nodo en Géminis (60° a 59° 59’) | NO OK |
| Nodo en Cáncer (90° a 119° 59’) | NO OK |
| Nodo en Leo (120° a 149° 59’) | NO OK |
| Nodo en Virgo (150° a 179° 59’) | NO OK |
| Nodo en Libra (180° a 209° 59’) | NO OK |
| Nodo en Escorpio (210° a 239° 59’) | NO OK |
| Nodo en Sagitario (240° a 269° 59’) | NO OK |
| Nodo en Capricornio (270° a 309° 59’) | NO OK |
| Nodo en Acuario (300° a 329° 59’) | NO OK |
| Nodo en Piscis (330° a 359° 59’) | NO OK |
| Nodo en casa 1 | NO OK |
| Nodo en casa 7 | NO OK |
| Nodo en casa  2 | OK |
| Nodo en casa 8 | NO OK |
| Nodo en casa 3 | NO OK |
| Nodo en casa 9 | NO OK |
| Nodo en casa 4 | NO OK |
| Nodo en casa 10 | NO OK |
| Nodo en casa 5 | NO OK |
| Nodo en casa 11 | NO OK |
| Nodo en casa 6 | NO OK |
| Nodo en casa 12 | NO OK |
| Ascendente en Aries (0° a 29° 59’) | NO OK |
| Ascendente en Tauro (30° a 59° 59’) | NO OK |
| Ascendente en Tauro y Marte está en casa 1, 4, 7 o 10. | REQUIERE LÓGICA ADICIONAL |
| Ascendente en Tauro y Marte está en conjunción al Sol o la Luna. | REQUIERE LÓGICA ADICIONAL |
| Ascendente en Géminis (60° a 89° 59’) | NO OK |
| Ascendente en Cáncer (90° a 119° 59’) | NO OK |
| Ascendente en Leo (120° a 149° 59’) | NO OK |
| Ascendente en Virgo (150° a 179° 59’) | NO OK |
| Ascendente en Libra (180° a 209° 59’) | NO OK |
| Ascendente en Escorpio (210° a 239° 59’) | NO OK |
| Ascendente en Sagitario (240° a 269° 59’) | NO OK |
| Ascendente en Capricornio (270° a 299° 59’) | NO OK |
| Ascendente en Acuario (300° a 329° 59’) | NO OK |
| Ascendente en Piscis (330° a 359° 59’) | OK |
| Luna en el ascendente | REQUIERE LÓGICA ADICIONAL |
| Mercurio en el ascendente | REQUIERE LÓGICA ADICIONAL |
| Venus en el ascendente | REQUIERE LÓGICA ADICIONAL |
| Marte en el ascendente | REQUIERE LÓGICA ADICIONAL |
| Júpiter en el ascendente | REQUIERE LÓGICA ADICIONAL |
| Saturno en el ascendente | REQUIERE LÓGICA ADICIONAL |
| Urano en el ascendente | REQUIERE LÓGICA ADICIONAL |
| Neptuno en el ascendente | REQUIERE LÓGICA ADICIONAL |
| Plutón en el ascendente | REQUIERE LÓGICA ADICIONAL |
| MERCURIO RETRÓGRADO | OK |
| Mercurio en Aries (0° a 29° 59’) | NO OK |
| Mercurio en Tauro (30° a 59° 59’) | NO OK |
| Mercurio en Géminis (60° a 89° 59’) | NO OK |
| Mercurio en Cáncer (90° a 109° 59’) | NO OK |
| Mercurio en Leo (120° a 149° 59’) | NO OK |
| Mercurio en Virgo (150° a 179° 59’) | NO OK |
| Mercurio en Libra (180° a 209° 59’) | NO OK |
| Mercurio en Escorpio (210° a 239° 59’) | OK |
| Mercurio en Sagitario (240° a 269° 59’) | NO OK |
| Mercurio en Capricornio (270° a 299° 59’) | NO OK |
| Mercurio en Acuario (300° a 329° 59’) | NO OK |
| Mercurio en Piscis (330° a 359° 59’) | NO OK |
| Mercurio en casa 2 | NO OK |
| Mercurio en casa 3 | NO OK |
| Mercurio en casa 4 | NO OK |
| Mercurio en casa 5 | NO OK |
| Mercurio en casa 6 | NO OK |
| Mercurio en casa 7 | NO OK |
| Mercurio en casa 8 | NO OK |
| Mercurio en casa 9 | OK |
| Mercurio en casa 10 | NO OK |
| Mercurio en casa 11 | NO OK |
| Mercurio en casa 12 | NO OK |
| Aspecto Mercurio conjunción a Venus | NO OK |
| Aspecto Mercurio en conjunción o cuadratura u oposición Marte | OK |
| Aspecto Mercurio en sextil o trígono a Marte | OK |
| Aspecto Mercurio en conjunción o cuadratura u oposición a Júpiter | OK |
| Aspecto Mercurio en sextil o trígono a Júpiter | OK |
| Aspecto Mercurio en sextil o trígono a Saturno | NO OK |
| Aspecto Mercurio en conjunción o cuadratura u oposición a Saturno | NO OK |
| Aspecto Mercurio en conjunción o cuadratura u oposición a Urano | NO OK |
| Aspecto Mercurio en conjunción, cuadratura u oposición a Urano y Urano está en casa 1, 4, 7 o 10. | REQUIERE LÓGICA ADICIONAL |
| Aspecto Mercurio en conjunción, cuadratura u oposición a Urano y Urano está en conjunción al Sol o la Luna. | REQUIERE LÓGICA ADICIONAL |
| Aspecto Mercurio en trígono o sextil a Urano | NO OK |
| Aspecto Mercurio conjunción o cuadratura u oposición a Neptuno | NO OK |
| Aspecto Mercurio sextil o trígono a Neptuno | NO OK |
| Aspecto Mercurio en conjunción o cuadratura u oposición a Plutón | NO OK |
| Aspecto Mercurio en conjunción a Lilith | NO OK |
| VENUS RETRÓGRADO | NO OK |
| Venus en Aries | NO OK |
| Venus en Tauro | NO OK |
| Venus en Géminis | NO OK |
| Venus en Cáncer | NO OK |
| Venus en Libra | NO OK |
| Venus en Leo | NO OK |
| Venus en Virgo | OK |
| Venus en Escorpio | NO OK |
| Venus en Sagitario | NO OK |
| Venus en Capricornio | NO OK |
| Venus en Acuario | NO OK |
| Venus en Piscis | NO OK |
| Aspecto Venus conjunción Lilith | NO OK |
| Venus en la casa 2 | NO OK |
| Venus en la casa 3 | NO OK |
| Venus en la casa 4: usar solo si no se dan las siguientes condiciones: Saturno en casa 4 o Plutón en casa 4 o  Venus conjunción Saturno o  Venus conjunción Plutón | REQUIERE LÓGICA ADICIONAL |
| Venus en la casa 5 | NO OK |
| Venus en la casa 6 | NO OK |
| Venus en la casa 7 | OK |
| Venus en la casa 8 | NO OK |
| Venus en la casa 9 | NO OK |
| Venus en la casa 10 | NO OK |
| Venus en la casa 11 | NO OK |
| Venus en la casa 12 | NO OK |
| Aspecto Venus en sextil o trígono a Marte | NO OK |
| Venus en cuadratura u oposición a Marte | NO OK |
| Venus en conjunción a Júpiter | NO OK |
| Venus en sextil o trígono a Júpiter | NO OK |
| Venus en cuadratura u oposición a Júpiter | NO OK |
| Venus en conjunción o cuadratura u oposición a Saturno | NO OK |
| Venus en sextil o trígono a Saturno | NO OK |
| Venus en conjunción o cuadratura u oposición a Urano | OK |
| Venus en conjunción o cuadratura u oposición a Neptuno. NO usar si Venus está en Piscis. | OK |
| Venus en conjunción o cuadratura u oposición a Plutón | OK |
| MARTE RETRÓGRADO | NO OK |
| Marte en Aries | NO OK |
| Marte en Tauro | NO OK |
| Marte en Géminis | NO OK |
| Marte en Cáncer | NO OK |
| Marte en Leo | NO OK |
| Marte en Virgo | NO OK |
| Marte en Libra | NO OK |
| Marte en Escorpio | NO OK |
| Marte en Sagitario | NO OK |
| Marte en Capricornio | OK |
| Marte en Acuario | NO OK |
| Marte en Piscis | NO OK |
| Marte en casa 2 | NO OK |
| Marte en casa 3 | NO OK |
| Marte en casa 4 | NO OK |
| Marte en casa 5 | NO OK |
| Marte en casa 6 | NO OK |
| Marte en casa 7 | NO OK |
| Marte en casa 8 | NO OK |
| Marte en casa 9 | NO OK |
| Marte en casa 10 | NO OK |
| Marte en casa 11 | OK |
| Marte en casa 12 | NO OK |
| Aspecto Marte conjunción o cuadratura u oposición a Júpiter | OK |
| Aspecto Marte en sextil o trígono a Júpiter | OK |
| Aspecto Marte conjunción o cuadratura u oposición a Saturno | OK |
| Aspecto Marte sextil o trígono a Saturno | NO OK |
| Aspecto Marte conjunción o cuadratura u oposición a Urano | NO OK |
| Aspecto Marte sextil o trígono a Urano | NO OK |
| Aspecto Marte conjunción o cuadratura u oposición a Neptuno | NO OK |
| Aspecto Marte sextil o trígono a Neptuno | NO OK |
| Aspecto Marte conjunción o cuadratura u oposición a Plutón | NO OK |
| El Sol en casa 10 | NO OK |
| La Luna en casa 10 | NO OK |
| Mercurio en casa 10 | NO OK |
| Júpiter en casa 10 | NO OK |
| Saturno en casa 10 | NO OK |
| Urano en casa 10 | NO OK |
| Neptuno en casa 10 | NO OK |
| Plutón en casa 10 | NO OK |
| JÚPITER RETRÓGRADO (atención, al ser lento es posible que no retome el movimiento directo por progresiones en toda la vida del individuo) | NO OK |
| Júpiter en casa 2 | NO OK |
| Júpiter en casa 3 | NO OK |
| Júpiter en casa 4 | NO OK |
| Júpiter en casa 5 | NO OK |
| Júpiter en casa 6 | OK |
| Júpiter en casa 7 | NO OK |
| Júpiter en casa 8 | NO OK |
| Júpiter en casa 9 | NO OK |
| Júpiter en casa 10 | NO OK |
| Júpiter en casa 11 | NO OK |
| Júpiter en casa 12 | NO OK |
| SATURNO RETROGRADO  (ojo, al ser lento es posible que no retome el movimiento directo por progresiones en toda la vida del individuo) | OK |
| Saturno en casa dos | OK |
| Saturno en casa 3 | NO OK |
| Saturno en casa 4 | NO OK |
| Saturno en casa 5 | NO OK |
| Saturno en casa 6 | NO OK |
| Saturno en casa 7 | NO OK |
| Saturno en casa 8 | NO OK |
| Saturno en casa 9 | NO OK |
| Saturno en casa 10 | NO OK |
| Saturno en casa 11 | NO OK |
| Saturno en casa 12 | NO OK |
| Aspecto Júpiter-Saturno en sextil o trígono | NO OK |
| Aspecto Júpiter-Saturno en conjunción o cuadratura u oposición | NO OK |
| Aspecto Saturno-Urano en conjunción o cuadratura u oposición | OK |
| Aspecto Saturno Plutón en conjunción o cuadratura u oposición | NO OK |
| Aspecto Saturno Neptuno en conjunción o cuadratura u oposición | NO OK |
| Saturno Neptuno II | NO OK |
| Aspecto: Saturno está en casa 1, 4, 7 o 10 y Urano está en casa 1, 4, 7 o 10. | REQUIERE LÓGICA ADICIONAL |
| Aspecto: Saturno está en casa 1, 4, 7 o 10 y Urano está en conjunción al Sol, la Luna, Mercurio, Venus o Marte. | REQUIERE LÓGICA ADICIONAL |
| Aspecto: Saturno está en casa 1, 4, 7 o 10 y hay conjunción, cuadratura u oposición entre Saturno y Urano. | REQUIERE LÓGICA ADICIONAL |
| Aspecto: Saturno está en conjunción al Sol, la Luna, Mercurio, Venus o Marte y Urano está en casa 1, 4, 7 o 10. | REQUIERE LÓGICA ADICIONAL |
| Aspecto: Saturno está en conjunción al Sol, la Luna, Mercurio, Venus o Marte y Urano está en conjunción al Sol, la Luna, Mercurio, Venus o Marte. | REQUIERE LÓGICA ADICIONAL |
| Aspecto: Saturno está en conjunción al Sol, la Luna, Mercurio, Venus o Marte y hay conjunción, cuadratura u oposición entre Saturno y Urano. | REQUIERE LÓGICA ADICIONAL |
| URANO RETRÓGRADO (ojo, al ser lento es posible que no retome el movimiento directo por progresiones en toda la vida del individuo) | NO OK |
| Urano en casa 2 | NO OK |
| Urano en casa 3 | NO OK |
| Urano en casa 4 | NO OK |
| Urano en casa 5 | NO OK |
| Urano en casa 6 | NO OK |
| Urano en casa 7 | OK |
| Urano en casa 8 | NO OK |
| Urano en casa 9 | NO OK |
| Urano en casa 10 | NO OK |
| Urano en casa 11 | NO OK |
| Urano en casa 12 | NO OK |
| Neptuno en casa 2 | NO OK |
| Neptuno en casa 3 | NO OK |
| Neptuno en casa 4 | NO OK |
| Neptuno en casa 5 | NO OK |
| Neptuno en casa 6 | NO OK |
| Neptuno en casa 7 | NO OK |
| Neptuno en casa 8 | NO OK |
| Neptuno en casa 9 | OK |
| Neptuno en casa 10 | NO OK |
| Neptuno en casa 11 | NO OK |
| Neptuno en casa 12 | NO OK |
| PLUTÓN RETRÓGRADO (ojo, al ser lento es posible que no retome el movimiento directo por progresiones en toda la vida del individuo) | NO OK |
| Plutón en casa 2 | NO OK |
| Plutón en casa 3 | NO OK |
| Plutón en casa 4 | NO OK |
| Plutón en casa 5 | NO OK |
| Plutón en casa 6 | NO OK |
| Plutón en casa 7 | OK |
| Plutón en casa 8 | NO OK |
| Plutón en casa 9 | NO OK |
| Plutón en casa 10 | NO OK |
| Plutón en casa 11 | NO OK |
| Plutón en la casa 12 | NO OK |
| POLARIDAD PLUTONIANA CUANDO PLUTÓN ESTÁ CON EL SOL O EN CASA 1 | REQUIERE LÓGICA ADICIONAL |
