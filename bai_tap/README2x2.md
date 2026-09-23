# Bài 2.2 - Phân tích giấy phép phần mềm mã nguồn mở

## 1. Công cụ thực hiện

- Python
- Virtual Environment
- pip-licenses

## 2. Kết quả

File `licenses.txt` chứa danh sách các package và giấy phép tương ứng được lấy bằng công cụ `pip-licenses`.

## 3. Phân loại giấy phép

### Permissive

MIT, BSD và Apache-2.0 là các giấy phép permissive. Chúng thường cho phép sử dụng trong phần mềm thương mại đóng nguồn nếu tuân thủ các điều kiện của giấy phép.

### Copyleft yếu

LGPL và MPL thuộc nhóm copyleft yếu. Nghĩa vụ phụ thuộc vào cách thành phần được sử dụng, sửa đổi và phân phối.

### Copyleft mạnh

GPL và AGPL thuộc nhóm copyleft mạnh. Khi phân phối phần mềm trong phạm vi áp dụng của giấy phép, có thể phát sinh nghĩa vụ cung cấp mã nguồn tương ứng.

## 4. Phần mềm thương mại đóng nguồn

Đối với MIT, BSD và Apache-2.0, có thể sử dụng trong phần mềm thương mại đóng nguồn nếu tuân thủ điều kiện của license.

Đối với LGPL, MPL, GPL và AGPL, cần kiểm tra kỹ cách tích hợp, sửa đổi và phân phối để xác định nghĩa vụ về mã nguồn.

Danh sách license thực tế của các package được trình bày trong file `licenses.txt`.
