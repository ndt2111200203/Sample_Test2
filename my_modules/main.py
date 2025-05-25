# Khai báo các thư viện cần thiết
# Nhập các module cần thiết từ các file khác trong thư mục

import sys
import os
import modules
import dialog
import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QLabel, QGridLayout, QVBoxLayout
from PyQt6 import uic

class MainWindow(QMainWindow):

    # Khởi tạo
    def __init__(self):

        # Gọi hàm khởi tạo của class cha QMainWindow
        super().__init__()
        
        # Load giao diện từ file .ui
        self.ui = uic.loadUi('ui\\main.ui', self)

        # Đặt stackedWidget luôn ở trang Home mỗi khi chạy ứng dụng
        self.ui.stackedWidget.setCurrentIndex(0) # setCurrentIndex() là phương thức đặt trang hiển thị theo thứ tự index

        # Tạo database
        self.dtb = modules.phim_database()
        self.dtb.load_data()

        # Hiển thị danh sách phim trong mục chỉnh sửa
        ten = self.dtb.get_title_list()
        self.ui.phimlist.addItems(ten)

        # Hiển thị danh sách phim trong bảng ở mục ranking
        self.load_movies_to_table()

        # Kết nối các nút chuyển trang
        self.bt_home.clicked.connect(self.show_home)
        self.bt_ranking.clicked.connect(self.show_ranking)
        self.bt_setting.clicked.connect(self.show_setting)

        # Kết nối các nút thêm, sửa, xóa, tìm kiếm
        self.bt_add.clicked.connect(self.add)
        self.bt_edit.clicked.connect(self.edit)
        self.bt_delete.clicked.connect(self.delete)
        self.bt_search.clicked.connect(self.search)

    # Phương thức chuyển sang trang home
    def show_home(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    
    # Phương thức chuyển sang trang ranking
    def show_ranking(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    # Phương thức chuyển sang trang setting
    def show_setting(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    # Phương thức thêm phim
    def add(self):

        # Tạo dialog add
        dialog_add = dialog.AddDialog()

        # Nếu nhấn nút OK
        if dialog_add.exec():

            # Lấy dữ liệu từ diaglog
            inputs = dialog_add.return_data()

            # Thêm dữ liệu vào listWidget
            self.ui.phimlist.addItem(inputs["ten"])

            # Thêm dữ liệu vào database
            self.dtb.add_item(inputs)

            # Thêm dữ liệu vào bảng Ranking
            self.load_movies_to_table()
    
    # Phương thức sửa phim
    def edit(self):

        # Tạo biến lưu trữ vị trí phần tử phim đang được chọn trong danh sách
        curr = self.ui.phimlist.currentRow()

        # Kiểm tra xem có phim nào đang được chọn không
        if curr == -1: # (currentRow = -1 có nghĩa là không có phần tử nào được chọn)
            QMessageBox.warning(self, "Error", "Vui lòng chọn một bộ phim để sửa!")
            return
        
        # Lấy tên phim đang được chọn
        ten = self.ui.phimlist.currentItem().text()
        phim_item = self.dtb.get_first_item_by_title(ten)

        # Nếu không tìm thấy phim muốn xóa trong cơ sở dữ liệu
        if not phim_item:
            QMessageBox.warning(self, "Error", "Không tìm thấy phim muốn sửa!")
            return
        
        # Tạo dialog edit và truyền dữ liệu cũ vào
        dialog_edit = dialog.EditDialog(phim_item)

        # Nếu người dùng nhấn OK
        if dialog_edit.exec():

            # Lấy dữ liệu mới từ form
            new_data = dialog_edit.return_data()

            # Gọi hàm edit_item để cập nhật dữ liệu
            self.dtb.edit_item(ten, new_data)

            # Cập nhật lại giao diện danh sách phim
            self.ui.phimlist.clear()
            self.ui.phimlist.addItems(self.dtb.get_title_list())

            # Cập nhật dữ liệu vào bảng Ranking
            self.load_movies_to_table()
    
    # Phương thức xóa phim
    def delete(self):

        # Tạo biến lưu trữ vị trí phần tử phim đang được chọn trong danh sách
        curr = self.ui.phimlist.currentRow()

        # Kiểm tra xem có phim nào đang được chọn hay không
        if curr == -1: # (currentRow = -1 có nghĩa là không có phần tử nào được chọn)
            QMessageBox.warning(self, "Error", "Vui lòng chọn một bộ phim để xóa!")
            return
        
        # Lấy tên phim đang được chọn
        ten = self.ui.phimlist.currentItem().text()

        # Hiển thị hộp thoại xác nhận trước khi xóa
        reply = QMessageBox.question(self, "Confirm", 
                                 f"Bạn có chắc chắn muốn xóa phim '{ten}' không?",
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                 QMessageBox.StandardButton.No)
        
        # Nếu chọn Yes trong hộp thoại
        if reply == QMessageBox.StandardButton.Yes:

            # Xóa phim khỏi danh sách hiển thị
            self.ui.phimlist.takeItem(curr)

            # Xóa phim khỏi database
            self.dtb.delete_item(ten)

            # Xóa dữ liệu ở bảng Ranking
            self.load_movies_to_table()

            # Hiển thị thông báo đã xóa thành công
            QMessageBox.information(self, "Successful", f"Phim '{ten}' đã được xóa thành công!")

    # Phương thức tìm phim
    def search(self):
        text = self.ui.searchbox.text()
        matched_items = self.ui.phimlist.findItems(text, Qt.MatchFlag.MatchContains)
        for i in range(self.ui.phimlist.count()):
            it = self.ui.phimlist.item(i)
            it.setHidden(it not in matched_items)

    # Phương thức hiển thị bảng xếp hạng phim
    def load_movies_to_table(self):

        # Sắp xếp danh sách phim theo tên
        sorted_phim = sorted(self.dtb.phim_dict_data, key=lambda x: x['ten'])

        # Lấy layout của rankinglist
        layout = self.ui.ranking_list.layout()
        if layout is None:
            layout = QGridLayout(self.ui.ranking_list)
            self.ui.ranking_list.setLayout(layout)

        # Xoá các widget cũ trong rankinglist
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Thêm từng phim vào rankinglist
        for idx, movie in enumerate(sorted_phim):
            item_widget = QWidget()
            v_layout = QVBoxLayout(item_widget)
            v_layout.setContentsMargins(10, 10, 10, 10)
            v_layout.setSpacing(5)

            # Ảnh
            label_img = QLabel()
            label_img.setFixedSize(140, 200)
            label_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_img.setStyleSheet("background-color: #e0e0e0; border: 1px solid #aaa; border-radius: 8px;")

            if movie.get("image") and os.path.exists(movie["image"]):
                pixmap = QPixmap(movie["image"]).scaled(
                    label_img.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                )
                label_img.setPixmap(pixmap)
            else:
                label_img.setText("No Image")

            # Tên phim
            label_text = QLabel(movie["ten"])
            label_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_text.setStyleSheet("font-size: 14px; font-weight: bold;")

            v_layout.addWidget(label_img)
            v_layout.addWidget(label_text)

            layout.addWidget(item_widget, idx // 3, idx % 3)

class StartWindow(QMainWindow):

    # Khởi tạo
    def __init__(self):

        # Gọi hàm khởi tạo của class cha QMainWindow
        super().__init__()
        
        # Load giao diện từ file .ui
        self.ui = uic.loadUi('ui\\start.ui', self)

        # Kết nối các nút chuyển trang
        self.bt_forgotpass.clicked.connect(self.show_changepass)
        self.bt_gotoregister.clicked.connect(self.show_register)
        self.bt_backtologin.clicked.connect(self.show_login)
        self.bt_backtologin2.clicked.connect(self.show_login)

        # Khởi tạo admin
        self.admin = modules.admin_database()
        
        # Kết nối các nút đăng ký, đăng nhập, đổi mật khẩu
        self.bt_register.clicked.connect(self.handle_register)
        self.bt_login.clicked.connect(self.handle_login)
        self.lg_password.returnPressed.connect(self.handle_login)
        self.bt_changepass.clicked.connect(self.handle_change_pass)

    # Phương thức xử lý đăng ký
    def handle_register(self):
        username = self.rg_username.text()
        password = self.rg_password.text()
        result = self.admin.register(username, password)
        if result:
            QMessageBox.warning(self, "Success", "Đăng ký thành công!")
            self.show_login()
        else:
            QMessageBox.warning(self, "Error", "Đăng ký thất bại!")

    # Phương thức xử lý đăng nhập
    def handle_login(self):
        username = self.lg_username.text()
        password = self.lg_password.text()
        result = self.admin.login(username, password)
        if result:
            QMessageBox.warning(self, "Success", "Đăng nhập thành công!")
            window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Đăng nhập thất bại!")

    # Phương thức xử lý đổi mật khẩu
    def handle_change_pass(self):
        username = self.cp_username.text()
        new_pass = self.cp_password.text()
        result = self.admin.change_password(username, new_pass)
        if result:
            QMessageBox.warning(self, "Success", "Đổi mật khẩu thành công!")
            self.show_login()
        else:
            QMessageBox.warning(self, "Error", "Đổi mật khẩu thất bại!")

    # Phương thức chuyển sang trang changepass
    def show_changepass(self):
        self.stackedWidget.setCurrentIndex(2)

    # Phương thức chuyển sang trang register
    def show_register(self):
        self.stackedWidget.setCurrentIndex(1)

    # Phương thức chuyển sang trang login
    def show_login(self):
        self.stackedWidget.setCurrentIndex(0)

# Hàm main chạy chương trình
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    start = StartWindow()
    # Hiển thị giao diện
    start.show()
    sys.exit(app.exec())