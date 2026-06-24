import argparse
import os

# Detect Hugging Face Spaces runtime — it sets SPACE_ID env var
IS_HF_SPACE = bool(os.environ.get("SPACE_ID"))

from demo.processor import IDPhotoProcessor
from demo.ui import create_ui
from hivision.creator.choose_handler import HUMAN_MATTING_MODELS

root_dir = os.path.dirname(os.path.abspath(__file__))

# 获取存在的人像分割模型列表
# 通过检查 hivision/creator/weights 目录下的 .onnx 和 .mnn 文件
# 只保留文件名（不包括扩展名）
HUMAN_MATTING_MODELS_EXIST = [
    os.path.splitext(file)[0]
    for file in os.listdir(os.path.join(root_dir, "hivision/creator/weights"))
    if file.endswith(".onnx") or file.endswith(".mnn")
]
# 在HUMAN_MATTING_MODELS中的模型才会被加载到Gradio中显示
HUMAN_MATTING_MODELS_CHOICE = [
    model for model in HUMAN_MATTING_MODELS if model in HUMAN_MATTING_MODELS_EXIST
]

if len(HUMAN_MATTING_MODELS_CHOICE) == 0:
    raise ValueError(
        "未找到任何存在的人像分割模型，请检查 hivision/creator/weights 目录下的文件"
        + "\n"
        + "No existing portrait segmentation model was found, please check the files in the hivision/creator/weights directory."
    )

FACE_DETECT_MODELS = ["face++ (联网Online API)", "mtcnn"]
FACE_DETECT_MODELS_EXPAND = (
    ["retinaface-resnet50"]
    if os.path.exists(
        os.path.join(
            root_dir, "hivision/creator/retinaface/weights/retinaface-resnet50.onnx"
        )
    )
    else []
)
FACE_DETECT_MODELS_CHOICE = FACE_DETECT_MODELS + FACE_DETECT_MODELS_EXPAND

LANGUAGE = ["es", "zh", "en", "ko", "ja"]

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--port", type=int, default=int(os.environ.get("PORT", "7860")), help="The port number of the server"
    )
    argparser.add_argument(
        "--host", type=str, default=os.environ.get("HOST", "0.0.0.0"), help="The host of the server"
    )
    argparser.add_argument(
        "--root_path",
        type=str,
        default=None,
        help="The root path of the server, default is None (='/'), e.g. '/myapp'",
    )
    args = argparser.parse_args()

    processor = IDPhotoProcessor()

    demo = create_ui(
        processor,
        root_dir,
        HUMAN_MATTING_MODELS_CHOICE,
        FACE_DETECT_MODELS_CHOICE,
        LANGUAGE,
    )

    # 如果RUN_MODE是Beast，打印已开启野兽模式
    if os.getenv("RUN_MODE") == "beast":
        print("[Beast mode activated.] 已开启野兽模式。")

    # === Login ===
    # Default credentials: admin / retoka2026
    # Override via env vars: RETOKA_USER / RETOKA_PASS
    # To add more users, use RETOKA_USERS env var with format "user1:pass1,user2:pass2"
    auth_users = []
    extra = os.environ.get("RETOKA_USERS", "")
    if extra:
        for pair in extra.split(","):
            pair = pair.strip()
            if ":" in pair:
                u, p = pair.split(":", 1)
                auth_users.append((u.strip(), p.strip()))
    default_user = os.environ.get("RETOKA_USER", "admin")
    default_pass = os.environ.get("RETOKA_PASS", "retoka2026")
    if (default_user, default_pass) not in auth_users:
        auth_users.append((default_user, default_pass))
    auth = auth_users if len(auth_users) > 1 else (auth_users[0] if auth_users else None)

    print(f"[Retoka] Login activo. Usuarios: {len(auth_users)} (user por defecto: {default_user})")

    demo.launch(
        server_name=args.host,
        server_port=args.port,
        favicon_path=os.path.join(root_dir, "assets/retoka_favicon.png"),
        root_path=args.root_path,
        auth=auth,
        auth_message="🔐 Retoka - Inicia sesión para continuar",
        share=False,
        _frontend=False,  # Skip the localhost check on HF Spaces (proxy interference)
        debug=IS_HF_SPACE,  # Show errors on HF to debug
        quiet=not IS_HF_SPACE,
    )
