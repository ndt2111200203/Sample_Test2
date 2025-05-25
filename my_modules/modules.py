from data_io import load_json_data, write_json_data, load_admin_data, write_admin_data

class phim_item:

    # Khởi tạo
    def __init__(self, ten, theloai, thoiluong, image = None):
        self.ten = ten
        self.theloai = theloai
        self.thoiluong = thoiluong
        self.image = image

class phim_database:

    # Khởi tạo
    def __init__(self):

        # Tạo danh sách chứa các đối tượng phim
        self.phim_item_list = list()

        # Đọc dữ liệu khi vừa khởi tạo
        self.phim_dict_data = load_json_data()

    # Phương thức chuyển đổi dữ liệu đã READ vào danh sách đối tượng
    def load_data(self):
        for phim_dict in self.phim_dict_data:
            phim = phim_item(ten = phim_dict["ten"],
                            theloai = phim_dict["theloai"],
                            thoiluong = phim_dict["thoiluong"],
                            image = phim_dict["image"])
            self.phim_item_list.append(phim)

    # Phương thức trả về danh sách title của các phim
    def get_title_list(self):
        title_list = list()
        for phim in self.phim_item_list:
            title_list.append(phim.ten)
        return title_list
    
    # Phương thức chuyển đổi danh sách đối tượng sang dữ liệu json
    def items_to_data(self):
        json_data = list()
        for phim in self.phim_item_list:
            json_data.append(phim.__dict__)
        return json_data
    
    # Phương thức tìm kiếm bằng tên phim
    def get_first_item_by_title(self, phim_ten):

        # Duyệt qua danh sách phim
        for phim_item in self.phim_item_list:

            # Nếu tìm thấy
            if phim_item.ten == phim_ten:
                return phim_item
            
        # Nếu không tìm thấy
        return None # Chỉ trả về None nếu không tìm thấy sau khi duyệt hết danh sách
    
    # Phương thức thêm một đối tượng phim_item mới vào danh sách    
    def add_item(self, phim_dict):
        
        # Chuyển đổi dữ liệu thoiluong thành int
        phim_dict['thoiluong'] = int(phim_dict['thoiluong'])

        # Tạo đối tượng
        new_item = phim_item(ten = phim_dict['ten'],
                            theloai = phim_dict['theloai'],
                            thoiluong = phim_dict['thoiluong'],
                            image = phim_dict['image'])
        
        # Thêm vào danh sách phần tử
        self.phim_item_list.append(new_item)

        # Thực hiện WRITE dữ liệu mỗi khi thay đổi danh sách đối tượng
        self.phim_dict_data.append(phim_dict)
        write_json_data(self.phim_dict_data)

    # Phương thức sửa một đối tượng phim_item có title là edit_title
    def edit_item(self, edit_title, new_dict):

        # Tìm đối tượng
        matched = self.get_first_item_by_title(edit_title)

        # Sửa đối tượng
        if matched:

            # Cập nhật lại các thuộc tính của đối tượng
            matched.ten = new_dict.get("ten", matched.ten)  # Nếu không có key "ten" thì giữ nguyên
            matched.theloai = new_dict.get("theloai", matched.theloai)
            matched.thoiluong = int(new_dict.get("thoiluong", matched.thoiluong))  # Chuyển thành indddđ
            matched.image = new_dict.get("image", matched.image)

            # Cập nhật lại danh sách phim_dict_data
            self.phim_dict_data = [phim.__dict__ for phim in self.phim_item_list]

            # Thực hiện WRITE mỗi khi thay đổi danh sách đối tượng
            write_json_data(self.phim_dict_data)

    # Phương thức xóa đối tượng phim_item có title là delete_title
    def delete_item(self, delete_title):
        
        # Tìm đối tượng
        matched = self.get_first_item_by_title(delete_title)

        # Xóa đối tượng
        if matched:

            # Xóa đối tượng khỏi danh sách hiển thị phim
            self.phim_item_list.remove(matched)

            # Cập nhật lại danh sách phim_dict_data sau khi xóa bớt đối tượng
            self.phim_dict_data = [phim.__dict__ for phim in self.phim_item_list]

            # Thực hiện WRITE mỗi khi thay đổi danh sách đối tượng
            write_json_data(self.phim_dict_data)

class admin_database:
    
    # Khởi tạo
    def __init__(self):
        self.admin_list = load_admin_data()

    # Phương thức đăng ký tài khoản
    def register(self, username, password):
        # Nếu tên đăng nhập đã tồn tại
        if any(u['username'] == username for u in self.admin_list):
            return False # Đăng ký thất bại vì tên đăng nhập đã tồn tại
        self.admin_list.append({'username': username, 'password': password})
        write_admin_data(self.admin_list)
        return True # Đăng ký thành công
    
    def login(self, username, password):
        for u in self.admin_list:
            # Kiểm tra tên đăng nhập và mật khẩu
            if u['username'] == username and u['password'] == password:
                return True # Đăng nhập thành công
        return False # Đăng nhập thất bại
    
    def change_password(self, username, new_password):
        for u in self.admin_list:
            # Tìm tên đăng nhập
            if u['username'] == username:
                u['password'] = new_password
                write_admin_data(self.admin_list)
                return True # Đổi mật khẩu thành công
            return False # Không tìm thấy username