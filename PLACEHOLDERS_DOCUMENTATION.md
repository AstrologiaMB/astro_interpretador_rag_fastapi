# DOCUMENTACIÓN DE PLACEHOLDERS DINÁMICOS

## DESCRIPCIÓN
Los archivos de interpretaciones contienen placeholders que deben ser reemplazados automáticamente con información específica de cada carta natal.

## PLACEHOLDERS IDENTIFICADOS

### EDADES Y PROGRESIONES
- `(agregar edad)` - Edad cuando un planeta retrógrado retoma movimiento directo
- `(poner edad)` - Edad específica de cambios planetarios por progresiones
- `YYYY` - Años específicos calculados por progresiones secundarias

### INFORMACIÓN ASTROLÓGICA
- `(nombrar casa)` - Número de casa astrológica donde está ubicado un planeta
- `(nombrar significado de la casa)` - Significado interpretativo de la casa específica

### EJEMPLOS DE USO ACTUAL
```markdown
"Mercurio retomó su movimiento directo por progresiones secundarias a partir de tus (agregar edad) años"
→ "Mercurio retomó su movimiento directo por progresiones secundarias a partir de tus 23 años"

"Marte en (nombrar casa) hace que tomes conciencia de tu fuerza a través de (nombrar significado de la casa)"
→ "Marte en casa 7 hace que tomes conciencia de tu fuerza a través de las relaciones"
```

## FUTURAS MEJORAS RECOMENDADAS

### FASE 1: SISTEMA DE REEMPLAZO AUTOMÁTICO
- Implementar función `replace_placeholders()` en main.py
- Integrar con datos de carta natal existentes
- Calcular progresiones secundarias automáticamente

### FASE 2: DICCIONARIO DE SIGNIFICADOS
```python
HOUSE_MEANINGS = {
    1: "refiere al ser, cuerpo físico e imagen. Individualidad. El nivel de vitalidad y fuerza personal.",
    2: "refiere a recursos, valores y posesiones. La manera de obtener riqueza. Bienes personales, ingresos y ganancias.", 
    3: "refiere a viajes, desplazamientos cortos. Hermanos/as, primos/as, vecinos. Conocimiento concreto. Chismes, rumores. Papeles, contratos. Mensajes. Educación temprana.",
    4: "refiere a la familia, padre. Casa, Fundaciones y raíces. País. Asuntos domésticos. La vivienda. Bienes raíces, la tierra.
",
    5: "efiere al disfrute personal y actividades que dan placer. Romance, creatividad. Hijos. Invenciones y creaciones. Juegos de azar. El arte y las musas.",
    6: "refiere a enfermedades físicas. Empleados, mascotas y animales pequeños. Trabajo rutinario.",
    7: "refiere a matrimonio y todas las formas de asociaciones. Rivales y competidores conocidos.",
    8: "refiere a recursos y bienes compartidos con otros. Impuestos, deudas, herencias. Pérdidas y angustias.",
    9: "refiere a religión, filosofía, sistema de creencias, enseñanza superior, viajes lejanos, extranjeros, publicaciones, conocimiento superior, Universidad.",
    10: "la carrera y reputación pública",
    11: "refiere a amistades, temas humanitarios, grupos, deseos y aspiraciones, libertad, altruismo.",
    12: "Casa 12 refiere a espiritualidad. Hospitalización. Retiro. Confinamiento. Encierro. Escapismo. Autosabotaje. Lo que está oculto, restringido y secreto."
}
```

### FASE 3: CÁLCULO DE PROGRESIONES
- Implementar cálculo de progresiones secundarias
- Determinar edades de cambio de dirección planetaria
- Integrar con fechas de nacimiento

## ARCHIVOS AFECTADOS
- `data/6 - MERCURIO_ LA COMUNICACIÓN.md` - Contiene `(agregar edad)` y `YYYY`
- `data/5 - EL ASCENDENTE (casa 1) _ EL MO.md` - Contiene `(nombrar casa)` y `(nombrar significado de la casa)`
- `data/7 - VENUS_ LA BELLEZA Y LAS RELACI.md` - Contiene `(poner edad)`
- Otros archivos pueden contener placeholders similares

## ESTADO ACTUAL
- ✅ Placeholders mantenidos intactos durante estandarización de formato
- ✅ Funcionalidad dinámica preservada
- ⏳ Sistema de reemplazo automático pendiente de implementación

## PRIORIDAD
**Media-Alta** - Mejorará significativamente la personalización de interpretaciones
