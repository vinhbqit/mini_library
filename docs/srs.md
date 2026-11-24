# Đặc tả yêu cầu phần mềm (SRS) – Hệ thống Thư viện mini

Nov 23, 2026 · @Vinh

Tài liệu này đặc tả đầy đủ yêu cầu cho phiên bản 1.0 của Hệ thống Thư viện mini – ứng dụng web quản lý sách, độc giả và mượn – trả sách cho Thư viện Khoa Công nghệ thông tin. Sau khi được phê duyệt, đây là căn cứ để thiết kế, lập trình, kiểm thử và nghiệm thu.

| Mục | Nội dung |
| --- | --- |
| Mã tài liệu | TVM-SRS-001 |
| Phiên bản | 1.0 |
| Trạng thái | Dự thảo, chờ phê duyệt |
| Đơn vị yêu cầu | Thư viện Khoa Công nghệ thông tin |
| Người soạn | @Vinh |

**Lịch sử thay đổi**

| Phiên bản | Ngày | Mô tả thay đổi |
| --- | --- | --- |
| 1.0 | 23/11/2026 | Bản đầu tiên |

**Phê duyệt**

| Vai trò | Họ tên | Ngày | Ý kiến |
| --- | --- | --- | --- |
| Trưởng thư viện (đại diện đơn vị yêu cầu) |  |  |  |
| Quản lý dự án |  |  |  |
| Trưởng nhóm phát triển |  |  |  |

## 1. Giới thiệu

### 1.1 Mục đích

Thư viện Khoa hiện quản lý khoảng 1.000 đầu sách và việc mượn – trả bằng sổ ghi tay và bảng tính. Cách làm này khiến thủ thư khó biết ngay một đầu sách còn bao nhiêu bản, ai đang giữ sách quá hạn, và phải tự tính tiền phạt. Hệ thống Thư viện mini được xây dựng để số hoá các nghiệp vụ này trên một ứng dụng web duy nhất.

### 1.2 Đối tượng đọc tài liệu

| Đối tượng | Cách sử dụng tài liệu |
| --- | --- |
| Trưởng thư viện | Xác nhận phạm vi, quy tắc nghiệp vụ và phê duyệt tài liệu |
| Thủ thư | Kiểm tra các kịch bản sử dụng có đúng cách làm việc thực tế |
| Quản lý dự án | Lập kế hoạch, ước lượng và kiểm soát thay đổi phạm vi |
| Nhóm phát triển | Thiết kế và lập trình theo từng yêu cầu có mã số |
| Nhóm kiểm thử | Viết ca kiểm thử từ các kịch bản Gherkin và quy tắc nghiệp vụ |
| Phụ trách hạ tầng CNTT của Khoa | Chuẩn bị môi trường triển khai theo mục 3.2 và 2.2 |

### 1.3 Mục đích sử dụng tài liệu

Tài liệu là căn cứ duy nhất về yêu cầu của phiên bản 1.0. Mọi yêu cầu có mã số (FR, NFR, BR) để truy vết tới thiết kế, mã nguồn và ca kiểm thử. Sau khi phê duyệt, mọi thay đổi phải qua yêu cầu thay đổi, được Trưởng thư viện đồng ý và ghi vào Lịch sử thay đổi với số phiên bản mới.

### 1.4 Phạm vi sản phẩm

Phiên bản 1.0 phục vụ một vai trò người dùng là thủ thư, chạy trên trình duyệt tại quầy thư viện.

**Trong phạm vi:** quản lý đầu sách (thêm, xem, tìm, sửa, xoá); cấp thẻ độc giả; lập phiếu mượn; ghi nhận trả sách và tính phí trễ hạn; theo dõi phiếu quá hạn; đăng nhập thủ thư.

**Ngoài phạm vi:** độc giả tự đăng nhập, đặt trước hoặc gia hạn sách; gửi email, SMS nhắc trả; thu tiền phạt trên hệ thống; nhiều thủ thư với phân quyền khác nhau; nhiều chi nhánh; quét mã vạch; ứng dụng di động.

**Mục tiêu nghiệp vụ:**

- Thủ thư lập một phiếu mượn trong dưới 1 phút.
- Biết ngay số bản còn của mọi đầu sách, không cần đối chiếu sổ.
- Tiền phạt trễ hạn được tính tự động, thống nhất theo quy định của thư viện.
- Danh sách độc giả quá hạn luôn sẵn sàng để nhắc trả.

### 1.5 Định nghĩa và từ viết tắt

| Từ | Ý nghĩa |
| --- | --- |
| SRS | Software Requirements Specification – Đặc tả yêu cầu phần mềm |
| FR | Functional Requirement – Yêu cầu chức năng |
| NFR | Non-Functional Requirement – Yêu cầu phi chức năng |
| BR | Business Rule – Quy tắc nghiệp vụ |
| EARS | Easy Approach to Requirements Syntax – cách viết yêu cầu theo mẫu "Khi \[sự kiện\], hệ thống phải \[phản hồi\]" |
| Gherkin | Ngôn ngữ mô tả kịch bản Given – When – Then, dùng làm tiêu chí chấp nhận |
| MoSCoW | Cách xếp ưu tiên: Must (bắt buộc), Should (nên có), Could (có thể), Won't (không làm ở phiên bản này) |
| ISBN | International Standard Book Number – mã số tiêu chuẩn quốc tế của sách |
| CSDL | Cơ sở dữ liệu |
| PK, FK | Khoá chính, khoá ngoại |
| FMEA | Failure Mode and Effects Analysis – phân tích chế độ lỗi và ảnh hưởng |
| RPN | Risk Priority Number – chỉ số ưu tiên rủi ro |
| TBD | To Be Determined – nội dung chưa xác định |

