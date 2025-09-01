import numpy as np
import json
import os
import sys
import django
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.models import Model

# A more robust method to find the project's root and set up Django
# This is a common pattern for running Django scripts outside of manage.py
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(project_root)
sys.path.insert(0, project_root)

# Set the Django settings module and configure the app
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home_project.settings")
django.setup()

# Now that the environment is set up, import the models
from product_app.models import Products, Product_image

# Load ResNet50 model without the top layers
base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
model = Model(inputs=base_model.input, outputs=base_model.output)

# Initialize empty lists to store data
product_embeddings = []
product_ids = []
products_metadata = []

# Loop through all products to ensure consistent data
for product in Products.objects.all():
    # Check if the product has an associated image
    img_obj = product.product_image_set.first()
    if img_obj:
        img_path = img_obj.image.path
        
        # Load and preprocess the image
        img = keras_image.load_img(img_path, target_size=(224, 224))
        x = keras_image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        
        # Get the feature embedding from the model
        features = model.predict(x).flatten()
        
        # Append the data to the lists
        product_embeddings.append(features)
        product_ids.append(product.p_id)
        
        # Create a dictionary for the product's metadata
        metadata = {
            "p_id": product.p_id,
            "name": product.p_name,
            "image_path": img_obj.image.url
        }
        products_metadata.append(metadata)

# Convert lists to NumPy arrays for efficient storage
embeddings_array = np.array(product_embeddings)
ids_array = np.array(product_ids)

# Save the data files to the correct directory
output_dir = "user_app" # Assuming this is your Django app directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

np.save(os.path.join(output_dir, "product_embeddings.npy"), embeddings_array)
np.save(os.path.join(output_dir, "product_ids.npy"), ids_array)

with open(os.path.join(output_dir, "products.json"), "w") as f:
    json.dump(products_metadata, f, indent=4)

print(f"Successfully created {len(embeddings_array)} embeddings and metadata entries.")
print("The files have been saved to the 'user_app' directory.")
