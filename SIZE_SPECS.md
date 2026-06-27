# SPECS POR TAMAÑO — Fuentes, matemática y valores por defecto

> **Objetivo:** Documentar, tamaño por tamaño, de dónde sale cada uno de los
> tres valores (`head_measure_ratio`, `head_height_ratio`, `top_distance`) que
> controlan el recorte de las fotos. Esto sirve como guía de referencia para el
> fotógrafo y como punto de partida verificable para futuros ajustes.

> **Revisión v3 (2026-06-26):** los defaults de v2 ponían la cara demasiado
> grande para Infantil (chin 90 %, head_h 85 %) y demasiado chica para
> Pasaporte (chin 75 %, head_h 65 %, debajo del mínimo ICAO de 69 %). v3 los
> recalibra contra imágenes de referencia reales: para Infantil se usa el
> estilo credencial escolar mexicana (chin 62 %, head_h 52 %), y para
> Pasaporte se usa mid-ICAO (chin 83 %, head_h 76 %).

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
- `r` = `head_measure_ratio` (área de la cara / área del crop final)
- `td` = `top_distance` (fracción del crop que queda libre encima de la cabeza)
- `hh` = `head_height_ratio` (fracción del crop donde está el centro de la cara)

Entonces, **por construcción del algoritmo**:

```
face_area_fraction    = r                        (cara ocupa r del área del crop final)
face_height_fraction  = √r                       (cara ocupa √r del alto del crop)
chin_position         = td + 1.30 × √r           (cabeza = cara × 1.30 = HAIR_VS_FACE_MULTIPLIER)
face_center_position  = td + 0.80 × √r           (centro de la cara dentro del rectángulo cara+pelo)
head_h_fraction       = 1.30 × √r                (alto total cara+pelo)
```

Estas relaciones son **independientes de la foto de entrada** porque el
algoritmo asegura `face_area / crop_area = r` por construcción del crop
inicial (líneas 30–46 de `photo_adjuster.py`). Esto lo verifiqué contra la
imagen de salida real de retoka: con `ratio=0.43` la cara ocupa exactamente
el 85 % del frame, igual a `1.30 × √0.43`.

### 1.2 Cálculo inverso

Dado un `chin%` objetivo y un `td`:

```
r = ((chin% − td) / 1.30)²
hh = chin% − (1.30 × √r) / 2 = td + 0.80 × √r
```

---

## 2. Especificaciones oficiales consultadas

| Estándar | Fuente oficial | Rango exigido |
|----------|----------------|---------------|
| **ICAO 9303 TD3** (pasaporte / visa) | International Civil Aviation Organization, *Doc 9303*, Part 1 §7.1.3 + Part 3 §6 | Altura de cabeza (cara + pelo): **31–36 mm** sobre 45 mm totales = **69–80 %**. Top de cabeza a **3–5 mm** del borde superior = **7–11 %**. |
| **US DS-160 / DS-260** (Visa Americana) | travel.state.gov, *Photo Requirements* | Cabeza **25–35 mm** sobre 51 mm = **49–69 %**. Ojos a **28–35 mm** del bottom = **31–45 %** desde el top. |
| **SRE México** (Pasaporte / Visa) | Secretaría de Relaciones Exteriores, *Requisitos de fotografía* | Mismo criterio que ICAO 9303 (alineado al estándar internacional). |
| **SEDENA** (Cartilla Militar) | Secretaría de la Defensa Nacional, *Requisitos de cartilla* | ICAO + cabeza ligeramente más grande (≈ 75–82 %). |
| **SEP / UNAM** (Título profesional) | SEP/UNAM, *Lineamientos para título profesional* | Formato retrato ejecutivo: 1/3 cara, 2/3 cuerpo. |

### 2.1 Estilo infantil (25×30 mm) — derivado de referencia visual

No existe spec oficial mexicana para "foto infantil 2.5×3 cm". La convención
de estudio más usada en México (y la que el cliente prefiere, confirmada con
imagen de referencia real `foto-infantil-878x1024.webp`):

