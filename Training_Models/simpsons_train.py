import os
import caer
import canaro
import numpy as np
import cv2
import gc
import matplotlib.pyplot as plt
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import LearningRateScheduler


def prepare(get_img):
    get_img = cv2.cvtColor(get_img, cv2.COLOR_BGR2GRAY)
    get_img = cv2.resize(get_img, IMG_SIZE)
    get_img = caer.reshape(get_img, IMG_SIZE, 1)
    return get_img


IMG_SIZE = (80, 80)
channels = 1
char_path = r'D:\Downloads\archive\simpsons_dataset'

char_dict = {}
for char in os.listdir(char_path):
    char_dict[char] = len(os.listdir(os.path.join(char_path, char)))

char_dict = caer.sort_dict(char_dict, descending=True)
print(char_dict)

char_list = []
# cnt = 0
for cnt, i in enumerate(char_dict):
    char_list.append(i[0])
    #     cnt += 1
    if cnt >= 10:
        break
print(char_list)

train = caer.preprocess_from_dir(char_path, char_list, channels=channels, IMG_SIZE=IMG_SIZE, isShuffle=True)

print(len(train))

plt.figure(figsize=(30, 30))
plt.imshow(train[0][0], cmap='gray')
# plt.show()

featureSet, labels = caer.sep_train(train, IMG_SIZE=IMG_SIZE)

featureSet = caer.normalize(featureSet)
labels = to_categorical(labels, len(char_list))

x_train, x_val, y_train, y_val = caer.train_val_split(featureSet, labels, val_ratio=.2)

del train
del featureSet
del labels
gc.collect()

BATCH_SIZE = 32
EPOCHS = 10

data_gen = canaro.generators.imageDataGenerator()
train_gen = data_gen.flow(x_train, y_train, batch_size=BATCH_SIZE)

model = canaro.models.createSimpsonsModel(IMG_SIZE=IMG_SIZE, channels=channels, output_dim=len(char_list),
                                          loss='binary_crossentropy', decay=1e-6, learning_rate=0.001,
                                          momentum=0.9, nesterov=True)

model.summary()

callbacks_list = [LearningRateScheduler(canaro.lr_schedule)]

training = model.fit(train_gen, steps_per_epoch=len(x_train) // BATCH_SIZE,
                     epochs=EPOCHS,
                     validation_data=(x_val, y_val),
                     validation_steps=len(y_val) // BATCH_SIZE,
                     callbacks=callbacks_list)

test_path = r'D:\Downloads\archive\kaggle_simpson_testset\kaggle_simpson_testset\charles_montgomery_burns_32.jpg'
img = cv2.imread(test_path)
plt.imshow(img, cmap='gray')


predictions = model.predict(prepare(img))

print(f'Model prediction in the picture: {char_list[np.argmax(predictions[0])]}')
plt.show()