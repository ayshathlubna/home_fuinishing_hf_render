from django.shortcuts import render,redirect
from category_app.models import Category
from sub_category_app.models import Sub_category
from product_app.models import Products,Product_image,Discount
from django.db.models import Case, When
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, RecentlyViewed
from cart_app.models import Cart_items,Wishlist
from django.db.models import Sum,Q
from .forms import ImageSearchForm
import numpy as np
from .utils import weighted_hybrid_recommendations
import requests
from django.shortcuts import render
from django.db.models import Q
from .models import Products
from .forms import ImageSearchForm
import json
import base64

from django.shortcuts import render

def custom_404(request, exception):
    return render(request, 'user/404.html', status=404)

ALLOWED_BRANDS = ["Homesake","Helios","Melody","Corsica","Tiffany","Vegas"]
def home(request):
    brand_products = {}
    if request.user.is_authenticated:
        total_items = Cart_items.objects.filter(cart__user=request.user).aggregate(Sum('quantity'))['quantity__sum'] or 0

        recommended_ids = weighted_hybrid_recommendations(request, top_k=6)
        recommended_products = Products.objects.filter(p_id__in=recommended_ids)

        recently_viewed = RecentlyViewed.objects.filter(user=request.user).order_by('-viewed_at')[:8]
        recently_viewed_products = [rv.product for rv in recently_viewed]

    
    for brand in ALLOWED_BRANDS:
        product = Products.objects.filter(brand=brand).first()  # any product from that brand
        if product:
            product_image = Product_image.objects.filter(p_id=product.p_id).first()  # first image of that product
            if product_image:
                brand_products[brand] = product_image.image.url  # store brand → image URL

    return render(request, "user/home.html", locals())



def aboutus(request):
    user = User.objects.all()
    if request.user.is_authenticated:
        total_items = Cart_items.objects.filter(cart__user=request.user).aggregate(Sum('quantity'))['quantity__sum'] or 0

        recommended_ids = weighted_hybrid_recommendations(request, top_k=6)
        recommended_products = Products.objects.filter(p_id__in=recommended_ids)


    return render(request,'user/aboutus.html',locals())

def group_items(lst, group_size):
    lst = list(lst)  # Convert QuerySet to list
    extended = lst + lst[:group_size * 2]
    return [extended[i:i + group_size] for i in range(0, len(lst), group_size)]

def living(request,id):
    category = Category.objects.get(category_id=id)
    sub_category = Sub_category.objects.filter(category=category)
    all_products = Products.objects.filter(sub_category__in=sub_category)
    product_images = []

    exclusive_products = [
    
    "Abby Fabric 3-Seater Sofa with Cushions",
    "Giza Composite Marble Top Coffee Table ",
    "Homeshores TV Unit",
    "Modern Radiance TV Unit",
    "Helios Bill Coffee Table",
    "Helios Emily Fabric 3+2+1 Seater Sofa Set"
    ]

    filtered_products = all_products.filter(p_name__in=exclusive_products)

    for i in filtered_products:
        image = Product_image.objects.filter(p_id=i).first()
        if image:
            product_images.append({'product': i, 'image': image.image})

    product_groups = group_items(product_images, 4)
    return render(request,'user/living.html',locals())

def bedroom(request,id):
    category = Category.objects.get(category_id=id)
    sub_category = Sub_category.objects.filter(category=category)
    all_products = Products.objects.filter(sub_category__in=sub_category)
    product_images = []

    exclusive_products = [
    
    "Helios Alton 4-Door Wardrobe with Mirrors",
    "Lexus Savanna King Bed with Hydraulic Storage",
    "Saga Bedside Table with Drawers",
    "Tiffany Caramel Queen Bed with Hydraulic Storage ",
    "Senorita 4-Door Wardrobe with Mirrors",
    "Vegas Bed Side Table with Drawers"
    ]

    filtered_products = all_products.filter(p_name__in=exclusive_products)

    for i in filtered_products:
        image = Product_image.objects.filter(p_id=i).first()
        if image:
            product_images.append({'product': i, 'image': image.image})

    product_groups = group_items(product_images, 4)
    return render(request,'user/bedroom.html',locals())