- **Top margin:** ~10 % del frame
- **Chin:** ~62 % del frame
- **Head_h (cara + pelo):** ~52 % del frame
- **Shoulders visibles** abajo
- **Estilo:** credencial escolar estándar (NO extreme close-up)

Midiendo píxeles de la imagen referencia (878×1024 px):
- top of hair a y ≈ 80 px (≈ 9 %)
- chin a y ≈ 640 px (≈ 62 %)
- head_h ≈ 560/1024 = 54.7 %

---

## 3. Cálculo tamaño por tamaño

### 3.1 Infantil 2.5×3 cm (354×295 px @ 300 DPI)

- **Objetivo:** estilo credencial escolar. top 10 %, chin 62 %, head_h 52 %.
- **Cálculo:**
  - `td = 0.10` (≈ 9 % medido)
  - `chin = 0.62` → `r = ((0.62 − 0.10) / 1.30)² = (0.400)² = 0.160`
  - `hh = 0.10 + 0.80 × √0.16 = 0.10 + 0.320 = 0.420`
- **Resultado:** `ratio=0.16, td=0.10, hh=0.42`
- **Verificación:** chin = 10 % + 1.30 × 0.400 = **62.0 %** ✓
- **head_h** = 1.30 × 0.400 = **52.0 %** ✓ (dentro de SCHOOL 45–65 %)
- **Nota:** un valor anterior (v2) usaba `ratio=0.43` que producía cara al
  85 % del frame. Eso era incorrecto — ese estilo solo se usa en algunos
  países asiáticos, no en México.

### 3.2 Credencial / Pasaporte MX 3.5×4.5 cm (531×413 px @ 300 DPI)

- **Objetivo:** ICAO 9303 TD3. Top 9 % (mid de 7–11 %), head_h 76 % (mid de
  69–80 %).
- **Cálculo:**
  - `td = 0.09`
  - `chin = 0.85` → `r = ((0.85 − 0.09) / 1.30)² = (0.585)² = 0.342`
  - `hh = 0.09 + 0.80 × √0.342 = 0.09 + 0.468 = 0.558`
- **Resultado:** `ratio=0.33, td=0.09, hh=0.55`
- **Verificación:** chin = 9 % + 1.30 × 0.574 = **83.6 %** ✓
- **head_h** = 1.30 × 0.574 = **74.6 %** ✓ (dentro de ICAO 69–80 %)
- **Nota:** el valor anterior (v2: `ratio=0.25`) daba head_h=65 %, por debajo
  del mínimo ICAO. Sube a 0.33 para entrar cómodo en el rango.

### 3.3 Cartilla Militar 3.5×4.5 cm (531×413 px @ 300 DPI)

- **Objetivo:** SEDENA, ICAO con cabeza ligeramente más grande.
  Top 8 %, head_h 79 %.
- **Cálculo:**
  - `td = 0.08`
  - `chin = 0.87` → `r = ((0.87 − 0.08) / 1.30)² = (0.608)² = 0.369`
  - `hh = 0.08 + 0.80 × √0.369 = 0.08 + 0.486 = 0.566`
- **Resultado:** `ratio=0.37, td=0.08, hh=0.57`
- **Verificación:** chin = 8 % + 1.30 × 0.608 = **87.0 %** ✓
- **head_h** = 1.30 × 0.608 = **79.0 %** ✓ (límite alto de ICAO)

### 3.4 Visa Americana 5×5 cm (600×600 px @ 300 DPI)

- **Objetivo:** US DS-160. Top 10 %, head_h 57 % (mid de 49–69 %).
- **Cálculo:**
  - `td = 0.10`
  - `chin = 0.67` → `r = ((0.67 − 0.10) / 1.30)² = (0.438)² = 0.192`
  - `hh = 0.10 + 0.80 × √0.192 = 0.10 + 0.351 = 0.451`
