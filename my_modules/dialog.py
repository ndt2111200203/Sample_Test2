import os
import shutil
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QFileDialog
from PyQt6.QtCore import QDir


class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('ui\\dialog_add.ui', self)
        self.image_path = None

        # Kết nối nút upload ảnh
        self.ui.upload_button.clicked.connect(self.upload_image)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn ảnh phim", QDir.homePath(), "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            # Copy ảnh vào thư mục img
            os.makedirs("img", exist_ok=True)
            filename = os.path.basename(file_path)
            new_path = os.path.join("img", filename)
            shutil.copy(file_path, new_path)
            self.image_path = new_path

            # Cập nhật giao diện
            self.ui.image_label.setText(filename)

    def return_data(self) -> dict:
        return {
            "ten": self.ui.addten.text(),
            "theloai": self.ui.addtheloai.text(),
            "thoiluong": self.ui.addthoiluong.text(),
            "image": self.image_path if self.image_path else ""
        }


class EditDialog(QDialog):
    def __init__(self, phim_item):
        super().__init__()
        self.ui = uic.loadUi('ui\\dialog_edit.ui', self)
        self.image_path = phim_item.image

        # Hiển thị dữ liệu cũ
        self.ui.editten.setText(phim_item.ten)
        self.ui.edittheloai.setText(phim_item.theloai)
        self.ui.editthoiluong.setText(str(phim_item.thoiluong))
        self.ui.image_label.setText(os.path.basename(phim_item.image) if phim_item.image else "Chưa chọn ảnh")

        # Kết nối nút upload
        self.ui.upload_button.clicked.connect(self.upload_image)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn ảnh phim", QDir.homePath(), "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            os.makedirs("img", exist_ok=True)
            filename = os.path.basename(file_path)
            new_path = os.path.join("img", filename)
            shutil.copy(file_path, new_path)
            self.image_path = new_path

            self.ui.image_label.setText(filename)

    def return_data(self) -> dict:
        return {
            "ten": self.ui.editten.text(),
            "theloai": self.ui.edittheloai.text(),
            "thoiluong": self.ui.editthoiluong.text(),
            "image": self.image_path if self.image_path else ""
        }