## 2. Mô tả tổng quan

### 2.1 Nhu cầu người dùng

Thủ thư là người dùng duy nhất thao tác trên hệ thống; các nhóm còn lại hưởng lợi hoặc hỗ trợ vận hành.

| Nhóm | Loại | Vai trò | Vấn đề cần giải quyết |
| --- | --- | --- | --- |
| Thủ thư | Người dùng chính | Nhập sách, cấp thẻ, lập phiếu mượn – trả hằng ngày | Tra số bản còn mất thời gian; tự tính phí dễ sai; khó lọc người quá hạn |
| Trưởng thư viện | Bên đặt hàng, người dùng phụ | Ban hành quy định mượn – trả, xem tình hình quá hạn | Quy định áp dụng chưa thống nhất giữa các ca trực |
| Độc giả (sinh viên, giảng viên, cán bộ của Khoa) | Người hưởng lợi gián tiếp, không đăng nhập | Mượn và trả sách tại quầy | Chờ lâu khi mượn; không rõ cách tính phí trễ |
| Phụ trách hạ tầng CNTT của Khoa | Hỗ trợ vận hành | Cài đặt, sao lưu, tạo tài khoản thủ thư | Cần hệ thống đơn giản, ít phụ thuộc bên ngoài |

### 2.2 Giả định và phụ thuộc

**Giả định:**

- Mỗi phiếu mượn gồm đúng một cuốn; độc giả mượn 3 cuốn tương ứng 3 phiếu.
- "Hôm nay" là ngày theo giờ Việt Nam (UTC+7). Ngày nghỉ, ngày lễ vẫn tính vào hạn trả và số ngày trễ.
- Tại một thời điểm có tối đa 2 thủ thư cùng thao tác.
- Tài khoản thủ thư do phụ trách hạ tầng tạo bằng lệnh quản trị `flask create-librarian`; hệ thống không có màn hình đăng ký.
- Phiên bản 1.0 không có chức năng sửa, xoá độc giả trên giao diện; yêu cầu sửa, xoá dữ liệu cá nhân của độc giả xử lý theo mục 4.2 và TBD-03.

**Phụ thuộc:**

| Thành phần | Phiên bản / ghi chú |
| --- | --- |
| Ngôn ngữ và framework | Python 3.12, Flask, SQLAlchemy, mẫu giao diện Jinja |
| Cơ sở dữ liệu | SQLite cho phiên bản 1.0 (đủ cho dưới 5.000 đầu sách và 2 người dùng đồng thời) |
| Băm mật khẩu | `werkzeug.security` hoặc bcrypt |
| Máy chủ triển khai | Do Khoa cung cấp trong mạng nội bộ (TBD-01) |
| Trình duyệt | Chrome hoặc Edge phiên bản hiện hành |
| Dịch vụ bên thứ ba | Không sử dụng; hệ thống chạy được khi không có Internet |

## 3. Tính năng hệ thống và yêu cầu

### 3.1 Yêu cầu chức năng

Hệ thống có 8 yêu cầu chức năng. Mỗi yêu cầu được viết theo mẫu EARS ("Khi …, hệ thống phải …") và kèm kịch bản Gherkin làm tiêu chí chấp nhận.

| Mã | Yêu cầu | Ưu tiên | Quy tắc nghiệp vụ | Màn hình |
| --- | --- | --- | --- | --- |
| FR-01 | Thêm đầu sách | Must | BR-01, BR-07 | MH-03 |
| FR-02 | Xem danh sách và tìm kiếm sách | Must | BR-07 | MH-02 |
| FR-03 | Sửa và xoá đầu sách | Should | BR-01, BR-06, BR-07 | MH-02, MH-03 |
| FR-04 | Thêm độc giả | Must | BR-08 | MH-04 |
| FR-05 | Tạo phiếu mượn | Must | BR-02, BR-03, BR-04, BR-07 | MH-05 |
| FR-06 | Ghi nhận trả sách và tính phí trễ hạn | Must | BR-05, BR-07 | MH-06 |
| FR-07 | Xem danh sách phiếu quá hạn | Should | BR-03, BR-05 | MH-07 |
| FR-08 | Đăng nhập và đăng xuất | Should | – | MH-01 |

#### FR-01 – Thêm đầu sách

Ưu tiên Must. Thủ thư thêm đầu sách mới gồm ISBN, tên sách, tác giả, năm xuất bản (tuỳ chọn) và số bản.

- **FR-01.1** Khi thủ thư gửi biểu mẫu thêm sách hợp lệ, hệ thống phải lưu đầu sách với số bản còn bằng số bản.
- **FR-01.2** Khi ISBN đã tồn tại, hệ thống phải từ chối lưu và hiển thị "ISBN đã tồn tại".
- **FR-01.3** Khi ISBN không thỏa BR-01, hệ thống phải từ chối lưu và hiển thị "ISBN không hợp lệ".
- **FR-01.4** Khi thiếu tên sách, tác giả hoặc số bản nhỏ hơn 1, hệ thống phải hiển thị lỗi cạnh ô tương ứng và giữ nguyên dữ liệu đã nhập.