- **Resultado:** `ratio=0.19, td=0.10, hh=0.45`
- **Verificación:** chin = 10 % + 1.30 × 0.438 = **66.9 %** ✓
- **head_h** = 1.30 × 0.438 = **57.0 %** ✓ (dentro de US_VISA 50–70 %)

### 3.5 Visa Mexicana 2.5×3.5 cm (413×295 px @ 300 DPI)

- **Objetivo:** SRE, equivalente a ICAO TD3.
- **Cálculo:** igual que 3.2 → `ratio=0.33, td=0.09, hh=0.55`
- **Verificación:** chin = 9 % + 1.30 × 0.574 = **83.6 %** ✓

### 3.6 Óvalo / Credencial Mignon 3.5×5 cm (591×413 px @ 300 DPI)

- **Objetivo:** estilo credencial. Top 8 %, chin 58 %, head_h 50 %.
- **Cálculo:**
  - `td = 0.08`
  - `chin = 0.58` → `r = ((0.58 − 0.08) / 1.30)² = (0.385)² = 0.148`
  - `hh = 0.08 + 0.80 × √0.148 = 0.08 + 0.308 = 0.388`
- **Resultado:** `ratio=0.15, td=0.08, hh=0.39`
- **Verificación:** chin = 8 % + 1.30 × 0.387 = **58.3 %** ✓
- **head_h** = 1.30 × 0.387 = **50.3 %** ✓ (en SCHOOL)

### 3.7 Diploma 5×7 cm (827×591 px @ 300 DPI)

- **Objetivo:** retrato ejecutivo. Top 8 %, chin 52 %, head_h 45 %.
- **Cálculo:**
  - `td = 0.08`
  - `chin = 0.52` → `r = ((0.52 − 0.08) / 1.30)² = (0.338)² = 0.114`
  - `hh = 0.08 + 0.80 × √0.114 = 0.08 + 0.270 = 0.350`
- **Resultado:** `ratio=0.12, td=0.08, hh=0.36`
- **Verificación:** chin = 8 % + 1.30 × 0.338 = **51.9 %** ✓
- **head_h** = 1.30 × 0.338 = **43.9 %** ✓ (en SCHOOL)

### 3.8 Título Universitario 6×9 cm (1063×709 px @ 300 DPI)

- **Objetivo:** retrato ejecutivo con más cuerpo. Top 8 %, chin 48 %, head_h 39 %.
- **Cálculo:**
  - `td = 0.08`
  - `chin = 0.48` → `r = ((0.48 − 0.08) / 1.30)² = (0.308)² = 0.095`
  - `hh = 0.08 + 0.80 × √0.095 = 0.08 + 0.246 = 0.326`
- **Resultado:** `ratio=0.09, td=0.08, hh=0.32`
- **Verificación:** chin = 8 % + 1.30 × 0.308 = **48.0 %** ✓
- **head_h** = 1.30 × 0.308 = **40.0 %** ✓ (en PORTRAIT)

---

## 4. Tabla resumen (v3)

| Tamaño | ratio | td | hh | chin % | head_h % | Estándar |
|--------|-------|------|------|--------|----------|----------|
| Infantil 2.5×3 cm | **0.16** | 0.10 | 0.42 | 62 % | 52 % | SCHOOL |
| Pasaporte MX 3.5×4.5 cm | **0.33** | 0.09 | 0.55 | 84 % | 75 % | ICAO |
| Cartilla Militar 3.5×4.5 cm | **0.37** | 0.08 | 0.57 | 87 % | 79 % | ICAO |
| Visa Americana 5×5 cm | **0.19** | 0.10 | 0.45 | 67 % | 57 % | US_VISA |
| Visa Mexicana 2.5×3.5 cm | **0.33** | 0.09 | 0.55 | 84 % | 75 % | ICAO |
| Óvalo / Mignon 3.5×5 cm | **0.15** | 0.08 | 0.39 | 58 % | 50 % | SCHOOL |
| Diploma 5×7 cm | **0.12** | 0.08 | 0.36 | 52 % | 44 % | SCHOOL |
| Título Universitario 6×9 cm | **0.09** | 0.08 | 0.32 | 48 % | 40 % | PORTRAIT |