def dining(request,id):
    category = Category.objects.get(category_id=id)
    sub_category = Sub_category.objects.filter(category=category)
    all_products = Products.objects.filter(sub_category__in=sub_category)
    product_images = []

    exclusive_products = [
    
    "Vegas Faux Marble Top 6-Seater Dining Set with Chairs",
    "Harmony Sia Set of 2 Faux Leather Dining Chairs",
    "Helios Reynan NXT Crockery Unit",
    "Modern Radiance Set of 2 Fabric Dining Chairs",
    "Hadley Buffet Sideboard",
    "Montoya 4-Seater Dining Set with Chairs and Bench"
    ]

    filtered_products = all_products.filter(p_name__in=exclusive_products)

    for i in filtered_products:
        image = Product_image.objects.filter(p_id=i).first()
        if image:
            product_images.append({'product': i, 'image': image.image})

    product_groups = group_items(product_images, 4)
    return render(request,'user/dining.html',locals())

def decor(request,id):
    category = Category.objects.get(category_id=id)
    sub_category = Sub_category.objects.filter(category=category)
    all_products = Products.objects.filter(sub_category__in=sub_category)
    product_images = []

    exclusive_products = [
    
    "Sierra Set of 2 Woven Room Darkening Door Curtains - 7ft",
    "Corsica Esteem Classic Woven Carpet - 183x122cm",
    "Iliano Metal Flowers and Leaves Wall Accent",
    "Contempo Set of 2 Colourblocked Room Darkening Door Curtains - 7ft",
    "Paradis Rafael Nylon Woven Carpet - 180x120cm",
    "Corvus Mystic Polypropylene Set of 3 Decorative Wall Arts"
    ]

    filtered_products = all_products.filter(p_name__in=exclusive_products)

    for i in filtered_products:
        image = Product_image.objects.filter(p_id=i).first()
        if image:
            product_images.append({'product': i, 'image': image.image})

    product_groups = group_items(product_images, 4)
    return render(request,'user/decor.html',locals())

def kids(request,id):
    category = Category.objects.get(category_id=id)
    sub_category = Sub_category.objects.filter(category=category)
    all_products = Products.objects.filter(sub_category__in=sub_category)
    product_images = []

    exclusive_products = [
    
    "Capel Kids Trundle Bed with Headboard Storage | (78x36 inch)",
    "Slate Kids Penguin Filled Cushion - 30x40cm",
    "Back To School Spark Set of 2 Stainless Steel Insulated Lunch Box",
    "Sunbeam Kids Bed | (72x36 inch) | (White & Yellow)",
    "Slate Kids Unicorn Filled Cushion",
    "Korobka Taze Set of 3 Stainless Steel Lunch Boxes with Bag"
    ]

    filtered_products = all_products.filter(p_name__in=exclusive_products)

    for i in filtered_products:
        image = Product_image.objects.filter(p_id=i).first()
        if image:
            product_images.append({'product': i, 'image': image.image})

    product_groups = group_items(product_images, 4)
    return render(request,'user/kids.html',locals())

def lighting(request,id):
    category = Category.objects.get(category_id=id)
    sub_category = Sub_category.objects.filter(category=category)
    all_products = Products.objects.filter(sub_category__in=sub_category)
    product_images = []

    exclusive_products = [
    
    "Melody Shellacs Glass Pendant Lamp",
    "HOMESAKE Metal Floor Lamp",
    "Riviera Dune Ceramic Table Lamp",
    "HOMESAKE Metal Pendant Ceiling Lamp",
    "Fluorescence Glint Metal Floor Lamp with Shelves	",
    "Monolith Marvel Ceramic Pebble Table Lamp"
    ]

    filtered_products = all_products.filter(p_name__in=exclusive_products)

    for i in filtered_products:
        image = Product_image.objects.filter(p_id=i).first()
        if image:
            product_images.append({'product': i, 'image': image.image})

    product_groups = group_items(product_images, 4)
    return render(request,'user/lighting.html',locals())

def kitchen(request,id):
    category = Category.objects.get(category_id=id)
    sub_category = Sub_category.objects.filter(category=category)
    all_products = Products.objects.filter(sub_category__in=sub_category)
    product_images = []

    exclusive_products = [
    "Gravis Stellar 5Pcs Triply Stainless Steel Cookware Set",
    "Spinel Bamboo Chopping Board",
    "Corsica Set of 3 Polypropylene Storage Containers - 450ml",
    "Valeria Carin Triply Stainless Steel Pressure Cooker - 3L",
    "Jarvis Hobbiton Set of 3 Stainless Steel Kitchen Scissors",
    "Mendo Dolomite Cookie Jar - 1.48L"
    ]

    filtered_products = all_products.filter(p_name__in=exclusive_products)

    for i in filtered_products:
        image = Product_image.objects.filter(p_id=i).first()
        if image:
            product_images.append({'product': i, 'image': image.image})

    product_groups = group_items(product_images, 4)
    return render(request,'user/kitchen.html',locals())

