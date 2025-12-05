import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import numpy as np
import pathlib
import os
import json

# --- Tham so ---
dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
data_dir = tf.keras.utils.get_file('flower_photos', origin=dataset_url, untar=True)
data_dir = pathlib.Path(data_dir) / "flower_photos"  # fix quan trọng


print("cwd:", os.getcwd())
print("data_dir:", data_dir)
# kiem tra file va folder con ben trong data_dir
print("Noi dung thu muc data_dir (folder con):")
for p in sorted(data_dir.iterdir()):
    print(" -", p.name, "(is_dir:", p.is_dir(), ", num files:", len(list(p.glob('*')) if p.is_dir() else []), ")")

# dem tong so anh
image_count = len(list(data_dir.glob('*/*.jpg')))
print(f'Tong so anh: {image_count}')

# tham so training
batch_size = 32
img_height = 180
img_width = 180

# tao dataset (co split)
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

# kiem tra class names
class_names = train_ds.class_names
print(f'Class names tu train_ds: {class_names}')
print("So luong class (len):", len(class_names))

# neu chi mot class -> thong bao va dung lai som
if len(class_names) == 1:
    print("!!! WARNING: Chi phat hien 1 class duy nhat. Kiem tra cau truc thu muc dataset.")
    print("HAY KIEM TRA: ban co dang truyen sai duong dan (vd: truyen vao mot folder chua tat ca anh thay vi folder chua cac nhom).")
    # tu dong thoat hoac ban co the tiep tuc; minh thong bao ra de ban xem
    # kiep tra de tranh train tren 1 class
    # raise SystemExit("Only 1 class found - stop training")

# toi uu performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# build model
num_classes = len(class_names)
model = keras.Sequential([
    layers.Rescaling(1. / 255, input_shape=(img_height, img_width, 3)),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(128, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.2),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)

print("Model output shape:", model.output_shape)
model.summary()

# train
epochs = 15
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
)

# ve do thi (giu nguyen phan lien quan)
acc = history.history.get('accuracy', [])
val_acc = history.history.get('val_accuracy', [])
loss = history.history.get('loss', [])
val_loss = history.history.get('val_loss', [])

epochs_range = range(len(acc) if acc else epochs)

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')

plt.savefig('training_history.png')
plt.show()

# tao thu muc models neu chua co
script_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(script_dir, 'models')
os.makedirs(models_dir, exist_ok=True)

# luu model (h5)
model_path = os.path.join(models_dir, 'flower_model.h5')
model.save(model_path)
print("Model da duoc luu:", model_path)

# luu class names vao file co duong dan tuyet doi va cung in ra
class_names_path = os.path.join(models_dir, 'class_names.json')
with open(class_names_path, 'w', encoding='utf-8') as f:
    json.dump(list(class_names), f, ensure_ascii=False, indent=2)
print("Class names da duoc luu vao:", class_names_path)

print("\\nHoan tat training.")
