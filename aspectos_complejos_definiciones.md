# Definiciones de Aspectos Complejos para Implementación

Este archivo contiene todos los aspectos complejos identificados en `Títulos Numerados tropico.md` que requieren lógica condicional especial. 

**INSTRUCCIONES PARA COMPLETAR:**
- Para cada aspecto, define exactamente qué condiciones deben verificarse
- Usa el formato sugerido para mantener consistencia
- Especifica si las condiciones son AND u OR
- Indica qué datos del JSON se necesitan para la verificación

---

## GRUPO 1: Aspectos Sol-Júpiter con condiciones adicionales

### 1.3.9 - Sol-Júpiter + Saturno/Plutón en casas angulares
**Texto original:** `Aspecto Sol en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en casa 1, 4, 7 o 10.`

**CONDICIÓN PRINCIPAL:** 
- [ ] Aspecto Sol en conjunción OR cuadratura OR oposición a Júpiter

**CONDICIÓN ADICIONAL:** 
- [ ]  Saturno OR Plutón están en casa 1 OR 4 OR 7 OR 10

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

### 1.3.10 - Sol-Júpiter + Saturno/Plutón conjunción a personales
**Texto original:** `Aspecto Sol en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en conjunción al Sol, la Luna, Mercurio, Venus o Marte.`

**CONDICIÓN PRINCIPAL:** 
- [ ] Aspecto Sol en conjunción OR cuadratura OR oposición a Júpiter 

**CONDICIÓN ADICIONAL:** 
- [ ] Saturno OR Plutón están en conjunción al Sol OR la Luna OR Mercurio, OR Venus OR Marte.

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

### 1.3.11 - Sol-Júpiter + Saturno/Plutón cuadratura a personales
**Texto original:** `Aspecto Sol en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en cuadratura al Sol, la Luna, Mercurio, Venus o Marte.`

**CONDICIÓN PRINCIPAL:** 
- [ ] Aspecto Sol en conjunción OR cuadratura OR oposición a Júpiter

**CONDICIÓN ADICIONAL:** 
- [ ] Saturno OR Plutón están en cuadratura al Sol OR la Luna OR Mercurio, OR Venus OR Marte.

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

### 1.3.12 - Sol-Júpiter + aspecto Saturno-Plutón
**Texto original:** `Aspecto Sol en conjunción, cuadratura u oposición a Júpiter y hay conjunción, cuadratura u oposición entre Saturno y Plutón.`

**CONDICIÓN PRINCIPAL:** 
- [ ] Aspecto Sol en conjunción OR cuadratura OR oposición a Júpiter

**CONDICIÓN ADICIONAL:** 
- [ ] Aspecto Saturno conjunción OR cuadratura OR oposición a Plutón

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

## GRUPO 2: Aspectos Luna-Júpiter con condiciones adicionales

### 2.3.10 - Luna-Júpiter + Saturno/Plutón en casas angulares
**Texto original:** `Aspecto Luna en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en casa 1, 4, 7 o 10.`

**CONDICIÓN PRINCIPAL:** 
- [ ] Aspecto Luna en conjunción OR cuadratura OR oposición a Júpiter 

**CONDICIÓN ADICIONAL:** 
- [ ] Saturno OR Plutón están en casa 1 OR 4 OR 7 OR 10

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

### 2.3.11 - Luna-Júpiter + Saturno/Plutón conjunción a personales
**Texto original:** `Aspecto Luna en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en conjunción al Sol, la Luna, Mercurio, Venus o Marte.`

**CONDICIÓN PRINCIPAL:** 
- [ ] Aspecto Luna en conjunción OR cuadratura OR oposición a Júpiter

**CONDICIÓN ADICIONAL:** 
- [ ] aspecto Saturno OR Plutón conjunción al Sol OR la Luna OR Mercurio OR Venus OR Marte.

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

### 2.3.12 - Luna-Júpiter + Saturno/Plutón cuadratura a personales
**Texto original:** `Aspecto Luna en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en cuadratura al Sol, la Luna, Mercurio, Venus o Marte.`

**CONDICIÓN PRINCIPAL:** 
- [ ] Aspecto Luna en conjunción OR cuadratura OR oposición a Júpiter

**CONDICIÓN ADICIONAL:** 
- [ ] Saturno OR Plutón están en cuadratura al Sol OR la Luna OR Mercurio OR Venus OR Marte.

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