def group_sub_items(items, group_size):
    items = list(items)
    if not items:
        return []

    num_groups = (len(items) + group_size - 1) // group_size

    # Extend list to make total items = num_groups * group_size
    extended_items = items.copy()
    while len(extended_items) < num_groups * group_size:
        extended_items += items  # Repeat if needed

    extended_items = extended_items[:num_groups * group_size]

    # Split into chunks of group_size
    return [extended_items[i:i + group_size] for i in range(0, len(extended_items), group_size)]


from django.db.models import Case, When

def product_page(request, id=None, sub_id=None, brand=None):
    category = Category.objects.all()
    sub_cats = Sub_category.objects.all()

    try:
        wishlist_ids = list(
            Wishlist.objects.filter(user=request.user)
            .values_list('product_id', flat=True)
        )
    except:
        wishlist_ids = []

    selected_category = request.GET.get('category')
    order = request.GET.get('order')
    if not brand:
        brand = request.GET.get('brand')   # ✅ support query param brand
    all_products = Products.objects.all()

    category_name = None
    subcategory_name = None
    brand_name = None

    # 1. Subcategory filter
    if sub_id and sub_id != 'None':
        all_products = Products.objects.filter(sub_category=sub_id)
        try:
            sub_obj = Sub_category.objects.get(sub_cat_id=sub_id)
            selected_category = sub_obj.category.category_id
            category_name = sub_obj.category.category_name
            subcategory_name = sub_obj.sub_cat_name
        except Sub_category.DoesNotExist:
            pass

    # 2. Category filter
    if id and id != 'None':
        all_products = all_products.filter(category_id=id)
        try:
            category_name = Category.objects.get(category_id=id).category_name
        except Category.DoesNotExist:
            pass

    # 3. Query param category filter
    if selected_category:
        sub_categories = Sub_category.objects.filter(category_id=selected_category)
        all_products = all_products.filter(sub_category__in=sub_categories)
        try:
            category_name = Category.objects.get(category_id=selected_category).category_name
        except Category.DoesNotExist:
            pass

    # 4. ✅ Brand filter (works with or without category/subcategory)
    if brand and brand != 'None':
        all_products = all_products.filter(brand__iexact=brand.strip())
        brand_name = brand

    print("Brand passed:", brand)
    print("Filtered products count:", all_products.count())

    # Sorting logic
    if order == 'asc':
        all_products = all_products.order_by('date')
    elif order == 'desc':
        all_products = all_products.order_by('-date')
    elif order == 'lowest':
        all_products = all_products.order_by('price')
    elif order == 'highest':
        all_products = all_products.order_by('-price')
    elif order == 'high_disc':
        discounts = Discount.objects.filter(product__in=all_products).order_by('-disc_percent')
        discounted_ids = [disc.product.p_id for disc in discounts]
        rank_map = {pid: pos for pos, pid in enumerate(discounted_ids)}
        preserved = Case(*[
            When(p_id=pid, then=rank_map.get(pid, 9999))
            for pid in all_products.values_list('p_id', flat=True)
        ])
        all_products = all_products.order_by(preserved)

    
    discount_filter = request.GET.get("discount")
    if discount_filter == "min70":
        all_products = all_products.filter(discount__disc_percent__gte=70)

    elif discount_filter == "from50to70":
        all_products = all_products.filter(discount__disc_percent__gte=50, discount__disc_percent__lte=70)

    elif discount_filter == "upto50":
        all_products = all_products.filter(discount__disc_percent__lte=50)

    elif discount_filter == "under999":
        all_products = all_products.filter(price__lte=999)


    # collect product images + discounts
    product_images = []
    for product in all_products:
        image = Product_image.objects.filter(p_id=product).first()
        discount = Discount.objects.filter(product=product).first()
        product_images.append({
            'product_id': product,
            'image': image,
            'discount': discount
        })

    sub_cat_groups = group_items(sub_cats, 6)

    return render(request, 'user/product_page.html', locals())




def signup(request):
    if request.method== "POST":
        first = request.POST.get("first")
        last = request.POST.get("last")
        username = request.POST.get("username")
        print(username)
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        email = request.POST.get("email")
        users=User.objects.filter(username=username).values()
        print(users)
        if users:
            messages.error(request,"Username already exists")
            return redirect("signup")
        if confirm_password==password:
            user = User.objects.create(first_name = first, last_name=last, username = username,email=email)
            user.set_password(password)
            user.save()
            # Profile.objects.create(user=user)
            return redirect('signin')
        else:
            messages.error(request,"Password doesn't match")
    return render(request,"user/signuppage.html")

