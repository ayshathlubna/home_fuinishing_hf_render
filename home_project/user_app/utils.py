import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import F
from .models import Products
from cart_app.models import Cart, Wishlist
from order_app.models import Order
from django.conf import settings
import os

# ------------------------------
# Load product embeddings and metadata
# ------------------------------
# We load two separate files now, to be consistent with our data generation script
file_path_embeddings = os.path.join(settings.BASE_DIR, "user_app", "product_embeddings.npy")
file_path_ids = os.path.join(settings.BASE_DIR, "user_app", "product_ids.npy")

if not os.path.exists(file_path_embeddings) or not os.path.exists(file_path_ids):
    raise FileNotFoundError("Embeddings or IDs file not found. Please run create_embeddings.py.")

product_embeddings = np.load(file_path_embeddings, allow_pickle=True)
product_ids = np.load(file_path_ids, allow_pickle=True)

# Create a fast lookup dictionary for product IDs
# This is much faster than np.where for repeated lookups.
pid_to_index = {pid: i for i, pid in enumerate(product_ids)}

# Pre-fetch all product data to avoid N+1 queries later
all_products = Products.objects.all().select_related('category', 'sub_category')
pid_to_product = {p.p_id: p for p in all_products}


# ------------------------------
# Helper: Get index of product (now uses a dictionary for speed)
# ------------------------------
def get_product_index(product_id):
    """Return the index of a product in embeddings based on product_id."""
    return pid_to_index.get(product_id)

# ------------------------------
# Image similarity
# ------------------------------
def get_image_similarity(pid):
    """Return cosine similarity of a product's embedding with all products."""
    idx = get_product_index(pid)
    if idx is None:
        return None
    emb = product_embeddings[idx].reshape(1, -1)
    sims = cosine_similarity(emb, product_embeddings)[0]
    return sims

# ------------------------------
# Category + Brand similarity
# ------------------------------
def get_category_brand_similarity(pid):
    """Return similarity scores based on a product's category and brand."""
    target = pid_to_product.get(pid)
    if not target:
        return np.zeros(len(product_ids))

    sims = []
    # Loop over the pre-fetched products, not a list of IDs
    for db_pid in product_ids:
        p = pid_to_product.get(db_pid)
        if not p:
            sims.append(0)
            continue

        score = 0
        if p.category == target.category:
            score += 0.6
        if p.brand == target.brand:
            score += 0.4
        sims.append(score)

    return np.array(sims)

# ------------------------------
# User preference similarity
# ------------------------------
def get_user_preference_similarity(user):
    """Return similarity scores based on user's wishlist, cart, and orders."""
    prefs = {}

    cart_pids = set(Cart.objects.filter(user=user).values_list('cart_items__product_id', flat=True))
    order_pids = set(Order.objects.filter(user=user).values_list('items__product_id', flat=True))

    wishlist_pids = set(Wishlist.objects.filter(user=user).values_list('product_id', flat=True))
    
    user_products = Products.objects.filter(p_id__in=wishlist_pids | cart_pids | order_pids)
    
    for product in user_products:
        key = (product.category, product.brand)
        weight = 0
        if product.p_id in wishlist_pids:
            weight += 1
        if product.p_id in cart_pids:
            weight += 2
        if product.p_id in order_pids:
            weight += 3
        prefs[key] = prefs.get(key, 0) + weight

    sims = []
    for db_pid in product_ids:
        p = pid_to_product.get(db_pid)
        if p:
            sims.append(prefs.get((p.category, p.brand), 0))
        else:
            sims.append(0)

    return np.array(sims)


# ------------------------------
# Hybrid Recommendation
# ------------------------------
def weighted_hybrid_recommendations(request, top_k=6,
                                    w_image=0.4, w_catbrand=0.2, w_history=0.2, w_user=0.2):
    """
    Generate hybrid recommendations using:
    1. Image similarity
    2. Category/Brand similarity
    3. User history (recency boost)
    4. User preferences (wishlist/cart/orders)
    """
    history = request.session.get("history", [])
    scores = np.zeros(len(product_ids))

    # --- 1. Image similarity ---
    for pid in history:
        img_sims = get_image_similarity(pid)
        if img_sims is not None:
            scores += w_image * img_sims

    # --- 2. Category/Brand similarity ---
    for pid in history:
        catbrand_sims = get_category_brand_similarity(pid)
        if catbrand_sims is not None:
            scores += w_catbrand * catbrand_sims

    # --- 3. History preference (recency boost) ---
    for i, pid in enumerate(history):
        idx = get_product_index(pid)
        if idx is not None:
            # More recent = higher weight
            scores[idx] += w_history * (1 - i / len(history))

    # --- 4. User preference signals ---
    if request.user.is_authenticated:
        user_sims = get_user_preference_similarity(request.user)
        scores += w_user * user_sims

    # --- Exclude already viewed ---
    history_indices = [get_product_index(pid) for pid in history if get_product_index(pid) is not None]
    scores[history_indices] = -np.inf

    # --- Get top-k recommendations ---
    top_indices = np.argsort(scores)[::-1]
    recommended_ids = []
    seen = set()
    for i in top_indices:
        if i < 0 or i >= len(product_ids):
            continue
        pid = str(product_ids[i])
        if pid not in seen:
            seen.add(pid)
            recommended_ids.append(pid)
        if len(recommended_ids) == top_k:
            break

    return recommended_ids