### 2.3.13 - Luna-Júpiter + aspecto Saturno-Plutón
**Texto original:** `Aspecto Luna en conjunción, cuadratura u oposición a Júpiter y hay conjunción, cuadratura u oposición entre Saturno y Plutón.`

**CONDICIÓN PRINCIPAL:** 
- [ ] Aspecto Luna en conjunción OR cuadratura OR oposición a Júpiter

**CONDICIÓN ADICIONAL:** 
- [ ] Aspecto Saturno conjunción OR cuadratura OR  oposición  a Plutón

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

## GRUPO 3: Aspectos Luna-Urano con condiciones adicionales

### 2.3.17 - Luna-Urano + Saturno en casas angulares
**Texto original:** `Aspecto Luna en conjunción, cuadratura u oposición a Urano y Saturno está en casa 1, 4, 7 o 10.`

**CONDICIÓN PRINCIPAL:** 
- [ ] Aspecto Luna en conjunción OR cuadratura OR oposición a Urano

**CONDICIÓN ADICIONAL:** 
- [ ] Saturno está en casa 1 OR 4 OR 7 OR 10

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

### 2.3.18 - Luna-Urano + Saturno conjunción a personales
**Texto original:** `Aspecto Luna en conjunción, cuadratura u oposición a Urano y Saturno está en conjunción al Sol, la Luna, Mercurio, Venus o Marte.`

**CONDICIÓN PRINCIPAL:** 
- [ ] Aspecto Luna en conjunción OR cuadratura OR oposición a Urano

**CONDICIÓN ADICIONAL:** 
- [ ] Saturno está en conjunción al Sol OR la Luna OR Mercurio OR Venus OR Marte

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

### 2.3.19 - Luna-Urano + Saturno cuadratura a personales
**Texto original:** `Aspecto Luna en conjunción, cuadratura u oposición a Urano y Saturno está en cuadratura al Sol, la Luna, Mercurio, Venus o Marte.`

**CONDICIÓN PRINCIPAL:** 
- [ ] Aspecto Luna en conjunción OR cuadratura OR  oposición a Urano

**CONDICIÓN ADICIONAL:** 
- [ ] Saturno está en cuadratura al Sol OR la Luna OR Mercurio OR Venus OR Marte

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

## GRUPO 4: Ascendente en Tauro con condiciones adicionales

### 4.1.3 - Ascendente Tauro + Marte en casas angulares
**Texto original:** `Ascendente en Tauro y Marte está en casa 1, 4, 7 o 10.`

**CONDICIÓN PRINCIPAL:** 
- [ ] Ascendente en Tauro

**CONDICIÓN ADICIONAL:** 
- [ ] Marte está en casa 1 OR 4 OR 7 OR 10

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

### 4.1.4 - Ascendente Tauro + Marte conjunción Sol/Luna
**Texto original:** `Ascendente en Tauro y Marte está en conjunción al Sol o la Luna.`

**CONDICIÓN PRINCIPAL:** 
- [ ] Ascendente Tauro

**CONDICIÓN ADICIONAL:** 
- [ ] Marte está en conjunción al Sol OR la Luna.

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

## GRUPO 5: Planetas ubicados en el ascendente (Casa 1)

### 4.2.1 - Luna en el ascendente
**Texto original:** `Luna en el ascendente`

**CONDICIÓN:** 
- [ ] Luna está en Casa 1 (ya aclarado que es casa, no proximidad)

**DATOS JSON:** 
- [ ] planets_in_houses["Moon"] == 1

---

### 4.2.2 - Mercurio en el ascendente
**Texto original:** `Mercurio en el ascendente`

**CONDICIÓN:** 
- [ ] Mercurio está en Casa 1

**DATOS JSON:** 
- [ ] planets_in_houses["Mercury"] == 1

---

### 4.2.3 - Venus en el ascendente
**Texto original:** `Venus en el ascendente`

**CONDICIÓN:** 
- [ ] Venus está en Casa 1

**DATOS JSON:** 
- [ ] planets_in_houses["Venus"] == 1

---

### 4.2.4 - Marte en el ascendente
**Texto original:** `Marte en el ascendente`

**CONDICIÓN:** 
- [ ] Marte está en Casa 1

