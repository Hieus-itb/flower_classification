import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import json

# Cấu hình trang
st.set_page_config(
    page_title="Phân loại hoa",
    page_icon="🌸",
    layout="centered"
)

# CSS tùy chỉnh
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)


# Load model và class names
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('models/flower_model.h5')
    return model


@st.cache_data
def load_class_names():
    with open('models/class_names.json', 'r', encoding='utf-8') as f:
        class_names = json.load(f)
    return class_names


# Hàm dự đoán
def predict_flower(image, model, class_names):
    # Resize ảnh
    img = image.resize((180, 180))

    # Chuyển thành array và chuẩn hóa
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Tạo batch

    # Dự đoán
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    # Lấy kết quả
    predicted_class = class_names[np.argmax(score)]
    confidence = 100 * np.max(score)

    return predicted_class, confidence, score


# Giao diện chính
st.title("🌸 Phân loại hoa với Deep Learning")
st.write("Upload ảnh hoa và model sẽ dự đoán loại hoa!")

# Load model
try:
    model = load_model()
    class_names = load_class_names()
    st.success(f"✅ Model đã sẵn sàng! Có thể nhận diện {len(class_names)} loại hoa")
    st.info(f"**Các loại hoa:** {', '.join(class_names)}")
except:
    st.error("⚠️ Không tìm thấy model. Vui lòng train model trước!")
    st.stop()

# Upload ảnh
uploaded_file = st.file_uploader(
    "Chọn ảnh hoa...",
    type=['jpg', 'jpeg', 'png']
)

# Tạo 2 cột
col1, col2 = st.columns(2)

if uploaded_file is not None:
    # Hiển thị ảnh gốc
    image = Image.open(uploaded_file)

    with col1:
        st.subheader("📷 Ảnh gốc")
        st.image(image, use_container_width=True)

    # Dự đoán
    with st.spinner('🔍 Đang phân tích...'):
        predicted_class, confidence, scores = predict_flower(image, model, class_names)

    with col2:
        st.subheader("🎯 Kết quả dự đoán")

        # Hiển thị kết quả chính
        st.metric(
            label="Loại hoa",
            value=predicted_class.upper(),
            delta=f"{confidence:.2f}% độ tin cậy"
        )

        # Hiển thị biểu đồ xác suất
        st.write("**Xác suất cho từng loại:**")
        for i, class_name in enumerate(class_names):
            prob = scores[i] * 100
            st.progress(float(prob / 100))
            st.write(f"{class_name}: {prob:.2f}%")

    # Thêm thông tin
    st.divider()
    st.info("""
    **💡 Gợi ý:**
    - Model hoạt động tốt nhất với ảnh rõ nét
    - Hoa nên chiếm phần lớn trong ảnh
    - Ánh sáng tốt giúp dự đoán chính xác hơn
    """)
else:
    st.info("👆 Vui lòng upload ảnh hoa để bắt đầu")

    # Ảnh mẫu
    st.subheader("📸 Ví dụ về các loại hoa")
    st.write(
        "Model có thể nhận diện các loại hoa phổ biến như hoa hồng, hoa cúc, hoa tulip, hoa hướng dương, và hoa bồ công anh.")

# Footer
st.divider()
st.caption("🤖 Demo Phân loại hoa với TensorFlow & Streamlit")