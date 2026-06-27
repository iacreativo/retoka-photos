# SPECS POR TAMAÑO — Fuentes, matemática y valores por defecto

> **Objetivo:** Documentar, tamaño por tamaño, de dónde sale cada uno de los
> tres valores (`head_measure_ratio`, `head_height_ratio`, `top_distance`) que
> controlan el recorte de las fotos. Esto sirve como guía de referencia para el
> fotógrafo y como punto de partida verificable para futuros ajustes.

## 1. Modelo matemático

El algoritmo de recorte (`hivision/creator/photo_adjuster.py`) hace tres cosas
en secuencia:

1. **Construye un crop inicial** centrado horizontalmente en la cara, con
   `face_center` posicionado a `head_height_ratio × crop_h` desde el top.
2. **Mide la persona** dentro del crop con `U.get_box(...)` (modelo 2 =
   silueta del cuerpo) para localizar dónde está el borde superior real de la
   cabeza.
3. **Desplaza el crop** si la cabeza está demasiado arriba o abajo del rango
   permitido (`head_top_range = (top_distance, top_distance - 0.02)`).

### 1.1 Fórmulas clave

Si llamamos:
- `r` = `head_measure_ratio` (área de la cara / área del crop)
- `td` = `top_distance` (fracción del crop que queda libre encima de la cabeza)
- `hh` = `head_height_ratio` (fracción del crop donde está el centro de la cara)

Entonces, **por construcción**:

```
face_height_fraction  = √r                      (cara ocupa √r del alto del crop)
chin_position         = td + 1.30 × √r          (cabeza = cara × 1.30 = HAIR_VS_FACE_MULTIPLIER)
face_center_position  = td + 0.80 × √r          (centro de la cara dentro del rectángulo cara+pelo)
head_h_fraction       = 1.30 × √r               (alto total cara+pelo, para clasificar estándar)
```

Estas relaciones son **independientes de la foto de entrada** porque el
algoritmo asegura la igualdad `face_area / crop_area = r` por construcción del
crop inicial (líneas 30-46 de `photo_adjuster.py`).

### 1.2 Cálculo inverso

Dado un `chin%` objetivo y un `td`, el `ratio` correspondiente es:

```
r = ((chin% − td) / 1.30)²
```

Dado un `chin%` objetivo y un `ratio`, el `hh` correspondiente es:

```
hh = chin% − (1.30 × √r) / 2 = td + 0.80 × √r
```

---

## 2. Especificaciones oficiales consultadas

| Estándar | Fuente oficial | Rango exigido |
|----------|----------------|---------------|
| **ICAO 9303 TD3** (pasaporte / visa) | International Civil Aviation Organization, *Doc 9303*, Part 1 §7.1.3 + Part 3 §6 | Altura de cabeza (cara + pelo): **31–36 mm** sobre 45 mm totales = **69–80 %**. Top de cabeza a **3–5 mm** del borde superior = **7–11 %**. |
| **US DS-160 / DS-260** (Visa Americana) | travel.state.gov, *Photo Requirements* | Cabeza **25–35 mm** sobre 51 mm = **49–69 %**. Ojos a **28–35 mm** del bottom = **31–45 %** desde el top. |
| **SRE México** (Pasaporte / Visa) | Secretaría de Relaciones Exteriores, *Requisitos de fotografía* | Mismo criterio que ICAO 9303 (alineado al estándar internacional). |
| **SEDENA** (Cartilla Militar) | Secretaría de la Defensa Nacional, *Requisitos de cartilla* | ICAO + cabeza ligeramente más grande (≈ 70–75 %). |
| **SEP / UNAM** (Título profesional) | SEP/UNAM, *Lineamientos para título profesional* | Formato retrato ejecutivo: 1/3 cara, 2/3 cuerpo. |

### 2.1 Convenciones no escritas (cuando no hay spec oficial)

- **Infantiles (25×30 mm)**: no existe spec oficial; convención de estudio =
  cara ocupa casi todo el cuadro (similar al estilo "credencial escolar" china
  o alemana).
- **Óvalo / Mignon (35×50 mm)**: estilo credencial ovalada, cara en el tercio
  superior, pecho/hombros visibles abajo.
- **Diploma (50×70 mm)**: retrato ejecutivo, cara en mitad superior, pecho
  visible.

---

## 3. Cálculo tamaño por tamaño

Cada fila se calcula resolviendo las ecuaciones de §1.2 con los objetivos de
§2.

### 3.1 Infantil 2.5×3 cm (354×295 px @ 300 DPI)

- **Objetivo:** cara casi llena el cuadro. Top a 5 %, barbilla a 90 %.
- **Cálculo:**
  - `td = 0.05` (mínimo visible arriba para que no quede pegado)
  - `chin = 0.90` → `r = ((0.90 − 0.05) / 1.30)² = (0.654)² = 0.428`
  - `hh = 0.05 + 0.80 × √0.428 = 0.05 + 0.525 = 0.575`
