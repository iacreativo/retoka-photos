import gradio as gr
import os
import pathlib
from demo.locales import LOCALES
from demo.processor import IDPhotoProcessor
from demo.photo_requirements import render_requirements as render_reqs

"""
只裁切模式:
1. 如果重新上传了照片，然后点击按钮，第一次会调用不裁切的模式，第二次会调用裁切的模式
"""


def load_description(fp):
    """
    加载title.md文件作为Demo的顶部栏
    """
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def create_ui(
    processor: IDPhotoProcessor,
    root_dir: str,
    human_matting_models: list,
    face_detect_models: list,
    language: list,
    return_extras: bool = False,
):
    # When return_extras=True, returns (demo, css_string)
    # When False (default), returns just demo (backward compat)

    # 加载环境变量DEFAULT_LANG, 如果有且在language中，则将DEFAULT_LANG设置为环境变量
    if "DEFAULT_LANG" in os.environ and os.environ["DEFAULT_LANG"] in language:
        DEFAULT_LANG = os.environ["DEFAULT_LANG"]
    else:
        DEFAULT_LANG = language[0]

    DEFAULT_HUMAN_MATTING_MODEL = "modnet_photographic_portrait_matting"
    DEFAULT_FACE_DETECT_MODEL = "retinaface-resnet50"

    if DEFAULT_HUMAN_MATTING_MODEL in human_matting_models:
        human_matting_models.remove(DEFAULT_HUMAN_MATTING_MODEL)
        human_matting_models.insert(0, DEFAULT_HUMAN_MATTING_MODEL)

    if DEFAULT_FACE_DETECT_MODEL not in face_detect_models:
        DEFAULT_FACE_DETECT_MODEL = "mtcnn"

    # Retoka custom CSS — DARK GRAY theme, SOFT WHITE text, easy on the eyes
    # Gradio 6.x renders radio/checkbox as: <label class="checkbox-container"><input/><span class="label-text">...</span></label>
    retoka_css = """
    /* === Retoka brand: DARK GRAY theme, easy on the eyes === */

    /* === Override Gradio 6 theme variables === */
    :root, .gradio-container {
        --checkbox-background-color: #2f3239;
        --checkbox-background-color-hover: #3a3d44;
        --checkbox-background-color-focus: #2f3239;
        --checkbox-background-color-selected: #f1f5f9;
        --checkbox-border-color: #4a4d54;
        --checkbox-border-color-hover: #60a5fa;
        --checkbox-border-color-focus: #60a5fa;
        --checkbox-check: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><path d='M13.5 4.5L6 12L2.5 8.5' stroke='%231f2126' stroke-width='2.5' fill='none' stroke-linecap='round' stroke-linejoin='round'/></svg>");
        --radio-circle: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><circle cx='8' cy='8' r='3' fill='%231f2126'/></svg>");
        --body-text-color: #f1f5f9;
        --body-text-color-subdued: #94a3b8;
        --block-label-text-color: #e2e8f0;
    }

    /* App background — soft dark gray gradient (not pure black) */
    .gradio-container, .app {
        background: linear-gradient(180deg, #1f2126 0%, #2a2d33 100%) !important;
        color: #f1f5f9 !important;
    }

    /* All text soft-white by default (not pure white — gentler on eyes) */
    body, p, span, div, label, li, td, th,
    .gr-block, .gr-panel, .gr-form, .gr-input, .gr-button, .gr-box,
    .prose, .prose p, .prose li, .prose h1, .prose h2, .prose h3,
    .prose h4, .prose h5, .prose h6, .prose strong, .prose code {
        color: #f1f5f9 !important;
    }

    /* === Title with Retoka gradient (blue -> cyan, soft on dark) === */
    h1, .prose h1 {
        background: linear-gradient(135deg, #60a5fa, #22d3ee) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }

    /* === Primary button — soft BLUE gradient === */
    .primary, button.primary, .gr-button-primary {
        background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%) !important;
        border: none !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        letter-spacing: 0.5px !important;
        padding: 12px 28px !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.35) !important;
        text-transform: none !important;
        transition: all 0.2s ease !important;
    }
    .primary:hover, button.primary:hover, .gr-button-primary:hover {
        background: linear-gradient(135deg, #60a5fa 0%, #22d3ee 100%) !important;
        box-shadow: 0 6px 20px rgba(96, 165, 250, 0.5) !important;
        transform: translateY(-1px) !important;
        color: #ffffff !important;
    }

    /* === Info panel: requisitos del tamaño elegido === */
    #size_requirements_panel {
        background: linear-gradient(180deg, #1f2126 0%, #262a31 100%) !important;
        border: 1px solid #3a3f4a !important;
        border-left: 4px solid #22d3ee !important;
        border-radius: 10px !important;
        padding: 16px 20px !important;
        margin-top: 12px !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25) !important;
    }
    #size_requirements_panel h3,
    #size_requirements_panel h3 *,
    #size_requirements_panel strong,
    #size_requirements_panel p,
    #size_requirements_panel em,
    #size_requirements_panel li {
        color: #e2e8f0 !important;
    }
    #size_requirements_panel h3 {
        color: #22d3ee !important;
        font-size: 18px !important;
        margin-top: 0 !important;
        margin-bottom: 8px !important;
        font-weight: 700 !important;
    }
    #size_requirements_panel strong {
        color: #60a5fa !important;
        font-weight: 600 !important;
    }

    /* === Tabs — soft blue bottom border for selected === */
    .tab-nav, [role="tablist"] {
        border-bottom: 2px solid #3f4451 !important;
    }
    .tab-nav button, .tabitem, [role="tab"] {
        color: #94a3b8 !important;
        background: transparent !important;
        font-weight: 500 !important;
        padding: 12px 20px !important;
    }
    .tab-nav button.selected, .tabitem.selected,
    [role="tab"][aria-selected="true"] {
        color: #f1f5f9 !important;
        background: #2f3239 !important;
        border-bottom: 3px solid #60a5fa !important;
        font-weight: 600 !important;
    }

    /* === Cards/panels — gray with subtle border === */
    .block, .gr-panel, .gr-box, .form, .container {
        background: #2f3239 !important;
        border: 1px solid #3f4451 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
    }

    /* === Inputs — darker gray bg, soft-white text, blue focus === */
    input, textarea, select,
    .gr-input, .gr-text-input, .gr-number-input,
    input[type="text"], input[type="number"], input[type="search"] {
        background: #26282e !important;
        border: 1.5px solid #4a4d54 !important;
        color: #f1f5f9 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 14px !important;
    }
    input::placeholder, textarea::placeholder {
        color: #6b7280 !important;
    }
    input:focus, textarea:focus, select:focus {
        border-color: #60a5fa !important;
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.2) !important;
        outline: none !important;
    }
    /* Dropdown closed state */
    .gr-dropdown .gr-dropdown-value, .gr-dropdown input {
        color: #f1f5f9 !important;
        background: #26282e !important;
    }
    /* Dropdown opened options */
    .gr-dropdown-options, .gr-dropdown-items,
    .gr-dropdown-options-list, ul.options, [role="listbox"] {
        background: #2f3239 !important;
        border: 1px solid #4a4d54 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
    }
    .gr-dropdown-options .gr-dropdown-option,
    .gr-dropdown-items .gr-dropdown-item, [role="option"] {
        background: #2f3239 !important;
        color: #f1f5f9 !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
    }
    .gr-dropdown-options .gr-dropdown-option:hover,
    .gr-dropdown-items .gr-dropdown-item:hover,
    [role="option"]:hover {
        background: #3a3d44 !important;
        color: #f1f5f9 !important;
    }
    .gr-dropdown-options .gr-dropdown-option.selected,
    [role="option"][aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #06b6d4) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* === Labels — soft white === */
    label, .gr-form-label, span.label, .label-wrap,
    .gradio-dropdown label, .gradio-radio > label, .gradio-checkbox > label,
    .gradio-radio .label-text, .gradio-checkbox .label-text {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* === Radio buttons & checkboxes — Gradio 6 structure === */
    /* In Gradio 6, structure is:
       <label class="checkbox-container">
         <input type="radio" />
         <span class="label-text">Option text</span>
       </label>
    */

    /* Unselected label text — medium gray */
    .checkbox-container .label-text {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }

    /* SELECTED: when the input inside the label is checked, style the whole label */
    .checkbox-container:has(input:checked) {
        background: #3a3d44 !important;
        border-radius: 6px !important;
        padding: 4px 8px !important;
        outline: 1px solid #4a4d54 !important;
    }
    .checkbox-container:has(input:checked) .label-text {
        color: #f1f5f9 !important;
        font-weight: 800 !important;
    }
    .checkbox-container:has(input:checked) input {
        background-color: #f1f5f9 !important;
        border-color: #f1f5f9 !important;
        accent-color: #f1f5f9 !important;
    }
    /* Fallback for browsers without :has() support */
    .checkbox-container.selected,
    .checkbox-container.checked {
        background: #3a3d44 !important;
        border-radius: 6px !important;
        padding: 4px 8px !important;
    }
    .checkbox-container.selected .label-text,
    .checkbox-container.checked .label-text {
        color: #f1f5f9 !important;
        font-weight: 800 !important;
    }
    .checkbox-container.selected input,
    .checkbox-container.checked input {
        background-color: #f1f5f9 !important;
        border-color: #f1f5f9 !important;
    }
    /* Fallback selector: input checked sibling */
    input[type="radio"]:checked ~ .label-text,
    input[type="checkbox"]:checked ~ .label-text {
        color: #f1f5f9 !important;
        font-weight: 800 !important;
    }
    /* Fallback: by aria-checked */
    [role="radio"][aria-checked="true"] .label-text,
    [role="checkbox"][aria-checked="true"] .label-text {
        color: #f1f5f9 !important;
        font-weight: 800 !important;
    }
    /* Direct check via :checked attribute */
    input[type="radio"]:checked, input[type="checkbox"]:checked {
        background-color: #f1f5f9 !important;
        border-color: #f1f5f9 !important;
    }
    /* Native accent for browser-rendered check/radio */
    input[type="radio"], input[type="checkbox"] {
        accent-color: #60a5fa !important;
    }

    /* === Sliders === */
    input[type="range"] {
        accent-color: #60a5fa !important;
    }

    /* === Image containers === */
    .image-container, .image-frame, .gradio-image {
        border: 2px dashed #4a4d54 !important;
        border-radius: 12px !important;
        background: #26282e !important;
    }
    .image-container.dragging, .image-container:hover {
        border-color: #60a5fa !important;
        background: #2a2d33 !important;
    }

    /* === Accordion === */
    .gr-accordion, .gr-group {
        background: #2f3239 !important;
        border: 1px solid #3f4451 !important;
        border-radius: 8px !important;
    }

    /* === Gallery / file === */
    .gradio-gallery, .gradio-file, .gradio-dataframe {
        background: #2f3239 !important;
        color: #f1f5f9 !important;
    }

    /* === Buttons secondary — gray === */
    button.secondary, .gr-button-secondary, button:not(.primary) {
        background: #3a3d44 !important;
        color: #e2e8f0 !important;
        border: 1px solid #4a4d54 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    button.secondary:hover, .gr-button-secondary:hover, button:not(.primary):hover {
        background: #454952 !important;
        color: #f1f5f9 !important;
        border-color: #60a5fa !important;
    }

    /* === Links === */
    a { color: #22d3ee !important; text-decoration: none !important; }
    a:hover { color: #60a5fa !important; }

    /* === Footer hide === */
    .footer { display: none !important; }
    .progress-text, .meta-text, .timestamp { color: #94a3b8 !important; }

    /* === Header gradient === */
    .gradio-container > .app > .header,
    .gradio-container > header,
    [data-testid="logo"] {
        background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%) !important;
    }

    /* ============================================================
       === MOBILE RESPONSIVE (max-width: 768px) — same look as desktop
       ============================================================ */
    @media (max-width: 768px) {
        /* Base font up so text is readable on phones */
        html, body, .gradio-container, .gr-panel, .gr-block,
        .gr-input, .gr-text-input, .gr-number-input, .gr-button,
        .gr-form, .gr-box, label, p, span, div, li, td, th {
            font-size: 16px !important;
            line-height: 1.5 !important;
        }
        /* Headers slightly bigger, easier to read */
        h1 { font-size: 26px !important; }
        h2 { font-size: 22px !important; }
        h3 { font-size: 19px !important; }
        h4 { font-size: 17px !important; }

        /* Inputs and dropdowns — large tap targets (>= 44px) */
        input, textarea, select,
        .gr-input, .gr-text-input, .gr-number-input,
        .gr-dropdown, .gr-dropdown input,
        input[type="text"], input[type="number"], input[type="search"] {
            min-height: 44px !important;
            padding: 10px 14px !important;
            font-size: 16px !important;
        }

        /* Sliders — full width, big thumb */
        input[type="range"] {
            height: 32px !important;
            width: 100% !important;
        }
        input[type="range"]::-webkit-slider-thumb {
            height: 26px !important;
            width: 26px !important;
        }

        /* Buttons — big enough for thumbs */
        .gr-button, button.primary, .lg, .secondary {
            min-height: 48px !important;
            font-size: 16px !important;
            padding: 12px 16px !important;
        }

        /* Radio / Checkbox — bigger touch targets */
        .gr-radio, .gr-checkbox, .gr-checkbox-group,
        .gr-radio-item, .gr-checkbox-item,
        label.checkbox-container, label.radio-container {
            min-height: 44px !important;
            padding: 10px 12px !important;
            font-size: 16px !important;
        }
        label.checkbox-container .label-text,
        label.radio-container .label-text {
            font-size: 16px !important;
        }

        /* Dropdown option list (when opened) */
        .gr-dropdown-options .gr-dropdown-option,
        .gr-dropdown-items .gr-dropdown-item,
        [role="option"] {
            min-height: 44px !important;
            padding: 12px 14px !important;
            font-size: 16px !important;
        }

        /* Stack Gradio rows/columns vertically on mobile */
        .gr-row, .gr-form, .gr-panel,
        .gradio-container .gr-row,
        .gradio-container .gr-form {
            flex-direction: column !important;
            display: flex !important;
        }
        /* Force single column inside any gr.Group / Row */
        .gr-row > *,
        .gr-form > *,
        .gr-panel > * {
            width: 100% !important;
            max-width: 100% !important;
            flex: 0 0 100% !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }

        /* Tabs — scroll horizontally if needed */
        .tab-nav, [role="tablist"] {
            overflow-x: auto !important;
            overflow-y: hidden !important;
            flex-wrap: nowrap !important;
            -webkit-overflow-scrolling: touch !important;
            scrollbar-width: thin !important;
        }
        .tab-nav button, [role="tab"] {
            flex: 0 0 auto !important;
            white-space: nowrap !important;
            padding: 12px 14px !important;
            font-size: 14px !important;
            min-height: 44px !important;
        }

        /* Images — fill width but don't overflow */
        .gr-image, .image-container, img {
            max-width: 100% !important;
            height: auto !important;
        }

        /* Reduce overall padding so content uses the screen */
        .gradio-container, .app, .main, .wrap {
            padding: 8px !important;
            margin: 0 !important;
            min-width: 0 !important;
        }
        .gr-panel, .gr-box, .form, .container, .block {
            padding: 12px !important;
            margin: 6px 0 !important;
            border-radius: 10px !important;
        }

        /* Markdown body — bigger text */
        .prose p, .prose li, .prose strong, .prose em {
            font-size: 15px !important;
        }
        .prose h3 { font-size: 18px !important; }

        /* Info panel — readable on phone */
        #size_requirements_panel {
            padding: 12px 14px !important;
            font-size: 15px !important;
        }

        /* Logo/title block — wrap on small screens */
        .gradio-container h1 {
            font-size: 22px !important;
            line-height: 1.2 !important;
            word-break: break-word !important;
        }
    }

    /* Very small phones (<= 480px) — extra adjustments */
    @media (max-width: 480px) {
        h1 { font-size: 22px !important; }
        h2 { font-size: 19px !important; }
        h3 { font-size: 17px !important; }
        .gr-button, button.primary { font-size: 15px !important; }
        .gr-panel, .gr-box { padding: 10px !important; }
    }
    """
    retoka_js = """
    <script>
    (function() {
        // Apply 'retoka-selected' to checked radio/checkbox containers
        function applySelection() {
            document.querySelectorAll('.checkbox-container').forEach(function(c) {
                var input = c.querySelector('input[type="radio"], input[type="checkbox"]');
                if (input && input.checked) {
                    c.classList.add('retoka-selected');
                } else {
                    c.classList.remove('retoka-selected');
                }
            });
        }
        // Run periodically + on change
        setInterval(applySelection, 200);
        document.addEventListener('change', applySelection, true);
        document.addEventListener('click', function(e) {
            setTimeout(applySelection, 50);
        }, true);
        // Run once on load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', applySelection);
        } else {
            applySelection();
        }
    })();
    </script>
    <style>
    /* JS-added class — guaranteed to work (dark theme) */
    .checkbox-container.retoka-selected {
        background: #3a3d44 !important;
        border-radius: 6px !important;
        padding: 4px 8px !important;
        outline: 2px solid #f1f5f9 !important;
    }
    .checkbox-container.retoka-selected .label-text {
        color: #f1f5f9 !important;
        font-weight: 800 !important;
    }
    .checkbox-container.retoka-selected input {
        background-color: #f1f5f9 !important;
        border-color: #f1f5f9 !important;
        accent-color: #f1f5f9 !important;
    }
    </style>
    """

    # Use Gradio's native "Default" theme as base (light, predictable)
    # NOTE: in Gradio 6+, theme/css should be passed to launch() instead of Blocks()
    demo = gr.Blocks(
        title="Retoka · Fotos de Identificación México",
    )

    with demo:
        gr.HTML(load_description(os.path.join(root_dir, "demo/assets/title.md")))
        with gr.Row():
            # ------------------------ 左半边 UI ------------------------
            with gr.Column():
                img_input = gr.Image(height=400)

                with gr.Row():
                    # 语言选择器
                    language_options = gr.Dropdown(
                        choices=language,
                        label="Language",
                        value=DEFAULT_LANG,
                    )

                    face_detect_model_options = gr.Dropdown(
                        choices=face_detect_models,
                        label=LOCALES["face_model"][DEFAULT_LANG]["label"],
                        value=DEFAULT_FACE_DETECT_MODEL,
                    )

                    matting_model_options = gr.Dropdown(
                        choices=human_matting_models,
                        label=LOCALES["matting_model"][DEFAULT_LANG]["label"],
                        value=human_matting_models[0],
                    )

                # TAB1 - 关键参数 ------------------------------------------------
                with gr.Tab(
                    LOCALES["key_param"][DEFAULT_LANG]["label"]
                ) as key_parameter_tab:
                    # 尺寸模式
                    with gr.Row():
                        mode_options = gr.Radio(
                            choices=LOCALES["size_mode"][DEFAULT_LANG]["choices"],
                            label=LOCALES["size_mode"][DEFAULT_LANG]["label"],
                            value=LOCALES["size_mode"][DEFAULT_LANG]["choices"][0],
                            min_width=520,
                        )
                        
                    # 尺寸列表
                    with gr.Row(visible=True) as size_list_row:
                        size_list_options = gr.Dropdown(
                            choices=LOCALES["size_list"][DEFAULT_LANG]["choices"],
                            label=LOCALES["size_list"][DEFAULT_LANG]["label"],
                            value=LOCALES["size_list"][DEFAULT_LANG]["choices"][0],
                            elem_id="size_list",
                        )

                    # ---- Panel informativo: requisitos del tamaño elegido ----
                    # Se actualiza con .change() sobre size_list_options y language_options.
                    # El usuario puede ocultar/mostrar el panel con el checkbox
                    # show_requirements_checkbox (default: visible).
                    show_requirements_checkbox = gr.Checkbox(
                        label=LOCALES["show_requirements"][DEFAULT_LANG]["label"],
                        value=True,
                        elem_id="show_requirements_checkbox",
                    )
                    size_requirements_panel = gr.Markdown(
                        value=render_reqs(
                            LOCALES["size_list"][DEFAULT_LANG]["choices"][0],
                            DEFAULT_LANG,
                        ),
                        elem_id="size_requirements_panel",
                        visible=True,
                    )
                    # 自定义尺寸px
                    with gr.Row(visible=False) as custom_size_px:
                        custom_size_height_px = gr.Number(
                            value=413,
                            label=LOCALES["custom_size_px"][DEFAULT_LANG]["height"],
                            interactive=True,
                        )
                        custom_size_width_px = gr.Number(
                            value=295,
                            label=LOCALES["custom_size_px"][DEFAULT_LANG]["width"],
                            interactive=True,
                        )
                    # 自定义尺寸mm
                    with gr.Row(visible=False) as custom_size_mm:
                        custom_size_height_mm = gr.Number(
                            value=35,
                            label=LOCALES["custom_size_mm"][DEFAULT_LANG]["height"],
                            interactive=True,
                        )
                        custom_size_width_mm = gr.Number(
                            value=25,
                            label=LOCALES["custom_size_mm"][DEFAULT_LANG]["width"],
                            interactive=True,
                        )

                    # 背景颜色
                    color_options = gr.Radio(
                        choices=LOCALES["bg_color"][DEFAULT_LANG]["choices"],
                        label=LOCALES["bg_color"][DEFAULT_LANG]["label"],
                        value=LOCALES["bg_color"][DEFAULT_LANG]["choices"][0],
                    )
                    
                    # 自定义颜色RGB
                    with gr.Row(visible=False) as custom_color_rgb:
                        custom_color_R = gr.Number(value=0, label="R", minimum=0, maximum=255, interactive=True)
                        custom_color_G = gr.Number(value=0, label="G", minimum=0, maximum=255, interactive=True)
                        custom_color_B = gr.Number(value=0, label="B", minimum=0, maximum=255, interactive=True)
                    
                    # 自定义颜色HEX
                    with gr.Row(visible=False) as custom_color_hex:
                        custom_color_hex_value = gr.Text(value="000000", label="Hex", interactive=True)

                    # 渲染模式
                    render_options = gr.Radio(
                        choices=LOCALES["render_mode"][DEFAULT_LANG]["choices"],
                        label=LOCALES["render_mode"][DEFAULT_LANG]["label"],
                        value=LOCALES["render_mode"][DEFAULT_LANG]["choices"][0],
                    )
                    
                    with gr.Row():
                        # 插件模式
                        plugin_options = gr.CheckboxGroup(
                            label=LOCALES["plugin"][DEFAULT_LANG]["label"],
                            choices=LOCALES["plugin"][DEFAULT_LANG]["choices"],
                            interactive=True,
                            value=LOCALES["plugin"][DEFAULT_LANG]["value"]
                        )
                        # Mostrar guia de cumplimiento (overlay visual)
                        show_overlay_option = gr.Checkbox(
                            label=LOCALES["show_overlay"][DEFAULT_LANG]["label"],
                            value=True,
                            interactive=True,
                        )

                # TAB2 - 高级参数 ------------------------------------------------
                with gr.Tab(
                    LOCALES["advance_param"][DEFAULT_LANG]["label"]
                ) as advance_parameter_tab:
                    photo_standard_option = gr.Radio(
                        choices=LOCALES["photo_standard"][DEFAULT_LANG]["choices"],
                        label=LOCALES["photo_standard"][DEFAULT_LANG]["label"],
                        value=LOCALES["photo_standard"][DEFAULT_LANG]["choices"][0],
                        interactive=True,
                    )
                    head_measure_ratio_option = gr.Slider(
                        minimum=0.1,
                        maximum=0.5,
                        value=0.20,
                        step=0.01,
                        label=LOCALES["head_measure_ratio"][DEFAULT_LANG]["label"],
                        interactive=True,
                    )
                    head_height_ratio_option = gr.Slider(
                        minimum=0.30,
                        maximum=0.60,
                        value=0.45,
                        step=0.01,
                        label=LOCALES["head_height_ratio"][DEFAULT_LANG]["label"],
                        interactive=True,
                    )
                    top_distance_option = gr.Slider(
                        minimum=0.02,
                        maximum=0.5,
                        value=0.12,
                        step=0.01,
                        label=LOCALES["top_distance"][DEFAULT_LANG]["label"],
                        interactive=True,
                    )

                    image_kb_options = gr.Radio(
                        choices=LOCALES["image_kb"][DEFAULT_LANG]["choices"],
                        label=LOCALES["image_kb"][DEFAULT_LANG]["label"],
                        value=LOCALES["image_kb"][DEFAULT_LANG]["choices"][0],
                    )

                    custom_image_kb_size = gr.Slider(
                        minimum=10,
                        maximum=1000,
                        value=50,
                        label=LOCALES["image_kb_size"][DEFAULT_LANG]["label"],
                        interactive=True,
                        visible=False,
                    )

                    image_dpi_options = gr.Radio(
                        choices=LOCALES["image_dpi"][DEFAULT_LANG]["choices"],
                        label=LOCALES["image_dpi"][DEFAULT_LANG]["label"],
                        value=LOCALES["image_dpi"][DEFAULT_LANG]["choices"][0],
                    )
                    custom_image_dpi_size = gr.Slider(
                        minimum=72,
                        maximum=600,
                        value=300,
                        label=LOCALES["image_dpi_size"][DEFAULT_LANG]["label"],
                        interactive=True,
                        visible=False,
                    )

                # TAB3 - 美颜 ------------------------------------------------
                with gr.Tab(
                    LOCALES["beauty_tab"][DEFAULT_LANG]["label"]
                ) as beauty_parameter_tab:
                    # 美白组件
                    whitening_option = gr.Slider(
                        label=LOCALES["whitening_strength"][DEFAULT_LANG]["label"],
                        minimum=0,
                        maximum=15,
                        value=2,
                        step=1,
                        interactive=True,
                    )

                    with gr.Row():
                        # 亮度组件
                        brightness_option = gr.Slider(
                            label=LOCALES["brightness_strength"][DEFAULT_LANG]["label"],
                            minimum=-5,
                            maximum=25,
                            value=0,
                            step=1,
                            interactive=True,
                        )
                        # 对比度组件
                        contrast_option = gr.Slider(
                            label=LOCALES["contrast_strength"][DEFAULT_LANG]["label"],
                            minimum=-10,
                            maximum=50,
                            value=0,
                            step=1,
                            interactive=True,
                        )
                        # 饱和度组件
                        saturation_option = gr.Slider(
                            label=LOCALES["saturation_strength"][DEFAULT_LANG]["label"],
                            minimum=-10,
                            maximum=50,
                            value=0,
                            step=1,
                            interactive=True,
                        )

                    # 锐化组件
                    sharpen_option = gr.Slider(
                        label=LOCALES["sharpen_strength"][DEFAULT_LANG]["label"],
                        minimum=0,
                        maximum=5,
                        value=0,
                        step=1,
                        interactive=True,
                    )

                    # ---- Blanco y negro para foto de identificación ----
                    gr.Markdown("---")
                    bw_enable = gr.Checkbox(
                        label=LOCALES["bw_enable"][DEFAULT_LANG]["label"],
                        value=False,
                        elem_id="bw_enable",
                    )
                    with gr.Row():
                        bw_intensity = gr.Slider(
                            label=LOCALES["bw_intensity"][DEFAULT_LANG]["label"],
                            minimum=0,
                            maximum=100,
                            value=100,
                            step=1,
                            interactive=True,
                        )
                        bw_contrast = gr.Slider(
                            label=LOCALES["bw_contrast"][DEFAULT_LANG]["label"],
                            minimum=-30,
                            maximum=40,
                            value=12,
                            step=1,
                            interactive=True,
                        )
                        bw_gamma = gr.Slider(
                            label=LOCALES["bw_gamma"][DEFAULT_LANG]["label"],
                            minimum=80,
                            maximum=130,
                            value=105,
                            step=1,
                            interactive=True,
                        )

                # TAB4 - 水印 ------------------------------------------------
                with gr.Tab(
                    LOCALES["watermark_tab"][DEFAULT_LANG]["label"]
                ) as watermark_parameter_tab:
                    watermark_options = gr.Radio(
                        choices=LOCALES["watermark_switch"][DEFAULT_LANG]["choices"],
                        label=LOCALES["watermark_switch"][DEFAULT_LANG]["label"],
                        value=LOCALES["watermark_switch"][DEFAULT_LANG]["choices"][0],
                    )

                    with gr.Row():
                        watermark_text_options = gr.Text(
                            max_length=20,
                            label=LOCALES["watermark_text"][DEFAULT_LANG]["label"],
                            value=LOCALES["watermark_text"][DEFAULT_LANG]["value"],
                            placeholder=LOCALES["watermark_text"][DEFAULT_LANG][
                                "placeholder"
                            ],
                            interactive=False,
                        )
                        watermark_text_color = gr.ColorPicker(
                            label=LOCALES["watermark_color"][DEFAULT_LANG]["label"],
                            interactive=False,
                            value="#FFFFFF",
                        )

                    watermark_text_size = gr.Slider(
                        minimum=10,
                        maximum=100,
                        value=20,
                        label=LOCALES["watermark_size"][DEFAULT_LANG]["label"],
                        interactive=False,
                        step=1,
                    )

                    watermark_text_opacity = gr.Slider(
                        minimum=0,
                        maximum=1,
                        value=0.15,
                        label=LOCALES["watermark_opacity"][DEFAULT_LANG]["label"],
                        interactive=False,
                        step=0.01,
                    )

                    watermark_text_angle = gr.Slider(
                        minimum=0,
                        maximum=360,
                        value=30,
                        label=LOCALES["watermark_angle"][DEFAULT_LANG]["label"],
                        interactive=False,
                        step=1,
                    )

                    watermark_text_space = gr.Slider(
                        minimum=10,
                        maximum=200,
                        value=25,
                        label=LOCALES["watermark_space"][DEFAULT_LANG]["label"],
                        interactive=False,
                        step=1,
                    )

                    def update_watermark_text_visibility(choice, language):
                        return [
                            gr.update(
                                interactive=(
                                    choice
                                    == LOCALES["watermark_switch"][language]["choices"][
                                        1
                                    ]
                                )
                            )
                        ] * 6

                    watermark_options.change(
                        fn=update_watermark_text_visibility,
                        inputs=[watermark_options, language_options],
                        outputs=[
                            watermark_text_options,
                            watermark_text_color,
                            watermark_text_size,
                            watermark_text_opacity,
                            watermark_text_angle,
                            watermark_text_space,
                        ],
                    )
                
                # TAB5 - 打印 ------------------------------------------------
                with gr.Tab(
                    LOCALES["print_tab"][DEFAULT_LANG]["label"]
                ) as print_parameter_tab:
                    print_options = gr.Radio(
                        choices=LOCALES["print_switch"][DEFAULT_LANG]["choices"],
                        label=LOCALES["print_switch"][DEFAULT_LANG]["label"],
                        value=LOCALES["print_switch"][DEFAULT_LANG]["choices"][0],
                        interactive=True,
                    )
                

                img_but = gr.Button(
                    LOCALES["button"][DEFAULT_LANG]["label"],
                    elem_id="btn",
                    variant="primary"
                )

                example_images = gr.Examples(
                    inputs=[img_input],
                    examples=[
                        [path.as_posix()]
                        for path in sorted(
                            pathlib.Path(os.path.join(root_dir, "demo/images")).rglob(
                                "*.jpg"
                            )
                        )
                    ],
                )

            # ---------------- 右半边 UI ----------------
            with gr.Column():
                notification = gr.Text(
                    label=LOCALES["notification"][DEFAULT_LANG]["label"], visible=False
                )
                with gr.Row():
                    # 标准照
                    img_output_standard = gr.Image(
                        label=LOCALES["standard_photo"][DEFAULT_LANG]["label"],
                        height=350,
                        format="png",
                    )
                    # 高清照
                    img_output_standard_hd = gr.Image(
                        label=LOCALES["hd_photo"][DEFAULT_LANG]["label"],
                        height=350,
                        format="png",
                    )
                # 排版照
                img_output_layout = gr.Image(
                    label=LOCALES["layout_photo"][DEFAULT_LANG]["label"],
                    height=350,
                    format="png",
                )
                # 模版照片
                with gr.Accordion(
                    LOCALES["template_photo"][DEFAULT_LANG]["label"], open=False
                ) as template_image_accordion:      
                    img_output_template = gr.Gallery(
                        label=LOCALES["template_photo"][DEFAULT_LANG]["label"],
                        height=350,
                        format="png",
                    )
                # 抠图图像
                with gr.Accordion(
                    LOCALES["matting_image"][DEFAULT_LANG]["label"], open=False
                ) as matting_image_accordion:
                    with gr.Row():
                        img_output_standard_png = gr.Image(
                            label=LOCALES["standard_photo_png"][DEFAULT_LANG]["label"],
                            height=350,
                            format="png",
                            elem_id="standard_photo_png",
                        )
                        img_output_standard_hd_png = gr.Image(
                            label=LOCALES["hd_photo_png"][DEFAULT_LANG]["label"],
                            height=350,
                            format="png",
                            elem_id="hd_photo_png",
                        )

            # ---------------- 多语言切换函数 ----------------
            def change_language(language):
                return {
                    face_detect_model_options: gr.update(
                        label=LOCALES["face_model"][language]["label"]
                    ),
                    matting_model_options: gr.update(
                        label=LOCALES["matting_model"][language]["label"]
                    ),
                    size_list_options: gr.update(
                        label=LOCALES["size_list"][language]["label"],
                        choices=LOCALES["size_list"][language]["choices"],
                        value=LOCALES["size_list"][language]["choices"][0],
                    ),
                    mode_options: gr.update(
                        label=LOCALES["size_mode"][language]["label"],
                        choices=LOCALES["size_mode"][language]["choices"],
                        value=LOCALES["size_mode"][language]["choices"][0],
                    ),
                    color_options: gr.update(
                        label=LOCALES["bg_color"][language]["label"],
                        choices=LOCALES["bg_color"][language]["choices"],
                        value=LOCALES["bg_color"][language]["choices"][0],
                    ),
                    img_but: gr.update(value=LOCALES["button"][language]["label"]),
                    render_options: gr.update(
                        label=LOCALES["render_mode"][language]["label"],
                        choices=LOCALES["render_mode"][language]["choices"],
                        value=LOCALES["render_mode"][language]["choices"][0],
                    ),
                    image_kb_options: gr.update(
                        label=LOCALES["image_kb_size"][language]["label"],
                        choices=LOCALES["image_kb"][language]["choices"],
                        value=LOCALES["image_kb"][language]["choices"][0],
                    ),
                    custom_image_kb_size: gr.update(
                        label=LOCALES["image_kb"][language]["label"]
                    ),
                    notification: gr.update(
                        label=LOCALES["notification"][language]["label"]
                    ),
                    img_output_standard: gr.update(
                        label=LOCALES["standard_photo"][language]["label"]
                    ),
                    img_output_standard_hd: gr.update(
                        label=LOCALES["hd_photo"][language]["label"]
                    ),
                    img_output_standard_png: gr.update(
                        label=LOCALES["standard_photo_png"][language]["label"]
                    ),
                    img_output_standard_hd_png: gr.update(
                        label=LOCALES["hd_photo_png"][language]["label"]
                    ),
                    img_output_layout: gr.update(
                        label=LOCALES["layout_photo"][language]["label"]
                    ),
                    head_measure_ratio_option: gr.update(
                        label=LOCALES["head_measure_ratio"][language]["label"]
                    ),
                    top_distance_option: gr.update(
                        label=LOCALES["top_distance"][language]["label"]
                    ),
                    key_parameter_tab: gr.update(
                        label=LOCALES["key_param"][language]["label"]
                    ),
                    advance_parameter_tab: gr.update(
                        label=LOCALES["advance_param"][language]["label"]
                    ),
                    watermark_parameter_tab: gr.update(
                        label=LOCALES["watermark_tab"][language]["label"]
                    ),
                    watermark_text_options: gr.update(
                        label=LOCALES["watermark_text"][language]["label"],
                        placeholder=LOCALES["watermark_text"][language]["placeholder"],
                    ),
                    watermark_text_color: gr.update(
                        label=LOCALES["watermark_color"][language]["label"]
                    ),
                    watermark_text_size: gr.update(
                        label=LOCALES["watermark_size"][language]["label"]
                    ),
                    watermark_text_opacity: gr.update(
                        label=LOCALES["watermark_opacity"][language]["label"]
                    ),
                    watermark_text_angle: gr.update(
                        label=LOCALES["watermark_angle"][language]["label"]
                    ),
                    watermark_text_space: gr.update(
                        label=LOCALES["watermark_space"][language]["label"]
                    ),
                    watermark_options: gr.update(
                        label=LOCALES["watermark_switch"][language]["label"],
                        choices=LOCALES["watermark_switch"][language]["choices"],
                        value=LOCALES["watermark_switch"][language]["choices"][0],
                    ),
                    matting_image_accordion: gr.update(
                        label=LOCALES["matting_image"][language]["label"]
                    ),
                    beauty_parameter_tab: gr.update(
                        label=LOCALES["beauty_tab"][language]["label"]
                    ),
                    whitening_option: gr.update(
                        label=LOCALES["whitening_strength"][language]["label"]
                    ),
                    image_dpi_options: gr.update(
                        label=LOCALES["image_dpi"][language]["label"],
                        choices=LOCALES["image_dpi"][language]["choices"],
                        value=LOCALES["image_dpi"][language]["choices"][0],
                    ),
                    custom_image_dpi_size: gr.update(
                        label=LOCALES["image_dpi"][language]["label"]
                    ),
                    brightness_option: gr.update(
                        label=LOCALES["brightness_strength"][language]["label"]
                    ),
                    contrast_option: gr.update(
                        label=LOCALES["contrast_strength"][language]["label"]
                    ),
                    sharpen_option: gr.update(
                        label=LOCALES["sharpen_strength"][language]["label"]
                    ),
                    saturation_option: gr.update(
                        label=LOCALES["saturation_strength"][language]["label"]
                    ),
                    bw_enable: gr.update(
                        label=LOCALES["bw_enable"][language]["label"]
                    ),
                    bw_intensity: gr.update(
                        label=LOCALES["bw_intensity"][language]["label"]
                    ),
                    bw_contrast: gr.update(
                        label=LOCALES["bw_contrast"][language]["label"]
                    ),
                    bw_gamma: gr.update(
                        label=LOCALES["bw_gamma"][language]["label"]
                    ),
                    custom_size_width_px: gr.update(
                        label=LOCALES["custom_size_px"][language]["width"]
                    ),
                    custom_size_height_px: gr.update(
                        label=LOCALES["custom_size_px"][language]["height"]
                    ),
                    custom_size_width_mm: gr.update(
                        label=LOCALES["custom_size_mm"][language]["width"]
                    ),
                    custom_size_height_mm: gr.update(
                        label=LOCALES["custom_size_mm"][language]["height"]
                    ),
                    img_output_template: gr.update(
                        label=LOCALES["template_photo"][language]["label"]
                    ),
                    template_image_accordion: gr.update(
                        label=LOCALES["template_photo"][language]["label"]
                    ),
                    plugin_options: gr.update(
                        label=LOCALES["plugin"][language]["label"],
                        choices=LOCALES["plugin"][language]["choices"],
                        value=LOCALES["plugin"][language]["choices"][0],
                    ),
                    show_overlay_option: gr.update(
                        label=LOCALES["show_overlay"][language]["label"],
                    ),
                    show_requirements_checkbox: gr.update(
                        label=LOCALES["show_requirements"][language]["label"],
                    ),
                    print_parameter_tab: gr.update(
                        label=LOCALES["print_tab"][language]["label"]
                    ),
                    print_options: gr.update(
                        label=LOCALES["print_switch"][language]["label"],
                        choices=LOCALES["print_switch"][language]["choices"],
                        value=LOCALES["print_switch"][language]["choices"][0],
                    ),
                    photo_standard_option: gr.update(
                        label=LOCALES["photo_standard"][language]["label"],
                        choices=LOCALES["photo_standard"][language]["choices"],
                        value=LOCALES["photo_standard"][language]["choices"][0],
                    ),
                    head_measure_ratio_option: gr.update(
                        label=LOCALES["head_measure_ratio"][language]["label"]
                    ),
                    head_height_ratio_option: gr.update(
                        label=LOCALES["head_height_ratio"][language]["label"]
                    ),
                    top_distance_option: gr.update(
                        label=LOCALES["top_distance"][language]["label"]
                    ),
                }

            def change_visibility(option, lang, locales_key, custom_component):
                return {
                    custom_component: gr.update(
                        visible=option == LOCALES[locales_key][lang]["choices"][-1]
                    )
                }

            def change_color(colors, lang):
                return {
                    custom_color_rgb: gr.update(visible = colors == LOCALES["bg_color"][lang]["choices"][-2]),
                    custom_color_hex: gr.update(visible = colors == LOCALES["bg_color"][lang]["choices"][-1]),
                }
                

            def change_size_mode(size_option_item, lang):
                choices = LOCALES["size_mode"][lang]["choices"]
                # 如果选择自定义尺寸mm
                if size_option_item == choices[3]:
                    return {
                        custom_size_px: gr.update(visible=False),
                        custom_size_mm: gr.update(visible=True),
                        size_list_row: gr.update(visible=False),
                        plugin_options: gr.update(interactive=True),
                    }
                # 如果选择自定义尺寸px
                elif size_option_item == choices[2]:
                    return {
                        custom_size_px: gr.update(visible=True),
                        custom_size_mm: gr.update(visible=False),
                        size_list_row: gr.update(visible=False),
                        plugin_options: gr.update(interactive=True),
                    }
                # 如果选择只换底，则隐藏所有尺寸组件
                elif size_option_item == choices[1]:
                    return {
                        custom_size_px: gr.update(visible=False),
                        custom_size_mm: gr.update(visible=False),
                        size_list_row: gr.update(visible=False),
                        plugin_options: gr.update(interactive=False),
                    }
                # 如果选择预设尺寸，则隐藏自定义尺寸组件
                else:
                    return {
                        custom_size_px: gr.update(visible=False),
                        custom_size_mm: gr.update(visible=False),
                        size_list_row: gr.update(visible=True),
                        plugin_options: gr.update(interactive=True),
                    }

            def change_image_kb(image_kb_option, lang):
                return change_visibility(
                    image_kb_option, lang, "image_kb", custom_image_kb_size
                )

            # Cuando el usuario cambia el estándar, ajusta los 3 sliders
            # a los valores preconfigurados. Si elige "Personalizado" no cambia nada.
            def change_photo_standard(standard_option):
                # Profiles (head_ratio, head_height_ratio, top_distance_max)
                # head_measure_ratio controla el area de la CARA detectada (no cabeza+cabello).
                # Para que la CABEZA COMPLETA quede al 70-80% del alto (cumple ICAO),
                # el valor debe estar entre 0.35-0.40 (la cara sera ~55-60% del alto).
                profiles = {
                    "ICAO / Pasaporte": (0.40, 0.45, 0.15),
                    "Visa Americana":  (0.35, 0.50, 0.12),
                    "Escolar / Niños":  (0.20, 0.45, 0.12),
                    "Personalizado":    None,  # don't change
                }
                vals = profiles.get(standard_option)
                if vals is None:
                    # Personalizado: leave slider values as they are
                    return {
                        head_measure_ratio_option: gr.update(),
                        head_height_ratio_option:  gr.update(),
                        top_distance_option:       gr.update(),
                    }
                hr, hh, td = vals
                return {
                    head_measure_ratio_option: gr.update(value=hr),
                    head_height_ratio_option:  gr.update(value=hh),
                    top_distance_option:       gr.update(value=td),
                }

            def change_image_dpi(image_dpi_option, lang):
                return change_visibility(
                    image_dpi_option, lang, "image_dpi", custom_image_dpi_size
                )

            # ---------------- 绑定事件 ----------------
            # 语言切换
            language_options.input(
                change_language,
                inputs=[language_options],
                outputs=[
                    size_list_options,
                    mode_options,
                    color_options,
                    img_but,
                    render_options,
                    image_kb_options,
                    matting_model_options,
                    face_detect_model_options,
                    custom_image_kb_size,
                    notification,
                    img_output_standard,
                    img_output_standard_hd,
                    img_output_standard_png,
                    img_output_standard_hd_png,
                    img_output_layout,
                    head_measure_ratio_option,
                    top_distance_option,
                    key_parameter_tab,
                    advance_parameter_tab,
                    watermark_parameter_tab,
                    watermark_text_options,
                    watermark_text_color,
                    watermark_text_size,
                    watermark_text_opacity,
                    watermark_text_angle,
                    watermark_text_space,
                    watermark_options,
                    matting_image_accordion,
                    beauty_parameter_tab,
                    whitening_option,
                    image_dpi_options,
                    custom_image_dpi_size,
                    brightness_option,
                    contrast_option,
                    sharpen_option,
                    saturation_option,
                    plugin_options,
                    custom_size_width_px,
                    custom_size_height_px,
                    custom_size_width_mm,
                    custom_size_height_mm,
                    img_output_template,
                    template_image_accordion,
                    print_parameter_tab,
                    print_options,
                ],
            )

            # ---------------- 设置隐藏/显示交互效果 ----------------
            # 尺寸模式
            mode_options.input(
                change_size_mode,
                inputs=[mode_options, language_options],
                outputs=[
                    custom_size_px,
                    custom_size_mm,
                    size_list_row,
                    plugin_options,
                ],
            )

            # Cuando el usuario cambia el TAMAÑO de foto, actualiza los 3 sliders
            # de recorte con los valores por defecto del CSV (head_ratio,
            # head_height, top_dist). Así cada tamaño se recorta correctamente
            # según el estándar oficial.
            def change_size(size_option_item, lang):
                size_data = LOCALES["size_list"][lang]["develop"].get(size_option_item)
                if not size_data or len(size_data) < 5:
                    return {
                        head_measure_ratio_option: gr.update(),
                        head_height_ratio_option:  gr.update(),
                        top_distance_option:       gr.update(),
                        size_requirements_panel:   gr.update(value=render_reqs(size_option_item, lang)),
                    }
                _, _, head_ratio, head_height, top_dist = size_data[:5]
                return {
                    head_measure_ratio_option: gr.update(value=head_ratio),
                    head_height_ratio_option:  gr.update(value=head_height),
                    top_distance_option:       gr.update(value=top_dist),
                    size_requirements_panel:   gr.update(value=render_reqs(size_option_item, lang)),
                }

            size_list_options.input(
                change_size,
                inputs=[size_list_options, language_options],
                outputs=[
                    head_measure_ratio_option,
                    head_height_ratio_option,
                    top_distance_option,
                    size_requirements_panel,
                ],
            )

            # Cuando el usuario cambia de IDIOMA, refresca también el panel
            # de requisitos para que aparezca traducido.
            def change_lang_for_requirements(lang, current_size):
                return render_reqs(current_size, lang)

            language_options.input(
                change_lang_for_requirements,
                inputs=[language_options, size_list_options],
                outputs=[size_requirements_panel],
            )

            # Mostrar / ocultar el panel de requisitos con el checkbox.
            # Actualiza la visibilidad y, si se vuelve a mostrar, refresca
            # el contenido por si cambió el tamaño mientras estaba oculto.
            def toggle_requirements_panel(show, lang, current_size):
                return gr.update(visible=show, value=render_reqs(current_size, lang))

            show_requirements_checkbox.input(
                toggle_requirements_panel,
                inputs=[show_requirements_checkbox, language_options, size_list_options],
                outputs=[size_requirements_panel],
            )

            # 颜色
            color_options.input(
                change_color,
                inputs=[color_options, language_options],
                outputs=[custom_color_rgb, custom_color_hex],
            )

            # 图片kb
            image_kb_options.input(
                change_image_kb,
                inputs=[image_kb_options, language_options],
                outputs=[custom_image_kb_size],
            )

            # 图片dpi
            image_dpi_options.input(
                change_image_dpi,
                inputs=[image_dpi_options, language_options],
                outputs=[custom_image_dpi_size],
            )

            # 照片标准 — al cambiar, ajusta los 3 sliders
            photo_standard_option.input(
                change_photo_standard,
                inputs=[photo_standard_option],
                outputs=[
                    head_measure_ratio_option,
                    head_height_ratio_option,
                    top_distance_option,
                ],
            )

            img_but.click(
                processor.process,
                inputs=[
                    img_input,
                    mode_options,
                    size_list_options,
                    color_options,
                    render_options,
                    image_kb_options,
                    custom_color_R,
                    custom_color_G,
                    custom_color_B,
                    custom_color_hex_value,
                    custom_size_height_px,
                    custom_size_width_px,
                    custom_size_height_mm,
                    custom_size_width_mm,
                    custom_image_kb_size,
                    language_options,
                    matting_model_options,
                    watermark_options,
                    watermark_text_options,
                    watermark_text_color,
                    watermark_text_size,
                    watermark_text_opacity,
                    watermark_text_angle,
                    watermark_text_space,
                    face_detect_model_options,
                    head_measure_ratio_option,
                    head_height_ratio_option,
                    top_distance_option,
                    whitening_option,
                    image_dpi_options,
                    custom_image_dpi_size,
                    brightness_option,
                    contrast_option,
                    sharpen_option,
                    saturation_option,
                    plugin_options,
                    show_overlay_option,
                    print_options,
                    bw_enable,
                    bw_intensity,
                    bw_contrast,
                    bw_gamma,
                ],
                outputs=[
                    img_output_standard,
                    img_output_standard_hd,
                    img_output_standard_png,
                    img_output_standard_hd_png,
                    img_output_layout,
                    img_output_template,
                    template_image_accordion,
                    notification,
                ],
            )

    if return_extras:
        return demo, retoka_css
    return demo
