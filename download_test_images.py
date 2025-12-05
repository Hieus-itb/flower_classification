import urllib.request
import os
from pathlib import Path

# Tạo thư mục test_images
test_dir = Path('test_images')
test_dir.mkdir(exist_ok=True)

print("📥 Đang tải ảnh test từ internet...")
print(f"📂 Lưu vào: {test_dir.absolute()}\n")

# Danh sách URL ảnh mẫu (từ Unsplash - miễn phí)
test_images = {
    'roses_1.jpg': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400',
    'roses_2.jpg': 'https://images.unsplash.com/photo-1455659817273-f96807779a8a?w=400',
    'roses_3.jpg': 'https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400',

    'tulips_1.jpg': 'https://images.unsplash.com/photo-1520763185298-1b434c919102?w=400',
    'tulips_2.jpg': 'https://images.unsplash.com/photo-1524386416438-98b9b2d4b433?w=400',
    'tulips_3.jpg': 'https://images.unsplash.com/photo-1582794543139-8ac9cb0f7b11?w=400',

    'sunflowers_1.jpg': 'https://images.unsplash.com/photo-1470509037663-253afd7f0f51?w=400',
    'sunflowers_2.jpg': 'https://images.unsplash.com/photo-1508847660436-d0d52fc5d9e7?w=400',
    'sunflowers_3.jpg': 'https://images.unsplash.com/photo-1568466401883-63f1904a67ce?w=400',

    'daisy_1.jpg': 'https://images.unsplash.com/photo-1574684891174-df6b02ab38d7?w=400',
    'daisy_2.jpg': 'https://images.unsplash.com/photo-1463003416389-296a1ad37ca0?w=400',
    'daisy_3.jpg': 'https://images.unsplash.com/photo-1592956522646-eedda0ac8658?w=400',

    'dandelion_1.jpg': 'https://images.unsplash.com/photo-1508249940650-2b0e11dd72fd?w=400',
    'dandelion_2.jpg': 'https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?w=400',
    'dandelion_3.jpg': 'https://images.unsplash.com/photo-1586506773040-ba3ab0e87b38?w=400',
}

success = 0
failed = 0

for filename, url in test_images.items():
    try:
        filepath = test_dir / filename
        print(f"⏳ Đang tải: {filename}...", end=' ')

        # Tải ảnh
        urllib.request.urlretrieve(url, filepath)

        # Kiểm tra kích thước file
        size_kb = os.path.getsize(filepath) / 1024
        print(f"✅ OK ({size_kb:.1f} KB)")
        success += 1

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        failed += 1

print(f"\n{'=' * 50}")
print(f"🎉 Hoàn tất!")
print(f"✅ Thành công: {success} ảnh")
if failed > 0:
    print(f"❌ Thất bại: {failed} ảnh")

print(f"\n📂 Vị trí: {test_dir.absolute()}")
print(f"\n💡 Danh sách ảnh đã tải:")
for img in sorted(test_dir.glob('*.jpg')):
    size_kb = os.path.getsize(img) / 1024
    print(f"   - {img.name} ({size_kb:.1f} KB)")

print(f"\n✨ Bây giờ bạn có thể upload các ảnh này trong demo app!")