```gherkin
Feature: Thêm đầu sách
  Scenario: Thêm sách hợp lệ
    Given chưa có sách nào có ISBN "9786041234567"
    When thủ thư thêm sách ISBN "9786041234567", tên "Lập trình Python cơ bản", tác giả "Nguyễn Văn A", số bản 3
    Then danh sách sách có sách này với số bản còn "3/3"

  Scenario: ISBN đã tồn tại
    Given đã có sách ISBN "9786041234567"
    When thủ thư thêm sách khác có cùng ISBN
    Then hệ thống báo "ISBN đã tồn tại" và số đầu sách không đổi

  Scenario Outline: ISBN không hợp lệ
    When thủ thư thêm sách có ISBN "<isbn>"
    Then hệ thống báo "ISBN không hợp lệ"
    Examples:
      | isbn           |
      | 12345          |
      | 978604123456X  |
      | 97860412345678 |
```

#### FR-02 – Xem danh sách và tìm kiếm sách

Ưu tiên Must. Thủ thư xem danh sách đầu sách và tìm theo tên hoặc tác giả.

- **FR-02.1** Khi thủ thư mở trang Sách, hệ thống phải hiển thị tối đa 20 đầu sách mỗi trang, xếp theo tên A→Z, gồm ISBN, tên, tác giả, số bản còn/số bản.
- **FR-02.2** Khi thủ thư nhập từ khoá, hệ thống phải trả về các đầu sách có từ khoá trong tên hoặc tác giả, không phân biệt hoa thường, có phân biệt dấu.
- **FR-02.3** Khi không có kết quả, hệ thống phải hiển thị "Không tìm thấy sách phù hợp".

```gherkin
Feature: Xem và tìm sách
  Scenario: Phân trang
    Given thư viện có 25 đầu sách
    When thủ thư mở trang Sách
    Then thấy 20 đầu sách đầu tiên xếp theo tên A→Z và có liên kết tới trang 2

  Scenario: Tìm không phân biệt hoa thường
    Given có sách "Lập trình Python cơ bản"
    When thủ thư tìm "lập TRÌNH"
    Then kết quả có sách "Lập trình Python cơ bản"

  Scenario: Không có kết quả
    When thủ thư tìm "không-tồn-tại"
    Then hệ thống hiển thị "Không tìm thấy sách phù hợp"
```

#### FR-03 – Sửa và xoá đầu sách

Ưu tiên Should. Thủ thư sửa thông tin nhập sai và xoá đầu sách nhập nhầm.

- **FR-03.1** Khi thủ thư lưu thay đổi hợp lệ, hệ thống phải cập nhật đầu sách; ISBN mới (nếu đổi) vẫn phải thỏa BR-01.
- **FR-03.2** Khi số bản mới nhỏ hơn số bản đang cho mượn, hệ thống phải từ chối và hiển thị "Số bản không được nhỏ hơn số bản đang cho mượn (n)".
- **FR-03.3** Khi thủ thư xoá một đầu sách, hệ thống phải yêu cầu xác nhận trước khi xoá.
- **FR-03.4** Khi đầu sách đã có phiếu mượn, hệ thống phải từ chối xoá và hiển thị "Sách đã có lịch sử mượn, không thể xoá".

```gherkin
Feature: Sửa và xoá đầu sách
  Scenario: Giảm số bản dưới số đang cho mượn
    Given sách có 3 bản, trong đó 2 bản đang được mượn
    When thủ thư sửa số bản thành 1
    Then hệ thống báo "Số bản không được nhỏ hơn số bản đang cho mượn (2)"

  Scenario: Xoá sách chưa từng được mượn
    Given sách chưa có phiếu mượn nào
    When thủ thư bấm Xoá và xác nhận
    Then sách không còn trong danh sách

  Scenario: Xoá sách đã có lịch sử mượn
    Given sách có một phiếu mượn đã trả
    When thủ thư bấm Xoá và xác nhận
    Then hệ thống báo "Sách đã có lịch sử mượn, không thể xoá"
```

#### FR-04 – Thêm độc giả

Ưu tiên Must. Thủ thư cấp thẻ cho độc giả mới gồm họ tên, email và số điện thoại (tuỳ chọn).

- **FR-04.1** Khi thủ thư gửi biểu mẫu hợp lệ, hệ thống phải tạo độc giả và cấp mã thẻ kế tiếp theo BR-08.
- **FR-04.2** Khi email đã thuộc độc giả khác, hệ thống phải từ chối và hiển thị "Email đã được dùng".
- **FR-04.3** Khi họ tên trống hoặc email sai định dạng, hệ thống phải hiển thị lỗi cạnh ô tương ứng.

```gherkin
Feature: Thêm độc giả
  Scenario: Cấp mã thẻ tăng dần
    Given chưa có độc giả nào
    When thủ thư thêm độc giả "Trần Thị B", email "b.tran@example.com"
    And thủ thư thêm độc giả "Lê Văn C", email "c.le@example.com"
    Then hai độc giả có mã thẻ lần lượt "DG0001" và "DG0002"

  Scenario: Email trùng không phân biệt hoa thường
    Given đã có độc giả email "b.tran@example.com"
    When thủ thư thêm độc giả email "B.Tran@Example.com"
    Then hệ thống báo "Email đã được dùng"
```

