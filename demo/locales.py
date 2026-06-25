# Copyright 2024 the LlamaFactory team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from demo.utils import csv_to_size_list
from demo.config import load_configuration
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
size_list_dict_CN = csv_to_size_list(os.path.join(base_dir, "assets/size_list_CN.csv"))
size_list_dict_EN = csv_to_size_list(os.path.join(base_dir, "assets/size_list_EN.csv"))
size_list_dict_ES = csv_to_size_list(os.path.join(base_dir, "assets/size_list_ES.csv"))
(
    size_list_config_CN,
    size_list_config_EN,
    size_list_config_ES,
    color_list_dict_CN,
    color_list_dict_EN,
    color_list_dict_ES,
) = load_configuration(base_dir)


LOCALES = {
    "face_model": {
        "en": {"label": "Face detection model"},
        "zh": {"label": "人脸检测模型"},
        "ja": {"label": "顔検出モデル"},
        "ko": {"label": "얼굴 감지 모델"},
        "es": {"label": "Modelo de detección de cara"},
    },
    "matting_model": {
        "en": {"label": "Matting model"},
        "zh": {"label": "抠图模型"},
        "ja": {"label": "マッティングモデル"},
        "ko": {"label": "매팅 모델"},
        "es": {"label": "Modelo de recorte de fondo"},
    },
    "key_param": {
        "en": {"label": "Key Parameters"},
        "zh": {"label": "核心参数"},
        "ja": {"label": "主要パラメータ"},
        "ko": {"label": "주요 매개변수"},
        "es": {"label": "Parámetros principales"},
    },
    "advance_param": {
        "en": {"label": "Advance Parameters"},
        "zh": {"label": "高级参数"},
        "ja": {"label": "詳細パラメータ"},
        "ko": {"label": "고급 매개변수"},
        "es": {"label": "Parámetros avanzados"},
    },
    "size_mode": {
        "en": {
            "label": "ID photo size options",
            "choices": ["Size List", "Only Change BG", "Custom(px)", "Custom(mm)"],
            "custom_size_eror": "The width should not be greater than the length; the length and width should not be less than 100, and no more than 1800.",
        },
        "zh": {
            "label": "证件照尺寸选项",
            "choices": ["尺寸列表", "只换底", "自定义(px)", "自定义(mm)"],
            "custom_size_eror": "宽度不应大于长度；长度和宽度不应小于100，不大于1800。",
        },
        "ja": {
            "label": "証明写真サイズオプション",
            "choices": [
                "サイズリスト",
                "背景のみ変更",
                "カスタムサイズ(px)",
                "カスタムサイズ(mm)",
            ],
            "custom_size_eror": "幅は長さより大きくしないでください。長さと幅は100以上1800以下にしてください。",
        },
        "ko": {
            "label": "증명사진 크기 옵션",
            "choices": [
                "크기 목록",
                "배경만 변경",
                "사용자 지정(px)",
                "사용자 지정(mm)",
            ],
            "custom_size_eror": "너비는 길이보다 크지 않아야 합니다; 길이와 너비는 100 이상 1800 이하여야 합니다.",
        },
        "es": {
            "label": "Opciones de tamaño de la foto",
            "choices": [
                "Lista de tamaños",
                "Solo cambiar fondo",
                "Personalizado (px)",
                "Personalizado (mm)",
            ],
            "custom_size_eror": "El ancho no debe ser mayor que el alto; el alto y el ancho no deben ser menores a 100, ni mayores a 1800.",
        },
    },
    "custom_size_px": {
        "en": {"height": "Height(px)", "width": "Width(px)"},
        "zh": {"height": "高度(px)", "width": "宽度(px)"},
        "ja": {"height": "高さ(px)", "width": "幅(px)"},
        "ko": {"height": "높이(px)", "width": "너비(px)"},
        "es": {"height": "Alto (px)", "width": "Ancho (px)"},
    },
    "custom_size_mm": {
        "en": {"height": "Height(mm)", "width": "Width(mm)"},
        "zh": {"height": "高度(mm)", "width": "宽度(mm)"},
        "ja": {"height": "高さ(mm)", "width": "幅(mm)"},
        "ko": {"height": "높이(mm)", "width": "너비(mm)"},
        "es": {"height": "Alto (mm)", "width": "Ancho (mm)"},
    },
    "size_list": {
        "en": {
            "label": "Size list",
            "choices": list(size_list_dict_EN.keys()),
            "develop": size_list_config_EN,
        },
        "zh": {
            "label": "预设尺寸",
            "choices": list(size_list_dict_CN.keys()),
            "develop": size_list_config_CN,
        },
        "ja": {
            "label": "サイズリスト",
            "choices": list(size_list_dict_EN.keys()),
            "develop": size_list_config_EN,
        },
        "ko": {
            "label": "크기 목록",
            "choices": list(size_list_dict_EN.keys()),
            "develop": size_list_config_EN,
        },
        "es": {
            "label": "Tamaño del documento",
            "choices": list(size_list_dict_ES.keys()),
            "develop": size_list_config_ES,
        },
    },
    "bg_color": {
        "en": {
            "label": "Background color",
            "choices": list(color_list_dict_EN.keys()) + ["American Style"] + ["Custom(RGB)", "Custom(HEX)"],
            "develop": color_list_dict_EN,
        },
        "zh": {
            "label": "背景颜色",
            "choices": list(color_list_dict_CN.keys()) + ["美式证件照"] + ["自定义(RGB)", "自定义(HEX)"],
            "develop": color_list_dict_CN,
        },
        "ja": {
            "label": "背景色",
            "choices": list(color_list_dict_EN.keys()) + ["American Style"] + ["カスタム(RGB)", "カスタム(HEX)"],
            "develop": color_list_dict_EN,
        },
        "ko": {
            "label": "배경색",
            "choices": list(color_list_dict_EN.keys()) + ["American Style"] + ["사용자 지정(RGB)", "사용자 지정(HEX)"],
            "develop": color_list_dict_EN,
        },
        "es": {
            "label": "Color de fondo",
            "choices": list(color_list_dict_ES.keys()) + ["Estilo americano"] + ["Personalizado (RGB)", "Personalizado (HEX)"],
            "develop": color_list_dict_ES,
        },
    },
    "button": {
        "en": {"label": "Start"},
        "zh": {"label": "开始制作"},
        "ja": {"label": "開始"},
        "ko": {"label": "시작"},
        "es": {"label": "Generar foto"},
    },
    "head_measure_ratio": {
        "en": {"label": "Head ratio"},
        "zh": {"label": "面部比例"},
        "ja": {"label": "頭部比率"},
        "ko": {"label": "머리 비율"},
        "es": {"label": "Proporción de la cabeza"},
    },
    "top_distance": {
        "en": {"label": "Top distance"},
        "zh": {"label": "头距顶距离"},
        "ja": {"label": "上部からの距離"},
        "ko": {"label": "상단 거리"},
        "es": {"label": "Distancia al borde superior"},
    },
    "image_kb": {
        "en": {"label": "Set KB size", "choices": ["Not Set", "Custom"]},
        "zh": {"label": "设置 KB 大小", "choices": ["不设置", "自定义"]},
        "ja": {"label": "KBサイズを設定", "choices": ["設定なし", "カスタム"]},
        "ko": {"label": "KB 크기 설정", "choices": ["설정 안 함", "사용자 지정"]},
        "es": {"label": "Tamaño en KB", "choices": ["Sin límite", "Personalizado"]},
    },
    "image_kb_size": {
        "en": {"label": "KB size"},
        "zh": {"label": "KB 大小"},
        "ja": {"label": "KBサイズ"},
        "ko": {"label": "KB 크기"},
        "es": {"label": "Tamaño en KB"},
    },
    "image_dpi": {
        "en": {"label": "Set DPI", "choices": ["Not Set", "Custom"]},
        "zh": {"label": "设置 DPI 大小", "choices": ["不设置", "自定义"]},
        "ja": {"label": "DPIを設定", "choices": ["設定なし", "カスタム"]},
        "ko": {"label": "DPI 설정", "choices": ["설정 안 함", "사용자 지정"]},
        "es": {"label": "Calidad de impresión (DPI)", "choices": ["Sin configurar", "Personalizado"]},
    },
    "image_dpi_size": {
        "en": {"label": "DPI size"},
        "zh": {"label": "DPI 大小"},
        "ja": {"label": "DPIサイズ"},
        "ko": {"label": "DPI 크기"},
        "es": {"label": "DPI"},
    },
    "render_mode": {
        "en": {
            "label": "Render mode",
            "choices": [
                "Solid Color",
                "Up-Down Gradient (White)",
                "Center Gradient (White)",
            ],
        },
        "zh": {
            "label": "渲染方式",
            "choices": ["纯色", "上下渐变（白色）", "中心渐变（白色）"],
        },
        "ja": {
            "label": "レンダリングモード",
            "choices": [
                "単色",
                "上下グラデーション（白）",
                "中心グラデーション（白）",
            ],
        },
        "ko": {
            "label": "렌더링 모드",
            "choices": [
                "단색",
                "위-아래 그라데이션 (흰색)",
                "중앙 그라데이션 (흰색)",
            ],
        },
        "es": {
            "label": "Estilo del fondo",
            "choices": [
                "Color sólido",
                "Degradado vertical (blanco)",
                "Degradado radial (blanco)",
            ],
        },
    },
    # Tab3 - 水印工作台
    "watermark_tab": {
        "en": {"label": "Watermark"},
        "zh": {"label": "水印"},
        "ja": {"label": "ウォーターマーク"},
        "ko": {"label": "워터마크"},
        "es": {"label": "Marca de agua"},
    },
    "watermark_text": {
        "en": {"label": "Text", "value": "Hello", "placeholder": "up to 20 characters"},
        "zh": {"label": "水印文字", "value": "Hello", "placeholder": "最多20个字符"},
        "ja": {"label": "テキスト", "value": "Hello", "placeholder": "最大20文字"},
        "ko": {"label": "텍스트", "value": "Hello", "placeholder": "최대 20자"},
        "es": {"label": "Texto", "value": "Retoka", "placeholder": "máx. 20 caracteres"},
    },
    "watermark_color": {
        "en": {"label": "Color"},
        "zh": {"label": "水印颜色"},
        "ja": {"label": "色"},
        "ko": {"label": "색상"},
        "es": {"label": "Color"},
    },
    "watermark_size": {
        "en": {"label": "Size"},
        "zh": {"label": "文字大小"},
        "ja": {"label": "サイズ"},
        "ko": {"label": "크기"},
        "es": {"label": "Tamaño"},
    },
    "watermark_opacity": {
        "en": {"label": "Opacity"},
        "zh": {"label": "水印透明度"},
        "ja": {"label": "不透明度"},
        "ko": {"label": "불투도"},
        "es": {"label": "Opacidad"},
    },
    "watermark_angle": {
        "en": {"label": "Angle"},
        "zh": {"label": "水印角度"},
        "ja": {"label": "角度"},
        "ko": {"label": "각도"},
        "es": {"label": "Ángulo"},
    },
    "watermark_space": {
        "en": {"label": "Space"},
        "zh": {"label": "水印间距"},
        "ja": {"label": "間隔"},
        "ko": {"label": "간격"},
        "es": {"label": "Espaciado"},
    },
    "watermark_switch": {
        "en": {"label": "Watermark", "value": "Not Add", "choices": ["Not Add", "Add"]},
        "zh": {"label": "水印", "value": "不添加", "choices": ["不添加", "添加"]},
        "ja": {"label": "ウォーターマーク", "value": "追加しない", "choices": ["追加しない", "追加"]},
        "ko": {"label": "워터마크", "value": "추가하지 않음", "choices": ["추가하지 않음", "추가"]},
        "es": {"label": "Marca de agua", "value": "Sin marca", "choices": ["Sin marca", "Agregar"]},
    },
    # 输出结果
    "notification": {
        "en": {
            "label": "notification",
            "face_error": "The number of faces is not equal to 1, please upload an image with a single face. If the actual number of faces is 1, it may be an issue with the accuracy of the detection model. Please switch to a different face detection model on the left or raise a Github Issue to notify the author.",
        },
        "zh": {
            "label": "通知",
            "face_error": "人脸数不等于1，请上传单人照片。如果实际人脸数为1，可能是检测模型的准确度问题，请切换左侧不同的人脸检测模型或提出Github Issue通知作者。",
        },
        "ja": {
            "label": "通知",
            "face_error": "顔の数が1ではありません。1つの顔を含む画像をアップロードしてください。実際の顔の数が1の場合、検出モデルの精度の問題かもしれません。左側で別の顔検出モデルに切り替えるか、Githubの問題を作成して作者に通知してください。",
        },
        "ko": {
            "label": "알림",
            "face_error": "얼굴 수가 1이 아닙니다. 단일 얼굴이 있는 이미지를 업로드해 주세요. 실제 얼굴 수가 1인 경우 감지 모델의 정확도 문제일 수 있습니다. 왼쪽에서 다른 얼굴 감지 모델로 전환하거나 Github Issue를 제기하여 작성자에게 알려주세요.",
        },
        "es": {
            "label": "Aviso",
            "face_error": "No se detectó exactamente una cara. Sube una imagen con una sola cara. Si tu imagen sí tiene una sola cara, puede ser un problema de precisión del modelo. Prueba cambiando el modelo de detección en el panel izquierdo o repórtalo al autor.",
        },
    },
    "standard_photo": {
        "en": {"label": "Standard photo"},
        "zh": {"label": "标准照"},
        "ja": {"label": "標準写真"},
        "ko": {"label": "표준 사진"},
        "es": {"label": "Foto estándar"},
    },
    "hd_photo": {
        "en": {"label": "HD photo"},
        "zh": {"label": "高清照"},
        "ja": {"label": "HD写真"},
        "ko": {"label": "HD 사진"},
        "es": {"label": "Foto en HD"},
    },
    "standard_photo_png": {
        "en": {"label": "Matting Standard photo"},
        "zh": {"label": "透明标准照"},
        "ja": {"label": "マッティング標準写真"},
        "ko": {"label": "매팅 표준 사진"},
        "es": {"label": "Foto estándar (PNG transparente)"},
    },
    "hd_photo_png": {
        "en": {"label": "Matting HD photo"},
        "zh": {"label": "透明高清照"},
        "ja": {"label": "マッティングHD写真"},
        "ko": {"label": "매팅 HD 사진"},
        "es": {"label": "Foto HD (PNG transparente)"},
    },
    "layout_photo": {
        "en": {"label": "Layout photo"},
        "zh": {"label": "排版照"},
        "ja": {"label": "レイアウト写真"},
        "ko": {"label": "레이아웃 사진"},
        "es": {"label": "Layout de impresión"},
    },
    "download": {
        "en": {"label": "Download the photo after adjusting the DPI or KB size"},
        "zh": {"label": "下载调整 DPI 或 KB 大小后的照片"},
        "ja": {"label": "DPIまたはKBサイズ調整後の写真をダウンロード"},
        "ko": {"label": "DPI 또는 KB 크기 조정 후 사진 다운로드"},
        "es": {"label": "Descarga la foto después de ajustar el DPI o el peso en KB"},
    },
    "matting_image": {
        "en": {"label": "Matting image"},
        "zh": {"label": "抠图图像"},
        "ja": {"label": "マット画像"},
        "ko": {"label": "매팅 이미지"},
        "es": {"label": "Imagen recortada"},
    },
    "beauty_tab": {
        "en": {"label": "Beauty"},
        "zh": {"label": "美颜"},
        "ja": {"label": "美顔"},
        "ko": {"label": "뷰티"},
        "es": {"label": "Retoque"},
    },
    "whitening_strength": {
        "en": {"label": "whitening strength"},
        "zh": {"label": "美白强度"},
        "ja": {"label": "美白強度"},
        "ko": {"label": "미백 강도"},
        "es": {"label": "Aclarado de piel"},
    },
    "brightness_strength": {
        "en": {"label": "brightness strength"},
        "zh": {"label": "亮度强度"},
        "ja": {"label": "明るさの強さ"},
        "ko": {"label": "밝기 강도"},
        "es": {"label": "Brillo"},
    },
    "contrast_strength": {
        "en": {"label": "contrast strength"},
        "zh": {"label": "对比度强度"},
        "ja": {"label": "コントラスト強度"},
        "ko": {"label": "대비 강도"},
        "es": {"label": "Contraste"},
    },
    "sharpen_strength": {
        "en": {"label": "sharpen strength"},
        "zh": {"label": "锐化强度"},
        "ja": {"label": "シャープ化強度"},
        "ko": {"label": "샤프 강도"},
        "es": {"label": "Nitidez"},
    },
    "saturation_strength": {
        "en": {"label": "saturation strength"},
        "zh": {"label": "饱和度强度"},
        "ja": {"label": "飽和度強度"},
        "ko": {"label": "포화도 강도"},
        "es": {"label": "Saturación"},
    },
    "plugin": {
        "en": {
            "label": "🤖Plugin",
            "choices": ["Face Alignment", "Horizontal Flip", "Layout Photo Crop Line", "JPEG Format", "Five Inch Paper"],
            "value": ["Layout Photo Crop Line"]
        },
        "zh": {
            "label": "🤖插件",
            "choices": ["人脸旋转对齐", "水平翻转", "排版照裁剪线", "JPEG格式"],
            "value": ["排版照裁剪线"]
        },
        "ja": {
            "label": "🤖プラグイン",
            "choices": ["顔の整列", "水平反転", "レイアウト写真の切り取り線", "JPEGフォーマット"],
            "value": ["レイアウト写真の切り取り線"]
        },
        "ko": {
            "label": "🤖플러그인",
            "choices": ["얼굴 정렬", "수평 반전", "레이아웃 사진 자르기 선", "JPEG 포맷", "오렌지 사진"],
            "value": ["레이아웃 사진 자르기 선"]
        },
        "es": {
            "label": "🤖Opciones extra",
            "choices": ["Alinear cara", "Voltear horizontal", "Líneas de corte en layout", "Formato JPEG", "Papel 5 pulgadas"],
            "value": ["Líneas de corte en layout"]
        },
    },
    "template_photo": {
        "en": {"label": "Social Media Template Photo"},
        "zh": {"label": "社交媒体模版照"},
        "ja": {"label": "SNS テンプレート写真"},
        "ko": {"label": "SNS 템플릿 사진"},
        "es": {"label": "Plantilla para redes sociales"},
    },
    "print_tab": {
        "en": {"label": "Print Layout"},
        "zh": {"label": "打印排版"},
        "ja": {"label": "印刷レイアウト"},
        "ko": {"label": "인쇄 레이아웃"},
        "es": {"label": "Imprimir (4x6)"},
    },
    "print_switch": {
        "shape": [
            [1205, 1795],
            [1051, 1500],
            [2479, 3508],
            [1205, 1795, "half-left"],
        ],
        "en": {"label": "Paper size", "choices": ["6 inch", "5 inch", "A4", "4x6 half sheet (6 photos, reuse paper)"]},
        "zh": {"label": "相纸选择", "choices": ["六寸", "五寸", "A4", "4x6 半页 (6 张,可复用)"]},
        "ja": {"label": "用紙サイズ", "choices": ["6インチ", "5インチ", "A4", "4x6 半分 (6枚、再利用可)"]},
        "ko": {"label": "용지 사이즈", "choices": ["6인치", "5인치", "A4", "4x6 반장 (6장, 재활용)"]},
        "es": {"label": "Tamaño del papel", "choices": ["6 pulgadas (4x6)", "5 pulgadas", "A4", "4x6 media hoja (6 fotos, reutilizable)"]},
    },
}