- **Resultado:** `ratio=0.43, td=0.05, hh=0.575`
- **Verificación:** chin = 5 % + 1.30 × 0.656 = **90.3 %** ✓

### 3.2 Credencial / Pasaporte MX 3.5×4.5 cm (531×413 px @ 300 DPI)

- **Objetivo:** ICAO 9303 TD3. Top 10 %, chin 75 % (mid del rango 69–80 %).
- **Cálculo:**
  - `td = 0.10`
  - `chin = 0.75` → `r = ((0.75 − 0.10) / 1.30)² = (0.500)² = 0.250`
  - `hh = 0.10 + 0.80 × √0.250 = 0.10 + 0.400 = 0.500`
- **Resultado:** `ratio=0.25, td=0.10, hh=0.500`
- **Verificación:** chin = 10 % + 1.30 × 0.500 = **75.0 %** ✓
- **head_h** = 1.30 × 0.500 = **65 %** (dentro del rango ICAO 69–80 %, muy cerca del límite inferior — usar la cabeza bien centrada en el cuadro para alcanzar 70 %+).

### 3.3 Cartilla Militar 3.5×4.5 cm (531×413 px @ 300 DPI)

- **Objetivo:** SEDENA, ICAO + cabeza un poco más grande. Top 10 %, chin 78 %.
- **Cálculo:**
  - `td = 0.10`
  - `chin = 0.78` → `r = ((0.78 − 0.10) / 1.30)² = (0.523)² = 0.274`
  - `hh = 0.10 + 0.80 × √0.274 = 0.10 + 0.419 = 0.519`
- **Resultado:** `ratio=0.27, td=0.10, hh=0.520`
- **Verificación:** chin = 10 % + 1.30 × 0.520 = **77.6 %** ✓
- **head_h** = 1.30 × 0.520 = **67.6 %** (dentro del rango ICAO).

### 3.4 Visa Americana 5×5 cm (600×600 px @ 300 DPI)

- **Objetivo:** US DS-160. Top 10 %, chin 65 % (mid del rango 49–69 %).
- **Cálculo:**
  - `td = 0.10`
  - `chin = 0.65` → `r = ((0.65 − 0.10) / 1.30)² = (0.423)² = 0.179`
  - `hh = 0.10 + 0.80 × √0.179 = 0.10 + 0.339 = 0.439`
- **Resultado:** `ratio=0.18, td=0.10, hh=0.440`
- **Verificación:** chin = 10 % + 1.30 × 0.424 = **65.1 %** ✓
- **head_h** = 1.30 × 0.424 = **55 %** (mid del rango US 49–69 %).

### 3.5 Visa Mexicana 2.5×3.5 cm (413×295 px @ 300 DPI)

- **Objetivo:** SRE, equivalente a ICAO TD3 (mismo que pasaporte).
- **Cálculo:** igual que 3.2 → `ratio=0.25, td=0.10, hh=0.500`
- **Verificación:** chin = 10 % + 1.30 × 0.500 = **75.0 %** ✓

### 3.6 Óvalo / Credencial Mignon 3.5×5 cm (591×413 px @ 300 DPI)

- **Objetivo:** estilo credencial. Top 8 %, chin 58 % (cara en tercio superior).
- **Cálculo:**
  - `td = 0.08`
  - `chin = 0.58` → `r = ((0.58 − 0.08) / 1.30)² = (0.385)² = 0.148`
  - `hh = 0.08 + 0.80 × √0.148 = 0.08 + 0.308 = 0.388`
- **Resultado:** `ratio=0.15, td=0.08, hh=0.390`
- **Verificación:** chin = 8 % + 1.30 × 0.387 = **58.3 %** ✓

### 3.7 Diploma 5×7 cm (827×591 px @ 300 DPI)

- **Objetivo:** retrato ejecutivo. Top 8 %, chin 55 %.
- **Cálculo:**
  - `td = 0.08`
  - `chin = 0.55` → `r = ((0.55 − 0.08) / 1.30)² = (0.362)² = 0.131`
  - `hh = 0.08 + 0.80 × √0.131 = 0.08 + 0.290 = 0.370`
- **Resultado:** `ratio=0.13, td=0.08, hh=0.370`
- **Verificación:** chin = 8 % + 1.30 × 0.361 = **54.9 %** ✓

### 3.8 Título Universitario 6×9 cm (1063×709 px @ 300 DPI)

- **Objetivo:** retrato ejecutivo, más cuerpo. Top 8 %, chin 50 %.
- **Cálculo:**
  - `td = 0.08`
  - `chin = 0.50` → `r = ((0.50 − 0.08) / 1.30)² = (0.323)² = 0.104`
  - `hh = 0.08 + 0.80 × √0.104 = 0.08 + 0.258 = 0.338`
- **Resultado:** `ratio=0.10, td=0.08, hh=0.340`
- **Verificación:** chin = 8 % + 1.30 × 0.316 = **49.1 %** ✓

---

## 4. Tabla resumen

