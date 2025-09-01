import numpy as np
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Model

# Load model (as in your app.py)
base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
model = Model(inputs=base_model.input, outputs=base_model.output)

# 1. Load the embeddings file
product_embeddings = np.load("user_app/product_embeddings.npy")
print("Product Embeddings:")
print(f"  Shape: {product_embeddings.shape}")
print(f"  Data Type: {product_embeddings.dtype}")

# 2. Get a sample embedding for a test image
# Replace 'test_image.jpg' with the path to a test image you're using
try:
    test_img = keras_image.load_img("/media/product_image/1000013983203-1000013983203-2709_01-2100.jpg", target_size=(224, 224))
    x = keras_image.img_to_array(test_img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    query_embedding = model.predict(x).flatten()
except FileNotFoundError:
    print("Test image not found. Skipping query embedding check.")
    query_embedding = None

if query_embedding is not None:
    print("\nQuery Embedding:")
    print(f"  Shape: {query_embedding.shape}")
    print(f"  Data Type: {query_embedding.dtype}")