#### FR-05 – Tạo phiếu mượn

Ưu tiên Must. Thủ thư lập phiếu khi độc giả mang sách đến quầy.

- **FR-05.1** Khi thủ thư lập phiếu cho độc giả và đầu sách thỏa BR-02, BR-04 và sách còn ít nhất 1 bản, hệ thống phải tạo phiếu với ngày mượn là hôm nay và hạn trả theo BR-03.
- **FR-05.2** Khi sách còn 0 bản, hệ thống phải từ chối và hiển thị "Sách đã hết bản".
- **FR-05.3** Khi độc giả đang có 3 phiếu mở, hệ thống phải từ chối và hiển thị "Độc giả đã mượn tối đa 3 cuốn".
- **FR-05.4** Khi độc giả có phiếu quá hạn chưa trả, hệ thống phải từ chối và hiển thị "Độc giả có sách quá hạn chưa trả".

```gherkin
Feature: Tạo phiếu mượn
  Scenario: Mượn thành công
    Given sách "Lập trình Python cơ bản" còn 3/3 bản
    And độc giả "DG0001" đang có 0 phiếu mở
    And hôm nay là 01/12/2026
    When thủ thư lập phiếu cho "DG0001" mượn sách này
    Then phiếu có hạn trả 15/12/2026
    And sách còn 2/3 bản

  Scenario: Đã mượn tối đa
    Given độc giả "DG0001" đang có 3 phiếu mở
    When thủ thư lập thêm một phiếu cho "DG0001"
    Then hệ thống báo "Độc giả đã mượn tối đa 3 cuốn"

  Scenario: Phiếu đã trả không tính vào giới hạn
    Given độc giả "DG0001" có 2 phiếu mở và 5 phiếu đã trả
    When thủ thư lập thêm một phiếu cho "DG0001"
    Then phiếu được tạo thành công

  Scenario: Có sách quá hạn
    Given độc giả "DG0002" có một phiếu mở hạn trả 30/11/2026
    And hôm nay là 01/12/2026
    When thủ thư lập phiếu mới cho "DG0002"
    Then hệ thống báo "Độc giả có sách quá hạn chưa trả"
```

#### FR-06 – Ghi nhận trả sách và tính phí trễ hạn

Ưu tiên Must. Thủ thư ghi nhận trả sách và biết ngay số tiền phạt nếu trễ.

- **FR-06.1** Khi thủ thư ghi nhận trả một phiếu đang mở, hệ thống phải lưu ngày trả là hôm nay, tính phí theo BR-05 và hiển thị số ngày trễ cùng số tiền.
- **FR-06.2** Khi phiếu đã được trả, hệ thống phải từ chối ghi nhận lần nữa và hiển thị "Phiếu đã được trả".

```gherkin
Feature: Trả sách
  Background:
    Given phiếu P1 đang mở có hạn trả 15/12/2026

  Scenario Outline: Tính phí trễ hạn
    When thủ thư ghi nhận trả P1 vào ngày <ngay_tra>
    Then số ngày trễ là <so_ngay> và phí là <phi> đồng
    Examples:
      | ngay_tra   | so_ngay | phi    |
      | 10/12/2026 | 0       | 0      |
      | 15/12/2026 | 0       | 0      |
      | 16/12/2026 | 1       | 5000   |
      | 18/12/2026 | 3       | 15000  |
      | 04/01/2027 | 20      | 100000 |
      | 14/01/2027 | 30      | 100000 |

  Scenario: Trả hai lần
    Given P1 đã được trả
    When thủ thư ghi nhận trả P1 lần nữa
    Then hệ thống báo "Phiếu đã được trả" và số bản còn không đổi
```

#### FR-07 – Xem danh sách phiếu quá hạn

Ưu tiên Should. Thủ thư xem ai đang giữ sách quá hạn để nhắc trả.

- **FR-07.1** Khi thủ thư mở trang Quá hạn, hệ thống phải liệt kê mọi phiếu quá hạn theo BR-03, xếp theo số ngày trễ giảm dần, gồm mã thẻ, họ tên, tên sách, hạn trả, số ngày trễ và phí tạm tính.
- **FR-07.2** Khi không có phiếu quá hạn, hệ thống phải hiển thị "Không có phiếu quá hạn".

```gherkin
Feature: Phiếu quá hạn
  Scenario: Sắp xếp và loại trừ
    Given hôm nay là 20/12/2026
    And có phiếu mở hạn trả 15/12/2026, phiếu mở hạn trả 18/12/2026 và phiếu mở hạn trả 20/12/2026
    When thủ thư mở trang Quá hạn
    Then thấy 2 phiếu: phiếu trễ 5 ngày (25.000 đ) trước, phiếu trễ 2 ngày (10.000 đ) sau
    And không thấy phiếu có hạn trả 20/12/2026
```

#### FR-08 – Đăng nhập và đăng xuất

Ưu tiên Should. Chỉ thủ thư đã đăng nhập mới được xem và thay đổi dữ liệu.

