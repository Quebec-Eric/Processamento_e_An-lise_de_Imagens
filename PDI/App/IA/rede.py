import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import confusion_matrix
import time
import numpy as np

# carregar o modelo MobileNetv2
modelo_base= MobileNetV2(weights='imagenet', include_top=False)

#Camadas totalemte conectada
camada = modelo_base.output
camada = GlobalAveragePooling2D()(camada)
prediction=Dense(1,activation='sigmoid')(camada)

construido_modelo=Model(input=modelo_base.input, outputs=prediction)

for nos in modelo_base.layers:
    nos.trainable=False

#compilar o modelo
construido_modelo.compile(optimizer=Adam(lr=0.001), loss='binary_crossentropy', metrics=['accuracy'])

#carregar os dados de trino 

trai_data= ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

train_generator = trai_data.flow_from_directory(
        'AkiTeste', 
        target_size=(224, 224), 
        batch_size=32,
        class_mode='binary') 

start_time = time.time()
construido_modelo.fit(train_generator, epochs=150)
end_time = time.time()       

# Medir o tempo de execução
execution_time = end_time - start_time
print('Tempo de execução: ', execution_time)


construido_modelo.save('my_model_binary.h5')


test_images = []
for img_path in test:
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    test_images.append(img_array)

test_data = np.vstack(test_images)

# Avaliar o modelo
predictions = model.predict(test_data)
predicted_classes = np.where(predictions > 0.5, 1, 0)

# Calcular as métricas
accuracy = accuracy_score(test_labels, predicted_classes)
precision = precision_score(test_labels, predicted_classes)
recall = recall_score(test_labels, predicted_classes)
f1 = f1_score(test_labels, predicted_classes)

cm = confusion_matrix(test_labels, predicted_classes)
tn, fp, fn, tp = cm.ravel()
sensitivity = tp / (tp + fn)
specificity = tn / (tn + fp)

print('Matriz de confusão: ', cm)
print('Acurácia: ', accuracy)
print('Precisão: ', precision)
print('Recall: ', recall)
print('F1 score: ', f1)
print('Sensibilidade: ', sensitivity)
print('Especificidade: ', specificity)