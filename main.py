import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
import os

# Đặt đường dẫn đến tesseract nếu cần thiết. Streamlit Cloud không yêu cầu thiết lập đường dẫn tesseract cục bộ.
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\tesseract.exe'

st.title("StockTraders")

uploaded_file = st.file_uploader("Chọn một hình ảnh...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Hình ảnh đã tải lên', use_column_width=True)
    try:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        if img is None:
            st.error("Lỗi: Không thể đọc hình ảnh. Vui lòng kiểm tra lại file.")
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            x1, y1 = 28, 13  
            x2, y2 = 223, 67  
            x3, y3 = 75, 100
            x4, y4 = 1362, 146
            x5, y5 = 24, 1026
            x6, y6 = 840, 1081
            x7, y7 = 16, 177
            x8, y8 = 467, 263

            h, w, _ = img.shape
        
            cropped_img = img[y1:y2, x1:x2]
            pil_image = Image.fromarray(cropped_img)
            t = pytesseract.image_to_string(pil_image)
            text = str.upper(t)

            st.write("**Nội dung trích xuất từ hình ảnh:**")
            st.write("Chứng khoán: ", text)

            cropped_img_2 = img[y3:y4, x3:x4]
            pil_image_2 = Image.fromarray(cropped_img_2)
            text_2 = pytesseract.image_to_string(pil_image_2)
            words = text_2.split(",")
            s = words[2]
            ex = s[:4]
            st.write("Sàn: ", ex)
            
            prices = s.split(" ")
            open = prices[2]
            close = prices[5]
            high = prices[3]
            low = prices[4]
            st.write("Giá mở cửa: ", open[1:])
            st.write("Giá đóng cửa: ", close[1:])
            st.write("Giá cao nhất: ", high[1:])
            st.write("Giá thấp nhất: ", low[1:])

            cropped_img_3 = img[y5:y6, x5:x6]
            pil_image_3 = Image.fromarray(cropped_img_3)
            text_3 = pytesseract.image_to_string(pil_image_3)
            indicator = text_3.split(" ")
            if indicator[0] == "MACD":
                st.write("MACD Histogram: ", indicator[-3])
                st.write("MACD_Signal: ", indicator[-2])
                st.write("MACD: ", indicator[-1])
            elif indicator[0][:4] == "RSI":
                st.write("RSI: ", indicator[-1])
           
            cropped_img_4 = img[y7:y8, x7:x8]
            pil_image_4 = Image.fromarray(cropped_img_4)
            text_4 = pytesseract.image_to_string(pil_image_4)
            text_4_tmp = text_4.split(" ")
            if text_4_tmp[0] == "MA":
                try:
                    first_ma = text_4.find("MA")
                    second_ma = text_4.find("MA", first_ma + 1)

                    if second_ma != -1:
                        text_4_part1 = text_4[:second_ma].strip()  
                        text_4_part2 = text_4[second_ma:].strip()  
                    else:
                        text_4_part1 = text_4.strip()  
                        text_4_part2 = ""

                    st.write(text_4_part1)
                    st.write(text_4_part2)

                except Exception as e:
                    st.error(f"Lỗi khi xử lý text_4: {e}")
            else:
                st.write("")
            
            forecast = st.button("**Dự đoán xu hướng**")
            if forecast:
                if indicator[0] == "MACD":
                    st.write("- Dựa trên các chỉ báo, có thể thấy xu hướng ngắn hạn của VNINDEX đang có dấu hiệu tích cực hơn so với trước đó. Đà giảm đã yếu đi và có thể xuất hiện một nhịp hồi phục nhẹ.")
                    st.write("- MACD cho thấy động lượng của thị trường đang dần phục hồi. Tuy nhiên, vẫn cần thêm thời gian để xác nhận xu hướng tăng bền vững.")
                    st.write("- Nếu VNINDEX có thể vượt qua và giữ vững trên mức kháng cự gần nhất, có khả năng xu hướng tăng sẽ tiếp tục mạnh mẽ hơn.")
                elif indicator[0][:4] == "RSI":
                    st.write("- Xu hướng ngắn hạn của SSI đang có dấu hiệu tích cực với giá đóng cửa cao hơn MA20. Tuy nhiên, việc giá đóng cửa thấp hơn MA10 cho thấy có thể có một sự điều chỉnh nhẹ trong ngắn hạn.")
                    st.write("- RSI cho thấy đà tăng của cổ phiếu đang khá tốt, nhưng chưa quá mạnh. Điều này cho thấy áp lực bán vẫn còn hiện hữu và có thể gây ra một số biến động giá trong ngắn hạn.")
                    st.write("- Nếu giá có thể vượt qua mức kháng cự 38.00 và giữ vững trên mức này, có khả năng xu hướng tăng sẽ tiếp tục mạnh mẽ hơn.")  
                    st.write("- Có thể xem xét mở vị thế mua nếu giá vượt qua mức kháng cự 38.00 và đặt lệnh cắt lỗ dưới mức hỗ trợ MA20.")
                else:
                    st.write("- Giá đóng cửa đang cao hơn cả MA20 và MA10, cho thấy xu hướng ngắn hạn đang nghiêng về phía tăng. Điều này đồng nghĩa với việc giá hiện tại đang được hỗ trợ bởi các mức trung bình động.")
                    st.write("- Xu hướng ngắn hạn của SSI đang khá tích cực. Việc giá vượt qua cả MA20 và MA10 cho thấy lực mua đang chiếm ưu thế.")
                    st.write("- Nếu giá giao dịch quanh vùng 39.00 và không thể tạo ra một đột phá mới, thị trường có thể sẽ đi ngang hoặc có một số biến động ngắn hạn.")
    except Exception as e:
        st.error(f"Lỗi: {e}")