- **FR-08.1** Khi thủ thư nhập đúng tên đăng nhập và mật khẩu, hệ thống phải tạo phiên làm việc và chuyển tới trang Sách.
- **FR-08.2** Khi thông tin đăng nhập sai, hệ thống phải hiển thị chung "Tên đăng nhập hoặc mật khẩu không đúng", không nói rõ sai ô nào.
- **FR-08.3** Khi người chưa đăng nhập truy cập bất kỳ trang nào khác trang đăng nhập, hệ thống phải chuyển họ về trang đăng nhập.
- **FR-08.4** Khi thủ thư đăng xuất, hệ thống phải huỷ phiên làm việc.

```gherkin
Feature: Đăng nhập
  Scenario: Sai mật khẩu
    Given tồn tại tài khoản "thuthu"
    When người dùng đăng nhập "thuthu" với mật khẩu sai
    Then hệ thống báo "Tên đăng nhập hoặc mật khẩu không đúng"

  Scenario: Truy cập sau khi đăng xuất
    Given thủ thư đã đăng nhập rồi đăng xuất
    When mở địa chỉ trang Sách
    Then bị chuyển về trang đăng nhập
```

### 3.2 Yêu cầu giao diện bên ngoài

#### 3.2.1 Giao diện người dùng

Giao diện web tiếng Việt gồm 7 màn hình, dùng chung thanh menu: Sách · Độc giả · Mượn sách · Phiếu đang mở · Quá hạn · Đăng xuất. Lỗi nhập liệu hiển thị ngay cạnh ô bị sai; thông báo thành công hiển thị ở đầu trang.

| Mã | Màn hình | Yêu cầu | Thành phần chính |
| --- | --- | --- | --- |
| MH-01 | Đăng nhập | FR-08 | Ô tên đăng nhập, ô mật khẩu, nút Đăng nhập, vùng báo lỗi |
| MH-02 | Danh sách sách | FR-02, FR-03 | Ô tìm kiếm, bảng 20 dòng, phân trang, nút Thêm sách; mỗi dòng có Sửa, Xoá |
| MH-03 | Thêm / sửa sách | FR-01, FR-03 | ISBN, tên sách, tác giả, năm xuất bản, số bản, nút Lưu và Huỷ |
| MH-04 | Độc giả | FR-04 | Form thêm độc giả; bảng mã thẻ, họ tên, email, số phiếu mở |
| MH-05 | Mượn sách | FR-05 | Chọn độc giả theo mã thẻ, chọn sách (chỉ liệt kê sách còn bản), hạn trả dự kiến, nút Lưu |
| MH-06 | Phiếu đang mở | FR-06 | Bảng phiếu mở (độc giả, sách, ngày mượn, hạn trả), nút Trả; sau khi trả hiện số ngày trễ và phí |
| MH-07 | Quá hạn | FR-07 | Bảng phiếu quá hạn xếp theo số ngày trễ giảm dần, có phí tạm tính |

#### 3.2.2 Giao diện phần cứng

- Máy tính tại quầy thư viện có màn hình độ rộng từ 1366 px, bàn phím và chuột.
- Máy chủ trong mạng nội bộ của Khoa, cấu hình tối thiểu 2 nhân CPU, 2 GB RAM, 10 GB ổ đĩa trống.
- Phiên bản 1.0 không giao tiếp với máy quét mã vạch hay máy in.

#### 3.2.3 Giao diện phần mềm

- Hệ điều hành máy chủ: Linux hoặc Windows có cài Python 3.12 (chốt tại TBD-01).
- Cơ sở dữ liệu SQLite, truy cập qua SQLAlchemy.
- Không tích hợp với hệ thống khác của Trường. Việc nhập danh mục sách từ bảng tính hiện có được xem xét tại TBD-02.

#### 3.2.4 Giao diện truyền thông

- Trình duyệt kết nối tới máy chủ qua HTTPS trong mạng nội bộ.
- Phiên đăng nhập dùng cookie có thuộc tính HttpOnly và Secure.
- Hệ thống không gửi email, SMS và không gọi dịch vụ nào qua Internet.

### 3.3 Yêu cầu phi chức năng

Mỗi yêu cầu có ngưỡng đo được và cách kiểm chứng khi nghiệm thu.

#### 3.3.1 Hiệu năng

| Mã | Yêu cầu | Cách kiểm chứng |
| --- | --- | --- |
| NFR-01 | Trang danh sách sách và kết quả tìm kiếm trả về dưới 2 giây với 5.000 đầu sách | Sinh 5.000 bản ghi thử, đo thời gian phản hồi trên máy chủ triển khai |
| NFR-02 | Lập phiếu mượn và ghi nhận trả phản hồi dưới 1 giây | Đo 20 lần liên tiếp, lấy giá trị lớn nhất |
| NFR-03 | Hoạt động đúng với 2 thủ thư thao tác đồng thời | Hai máy cùng mượn bản cuối cùng của một sách: chỉ một phiếu được tạo |

#### 3.3.2 An toàn dữ liệu

| Mã | Yêu cầu | Cách kiểm chứng |
| --- | --- | --- |
| NFR-04 | Tạo phiếu, trả sách và cập nhật số bản còn thực hiện trong một giao dịch; lỗi giữa chừng thì không thay đổi gì | Kiểm thử tích hợp giả lập lỗi CSDL |
| NFR-05 | CSDL được sao lưu tự động mỗi ngày, giữ 30 bản gần nhất | Kiểm tra thư mục sao lưu sau 2 ngày vận hành |
| NFR-06 | Khôi phục từ bản sao lưu trong dưới 1 giờ | Diễn tập khôi phục trước khi nghiệm thu |
| NFR-07 | Mọi thao tác xoá phải được xác nhận | Kiểm thử thủ công |

