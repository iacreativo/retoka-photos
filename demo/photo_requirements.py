# -*- coding: utf-8 -*-
"""
Requisitos oficiales por tamaño de foto de identificación.

Fuentes consultadas:
- ICAO Doc 9303 (estándar mundial de pasaportes / ICAO 9303)
- travel.state.gov — US Department of State (Visa, DS-160 / DS-1648)
- gob.mx / SRE — Pasaporte y Visa Mexicana
- INE / IFE — Credencial para Votar
- SEDENA — Cartilla del Servicio Militar Nacional
- SEP / UNAM — Foto escolar infantil mexicana
- Convenciones de estudio fotográfico profesional para Diploma y Título

Cada entrada tiene los mismos campos (en 5 idiomas):
  name, short_desc, use_for,
  pose, expression, gaze,
  background, clothing, accessories,
  face_position, recent,
  sources
"""

REQUIREMENTS = {
    # -----------------------------------------------------------
    # INFANTIL — Foto escolar mexicana 2.5x3 cm
    # -----------------------------------------------------------
    "Infantil 2.5x3 cm": {
        "es": {
            "name": "Foto Infantil (2.5×3 cm)",
            "use_for": "Kínder, primaria, secundaria — credenciales escolares, controles, exámenes.",
            "pose": "De frente, sentado o de pie con ambos hombros visibles.",
            "expression": "Sonrisa ligera o neutra. Niños pueden sonreír abiertamente.",
            "gaze": "Mirando directo a la cámara.",
            "background": "Blanco liso o azul muy claro (cielo). Sin sombras ni objetos.",
            "clothing": "Uniforme escolar o ropa casual de color oscuro/media. Evita camisetas blancas si el fondo es blanco.",
            "accessories": "Sin gorras ni lentes oscuros. Lentes oftálmicos sí (si los usa diario).",
            "face_position": "Cabeza completa dentro del marco. Cara ocupa ~60–70% del alto.",
            "recent": "Menos de 6 meses de antigüedad.",
            "sources": "SEP, Foto-estudios mexicanos, kínder y primarias.",
        },
        "en": {
            "name": "Children's ID Photo (2.5×3 cm)",
            "use_for": "School IDs, kindergarten through secondary, exams, report cards.",
            "pose": "Facing front, both shoulders visible.",
            "expression": "Slight or natural smile. Children may smile openly.",
            "gaze": "Looking directly at the camera.",
            "background": "Plain white or very light blue. No shadows or objects.",
            "clothing": "School uniform or dark/mid-tone casual clothes. Avoid white shirts on white backgrounds.",
            "accessories": "No hats or sunglasses. Prescription glasses OK if worn daily.",
            "face_position": "Whole head inside the frame. Face takes ~60–70% of height.",
            "recent": "Less than 6 months old.",
            "sources": "SEP, Mexican school photo studios.",
        },
        "zh": {
            "name": "儿童证件照 (2.5×3 cm)",
            "use_for": "墨西哥幼儿园至中学 — 学生证、考试、报告册。",
            "pose": "正面, 双肩可见。",
            "expression": "轻微或自然微笑, 儿童可开朗笑。",
            "gaze": "直视相机。",
            "background": "纯白或淡蓝背景, 无阴影。",
            "clothing": "校服或深色休闲装, 白底避免白衫。",
            "accessories": "不可戴帽子与墨镜, 日常眼镜可。",
            "face_position": "头部完整入画, 脸占约60–70%。",
            "recent": "6个月内拍摄。",
            "sources": "墨西哥教育部及儿童摄影惯例。",
        },
        "ja": {
            "name": "子供用証明写真 (2.5×3 cm)",
            "use_for": "メキシコ幼稚園〜中学校 — 学生証、試験、通知表。",
            "pose": "正面、両肩が見える。",
            "expression": "微笑または自然な笑顔、子供は自然な笑顔でOK。",
            "gaze": "カメラを真っ直ぐ見る。",
            "background": "無地白または薄い青、影なし。",
            "clothing": "制服または暗い色の私服、白背景では白シャツを避ける。",
            "accessories": "帽子・サングラス不可、普段使いの眼鏡は可。",
            "face_position": "頭がフレーム内、顔が約60–70%。",
            "recent": "6ヶ月以内。",
            "sources": "メキシコ教育省、子供向け写真スタジオ慣行。",
        },
        "ko": {
            "name": "어린이 신분증 사진 (2.5×3 cm)",
            "use_for": "멕시코 유치원~중학교 — 학생증, 시험, 성적표。",
            "pose": "정면, 양쪽 어깨 보임。",
            "expression": "가벼운 미소, 아이는 자연스러운 미소 가능。",
            "gaze": "카메라 정면 응시。",
            "background": "흰색 또는 연한 파란색, 그림자 없음。",
            "clothing": "교복 또는 어두운 색 캐주얼, 흰 배경엔 흰 옷 피함。",
            "accessories": "모자·선글라스 불가, 안경은 일상용이면 OK。",
            "face_position": "머리 전체 프레임 내, 얼굴 약60–70%。",
            "recent": "6개월 이내。",
            "sources": "멕시코 교육부, 어린이 사진관 관행。",
        },
    },

    # -----------------------------------------------------------
    # CREDENCIAL / PASAPORTE MX — 3.5x4.5 cm (ICAO 9303)
    # -----------------------------------------------------------
    "Credencial / Pasaporte MX 3.5x4.5 cm": {
        "es": {
            "name": "Credencial / Pasaporte Mexicano (3.5×4.5 cm)",
            "use_for": "Pasaporte mexicano, INE/IFE, credenciales oficiales que usan estándar ICAO.",
            "pose": "Frontal, hombros rectos y paralelos al suelo. Cuello visible.",
            "expression": "Neutral, boca cerrada SIN mostrar dientes. Cejas relajadas.",
            "gaze": "Directo a la cámara, ojos totalmente abiertos y descubiertos.",
            "background": "Blanco puro y uniforme, sin sombras ni texturas.",
            "clothing": "Color oscuro o medio (negro, marino, gris oscuro). Camisa con cuello.",
            "accessories": "SIN lentes (gafas) desde 2016. SIN gorras, sombreros o lentes de sol. Joyería mínima y que no toque el rostro.",
            "face_position": "Cabeza completa dentro del marco. Cara ocupa 50–69% del alto de la imagen. Ojos entre 56–69% desde la base.",
            "recent": "Menos de 6 meses, sin ediciones ni filtros.",
            "sources": "ICAO Doc 9303; SRE gob.mx/pasaporte; INE.",
        },
        "en": {
            "name": "Mexican Credential / Passport (3.5×4.5 cm)",
            "use_for": "Mexican passport, INE/IFE voter ID, official credentials following ICAO standard.",
            "pose": "Front-facing, shoulders straight and level. Neck visible.",
            "expression": "Neutral, mouth closed WITHOUT showing teeth. Relaxed eyebrows.",
            "gaze": "Looking straight at the camera, eyes fully open and uncovered.",
            "background": "Pure, uniform white. No shadows or textures.",
            "clothing": "Dark or mid-tone (black, navy, dark gray). Collared shirt.",
            "accessories": "NO glasses since 2016. NO hats, caps or sunglasses. Minimal jewelry, must not touch the face.",
            "face_position": "Full head inside the frame. Face fills 50–69% of image height. Eyes at 56–69% from the bottom.",
            "recent": "Less than 6 months old. No filters or edits.",
            "sources": "ICAO Doc 9303; SRE gob.mx/passport; INE.",
        },
        "zh": {
            "name": "墨西哥护照/身份证 (3.5×4.5 cm)",
            "use_for": "墨西哥护照、INE 选民证、其他 ICAO 标准证件。",
            "pose": "正面, 双肩水平, 颈部可见。",
            "expression": "中性, 闭嘴不露齿, 眉放松。",
            "gaze": "直视相机, 眼睛全开无遮挡。",
            "background": "纯白均匀背景, 无阴影。",
            "clothing": "深色或中色西装/衬衫, 有领。",
            "accessories": "2016 起不可戴眼镜, 不可戴帽/墨镜。饰品最小化且不接触面部。",
            "face_position": "头部完整, 脸占画面50–69%高, 眼睛距底边56–69%。",
            "recent": "6个月内, 不可修图。",
            "sources": "ICAO Doc 9303; 墨西哥外交部 SRE; INE。",
        },
        "ja": {
            "name": "メキシコID/パスポート (3.5×4.5 cm)",
            "use_for": "メキシコパスポート、INE(選挙証)、ICAO準拠の公的証明書。",
            "pose": "正面、肩水平、首見える。",
            "expression": "無表情、口を閉じ歯を見せない、眉リラックス。",
            "gaze": "カメラを真っ直ぐ、目全開で遮蔽なし。",
            "background": "純白均一、影なし。",
            "clothing": "暗い色または中色(黒・紺・濃灰)、襟付きシャツ。",
            "accessories": "2016年以降眼鏡不可、帽子・サングラス不可。装飾品は最小限で顔に触れない。",
            "face_position": "頭全体フレーム内、顔が画像高さの50–69%、目は下から56–69%。",
            "recent": "6ヶ月以内、加工不可。",
            "sources": "ICAO Doc 9303; メキシコ外務省(SRE); INE。",
        },
        "ko": {
            "name": "멕시코 신분증/여권 (3.5×4.5 cm)",
            "use_for": "멕시코 여권, INE 투표증, ICAO 표준 공문서。",
            "pose": "정면, 어깨 수평, 목 보임。",
            "expression": "무표정, 입 닫고 이 안 보임, 눈썹 이완。",
            "gaze": "카메라 정면 응시, 눈 완전 개방, 가림 없음。",
            "background": "순백 균일, 그림자 없음。",
            "clothing": "어두운 색 또는 중간색(검정·네이비·진회색), 칼라 있는 셔츠。",
            "accessories": "2016년부터 안경 불가, 모자·선글라스 불가. 장신구는 최소화하고 얼굴에 닿지 않게。",
            "face_position": "머리 전체 프레임 내, 얼굴이 이미지 높이의 50–69%, 눈은 하단에서 56–69%。",
            "recent": "6개월 이내, 보정 금지。",
            "sources": "ICAO Doc 9303; 멕시코 외무부(SRE); INE。",
        },
    },

    # -----------------------------------------------------------
    # CARTILLA MILITAR — 3.5x4.5 cm (SEDENA)
    # -----------------------------------------------------------
    "Cartilla Militar 3.5x4.5 cm": {
        "es": {
            "name": "Cartilla del Servicio Militar (3.5×4.5 cm)",
            "use_for": "Cartilla de identidad militar liberada por SEDENA.",
            "pose": "Frontal, cuello y hombros descubiertos (sin cuello alto).",
            "expression": "Neutral, boca cerrada. Sin bigote exagerado ni barba (preferible afeitado).",
            "gaze": "Directo a la cámara, ojos abiertos.",
            "background": "Blanco uniforme.",
            "clothing": "Ropa CIVIL formal — camisa con cuello o playera oscura. NO uniforme militar ni deportivo.",
            "accessories": "Sin gorras, lentes o gorras militares. Joyería discreta.",
            "face_position": "Cabeza completa visible, centrada. Cara ocupa ~50% del alto.",
            "recent": "Menos de 3 meses.",
            "sources": "SEDENA — Secretaría de la Defensa Nacional.",
        },
        "en": {
            "name": "Military Service Card (3.5×4.5 cm)",
            "use_for": "Military ID card issued by SEDENA.",
            "pose": "Front-facing, neck and shoulders uncovered (no turtleneck).",
            "expression": "Neutral, mouth closed. No heavy mustache or beard (clean-shaven preferred).",
            "gaze": "Directly at the camera, eyes open.",
            "background": "Uniform white.",
            "clothing": "CIVIL formal wear — collared shirt or dark t-shirt. NO military uniform or sports gear.",
            "accessories": "No caps, glasses or military hats. Discreet jewelry only.",
            "face_position": "Full head visible, centered. Face fills ~50% of height.",
            "recent": "Less than 3 months old.",
            "sources": "SEDENA — Mexican Ministry of National Defense.",
        },
        "zh": {
            "name": "墨西哥军役证 (3.5×4.5 cm)",
            "use_for": "墨西哥国防部(SEDENA)颁发的军役身份证。",
            "pose": "正面, 颈肩露出(勿穿高领)。",
            "expression": "中性闭嘴, 不留夸张胡须(建议刮净)。",
            "gaze": "直视相机, 眼睛睁开。",
            "background": "纯白均匀。",
            "clothing": "便装正装(衬衫/深色T恤), 禁穿军装或运动服。",
            "accessories": "无帽、眼镜、军帽, 饰品低调。",
            "face_position": "头部完整居中, 脸约占50%高。",
            "recent": "3个月内。",
            "sources": "墨西哥国防部 SEDENA。",
        },
        "ja": {
            "name": "メキシコ兵役証 (3.5×4.5 cm)",
            "use_for": "SEDENA発行の兵役IDカード。",
            "pose": "正面、首肩露出(タートルネック不可)。",
            "expression": "無表情、口閉じ。派手な口髭・髭なし(無精髭推奨)。",
            "gaze": "カメラ正面、目開。",
            "background": "均一白。",
            "clothing": "私服正装(襟シャツ/暗いTシャツ)、軍服やスポーツ服は不可。",
            "accessories": "帽子・眼鏡・軍帽不可、装飾品は控えめ。",
            "face_position": "頭全体中央、顔が約50%高さ。",
            "recent": "3ヶ月以内。",
            "sources": "メキシコ国防省 SEDENA。",
        },
        "ko": {
            "name": "멕시코 군복무 카드 (3.5×4.5 cm)",
            "use_for": "SEDENA 발급 군복무 신분증。",
            "pose": "정면, 목·어깨 노출(터틀넥 금지)。",
            "expression": "무표정, 입 닫음, 과도한 콧수염·수염 없음(면도 권장)。",
            "gaze": "카메라 정면, 눈 개방。",
            "background": "균일 흰색。",
            "clothing": "민정복(칼라 셔츠/어두운 티), 군복·스포츠웨어 금지。",
            "accessories": "모자·안경·군모 금지, 장신구 절제。",
            "face_position": "머리 전체 중앙, 얼굴 약50% 높이。",
            "recent": "3개월 이내。",
            "sources": "멕시코 국방부 SEDENA。",
        },
    },

    # -----------------------------------------------------------
    # VISA AMERICANA — 5x5 cm (US DS-160)
    # -----------------------------------------------------------
    "Visa Americana 5x5 cm": {
        "es": {
            "name": "Visa Americana (5×5 cm / 2×2\")",
            "use_for": "Trámite DS-160 / DS-1648 ante la embajada o consulado de EE.UU.",
            "pose": "Frontal, cuello y hombros visibles. Encuadre ligeramente más amplio que el rostro.",
            "expression": "Neutral, sin sonrisa amplia, boca cerrada, dientes no visibles.",
            "gaze": "Directo a la cámara, ojos abiertos y sin obstrucción.",
            "background": "Blanco puro, liso, sin sombras.",
            "clothing": "Color oscuro o medio. SIN uniformes, camuflaje ni ropa con charreteras/insignias.",
            "accessories": "SIN lentes (prohibidos desde 2016), gorras ni sombreros. Audífonos no. Pañoleta religiosa permitida si no oculta el rostro.",
            "face_position": "Cabeza completa (incluyendo pelo) entre 50% y 69% de la altura total. Ojos entre 56% y 69% desde la base. Centrado horizontalmente.",
            "recent": "Menos de 6 meses. Tamaño digital 600×600 a 1200×1200 px, JPEG, sRGB, ≤240 KB.",
            "sources": "US Department of State — travel.state.gov.",
        },
        "en": {
            "name": "US Visa Photo (5×5 cm / 2×2\")",
            "use_for": "DS-160 / DS-1648 form for US embassy or consulate.",
            "pose": "Front-facing, neck and shoulders visible. Slightly wider framing than just the face.",
            "expression": "Neutral, no wide smile, mouth closed, teeth not visible.",
            "gaze": "Directly at the camera, eyes open and unobstructed.",
            "background": "Pure white, plain, no shadows.",
            "clothing": "Dark or mid-tone. NO uniforms, camouflage or clothing with epaulettes/insignia.",
            "accessories": "NO glasses (banned since 2016), NO hats or caps. No headphones. Religious head covering allowed if it doesn't hide the face.",
            "face_position": "Head height (top of hair to chin) between 50% and 69% of image height. Eyes between 56% and 69% from the bottom. Horizontally centered.",
            "recent": "Less than 6 months old. Digital 600×600 to 1200×1200 px, JPEG, sRGB, ≤240 KB.",
            "sources": "US Department of State — travel.state.gov.",
        },
        "zh": {
            "name": "美国签证照 (5×5 cm / 2×2英寸)",
            "use_for": "DS-160 / DS-1648 美国使馆签证申请。",
            "pose": "正面, 颈肩可见, 比纯脸部稍宽。",
            "expression": "中性, 不大笑, 闭嘴不露齿。",
            "gaze": "直视相机, 眼睛无遮挡。",
            "background": "纯白均匀, 无阴影。",
            "clothing": "深色或中色, 禁军装/迷彩/肩章服。",
            "accessories": "2016 起禁戴眼镜, 无帽/头巾(宗教例外)。无耳机。",
            "face_position": "头顶到下巴占图高50–69%, 眼睛距底边56–69%, 水平居中。",
            "recent": "6个月内, 数字600×600–1200×1200 px, JPEG, sRGB, ≤240 KB。",
            "sources": "美国国务院 travel.state.gov。",
        },
        "ja": {
            "name": "米国ビザ写真 (5×5 cm / 2×2インチ)",
            "use_for": "DS-160 / DS-1648 米国大使館・領事館申請。",
            "pose": "正面、首肩見える、顔よりやや広め。",
            "expression": "中立、口閉じ、歯見せず、大笑いなし。",
            "gaze": "カメラ正面、目遮蔽なし。",
            "background": "純白、影なし。",
            "clothing": "暗い色または中色、軍服・迷彩・肩章付き服不可。",
            "accessories": "2016年以降眼鏡不可、帽子不可、宗教上のスカーフは顔を隠さなければ可。",
            "face_position": "頭頂~顎が画像高さの50–69%、目は下から56–69%、水平中央。",
            "recent": "6ヶ月以内、デジタル600×600~1200×1200 px、JPEG、sRGB、≤240 KB。",
            "sources": "米国国務省 travel.state.gov。",
        },
        "ko": {
            "name": "미국 비자 사진 (5×5 cm / 2×2인치)",
            "use_for": "DS-160 / DS-1648 미국 대사관·영사관 신청。",
            "pose": "정면, 목·어깨 보임, 얼굴보다 약간 넓게。",
            "expression": "무표정, 큰 미소 없음, 입 닫고 이 안 보임。",
            "gaze": "카메라 정면, 눈 가림 없음。",
            "background": "순백, 그림자 없음。",
            "clothing": "어두운 색 또는 중간색, 군복·카모·견장服 금지。",
            "accessories": "2016년부터 안경 금지, 모자 금지(종교 예외), 이어폰 금지。",
            "face_position": "머리꼭대기~턱이 이미지 높이 50–69%, 눈은 하단에서 56–69%, 수평 중앙。",
            "recent": "6개월 이내, 디지털 600×600–1200×1200 px, JPEG, sRGB, ≤240 KB。",
            "sources": "미국 국무부 travel.state.gov。",
        },
    },

    # -----------------------------------------------------------
    # VISA MEXICANA — 2.5x3.5 cm (SRE)
    # -----------------------------------------------------------
    "Visa Mexicana 2.5x3.5 cm": {
        "es": {
            "name": "Visa Mexicana (2.5×3.5 cm)",
            "use_for": "Visa de visitante sin permiso para realizar actividades remuneradas expedida por la SRE.",
            "pose": "Frontal, hombros rectos, cuello visible.",
            "expression": "Neutral, boca cerrada.",
            "gaze": "Directo a la cámara, ojos abiertos.",
            "background": "Blanco uniforme, sin sombras.",
            "clothing": "Ropa formal u oscura. NO uniformes.",
            "accessories": "Sin lentes, gorras ni lentes de sol.",
            "face_position": "Cabeza completa visible, centrada.",
            "recent": "Menos de 6 meses. Tamaño digital 413×531 px, 300 DPI, 100–500 KB.",
            "sources": "SRE — Secretaría de Relaciones Exteriores de México.",
        },
        "en": {
            "name": "Mexican Visa (2.5×3.5 cm)",
            "use_for": "Visitor visa issued by SRE (Mexican Secretary of Foreign Affairs).",
            "pose": "Front-facing, shoulders level, neck visible.",
            "expression": "Neutral, mouth closed.",
            "gaze": "Directly at the camera, eyes open.",
            "background": "Uniform white, no shadows.",
            "clothing": "Formal or dark clothing. NO uniforms.",
            "accessories": "No glasses, caps or sunglasses.",
            "face_position": "Full head visible, centered.",
            "recent": "Less than 6 months. Digital 413×531 px, 300 DPI, 100–500 KB.",
            "sources": "SRE — Mexican Secretary of Foreign Affairs.",
        },
        "zh": {
            "name": "墨西哥签证 (2.5×3.5 cm)",
            "use_for": "墨西哥外交部(SRE)签发的访客签证。",
            "pose": "正面, 双肩水平, 颈部可见。",
            "expression": "中性闭嘴。",
            "gaze": "直视相机, 眼睛睁开。",
            "background": "纯白均匀, 无阴影。",
            "clothing": "正装/深色, 禁军装。",
            "accessories": "无眼镜、帽子、墨镜。",
            "face_position": "头部完整居中。",
            "recent": "6个月内, 413×531 px, 300 DPI, 100–500 KB。",
            "sources": "墨西哥外交部 SRE。",
        },
        "ja": {
            "name": "メキシコビザ (2.5×3.5 cm)",
            "use_for": "メキシコ外務省(SRE)発行の訪問者ビザ。",
            "pose": "正面、肩水平、首見える。",
            "expression": "無表情、口閉じ。",
            "gaze": "カメラ正面、目開。",
            "background": "均一白、影なし。",
            "clothing": "フォーマルまたは暗い服、軍服不可。",
            "accessories": "眼鏡・帽子・サングラス不可。",
            "face_position": "頭全体中央。",
            "recent": "6ヶ月以内、413×531 px、300 DPI、100–500 KB。",
            "sources": "メキシコ外務省 SRE。",
        },
        "ko": {
            "name": "멕시코 비자 (2.5×3.5 cm)",
            "use_for": "멕시코 외무부(SRE) 발급 방문 비자。",
            "pose": "정면, 어깨 수평, 목 보임。",
            "expression": "무표정, 입 닫음。",
            "gaze": "카메라 정면, 눈 개방。",
            "background": "균일 흰색, 그림자 없음。",
            "clothing": "정장 또는 어두운 옷, 군복 금지。",
            "accessories": "안경·모자·선글라스 금지。",
            "face_position": "머리 전체 중앙。",
            "recent": "6개월 이내, 413×531 px, 300 DPI, 100–500 KB。",
            "sources": "멕시코 외무부 SRE。",
        },
    },

    # -----------------------------------------------------------
    # ÓVALO / MIGNON — 3.5x5 cm (tradicional escolar)
    # -----------------------------------------------------------
    "Óvalo / Credencial Mignon 3.5x5 cm": {
        "es": {
            "name": "Óvalo / Credencial Mignon (3.5×5 cm)",
            "use_for": "Credenciales escolares tipo óvalo, diplomas clásicos, retratos de estudio tradicionales.",
            "pose": "Frontal con leve giro permitido (3/4). Hombros visibles.",
            "expression": "Sonrisa suave o neutral.",
            "gaze": "Mirando a la cámara.",
            "background": "Blanco, gris claro o azul cielo.",
            "clothing": "Ropa formal: saco, blazer, camisa blanca, corbata opcional.",
            "accessories": "Lentes oftálmicos permitidos. Sin gorras.",
            "face_position": "Encuadre retrato clásico — cabeza + cuello + hombros. Cara ~50–60% del alto.",
            "recent": "Sin límite estricto, pero foto reciente.",
            "sources": "Convenciones de estudios fotográficos profesionales (escuela, retrato).",
        },
        "en": {
            "name": "Oval / Mignon Credential (3.5×5 cm)",
            "use_for": "Oval school credentials, classic diplomas, traditional studio portraits.",
            "pose": "Frontal, slight 3/4 turn allowed. Shoulders visible.",
            "expression": "Soft smile or neutral.",
            "gaze": "Looking at the camera.",
            "background": "White, light gray or sky blue.",
            "clothing": "Formal: blazer, white shirt, optional tie.",
            "accessories": "Prescription glasses allowed. No caps.",
            "face_position": "Classic portrait framing — head + neck + shoulders. Face ~50–60% of height.",
            "recent": "No strict limit, but recent.",
            "sources": "Professional studio conventions (school, portrait).",
        },
        "zh": {
            "name": "椭圆/迷你证件照 (3.5×5 cm)",
            "use_for": "椭圆学生证、传统毕业照、影楼肖像。",
            "pose": "正面或微3/4侧脸, 双肩可见。",
            "expression": "柔和微笑或中性。",
            "gaze": "看向相机。",
            "background": "白、浅灰或天蓝。",
            "clothing": "正装:西装、白衫、可选领带。",
            "accessories": "可戴日常眼镜, 无帽。",
            "face_position": "经典肖像构图 — 头+颈+肩, 脸约50–60%。",
            "recent": "无严格要求, 但需近期。",
            "sources": "专业影楼惯例。",
        },
        "ja": {
            "name": "オーバル/ミニョン (3.5×5 cm)",
            "use_for": "オーバル学生証、伝統的な卒業写真、スタジオ肖像。",
            "pose": "正面または軽い3/4、両肩見える。",
            "expression": "ソフトな微笑または中立。",
            "gaze": "カメラを見る。",
            "background": "白、薄グレーまたは空色。",
            "clothing": "フォーマル:ブレザー、白シャツ、ネクタイ任意。",
            "accessories": "普段使いの眼鏡可、帽子不可。",
            "face_position": "クラシック肖像フレーミング — 頭+首+肩、顔50–60%。",
            "recent": "厳密な期限なし、ただし最近。",
            "sources": "プロ写真スタジオ慣行。",
        },
        "ko": {
            "name": "타원/미뇽 신분증 (3.5×5 cm)",
            "use_for": "타원 학생증, 클래식 졸업사진, 스튜디오 초상。",
            "pose": "정면 또는 약간 3/4, 양쪽 어깨 보임。",
            "expression": "부드러운 미소 또는 무표정。",
            "gaze": "카메라 응시。",
            "background": "흰색, 연한 회색 또는 하늘색。",
            "clothing": "정장: 블레이저, 흰 셔츠, 넥타이 선택。",
            "accessories": "일상용 안경 가능, 모자 금지。",
            "face_position": "클래식 초상 프레이밍 — 머리+목+어깨, 얼굴 약50–60%。",
            "recent": "엄격한 기한 없음, 최근 촬영 권장。",
            "sources": "전문 사진관 관행。",
        },
    },

    # -----------------------------------------------------------
    # DIPLOMA — 5x7 cm (retrato de estudio)
    # -----------------------------------------------------------
    "Diploma 5x7 cm": {
        "es": {
            "name": "Foto para Diploma (5×7 cm)",
            "use_for": "Diplomas de preparatoria, secundaria, cursos, certificaciones.",
            "pose": "Retrato formal, cabeza + cuello + hombros. Cuello y clavículas visibles.",
            "expression": "Sonrisa leve o expresión seria y profesional.",
            "gaze": "Directa a la cámara, ojos brillantes.",
            "background": "Azul claro, blanco o gris muy claro (estudio).",
            "clothing": "Muy formal. Hombres: saco/blazer oscuro, camisa clara, corbata opcional. Mujeres: blazer o vestido formal.",
            "accessories": "Maquillaje suave. Joyería mínima. Lentes de armazón fino permitidos.",
            "face_position": "Retrato medio — cabeza completa, cara ocupa ~60% del alto. Centrada.",
            "recent": "Reciente (meses).",
            "sources": "Convenciones de estudio fotográfico profesional en México.",
        },
        "en": {
            "name": "Diploma Photo (5×7 cm)",
            "use_for": "High school, middle school or course diplomas and certifications.",
            "pose": "Formal portrait, head + neck + shoulders. Neck and collarbones visible.",
            "expression": "Slight smile or serious, professional look.",
            "gaze": "Direct at the camera, bright eyes.",
            "background": "Light blue, white or very light gray (studio).",
            "clothing": "Very formal. Men: dark blazer, light shirt, optional tie. Women: blazer or formal dress.",
            "accessories": "Soft makeup. Minimal jewelry. Thin-frame glasses allowed.",
            "face_position": "Half portrait — full head, face ~60% of height. Centered.",
            "recent": "Recent (within months).",
            "sources": "Mexican professional studio conventions.",
        },
        "zh": {
            "name": "毕业证书照 (5×7 cm)",
            "use_for": "中学/高中/课程毕业证书照。",
            "pose": "正式肖像, 头+颈+肩, 颈部锁骨可见。",
            "expression": "微笑或严肃专业。",
            "gaze": "直视相机, 眼睛明亮。",
            "background": "浅蓝、白或浅灰(影楼)。",
            "clothing": "很正式: 男深色西装+浅色衬衫+可选领带; 女西装或正装连衣裙。",
            "accessories": "淡妆, 饰品最少, 细框眼镜可。",
            "face_position": "半身肖像, 头完整, 脸约60%高, 居中。",
            "recent": "近期(数月内)。",
            "sources": "墨西哥专业影楼惯例。",
        },
        "ja": {
            "name": "卒業証書写真 (5×7 cm)",
            "use_for": "中学校・高校・課程の卒業証書・資格証明書。",
            "pose": "フォーマル肖像、頭+首+肩、首と鎖骨見える。",
            "expression": "微笑または真剣でプロフェッショナル。",
            "gaze": "カメラ正面、目に輝き。",
            "background": "薄青、白または薄グレー(スタジオ)。",
            "clothing": "とてもフォーマル。男性: 濃色ブレザー、淡色シャツ、ネクタイ任意。女性: ブレザーまたはフォーマルドレス。",
            "accessories": "薄化粧、装飾品最小、細枠眼鏡可。",
            "face_position": "ハーフポートレート — 頭全体、顔約60%高さ、中央。",
            "recent": "最近(数ヶ月)。",
            "sources": "メキシコのプロ写真スタジオ慣行。",
        },
        "ko": {
            "name": "졸업증 사진 (5×7 cm)",
            "use_for": "중·고교, 강좌 졸업증·자격증。",
            "pose": "정식 초상, 머리+목+어깨, 목·쇄골 보임。",
            "expression": "가벼운 미소 또는 진지한 프로페셔널。",
            "gaze": "카메라 정면, 눈빛 밝게。",
            "background": "연파랑, 흰색 또는 연회색(스튜디오)。",
            "clothing": "매우 정장. 남성: 진색 블레이저, 밝은 셔츠, 넥타이 선택. 여성: 블레이저 또는 정장 드레스。",
            "accessories": "은은한 메이크업, 장신구 최소, 가는 안경테 가능。",
            "face_position": "하프 초상 — 머리 전체, 얼굴 약60% 높이, 중앙。",
            "recent": "최근(수개월 이내)。",
            "sources": "멕시코 전문 사진관 관행。",
        },
    },

    # -----------------------------------------------------------
    # TÍTULO UNIVERSITARIO — 6x9 cm
    # -----------------------------------------------------------
    "Título universitario 6x9 cm": {
        "es": {
            "name": "Foto para Título Universitario (6×9 cm)",
            "use_for": "Título profesional universitario, cédula profesional, maestría, doctorado.",
            "pose": "Retrato formal estilo ejecutivo: cabeza, cuello y hombros amplios. Cuello y parte superior del pecho visibles.",
            "expression": "Seria, profesional y digna. Sonrisa MUY leve (opcional).",
            "gaze": "Directa a la cámara.",
            "background": "Azul claro (preferido), blanco o gris claro uniforme.",
            "clothing": "Hombres: traje oscuro (negro, marino o grafito), camisa blanca, corbata formal. Mujeres: saco/blazer oscuro o vestido formal de cuello.",
            "accessories": "Maquillaje sobrio. Joyería mínima y discreta. SIN lentes de sol. Lentes oftálmicos de armazón discreto sí.",
            "face_position": "Retrato medio-largo. Cara ~55–65% del alto. Centrada horizontalmente. Espacio libre arriba y abajo.",
            "recent": "Foto reciente, tomada en estudio profesional con buena iluminación.",
            "sources": "UNAM, IPN, universidades públicas y privadas de México — convenciones de titulación.",
        },
        "en": {
            "name": "University Degree Photo (6×9 cm)",
            "use_for": "University degree, professional license, master's or doctorate.",
            "pose": "Formal executive portrait: head, neck and wide shoulders. Neck and upper chest visible.",
            "expression": "Serious, professional and dignified. Very slight smile (optional).",
            "gaze": "Directly at the camera.",
            "background": "Light blue (preferred), white or light gray, uniform.",
            "clothing": "Men: dark suit (black, navy or charcoal), white shirt, formal tie. Women: dark blazer or formal collared dress.",
            "accessories": "Subtle makeup. Minimal, discreet jewelry. NO sunglasses. Discreet-frame prescription glasses OK.",
            "face_position": "Medium portrait. Face ~55–65% of height. Horizontally centered. Headroom above and below.",
            "recent": "Recent, taken in a professional studio with good lighting.",
            "sources": "UNAM, IPN, Mexican public and private universities — graduation conventions.",
        },
        "zh": {
            "name": "大学毕业证书照 (6×9 cm)",
            "use_for": "大学毕业证、专业证、硕士、博士。",
            "pose": "正式高管肖像: 头+颈+宽肩, 颈和上胸可见。",
            "expression": "严肃专业端庄, 可选极轻微笑。",
            "gaze": "直视相机。",
            "background": "浅蓝(首选)、白或浅灰均匀。",
            "clothing": "男:深色西装(黑/海军蓝/炭灰)、白衬衫、正式领带。女:深色西装外套或正式有领连衣裙。",
            "accessories": "妆感低调, 饰品最少且不张扬, 无墨镜, 低调镜框眼镜可。",
            "face_position": "中肖像, 脸约55–65%高, 水平居中, 上下留白。",
            "recent": "近期, 专业影楼拍摄。",
            "sources": "墨西哥 UNAM、IPN 及公私立大学毕业照惯例。",
        },
        "ja": {
            "name": "大学卒業証書写真 (6×9 cm)",
            "use_for": "大学卒業証、職業免許、修士・博士。",
            "pose": "フォーマル役員ポートレート: 頭+首+広い肩、首と上胸見える。",
            "expression": "真剣でプロフェッショナル・威厳、ごく軽い微笑も可。",
            "gaze": "カメラ正面。",
            "background": "薄青(推奨)、白または薄グレー、均一。",
            "clothing": "男性: ダークスーツ(黒/紺/チャコール)、白シャツ、フォーマルネクタイ。女性: ダークブレザーまたはフォーマル襟付きドレス。",
            "accessories": "控えめなメイク、最小控えめアクセサリー、サングラス不可、地味なフレームの眼鏡は可。",
            "face_position": "ハーフポートレート、顔55–65%高さ、水平中央、上下余白。",
            "recent": "最近、プロのスタジオ撮影。",
            "sources": "メキシコ UNAM、IPN、公私立大学の卒業写真慣行。",
        },
        "ko": {
            "name": "대학 졸업증명 사진 (6×9 cm)",
            "use_for": "대학 졸업증, 전문자격증, 석·박사。",
            "pose": "격식 있는 임원용 초상: 머리+목+넓은 어깨, 목과 윗가슴 보임。",
            "expression": "진지하고 프로페셔널·위엄, 아주 가벼운 미소도 가능。",
            "gaze": "카메라 정면。",
            "background": "연파랑(권장), 흰색 또는 연회색 균일。",
            "clothing": "남성: 어두운 정장(검정·네이비·차콜), 흰 셔츠, 격식 넥타이. 여성: 어두운 블레이저 또는 격식 있는 칼라 드레스。",
            "accessories": "은은한 메이크업, 절제된 장신구만, 선글라스 금지, 단정한 안경테 가능。",
            "face_position": "중반신 초상, 얼굴 약55–65% 높이, 수평 중앙, 상하 여백。",
            "recent": "최근, 전문 스튜디오 촬영。",
            "sources": "멕시코 UNAM, IPN, 공립·사립 대학 졸업 사진 관행。",
        },
    },
}


