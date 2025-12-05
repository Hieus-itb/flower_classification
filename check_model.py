import json
import os
import tensorflow as tf
import numpy as np

# Kiểm tra file class_names.json
print("🔍 Đang kiểm tra model...")

json_path = 'models/class_names.json'
model_path = 'models/flower_model.h5'

if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        class_names = json.load(f)

    print(f"\n📋 Class names hiện tại: {class_names}")
    print(f"📊 Số lượng classes trong JSON: {len(class_names)}")

    # Load model và kiểm tra output shape
    if os.path.exists(model_path):
        print("\n🤖 Đang load model...")
        model = tf.keras.models.load_model(model_path)

        # Kiểm tra output layer
        output_shape = model.output_shape
        num_classes_model = output_shape[-1]

        print(f"📊 Số lượng classes trong MODEL: {num_classes_model}")
        print(f"📐 Output shape: {output_shape}")

        if len(class_names) != num_classes_model:
            print(f"\n⚠️  LỖI KHÔNG KHỚP!")
            print(f"   JSON có {len(class_names)} classes")
            print(f"   Model có {num_classes_model} classes")
            print(f"\n🔧 Cần train lại model!")
        else:
            print(f"\n✅ Model và class_names khớp nhau!")

    print(f"\n📊 Số lượng classes: {len(class_names)}")

    # Kiểm tra nếu có 'flower_photos' trong danh sách
    if 'flower_photos' in class_names:
        print("\n⚠️  PHÁT HIỆN LỖI: Có class 'flower_photos' không hợp lệ!")
        print("🔧 Đang sửa...")

        # Xóa 'flower_photos' khỏi danh sách
        class_names = [name for name in class_names if name != 'flower_photos']

        # Lưu lại
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(class_names, f, ensure_ascii=False, indent=2)

        print(f"✅ Đã sửa! Class names mới: {class_names}")
        print(f"✅ Số lượng classes: {len(class_names)}")
    else:
        print("\n✅ Model OK! Không có lỗi.")
        print(f"✅ Các loại hoa hợp lệ: {', '.join(class_names)}")
else:
    print(f"\n❌ Không tìm thấy file {json_path}")
    print("💡 Vui lòng chạy train_model.py trước!")

print("\n" + "=" * 50)

# Kiểm tra model file
model_path = 'models/flower_model.h5'
if os.path.exists(model_path):
    print(f"✅ Model file tồn tại: {model_path}")

    # Kiểm tra kích thước
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"📦 Kích thước model: {size_mb:.2f} MB")
else:
    print(f"❌ Không tìm thấy model: {model_path}")

print("\n💡 Nếu vẫn lỗi, hãy train lại model bằng cách chạy: python train_model.py")