#### 3.3.3 Bảo mật

| Mã | Yêu cầu | Cách kiểm chứng |
| --- | --- | --- |
| NFR-08 | Mật khẩu chỉ lưu dạng băm có salt (bcrypt hoặc PBKDF2) | Xem trực tiếp CSDL |
| NFR-09 | Mọi truy vấn CSDL tham số hoá; mọi dữ liệu hiển thị được escape | Thử nhập `' OR 1=1 --` và `<script>` vào ô tìm kiếm, tên sách |
| NFR-10 | Mọi biểu mẫu có mã chống CSRF | Gửi biểu mẫu không kèm mã: bị từ chối |
| NFR-11 | Phiên hết hạn sau 30 phút không thao tác | Kiểm thử với đồng hồ giả lập |
| NFR-12 | Sau 5 lần đăng nhập sai liên tiếp, tài khoản bị khoá 5 phút | Kiểm thử tự động |

#### 3.3.4 Thuộc tính chất lượng phần mềm

| Mã | Thuộc tính | Yêu cầu | Cách kiểm chứng |
| --- | --- | --- | --- |
| NFR-13 | Dễ sử dụng | Thủ thư mới tự thực hiện được thêm sách, cấp thẻ, mượn, trả sau 30 phút hướng dẫn | Thử với một thủ thư chưa dùng hệ thống |
| NFR-14 | Tin cậy | Hệ thống sẵn sàng từ 99% thời gian trong giờ mở cửa thư viện | Theo dõi nhật ký vận hành tháng đầu |
| NFR-15 | Dễ bảo trì | Kiến trúc phân lớp giao diện – nghiệp vụ – dữ liệu; độ phủ kiểm thử tầng nghiệp vụ từ 70%; mỗi BR có kiểm thử đơn vị | Báo cáo độ phủ kiểm thử |
| NFR-16 | Dễ triển khai | Cài đặt và chạy được trong 15 phút chỉ theo tài liệu cài đặt | Phụ trách hạ tầng làm thử |
| NFR-17 | Tương thích | Chạy đúng trên Chrome và Edge phiên bản hiện hành | Kiểm thử thủ công trước phát hành |

#### 3.3.5 Quy tắc nghiệp vụ

Các quy tắc do Trưởng thư viện ban hành và áp dụng thống nhất cho mọi giao dịch.

| Mã | Quy tắc | Trường hợp biên cần kiểm thử |
| --- | --- | --- |
| BR-01 | ISBN gồm 13 chữ số, hoặc 10 ký tự với 9 ký tự đầu là chữ số và ký tự cuối là chữ số hoặc X; dấu gạch được bỏ trước khi kiểm tra; không trùng giữa các đầu sách | 9, 10, 11, 13, 14 ký tự; X ở vị trí cuối và vị trí khác; có dấu gạch |
| BR-02 | Mỗi độc giả có tối đa 3 phiếu mở cùng lúc | Đang có 2 phiếu (được), 3 phiếu (không); phiếu đã trả không tính |
| BR-03 | Hạn trả = ngày mượn + 14 ngày; phiếu quá hạn khi còn mở và hạn trả trước hôm nay | Mượn cuối tháng, cuối năm; hạn trả đúng hôm nay (chưa quá hạn) |
| BR-04 | Độc giả có phiếu quá hạn thì không được mượn thêm | Phiếu quá hạn đã trả rồi thì được mượn lại |
| BR-05 | Phí trễ = 5.000 đ × số ngày trễ, tối đa 100.000 đ mỗi phiếu; trả đúng ngày hạn thì trễ 0 ngày | Trễ 0, 1, 19, 20, 21, 30 ngày |
| BR-06 | Chỉ xoá được đầu sách chưa từng có phiếu mượn | Sách có phiếu đã trả vẫn không xoá được |
| BR-07 | Số bản từ 1 trở lên; số bản còn = số bản − số phiếu mở của đầu sách, không bao giờ âm | Mượn bản cuối cùng; giảm số bản khi đang có phiếu mở |
| BR-08 | Mã thẻ tự sinh dạng `DG` + 4 chữ số, tăng dần từ `DG0001`; email đúng định dạng, lưu chữ thường và không trùng | Độc giả đầu tiên; email chỉ khác nhau ở chữ hoa (coi là trùng) |

### 3.4 Đặc tính hệ thống

Các đặc tính dưới đây áp dụng chung cho mọi chức năng, giúp người dùng hiểu lỗi và giúp phụ trách hạ tầng truy vết sự cố.