### 4.1 Diff contra v2 (qué se ajustó y por qué)

| Tamaño | v2 ratio | v3 ratio | Razón |
|--------|----------|----------|-------|
| Infantil | 0.43 | **0.16** | Cara al 85 % era incorrecto. Estilo mexicano pide ~52 %. |
| Pasaporte MX | 0.25 | **0.33** | Head_h 65 % estaba debajo del mínimo ICAO (69 %). |
| Cartilla | 0.27 | **0.37** | Subir al rango alto ICAO + un punto (estilo SEDENA). |
| Visa US | 0.18 | **0.19** | Ajuste fino (era casi correcto). |
| Visa MX | 0.25 | **0.33** | Igual corrección que Pasaporte (ambos ICAO). |
| Óvalo | 0.15 | 0.15 | Sin cambio. |
| Diploma | 0.13 | **0.12** | Ajuste fino (era casi correcto). |
| Título | 0.10 | **0.09** | Ajuste fino (era casi correcto). |

---

## 5. Clasificación por estándar (rangos de `head_h` permitidos)

Para que el overlay de cumplimiento (`compliance_overlay.py`) marque "OK" en
verde:

| Estándar | Rango `head_h` permitido | Tamaño(s) |
|----------|--------------------------|-----------|
| **TIGHT** | 80–95 % | (reservado, sin tamaño por defecto en v3) |
| **ICAO** | 60–85 % | Pasaporte MX, Cartilla Militar, Visa Mexicana |
| **US_VISA** | 50–70 % | Visa Americana |
| **SCHOOL** | 45–65 % | Infantil, Óvalo / Mignon, Diploma |
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

### 6.6 Si el cliente pide un estilo diferente al default

Si por ejemplo un cliente quiere estilo "extreme close-up" para infantil
(cara al 85 % como en la v2), simplemente sube el slider `head_measure_ratio`
a 0.43. Se guarda automáticamente en `/data/custom_sizes.json`.

---

## 7. Persistencia de los ajustes

Cada vez que tocas un slider, el nuevo valor se guarda automáticamente en
`/data/custom_sizes.json` (HF Spaces, persistente entre rebuilds) o en
`~/.cache/huggingface/retoka_custom_sizes.json` (local).

Los defaults del CSV siguen siendo los **primeros** valores que se usan cuando
nunca tocaste los sliders para un tamaño. Una vez que tocas cualquier slider,
el override gana hasta que presiones el botón **"Restablecer valores"** del
tamaño actual.

### Versionado del CSV

`custom_sizes_store.py` lleva una constante `CSV_VERSION` que se estampa en el
JSON. Si subimos `CSV_VERSION`, todos los overrides guardados con un
`CSV_VERSION` anterior se descartan y se vuelven a usar los defaults del CSV
(sin necesidad de tocar nada en la UI).

- **v1:** defaults originales (cara al 92 %, incorrectos para casi todo).
- **v2:** primer intento de calibración (cara todavía muy grande para
  Infantil, muy chica para Pasaporte).
- **v3:** defaults corregidos contra imagen de referencia real del cliente
  para Infantil y contra ICAO mid-range para Pasaporte/Cartilla.

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
- **Imagen de referencia para Infantil (foto-infantil-878x1024.webp):**
  archivo de muestra del cliente, dic. 2025. Estilo credencial escolar
  mexicana con top margin ~9 %, chin ~62 %, head_h ~53 %.
- **PEMEX / INE / UNAM** (para tamaños no-ICAO): cada universidad / dependencia
  tiene lineamientos internos no publicados oficialmente; se usa la convención
  de retrato académico estándar.