**DATOS JSON:** 
- [ ] planets_in_houses["Mars"] == 1

---

### 4.2.5 - Júpiter en el ascendente
**Texto original:** `Júpiter en el ascendente`

**CONDICIÓN:** 
- [ ] Júpiter está en Casa 1

**DATOS JSON:** 
- [ ] planets_in_houses["Jupiter"] == 1

---

### 4.2.6 - Saturno en el ascendente
**Texto original:** `Saturno en el ascendente`

**CONDICIÓN:** 
- [ ] Saturno está en Casa 1

**DATOS JSON:** 
- [ ] planets_in_houses["Saturn"] == 1

---

### 4.2.7 - Urano en el ascendente
**Texto original:** `Urano en el ascendente`

**CONDICIÓN:** 
- [ ] Urano está en Casa 1

**DATOS JSON:** 
- [ ] planets_in_houses["Uranus"] == 1

---

### 4.2.8 - Neptuno en el ascendente
**Texto original:** `Neptuno en el ascendente`

**CONDICIÓN:** 
- [ ] Neptuno está en Casa 1

**DATOS JSON:** 
- [ ] planets_in_houses["Neptune"] == 1

---

### 4.2.9 - Plutón en el ascendente
**Texto original:** `Plutón en el ascendente`

**CONDICIÓN:** 
- [ ] Plutón está en Casa 1

**DATOS JSON:** 
- [ ] planets_in_houses["Pluto"] == 1

---

## GRUPO 6: Aspectos Mercurio-Urano con condiciones adicionales

### 5.4.9 - Mercurio-Urano + Urano en casas angulares
**Texto original:** `Aspecto Mercurio en conjunción, cuadratura u oposición a Urano y Urano está en casa 1, 4, 7 o 10.`

**CONDICIÓN PRINCIPAL:** 
- [ ] Aspecto Mercurio en conjunción OR cuadratura OR oposición a Urano

**CONDICIÓN ADICIONAL:** 
- [ ] Urano está en casa 1 OR 4 OR 7 OR 10

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

### 5.4.10 - Mercurio-Urano + Urano conjunción Sol/Luna
**Texto original:** `Aspecto Mercurio en conjunción, cuadratura u oposición a Urano y Urano está en conjunción al Sol o la Luna.`

**CONDICIÓN PRINCIPAL:** 
- [ ] Aspecto Mercurio en conjunción OR cuadratura OR oposición a Urano

**CONDICIÓN ADICIONAL:** 
- [ ] Urano está en conjunción al Sol OR la Luna

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

## GRUPO 7: Venus en casa 4 con exclusiones

### 8.1.3 - Venus casa 4 con exclusiones
**Texto original:** `Venus en la casa 4: usar solo si no se dan las siguientes condiciones: Saturno en casa 4 o Plutón en casa 4 o Venus conjunción Saturno o Venus conjunción Plutón`

**CONDICIÓN PRINCIPAL:** 
- [ ] Venus en la casa 4

**EXCLUSIONES (NO deben cumplirse):** 
- [ ] Saturno en casa 4 OR Plutón en casa 4 OR Venus conjunción Saturno OR Venus conjunción Plutón

**LÓGICA:** 
- [ ] Principal AND NOT Exclusion
- [ ] Datos JSON necesarios

---

## GRUPO 8: Aspectos complejos Saturno-Urano

### 13.3.10 - Saturno y Urano ambos en casas angulares
**Texto original:** `Aspecto: Saturno está en casa 1, 4, 7 o 10 y Urano está en casa 1, 4, 7 o 10.`

Aclaracion adicional: no se busca un aspecto entre Saturno y Urano

**CONDICIÓN 1:** 
- [ ] Saturno está en casa 1 OR 4 OR  7 OR 10

**CONDICIÓN 2:** 
- [ ] Urano está en casa 1 OR 4 OR 7 OR 10.

**LÓGICA:** 
- [ ] AND condiciones
- [ ] Datos JSON necesarios

---

### 13.3.11 - Saturno en angulares + Urano conjunción a personales
**Texto original:** `Aspecto: Saturno está en casa 1, 4, 7 o 10 y Urano está en conjunción al Sol, la Luna, Mercurio, Venus o Marte.`

Aclaracion adicional: no se busca un aspecto entre Saturno y Urano

