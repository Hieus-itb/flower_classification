import tensorflow as tf
import pathlib
import shutil
import os
import random

print("🔍 Đang tải dataset...")

# Download dataset
dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
data_dir = tf.keras.utils.get_file('flower_photos', origin=dataset_url, untar=True)
data_dir = pathlib.Path(data_dir)

print(f"📂 Dataset location: {data_dir}")

# Kiểm tra các thư mục có sẵn
print("\n🔍 Kiểm tra cấu trúc thư mục:")
all_dirs = [d for d in data_dir.iterdir() if d.is_dir()]
print(f"Tìm thấy {len(all_dirs)} thư mục: {[d.name for d in all_dirs]}")

# Tạo thư mục test_images
test_dir = pathlib.Path('test_images')
if test_dir.exists():
    shutil.rmtree(test_dir)
test_dir.mkdir()

print(f"\n📁 Đã tạo thư mục: {test_dir.absolute()}")

# Các loại hoa
flower_types = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']

print("\n📸 Đang copy ảnh test...")

total_copied = 0

for flower in flower_types:
    flower_dir = data_dir / flower

    print(f"\n🌸 Đang xử lý: {flower}")
    print(f"   Thư mục: {flower_dir}")

    if not flower_dir.exists():
        print(f"   ⚠️  Thư mục không tồn tại!")
        continue

    # Lấy tất cả ảnh .jpg
    images = list(flower_dir.glob('*.jpg'))
    print(f"   Tìm thấy: {len(images)} ảnh")

    if len(images) == 0:
        print(f"   ⚠️  Không có ảnh .jpg!")
        continue

    # Chọn ngẫu nhiên 3 ảnh
    num_to_copy = min(3, len(images))
    selected = random.sample(images, num_to_copy)

    # Copy vào thư mục test
    for i, img_path in enumerate(selected, 1):
        new_name = f"{flower}_{i}.jpg"
        dest = test_dir / new_name
        shutil.copy(img_path, dest)
        print(f"   ✅ {new_name}")
        total_copied += 1

print(f"\n{'=' * 50}")
if total_copied > 0:
    print(f"🎉 Hoàn tất! Đã tạo {total_copied} ảnh test")
    print(f"📂 Vị trí: {test_dir.absolute()}")
    print(f"\n💡 Các file trong test_images:")
    for img in sorted(test_dir.glob('*.jpg')):
        print(f"   - {img.name}")
    print(f"\n✨ Bây giờ bạn có thể upload các ảnh này trong demo app!")
else:
    print(f"❌ Không copy được ảnh nào!")
    print(f"\n🔍 Debug info:")
    print(f"   Dataset dir: {data_dir}")
    print(f"   Các thư mục con: {[d.name for d in data_dir.iterdir() if d.is_dir()]}")

    # Thử tìm ảnh ở bất kỳ đâu
    all_jpgs = list(data_dir.rglob('*.jpg'))
    print(f"   Tổng số .jpg files: {len(all_jpgs)}")
    if len(all_jpgs) > 0:
        print(f"   Ví dụ: {all_jpgs[0]}")