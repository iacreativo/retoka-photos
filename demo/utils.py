import csv


def csv_to_size_list(csv_file: str) -> dict:
    """
    Load size_list.csv with optional crop metadata columns.

    Expected columns: Name, Height, Width [, HeadRatio, HeadHeight, TopDist]
    Optional columns (HeadRatio/HeadHeight/TopDist) control the crop defaults
    for each photo size. If missing, sensible fallbacks are used.

    Returns a dict {display_name: (h, w, head_ratio, head_height, top_dist)}.
    """
    size_list_dict = {}

    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader, None)
        has_crop_cols = header and len(header) >= 6 and "HeadRatio" in header

        for row in reader:
            if not row:
                continue
            size_name, h, w = row[0], row[1], row[2]
            if has_crop_cols:
                head_ratio = float(row[3]) if row[3] else 0.20
                head_height = float(row[4]) if row[4] else 0.45
                top_dist = float(row[5]) if row[5] else 0.12
            else:
                # Fallback defaults (used if CSV has no crop metadata)
                head_ratio, head_height, top_dist = 0.20, 0.45, 0.12

            size_name_add_size = "{}\t\t({}, {})".format(size_name, h, w)
            size_list_dict[size_name_add_size] = (
                int(h), int(w), head_ratio, head_height, top_dist,
            )

    return size_list_dict


def csv_to_color_list(csv_file: str) -> dict:
    # 初始化一个空字典
    color_list_dict = {}

    # 打开 CSV 文件并读取数据
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        # 跳过表头
        next(reader)
        # 读取数据并填充字典
        for row in reader:
            color_name, hex_code = row
            color_list_dict[color_name] = hex_code

    return color_list_dict


def range_check(value, min_value=0, max_value=255):
    value = int(value)
    return max(min_value, min(value, max_value))