**CONDICIÓN 1:** 
- [ ] Saturno está en casa 1 OR  4 OR 7 OR 10

**CONDICIÓN 2:** 
- [ ]  Urano está en conjunción al Sol OR la Luna OR Mercurio OR Venus OR Marte.

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

### 13.3.12 - Saturno en angulares + aspecto Saturno-Urano
**Texto original:** `Aspecto: Saturno está en casa 1, 4, 7 o 10 y hay conjunción, cuadratura u oposición entre Saturno y Urano.`

**CONDICIÓN 1:** 
- [ ] Saturno está en casa 1 OR 4 OR 7 OR 10

**CONDICIÓN 2:** 
- [ ] Aspecto Saturno conjunción OR cuadratura OR oposición a Urano 

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

### 13.3.13 - Saturno conjunción a personales + Urano en angulares
**Texto original:** `Aspecto: Saturno está en conjunción al Sol, la Luna, Mercurio, Venus o Marte y Urano está en casa 1, 4, 7 o 10.`

Aclaracion adicional: no se busca un aspecto entre Saturno y Urano

**CONDICIÓN 1:** 
- [ ] Saturno está en conjunción al Sol OR la Luna OR Mercurio OR Venus OR Marte

**CONDICIÓN 2:** 
- [ ] Urano está en casa 1 OR 4 OR 7 OR 10

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

### 13.3.14 - Saturno y Urano ambos conjunción a personales
**Texto original:** `Aspecto: Saturno está en conjunción al Sol, la Luna, Mercurio, Venus o Marte y Urano está en conjunción al Sol, la Luna, Mercurio, Venus o Marte.`

Aclaracion adicional: no se busca un aspecto entre Saturno y Urano

**CONDICIÓN 1:** 
- [ ] Saturno está en conjunción al Sol OR la Luna OR Mercurio OR Venus OR Marte

**CONDICIÓN 2:** 
- [ ] Urano está en conjunción al Sol OR la Luna OR Mercurio OR Venus OR Marte.

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

### 13.3.15 - Saturno conjunción a personales + aspecto Saturno-Urano
**Texto original:** `Aspecto: Saturno está en conjunción al Sol, la Luna, Mercurio, Venus o Marte y hay conjunción, cuadratura u oposición entre Saturno y Urano.`

**CONDICIÓN 1:** 
- [ ] Saturno está en conjunción al Sol OR la Luna OR Mercurio OR Venus OR Marte 

**CONDICIÓN 2:** 
- [ ] hay aspecto Saturno conjunción OR cuadratura OR oposición a Urano.

**LÓGICA:** 
- [ ] AND entre condiciones
- [ ] Datos JSON necesarios

---

## GRUPO 9: Polaridad cl

### 16.3 - Polaridad plutoniana
**Texto original:** `POLARIDAD PLUTONIANA CUANDO PLUTÓN ESTÁ CON EL SOL O EN CASA 1`

**CONDICIÓN 1:** 
- [ ] Aspecto Plutón conjunción OR oposición OR cuadratura al Sol

**CONDICIÓN 2:** 
- [ ] Plutón en Casa 1

**LÓGICA:** 
- [ ] OR entre las dos opciones
- [ ] Datos JSON necesarios

---

## DATOS DISPONIBLES EN EL SISTEMA

Para referencia, estos son los datos que tenemos disponibles:

### Del JSON de la carta natal:
- `raw_json_data["points"][planeta]["longitude"]` - Longitud de cada planeta
- `raw_json_data["points"][planeta]["sign"]` - Signo de cada planeta  
- `raw_json_data["points"][planeta]["retrograde"]` - Si está retrógrado
- `raw_json_data["aspects"]` - Lista de todos los aspectos detectados
- `raw_json_data["houses"][numero]["sign"]` - Signo de cada casa

### Calculado por el sistema:
- `planets_in_houses[planeta]` - Casa donde está cada planeta
- `eventos` - Lista de eventos extraídos (aspectos, planetas en signos, etc.)

### Nombres de planetas en el JSON:
- "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"
- "Asc", "MC", "True North Node", "Lilith", "Chiron", "Part of Fortune", "Vertex"

### Tipos de aspectos en el JSON:
- "Conjunción", "Oposición", "Cuadratura", "Trígono", "Sextil"