| Mã | Đặc tính | Yêu cầu |
| --- | --- | --- |
| SF-01 | Xử lý lỗi nhập liệu | Lỗi hiển thị cạnh ô bị sai bằng câu tiếng Việt; dữ liệu đã nhập được giữ nguyên |
| SF-02 | Xử lý lỗi hệ thống | Hiển thị trang "Đã có lỗi xảy ra, vui lòng thử lại hoặc liên hệ phụ trách CNTT" kèm mã sự cố; không hiển thị chi tiết kỹ thuật |
| SF-03 | Nhật ký lỗi | Ghi thời điểm, mã sự cố và chi tiết kỹ thuật vào tệp nhật ký trên máy chủ; lưu 90 ngày |
| SF-04 | Nhật ký nghiệp vụ | Ghi mỗi lần tạo phiếu, trả sách, sửa hoặc xoá sách: thời điểm, tài khoản thủ thư, đối tượng bị thay đổi |
| SF-05 | Nhật ký đăng nhập | Ghi mỗi lần đăng nhập thành công, thất bại và bị khoá; không ghi mật khẩu |
| SF-06 | Kiểm tra tình trạng | Địa chỉ `/health` trả mã 200 khi ứng dụng và CSDL hoạt động, phục vụ giám sát |

## 4. Yêu cầu khác

### 4.1 Yêu cầu cơ sở dữ liệu

CSDL gồm 3 bảng nghiệp vụ và 1 bảng tài khoản; mỗi đầu sách và mỗi độc giả có nhiều phiếu mượn.

&#91;embedded content: mô hình dữ liệu · 3 bảng nghiệp vụ\]

Một phiếu đang mở khi `ngay_tra` còn rỗng; các quy tắc về số bản còn, giới hạn 3 cuốn và quá hạn đều dựa vào cột này.

| Bảng | Cột | Kiểu | Ràng buộc |
| --- | --- | --- | --- |
| sach | isbn | chuỗi 13 | Bắt buộc, duy nhất, lưu không dấu gạch (BR-01) |
| sach | ten, tac\_gia | chuỗi 200 | Bắt buộc |
| sach | nam\_xb | số nguyên | Tuỳ chọn |
| sach | so\_ban | số nguyên | Bắt buộc, ≥ 1 (BR-07) |
| doc\_gia | ma\_the | chuỗi 6 | Tự sinh, duy nhất (BR-08) |
| doc\_gia | ho\_ten | chuỗi 100 | Bắt buộc |
| doc\_gia | email | chuỗi 120 | Bắt buộc, duy nhất, lưu chữ thường (BR-08) |
| doc\_gia | sdt | chuỗi 15 | Tuỳ chọn |
| phieu\_muon | sach\_id, doc\_gia\_id | khoá ngoại | Bắt buộc |
| phieu\_muon | ngay\_muon, han\_tra | ngày | Bắt buộc; han\_tra = ngay\_muon + 14 (BR-03) |
| phieu\_muon | ngay\_tra | ngày | Rỗng khi đang mở |
| phieu\_muon | tien\_phat | số nguyên (đồng) | Mặc định 0, tính khi trả (BR-05) |
| thu\_thu | ten\_dang\_nhap | chuỗi 50 | Bắt buộc, duy nhất |
| thu\_thu | mat\_khau\_hash | chuỗi 255 | Chỉ lưu bản băm (NFR-08) |

**Yêu cầu chung về dữ liệu:**

- **DB-01** Số bản còn được tính từ các phiếu mở, không lưu thành cột riêng, để không bao giờ lệch với dữ liệu phiếu.
- **DB-02** Ràng buộc khoá ngoại, duy nhất và bắt buộc phải được khai báo ở mức CSDL, không chỉ kiểm tra trong mã nguồn.
- **DB-03** Phiếu mượn không bao giờ bị xoá, để giữ lịch sử và đối chiếu tiền phạt.
- **DB-04** Dữ liệu lưu bằng mã UTF-8, ngày lưu theo chuẩn ISO (YYYY-MM-DD).
- **DB-05** Thay đổi cấu trúc CSDL được thực hiện bằng tệp migration có phiên bản.

### 4.2 Yêu cầu pháp lý và quy định

