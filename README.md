# Multi-dimensional data Visualization

## 1. Mục tiêu bài làm

Dự án này tạo 4 biểu đồ trực quan hóa dữ liệu khí hậu/thời tiết đa chiều bằng Python. Mã nguồn nằm trong `src/create_visualizations.py`, dữ liệu đầu vào nằm trong thư mục `data/`, và toàn bộ hình ảnh đầu ra được lưu trong thư mục `output/` với độ phân giải 300 DPI.

Bộ sản phẩm đáp ứng 3 yêu cầu chính:

| Sản phẩm | File/thư mục | Trạng thái |
|---|---|---|
| Mã nguồn Python | `src/create_visualizations.py` | Hoàn thành, có chú thích và chia hàm rõ ràng |
| Bộ 4 hình ảnh | `output/*.png` | Hoàn thành, 300 DPI, có tiêu đề, nhãn trục, thang màu và legend |
| Báo cáo ngắn | `README.md` | Hoàn thành, giải thích tiền xử lý và nhận xét khoa học |

## 2. Cấu trúc thư mục

```text
multi-dimensional-data-visualization/
├── data/
│   ├── global_temp.csv
│   ├── minnesota_weather.csv
│   └── weather_data.csv
├── output/
│   ├── global_temp_heatmap.png
│   ├── minnesota_precip_line.png
│   ├── weather_heatmap.png
│   └── weather_scatter.png
├── src/
│   └── create_visualizations.py
└── README.md
```

## 3. Cách chạy chương trình

Cài các thư viện cần thiết:

```bash
pip install pandas numpy matplotlib seaborn
```

Chạy script từ thư mục gốc dự án:

```bash
python src/create_visualizations.py
```

Sau khi chạy, chương trình tự tạo/cập nhật 4 file `.png` trong thư mục `output/`.

## 4. Dữ liệu sử dụng

### 4.1. `weather_data.csv`

Dữ liệu thời tiết theo ngày của nhiều thành phố, gồm các biến như thành phố, ngày, tháng, nhiệt độ trung bình, độ ẩm trung bình, lượng mưa và các yếu tố thời tiết khác.

Các biểu đồ sử dụng file này:

- `weather_heatmap.png`
- `weather_scatter.png`

### 4.2. `global_temp.csv`

Dữ liệu bất thường nhiệt độ toàn cầu theo năm và theo tháng. File gốc có một dòng mô tả ở đầu nên khi đọc dữ liệu cần dùng `skiprows=1`. Một số giá trị thiếu được ký hiệu bằng `***`, được chuyển thành `NA` trước khi chuyển kiểu số.

Biểu đồ sử dụng file này:

- `global_temp_heatmap.png`

### 4.3. `minnesota_weather.csv`

Dữ liệu thời tiết theo tháng tại các điểm quan trắc ở Minnesota, gồm năm, tháng, điểm đo, lượng mưa, nhiệt độ thấp nhất và cao nhất.

Biểu đồ sử dụng file này:

- `minnesota_precip_line.png`

## 5. Tiền xử lý dữ liệu

Các bước tiền xử lý chính trong `create_visualizations.py`:

1. Chuyển các cột định lượng như `avg_temp`, `avg_humidity`, `precip`, `year`, `month`, `mo` sang kiểu số bằng `pd.to_numeric(..., errors="coerce")`.
2. Với dữ liệu nhiệt độ toàn cầu, thay ký hiệu thiếu `***` bằng `pd.NA` để tránh lỗi khi vẽ heatmap.
3. Gom nhóm dữ liệu theo chiều phân tích phù hợp:
   - Theo `city` và `month` để tính nhiệt độ trung bình theo tháng.
   - Theo `site` và `date` để phân tích lượng mưa theo thời gian.
4. Dùng `pivot()` để chuyển dữ liệu từ dạng dài sang ma trận khi vẽ heatmap.
5. Tạo cột ngày `date` từ `year`, `mo`, và ngày mặc định là 1 để vẽ chuỗi thời gian.
6. Xuất toàn bộ hình ảnh bằng `plt.savefig(..., dpi=300, bbox_inches="tight")`.

## 6. Mô tả và nhận xét từng biểu đồ

### 6.1. `weather_heatmap.png` – Nhiệt độ trung bình theo thành phố và tháng

Biểu đồ heatmap thể hiện nhiệt độ trung bình theo từng tháng của từng thành phố. Trục X là tháng, trục Y là thành phố, màu sắc biểu diễn mức nhiệt độ trung bình.

**Nhận xét khoa học:** Các tháng mùa hè có màu nóng hơn, thể hiện nhiệt độ trung bình cao hơn so với các tháng mùa đông. Sự khác biệt giữa các thành phố cho thấy yếu tố vị trí địa lý có ảnh hưởng rõ rệt đến đặc điểm nhiệt độ theo mùa.

### 6.2. `weather_scatter.png` – Quan hệ giữa độ ẩm, nhiệt độ, lượng mưa và thành phố

Biểu đồ scatter dùng trục X cho độ ẩm trung bình, trục Y cho nhiệt độ trung bình, màu sắc cho thành phố và kích thước điểm cho lượng mưa.

**Nhận xét khoa học:** Những điểm có kích thước lớn thường tập trung ở vùng độ ẩm cao hơn, cho thấy lượng mưa có xu hướng liên quan đến điều kiện không khí ẩm. Việc mã hóa đồng thời bằng màu và kích thước giúp quan sát được nhiều biến trong cùng một biểu đồ.

### 6.3. `global_temp_heatmap.png` – Bất thường nhiệt độ toàn cầu theo năm và tháng

Biểu đồ heatmap thể hiện bất thường nhiệt độ toàn cầu từ năm 1880 đến 2025. Trục X là tháng, trục Y là năm, màu sắc biểu diễn mức bất thường nhiệt độ so với mốc chuẩn 1951–1980.

**Nhận xét khoa học:** Các năm gần đây xuất hiện nhiều vùng màu đỏ hơn, thể hiện mức bất thường nhiệt độ dương cao hơn so với giai đoạn đầu chuỗi dữ liệu. Xu hướng này phản ánh sự gia tăng nhiệt độ toàn cầu theo thời gian.

### 6.4. `minnesota_precip_line.png` – Lượng mưa theo tháng tại các điểm đo ở Minnesota

Biểu đồ đường thể hiện lượng mưa theo thời gian tại nhiều điểm đo. Trục X là thời gian, trục Y là lượng mưa, mỗi đường biểu diễn một địa điểm.

**Nhận xét khoa học:** Lượng mưa thay đổi mạnh theo mùa và theo từng điểm đo. Một số tháng có đỉnh lượng mưa cao hơn rõ rệt, cho thấy tính mùa vụ của lượng mưa và sự khác biệt không gian giữa các địa điểm quan trắc.

## 7. Kết luận

Bài làm đã sử dụng Pandas để làm sạch, chuyển đổi và tổng hợp dữ liệu; sử dụng Seaborn/Matplotlib để trực quan hóa dữ liệu đa chiều. Bốn biểu đồ đầu ra đều có tiêu đề, nhãn trục, legend hoặc thang màu đầy đủ, và được lưu dưới định dạng `.png` 300 DPI theo đúng yêu cầu, qua đó rút ra được những nhận xét khoa học dựa theo từng biểu đồ.
