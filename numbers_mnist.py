import tensorflow as tf
import os
import h5py

# from tf.python.compiler.tensorrt import trt_convert as trt
# from tensorflow.contrib import lite

# Load the MNIST dataset
mnist = tf.keras.datasets.mnist
(x_train, y_train),(x_test, y_test) = mnist.load_data()

# Normalize the training values
x_train, x_test = x_train / 255.0, x_test / 255.0

# A callback to stop our tranning
# when reaching enough accuracy
class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    # If you are using Tensorflow 1.x, replace 'accuracy' for 'acc' in the next line
    if(logs.get('accuracy')>0.99):
      print("\nReached 99.0% accuracy so cancelling training!")
      self.model.stop_training = True

# Create a basic model
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(x_train,
          y_train,
          epochs=30,
          callbacks=[myCallback()])

# Evaluate the model
model.evaluate(x_test, y_test)

# Save the model
model.save('models/my_mnist_model.pb')

# Convert the model.
converter = tf.lite.TFLiteConverter.from_saved_model('/Users/jakelee/dev/handwriting/models/my_mnist_model.pb')
print("im here")
tflite_model = converter.convert()
open("models/converted_mnist_model.tflite", "wb").write(tflite_model)
