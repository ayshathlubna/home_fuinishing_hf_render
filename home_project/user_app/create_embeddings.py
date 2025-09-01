# create_embeddings_mobilenet.py
import os
import sys
import json
import numpy as np
import django
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.models import Model

# ------------------ Setup Django environment ------------------
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(project_root)
sys.path.insert(0, project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home_project.settings")
django.setup()

# Import Django models
from product_app.models import Products, Product_image

# ------------------ Load MobileNetV2 model ------------------
mobilenet_model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

# ------------------ Prepare storage lists ------------------
product_embeddings = []
product_ids = []
products_metadata = []

# ------------------ Generate embeddings ------------------
for product in Products.objects.all():
    img_obj = product.product_image_set.first()
    if not img_obj:
        continue

    img_path = img_obj.image.path
    img = keras_image.load_img(img_path, target_size=(224, 224))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    features = mobilenet_model.predict(x).flatten()
    product_embeddings.append(features)
    product_ids.append(product.p_id)

    metadata = {
        "p_id": product.p_id,
        "name": product.p_name,
        "image_url": img_obj.image.url
    }
    products_metadata.append(metadata)

# ------------------ Save embeddings and metadata ------------------
output_dir = os.path.join("user_app")
os.makedirs(output_dir, exist_ok=True)

np.save(os.path.join(output_dir, "product_embeddings.npy"), np.array(product_embeddings))
np.save(os.path.join(output_dir, "product_ids.npy"), np.array(product_ids))

with open(os.path.join(output_dir, "products.json"), "w") as f:
    json.dump(products_metadata, f, indent=4)

print(f"✅ Successfully created {len(product_embeddings)} embeddings and saved metadata.")