@never_cache
def signin(request):
     
    if request.method =="POST":
        username=request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        user = authenticate(username = username, password=password)
        print(user)
        if user:
            login(request,user)
            return redirect('home')
        else:
          messages.error(request, "User not found or password is incorrect.")
    return render(request,"user/loginpage.html")


@login_required    
@never_cache
def profile(request):
    return render(request,"user/profile.html")


@login_required 
def profile_update(request):
    gender=Profile.gender_choice
    user=request.user
    profile=Profile.objects.get_or_create(user=user)
    print(user,profile)

    if request.method=="POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.profile.gender = request.POST.get("gender")
        user.profile.mobile = request.POST.get("contact_no")
        user.profile.address = request.POST.get("address")
        img=request.FILES.get('profile')
        print(img)
        print(user.first_name,user.last_name, user.profile.mobile)
        if img:
            user.profile.profile_img=img

        user.save()

        user.profile.save()
        return redirect('profile')
    
    return render(request,"user/profile_update.html",locals())

def profile_delete(request):
    user = request.user
    user.delete()
    return redirect('signin')

@never_cache
def logout_profile(request):
    logout(request)
    return redirect('home')

def search_page(request):
    """
    Handles both text-based and image-based product searches.
    """
    query = request.GET.get("q", "")
    form = ImageSearchForm(request.POST or None, request.FILES or None)
    products = Products.objects.none()

    # Initialize recent searches
    if "recent_searches" not in request.session:
        request.session["recent_searches"] = []

    # Clear recent searches
    if request.GET.get("clear") == "1":
        request.session.pop("recent_searches", None)
        request.session.modified = True

    # ------------------ TEXT SEARCH ------------------
    if query:
        products = Products.objects.filter(
            Q(p_name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__category_name__icontains=query) |
            Q(sub_category__sub_cat_name__icontains=query) |
            Q(brand__icontains=query)
        ).only("p_id", "p_name", "price").prefetch_related("product_image_set")

        # Save text search in recent searches
        first_image_url = None
        first_product = products.first()
        if first_product:
            first_image = first_product.product_image_set.first()
            if first_image:
                first_image_url = first_image.image.url

        new_entry = {"text": query, "image": first_image_url}
        recent_searches = request.session["recent_searches"]
        if new_entry not in recent_searches:
            recent_searches.insert(0, new_entry)
            request.session["recent_searches"] = recent_searches[:10]
            request.session.modified = True

    # ------------------ IMAGE SEARCH ------------------
    elif request.method == "POST" and form.is_valid():
        uploaded_image = request.FILES.get("image")
        if uploaded_image:
            try:
                # Encode the uploaded image as base64
                base64_image = base64.b64encode(uploaded_image.read()).decode("utf-8")

                # Your ML service API endpoint
                ml_api_url = "https://home-furnishing-ml.streamlit.app/"

                # Prepare JSON payload
                payload = {"image": f"data:{uploaded_image.content_type};base64,{base64_image}"}
                headers = {"Content-Type": "application/json"}

                # Send POST request to ML service
                response = requests.post(ml_api_url, headers=headers, data=json.dumps(payload), timeout=60)
                response.raise_for_status()

                # Parse API response
                api_response = response.json()
                matching_ids = api_response.get("product_ids", [])
                image_description = api_response.get("description", "")

                # Query products based on ML results
                if matching_ids:
                    products = Products.objects.filter(p_id__in=matching_ids).prefetch_related("product_image_set")
                elif image_description:
                    products = Products.objects.filter(
                        Q(p_name__icontains=image_description) |
                        Q(description__icontains=image_description) |
                        Q(category__category_name__icontains=image_description) |
                        Q(sub_category__sub_cat_name__icontains=image_description) |
                        Q(brand__icontains=image_description)
                    ).only("p_id", "p_name", "price").prefetch_related("product_image_set")

            except requests.exceptions.RequestException as e:
                print(f"Error contacting ML API: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

    # Get recent searches for template
    recent_searches = request.session.get("recent_searches", [])[:10]

    return render(request, "user/search_page.html", {
        "query": query,
        "products": products,
        "recent_searches": recent_searches,
        "form": form,
    })