Hệ thống lưu họ tên, email, số điện thoại của độc giả nên phải tuân thủ [Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15](https://thuvienphapluat.vn/van-ban/Cong-nghe-thong-tin/Luat-Bao-ve-du-lieu-ca-nhan-2025-91-2025-QH15-625628.aspx), có hiệu lực từ 01/01/2026. Luật trao cho chủ thể dữ liệu các quyền được biết, đồng ý, truy cập, sửa và yêu cầu xoá dữ liệu. Các yêu cầu dưới đây cần bộ phận pháp chế của Trường rà soát trước khi phê duyệt (TBD-05).

| Mã | Yêu cầu |
| --- | --- |
| LG-01 | Chỉ thu thập dữ liệu cần cho mượn – trả: họ tên, email, số điện thoại (tuỳ chọn) |
| LG-02 | Khi cấp thẻ, độc giả được thông báo mục đích xử lý dữ liệu và xác nhận đồng ý; mẫu thông báo do Thư viện ban hành |
| LG-03 | Yêu cầu xem, sửa, xoá dữ liệu của độc giả phải được xử lý; cách xử lý trong phiên bản 1.0 chốt tại TBD-03 |
| LG-04 | Chỉ tài khoản thủ thư đã đăng nhập mới xem được dữ liệu độc giả; bản sao lưu chỉ lưu trong mạng nội bộ của Khoa |
| LG-05 | Khi phát hiện lộ lọt dữ liệu, phụ trách hạ tầng báo ngay cho Trưởng thư viện để thực hiện thông báo theo quy định |

### 4.3 Quốc tế hoá và bản địa hoá

- Giao diện, thông báo và nhãn hoàn toàn bằng tiếng Việt có dấu, mã UTF-8.
- Ngày hiển thị dạng dd/mm/yyyy; múi giờ UTC+7.
- Tiền hiển thị dạng "15.000 đ" (dấu chấm ngăn cách hàng nghìn, không có phần thập phân).
- Sắp xếp theo tên dùng thứ tự chữ cái tiếng Việt (ví dụ "Đ" đứng sau "D").
- Văn bản giao diện đặt tập trung, tách khỏi mã xử lý, để có thể bổ sung tiếng Anh ở phiên bản sau (Could).

### 4.4 Quản lý rủi ro (ma trận FMEA)

Mỗi chế độ lỗi được chấm độ nghiêm trọng (S), khả năng xảy ra (O) và khả năng phát hiện (D, càng cao càng khó phát hiện) trên thang 1–10; RPN = S × O × D. Rủi ro có RPN từ 100 phải có biện pháp hoàn thành trước khi phát hành.

| Chế độ lỗi | Nguyên nhân | Ảnh hưởng | S | O | D | RPN | Biện pháp |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Lộ dữ liệu cá nhân độc giả | SQL injection, mật khẩu yếu, dò mật khẩu | Vi phạm LG-04, ảnh hưởng uy tín | 9 | 3 | 5 | 135 | NFR-08 đến NFR-12; rà soát bảo mật trước phát hành |
| Phiếu gán nhầm độc giả hoặc sách | Thủ thư chọn nhầm mã thẻ, ISBN | Tính phí và quá hạn cho sai người | 5 | 5 | 5 | 125 | MH-05 hiển thị họ tên và tên sách để xác nhận trước khi lưu |
| Số bản còn bị âm | Hai thủ thư cùng mượn bản cuối cùng | Cho mượn sách không có trên giá | 6 | 3 | 6 | 108 | NFR-03, NFR-04: kiểm tra và tạo phiếu trong cùng giao dịch |
| Tính sai phí trễ hạn | Lệch một ngày ở ranh giới hạn trả, sai múi giờ, quên mức trần | Thu sai tiền, khiếu nại | 7 | 4 | 3 | 84 | Kiểm thử biên BR-05; cố định múi giờ UTC+7 |
| Mất dữ liệu | Hỏng ổ đĩa máy chủ | Mất lịch sử mượn – trả | 9 | 2 | 4 | 72 | NFR-05, NFR-06: sao lưu hằng ngày, diễn tập khôi phục |
| Hệ thống ngừng trong giờ mở cửa | Máy chủ hoặc mạng nội bộ gặp sự cố | Không lập được phiếu | 6 | 3 | 2 | 36 | SF-06 giám sát; ghi phiếu giấy tạm thời và nhập lại sau |

## 5. Phụ lục

### 5.1 Bảng thuật ngữ nghiệp vụ

| Thuật ngữ | Ý nghĩa |
| --- | --- |
| Đầu sách | Một tựa sách, xác định bằng ISBN; một đầu sách có thể có nhiều bản |
| Bản sách | Một cuốn vật lý của đầu sách |
| Số bản còn | Số bản của đầu sách đang nằm trên giá, chưa được mượn |
| Độc giả | Người được cấp thẻ và có quyền mượn sách |
| Mã thẻ | Mã định danh độc giả dạng DG0001 |
| Phiếu mượn | Ghi nhận một độc giả mượn một bản của một đầu sách |
| Phiếu đang mở | Phiếu mượn chưa có ngày trả |
| Phiếu quá hạn | Phiếu đang mở có hạn trả trước ngày hôm nay |
| Phí trễ hạn | Số tiền độc giả phải nộp khi trả sách sau hạn, tính theo BR-05 |

### 5.2 Use case và sơ đồ

Thủ thư là tác nhân duy nhất; mỗi use case tương ứng một yêu cầu chức năng ở mục 3.1. Sơ đồ dữ liệu nằm ở mục 4.1.

&#91;embedded content: sơ đồ use case · 1 tác nhân, 8 chức năng\]

Trừ FR-08, mọi use case yêu cầu thủ thư đã đăng nhập.

### 5.3 Danh sách nội dung chưa xác định (TBD)

| Mã | Nội dung cần chốt | Người chịu trách nhiệm | Ảnh hưởng tới |
| --- | --- | --- | --- |
| TBD-01 | Máy chủ và hệ điều hành triển khai | Phụ trách hạ tầng CNTT | 2.2, 3.2.2, 3.2.3 |
| TBD-02 | Có nhập danh mục sách từ bảng tính hiện có không; định dạng tệp | Trưởng thư viện | 3.2.3, phạm vi 1.4 |
| TBD-03 | Cách xử lý yêu cầu xem, sửa, xoá dữ liệu cá nhân của độc giả: thủ công hoặc bổ sung chức năng mới | Trưởng thư viện | 2.2, LG-03 |
| TBD-04 | Giờ mở cửa thư viện dùng để đo NFR-14 | Trưởng thư viện | NFR-14 |
| TBD-05 | Rà soát pháp lý mục 4.2 | Bộ phận pháp chế của Trường | 4.2 |
| TBD-06 | Mẫu thông báo và xác nhận đồng ý xử lý dữ liệu khi cấp thẻ | Trưởng thư viện | LG-02, FR-04 |
