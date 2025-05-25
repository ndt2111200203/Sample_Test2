import json

# Phương thức READ dữ liệu từ file json
def load_json_data():

    # Tạo list chứa dữ liệu
    phim_dict_data = list()

    # Mở file json, load dữ liệu vào
    with open('data\\phim.json', 'r') as json_in:
        json_data = json.load(json_in)

    # Nối thêm dữ liệu vào list
    phim_dict_data.extend(json_data)

    # Trả về dữ liệu dưới dạng list
    return phim_dict_data

# Phương thức WRITE dữ liệu vào file json
def write_json_data(data):

    # Mở file json ở chế độ WRITE, mã hóa utf-8 cho phép ghi tiếng Việt
    with open('data\\phim.json', 'w', encoding='utf-8') as json_out:

        # Ghi dữ liệu vào file dưới định dạng đẹp, thụt lùi 4 khoảng trắng, cho phép ghi tiếng Việt chính xác
        json.dump(data, json_out, indent=4, ensure_ascii=False)

# Phương thức READ dữ liệu từ file admin
def load_admin_data():
    with open('data\\admin.json', 'r') as f:
        return json.load(f)

# Phương thức WRITE dữ liệu vào file admin
def write_admin_data(data):
    with open('data\\admin.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Thêm phương thức khác