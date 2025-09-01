# 🏠 Home Furnishing – E-Commerce Platform  

A full-stack **Django eCommerce platform** for selling home furnishing products with advanced features like **AI chatbot search, personalized recommendations, wishlist, cart, order management, staff dashboard, and discounts.**  
## ⚠️ Note: 
  Image-based product search has been removed due to Render memory limitations.

🔗 **Live Demo:** [Izyaansh Home Furnishing](https://izyaansh-home-furnishing.onrender.com)  

---

## ✨ Features  

### 👤 User Features  
- User registration, login, logout, and profile management  
- Profile update with picture, gender, contact, and address  
- Wishlist management (add/remove products)  
- Shopping cart with discounts and dynamic shipping calculation  
- Address management (add, update, delete, set default)  
- Order placement with **Cash on Delivery** or simulated online payment  
- Order tracking, cancellation, and return requests  
- Recently viewed products  
- **Text-based Product Search:**:  
  - 🔍 Search by name, category, brand, or description
- Personalized recommendations (weighted hybrid recommender system)  

---

### 🛒 Product & Categories  
- Add, update, and delete categories, subcategories, and products  
- Product detail page with multiple images, discounts, and related products  
- Category-wise product listing with sorting & filtering:  
  - By newest/oldest  
  - By price (low → high / high → low)  
  - By discount %  
  - By under ₹999  

---

### 🤖 AI Chatbot  
- **NLP-powered chatbot** for:  
  - Price-range queries → *“Show me sofas under 10000”*  
  - Keyword/category/brand queries → *“blue curtains”, “Corsica carpet”*  
- Returns either **text response** or **list of matching products**  

---

### 📦 Order Management  
- Place orders with real-time stock validation  
- Order details with per-item delivery status  
- Cancel and return requests with automatic refund calculation  
- Refunds include delivery and platform fees  

---

### 👨‍💼 Staff & Admin Features  
- **Admin Dashboard**: Manage users, products, categories, orders, newsletter subscribers, staff  
- **Staff Dashboard**: Manage orders, cancellations, returns, and refunds  
- Approve/reject cancellation & return requests  
- Staff creation with profiles  

---

### 📰 Newsletter  
- Subscribe/unsubscribe to newsletters  
- Managed by admin & staff dashboards  

---

## 🛠 Tech Stack  

- **Backend:** Django, Django ORM  
- **Frontend:** Django Templates (HTML, CSS, Bootstrap)  
- **Database:** SQLite3 
- **AI Chatbot:** Custom NLP parser for chatbot  
- **Other:** Pillow, NumPy, Pandas
- **Deployment:** Render

---

## ⚙️ Local Installation  

1. **Clone the repo**  
   ```bash
   git clone https://github.com/ayshathlubna/home_furnishing_render.git
   cd home_furnishing

2. **Create virtual environment & install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt

3. **Apply migrations & create superuser**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser

4. **Run server**
   ```bash
   python manage.py runserver


## 🚀 Deployment on Render

1. Connect GitHub repo to Render.

2. Add a Procfile:
   ```makefile
   web: gunicorn home_project.wsgi

 3. **Set environment variables in Render dashboard:**

- SECRET_KEY
- DEBUG=False
- DATABASE_URL (from Render Postgres)

4. **Build command:**
   ```bash
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput

5. **Start command:**
   ```bash
   gunicorn home_project.wsgi


## 📂 Project Structure

    ```csharp
    home_furnishing/
    │── admin_app/           # Admin management
    │── cart_app/            # Cart, wishlist, addresses
    │── category_app/        # Categories
    │── chatbot_app/         # AI chatbot
    │── order_app/           # Orders & items
    │── product_app/         # Products & discounts
    │── staff_dashboard/     # Staff tools
    │── sub_category_app/    # Subcategories
    │── user_app/            # User & profile
    │── templates/           # HTML templates
    │── static/              # CSS, JS, images
    │── manage.py


## 👩‍💻Author

Ayshath Lubna

💼 Data Scientist & Full-Stack Developer

🌐 [GitHub](https://github.com/ayshathlubna)

