# Product Context

## Purpose
The Astro Interpretador RAG is a microservice that provides automated astrological interpretations using Retrieval-Augmented Generation (RAG). It processes natal chart data and generates comprehensive, personalized astrological readings in Spanish.

## Problem Solved
- **Manual Interpretation Bottleneck**: Eliminates the need for manual astrological interpretation of natal charts
- **Consistency**: Provides consistent interpretations based on established astrological knowledge
- **Scalability**: Can process multiple chart interpretations simultaneously
- **Personalization**: Generates gender-specific and personalized interpretations

## Core Functionality
Given natal chart data (planets, houses, aspects), the system:
1. Extracts astrological events from the chart
2. Matches events against available interpretations using flexible title matching
3. Retrieves relevant content from the knowledge base using semantic search
4. Generates individual interpretations for each event using LLM
5. Creates a unified narrative interpretation combining all elements

## CRITICAL: Content Management Rules (2025-07-16)

### The Source of Truth Principle
**FUNDAMENTAL RULE**: All astrological content is managed through two primary data sources:
- `data/Títulos normalizados minusculas.txt` - Master list of valid interpretation titles
- `data/*.md` files - Astrological interpretation content organized by topic

### Content Update Workflow

#### Step 1: Google Doc to Markdown
When new interpretations are added to the master Google Doc:
1. Export the relevant section to Markdown format
2. Save as numbered `.md` file in `/data/` directory (e.g., `27-new-topic.md`)
3. Ensure content follows established format and structure

#### Step 2: Title Normalization (CRITICAL)
**ALL NEW TITLES MUST BE ADDED TO**: `data/Títulos normalizados minusculas.txt`

**MANDATORY TITLE FORMATTING RULES:**

1. **Lowercase Only**: All titles must be in lowercase
   ```
   ✅ CORRECT: "sol en aries"
   ❌ WRONG: "Sol en Aries" or "SOL EN ARIES"
   ```

2. **No Numbering or Bullets**: Remove all numerical prefixes and bullet points
   ```
   ✅ CORRECT: "luna en casa 3"
   ❌ WRONG: "### 3.2.1 luna en casa 3" or "• luna en casa 3"
   ```

3. **Compound Aspects Format**: Use "o" and "u" for multiple aspects
   ```
   ✅ CORRECT: "marte conjunción o cuadratura u oposición a urano"
   ❌ WRONG: "marte conjunción/cuadratura/oposición a urano"
   ```

4. **Angle Format**: Include "(ángulo)" for astrological angles
   ```
   ✅ CORRECT: "ascendente (ángulo) en cáncer"
   ❌ WRONG: "ascendente en cáncer"
   ```

5. **Retrograde Format**: Simple format for retrograde planets
   ```
   ✅ CORRECT: "mercurio retrógrado"
   ❌ WRONG: "mercurio en retrogradación"
   ```

6. **House Format**: Use "casa" followed by number
   ```
   ✅ CORRECT: "sol en casa 6"
   ❌ WRONG: "sol en la sexta casa"
   ```

### Content Categories and Examples

#### Basic Placements
- Planets in signs: `"sol en capricornio"`, `"luna en libra"`
- Planets in houses: `"sol en casa 6"`, `"luna en casa 3"`
- Angles: `"ascendente (ángulo) en cáncer"`, `"medio cielo (ángulo) en tauro"`

#### Aspects
- Simple aspects: `"sol conjunción a lilith"`, `"luna sextil a mercurio"`
- Compound aspects: `"marte conjunción o cuadratura u oposición a plutón"`
- Flexible matching: `"venus en conjunción o cuadratura u oposición a saturno"`

#### Special Conditions
- Retrograde planets: `"mercurio retrógrado"`, `"júpiter retrógrado"`
- Complex aspects: Custom titles based on specific astrological conditions

### Quality Assurance Checklist

Before adding new content, verify:
- [ ] Title is in `Títulos normalizados minusculas.txt`
- [ ] Title follows all formatting rules (lowercase, no numbering, correct format)
- [ ] Content is in appropriate `.md` file in `/data/` directory
- [ ] Title format matches exactly what the system will generate as queries
- [ ] Compound aspects use "o" and "u" connectors
- [ ] Angles include "(ángulo)" specification

### Testing New Content

After adding new titles and content:
1. Restart the microservice to reload the title list
2. Test with a chart that should trigger the new interpretation
3. Check logs for "✅ EVENTO APROBADO" vs "❌ EVENTO RECHAZADO"
4. Verify the interpretation appears in the final output

### Common Mistakes to Avoid

1. **Case Sensitivity**: System is case-sensitive. All titles must be lowercase.
2. **Format Mismatch**: Query format must exactly match title format.
3. **Missing Titles**: Adding content without updating the title list will result in events being rejected.
4. **Inconsistent Formatting**: Different formats for similar concepts will break matching.

### Maintenance Schedule

**Monthly Review**:
- Audit rejected events in logs to identify missing interpretations
- Review and update title list for consistency
- Validate that all `.md` files have corresponding titles

**Quarterly Update**:
- Comprehensive review of interpretation quality
- Update compound aspect titles based on usage patterns
- Performance optimization review

## System Integration

### Input Format
The system receives natal chart data in JSON format containing:
- `points`: Planetary positions with signs and degrees
- `houses`: House cusps with signs
- `aspects`: Planetary aspects with types and orbs

### Output Format
Returns structured JSON with:
- `interpretacion_narrativa`: Unified narrative interpretation
- `interpretaciones_individuales`: Array of individual event interpretations
- `tiempo_generacion`: Processing time in seconds

### Performance Characteristics
- **Capacity**: Processes 30-40 astrological events per chart
- **Speed**: ~30-60 seconds per complete interpretation (optimized with parallel processing)
- **Accuracy**: Flexible matching system handles compound aspect titles
- **Reliability**: Graceful degradation with fallback interpretations

## Business Value

### For Users
- **Instant Interpretations**: No waiting for manual astrological readings
- **Comprehensive Coverage**: All major astrological elements included
- **Personalized Content**: Gender-specific and contextual interpretations
- **Professional Quality**: Based on established astrological knowledge

### For Business
- **Scalability**: Unlimited concurrent interpretations
- **Consistency**: Standardized interpretation quality
- **Cost Efficiency**: Reduces need for manual astrological consultations
- **Extensibility**: Easy to add new astrological content and interpretations

### For Developers
- **Maintainable**: Clear separation between content and code
- **Testable**: Comprehensive logging and debugging capabilities
- **Flexible**: Adaptable to new astrological concepts and requirements
- **Documented**: Extensive documentation for all system components