# ---------------------------------------------------------------
# Header texts (titles + intro) for the info panel
# ---------------------------------------------------------------
HEADERS = {
    "es": {
        "title": "ℹ️  Guía de la foto",
        "intro": "Requisitos oficiales para que la foto sea aceptada al primer intento.",
        "section_labels": {
            "use_for":      "📌  Se usa para",
            "pose":         "🧍  Postura",
            "expression":   "🙂  Expresión",
            "gaze":         "👀  Mirada",
            "background":   "🎨  Fondo",
            "clothing":     "👔  Ropa",
            "accessories":  "🕶  Lentes / accesorios",
            "face_position":"📏  Tamaño y posición del rostro",
            "recent":       "📅  Antigüedad",
            "sources":      "📚  Fuentes",
        },
        "default_msg": "Selecciona un tamaño para ver sus requisitos.",
    },
    "en": {
        "title": "ℹ️  Photo guide",
        "intro": "Official requirements so your photo is accepted on the first try.",
        "section_labels": {
            "use_for":      "📌  Used for",
            "pose":         "🧍  Pose",
            "expression":   "🙂  Expression",
            "gaze":         "👀  Gaze",
            "background":   "🎨  Background",
            "clothing":     "👔  Clothing",
            "accessories":  "🕶  Glasses / accessories",
            "face_position":"📏  Face size and position",
            "recent":       "📅  Recency",
            "sources":      "📚  Sources",
        },
        "default_msg": "Select a size to see its requirements.",
    },
    "zh": {
        "title": "ℹ️  拍摄指引",
        "intro": "官方要求, 让你的照片一次通过。",
        "section_labels": {
            "use_for":      "📌  用途",
            "pose":         "🧍  姿势",
            "expression":   "🙂  表情",
            "gaze":         "👀  视线",
            "background":   "🎨  背景",
            "clothing":     "👔  服装",
            "accessories":  "🕶  眼镜 / 配饰",
            "face_position":"📏  脸的大小与位置",
            "recent":       "📅  拍摄时间",
            "sources":      "📚  来源",
        },
        "default_msg": "请选择尺寸以查看要求。",
    },
    "ja": {
        "title": "ℹ️  撮影ガイド",
        "intro": "公式要件、初回の申請で受理されるためのご案内。",
        "section_labels": {
            "use_for":      "📌  用途",
            "pose":         "🧍  ポーズ",
            "expression":   "🙂  表情",
            "gaze":         "👀  視線",
            "background":   "🎨  背景",
            "clothing":     "👔  服装",
            "accessories":  "🕶  メガネ・アクセサリー",
            "face_position":"📏  顔のサイズと位置",
            "recent":       "📅  撮影時期",
            "sources":      "📚  出典",
        },
        "default_msg": "サイズを選択すると要件を表示します。",
    },
    "ko": {
        "title": "ℹ️  촬영 가이드",
        "intro": "첫 신청에서 통과할 수 있는 공식 요건。",
        "section_labels": {
            "use_for":      "📌  용도",
            "pose":         "🧍  자세",
            "expression":   "🙂  표정",
            "gaze":         "👀  시선",
            "background":   "🎨  배경",
            "clothing":     "👔  의상",
            "accessories":  "🕶  안경·소품",
            "face_position":"📏  얼굴 크기 및 위치",
            "recent":       "📅  촬영 시기",
            "sources":      "📚  출처",
        },
        "default_msg": "크기를 선택하면 요건이 표시됩니다。",
    },
}


def render_requirements(size_name: str, lang: str = "es") -> str:
    """
    Render the requirements panel as Markdown for the given size + language.
    Returns a default placeholder if size_name is unknown or has no entry.
    """
    headers = HEADERS.get(lang, HEADERS["es"])
    labels = headers["section_labels"]
    fallback = headers["default_msg"]

    if not size_name:
        return f"### {headers['title']}\n\n*{fallback}*"

    entry = REQUIREMENTS.get(size_name, {}).get(lang) or REQUIREMENTS.get(size_name, {}).get("es")
    if not entry:
        return f"### {headers['title']}\n\n*{fallback}*"

    lines = [f"### {headers['title']}", "", f"**{entry['name']}**", ""]
    lines.append(f"*{headers['intro']}*")
    lines.append("")

    field_order = [
        "use_for", "pose", "expression", "gaze",
        "background", "clothing", "accessories",
        "face_position", "recent", "sources",
    ]
    for field in field_order:
        if field in entry and entry[field]:
            lines.append(f"**{labels[field]}** — {entry[field]}")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"