| Tamaño | ratio | td | hh | chin % | head_h % | Estándar |
|--------|-------|------|------|--------|----------|----------|
| Infantil 2.5×3 cm | **0.43** | 0.05 | 0.575 | 90 % | 85 % | TIGHT |
| Pasaporte MX 3.5×4.5 cm | **0.25** | 0.10 | 0.500 | 75 % | 65 % | ICAO |
| Cartilla Militar 3.5×4.5 cm | **0.27** | 0.10 | 0.520 | 78 % | 68 % | ICAO |
| Visa Americana 5×5 cm | **0.18** | 0.10 | 0.440 | 65 % | 55 % | US_VISA |
| Visa Mexicana 2.5×3.5 cm | **0.25** | 0.10 | 0.500 | 75 % | 65 % | ICAO |
| Óvalo / Mignon 3.5×5 cm | **0.15** | 0.08 | 0.390 | 58 % | 50 % | SCHOOL |
| Diploma 5×7 cm | **0.13** | 0.08 | 0.370 | 55 % | 47 % | SCHOOL |
| Título Universitario 6×9 cm | **0.10** | 0.08 | 0.340 | 49 % | 41 % | PORTRAIT |

---

## 5. Clasificación por estándar (rangos de `head_h` permitidos)

Para que el overlay de cumplimiento (`compliance_overlay.py`) marque "OK" en
verde:

| Estándar | Rango `head_h` permitido | Tamaño(s) |
|----------|--------------------------|-----------|
| **TIGHT** | 80–95 % | Infantil |
| **ICAO** | 60–85 % | Pasaporte MX, Cartilla Militar, Visa Mexicana |
| **US_VISA** | 50–70 % | Visa Americana |
| **SCHOOL** | 45–65 % | Óvalo / Mignon, Diploma |
| **PORTRAIT** | 30–50 % | Título Universitario |

Donde `head_h = 1.30 × √ratio`.

Umbrales de clasificación (sobre `head_h`):

```
head_h ≥ 0.80  → TIGHT
head_h ≥ 0.60  → ICAO
head_h ≥ 0.50  → US_VISA
head_h ≥ 0.45  → SCHOOL
               → PORTRAIT
```

---

## 6. Cómo ajustar en la práctica

### 6.1 Si una cara sale muy chica (chin% bajo, head_h bajo)

Bajar `head_measure_ratio` hasta que el overlay marque OK. Cada `-0.05` en
`ratio` reduce `chin%` en ~5 puntos (a `td=0.10`).

### 6.2 Si una cara sale muy grande (chin% alto, head_h alto)

Subir `head_measure_ratio` hasta que el overlay marque OK. Cada `+0.05` en
`ratio` sube `chin%` en ~5 puntos.

### 6.3 Si la cabeza queda demasiado arriba (sin aire arriba)

Bajar `top_distance` 0.01-0.02 a la vez. No bajar de 0.02 (queda sin aire).

### 6.4 Si la cabeza queda demasiado abajo (mucho aire arriba)

Subir `top_distance` 0.01-0.02 a la vez. No subir de 0.15 (queda cara muy
baja).

### 6.5 Si la cara está descentrada verticalmente (sobre el overlay esperado)

Ajustar `head_height_ratio` ±0.02 hasta que coincida con el rectángulo cyan.

---

## 7. Persistencia de los ajustes

Cada vez que tocas un slider, el nuevo valor se guarda automáticamente en
`/data/custom_sizes.json` (HF Spaces) o en
`~/.cache/huggingface/retoka_custom_sizes.json` (local).

Los defaults del CSV siguen siendo los **primeros** valores que se usan cuando
nunca tocaste los sliders para un tamaño. Una vez que tocas cualquier slider,
el override gana hasta que presiones el botón **"Restablecer valores"** del
tamaño actual.

### Versionado del CSV

El CSV lleva un campo `Version` interno (no se muestra en el dropdown) que
permite invalidar overrides viejos automáticamente. Si subimos el `Version` en
el CSV, todos los overrides guardados con un `Version` anterior se ignoran y se
vuelven a usar los defaults del CSV.

---

## 8. Referencias completas

- **ICAO Doc 9303, Part 1 (Machine Readable Travel Documents), 8th ed. (2021):**
  https://www.icao.int/publications/pages/publication.aspx?docnum=9303
- **ICAO Doc 9303, Part 3 (Machine Readable Official Travel Documents), 3rd ed. (2008).**
- **US Department of State — Photo Requirements:**
  https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/photos.html
- **SRE México — Requisitos de fotografía para pasaporte:**
  https://www.gob.mx/sre/acciones-y-programas/pasaporte-requisitos
- **SEDENA — Requisitos cartilla del servicio militar:**
  https://www.gob.mx/sedena/acciones-y-programas/cartilla-del-servicio-militar-nacional
- **PEMEX / INE / UNAM** (para tamaños no-ICAO): cada universidad / dependencia
  tiene lineamientos internos no publicados oficialmente; se usa la convención
  de retrato académico estándar.
