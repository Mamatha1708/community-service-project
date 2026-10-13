# 🦚 Kalamkari Connect: AI-Powered Kalamkari Artisan Support System

> **College Community Service Project (CSP) 2026**  
> *A full-stack ethical handloom marketplace and AI support ecosystem dedicated to preserving 3,000 years of Geographical Indication (GI) protected craft heritage.*

---

## 📖 1. Project Background & Social Impact

**Kalamkari** (*Kalam* = bamboo pen, *Kari* = craftsmanship) is one of India’s most revered textile art traditions, protected under India's Geographical Indications of Goods Act:
1. **Srikalahasti Pen Kalamkari (GI: AP/19):** Centered in Srikalahasti along the holy Swarnamukhi River. Every intricate motif is drawn freehand with a bamboo pen dipped in fermented iron-jaggery black ink (*Kasinam*) on buffalo-milk scoured fabric.
2. **Machilipatnam Block Kalamkari (GI: AP/17):** Centered in Pedana and Machilipatnam. Intricate designs are hand-carved onto seasoned teakwood blocks and immersed in fermented natural indigo vats.

### The Social Problem Identified during CSP Field Work:
- **Commercial Intermediary Exploitation:** Rural artisans receive only 20% to 30% of final retail margins.
- **Counterfeit Chemical Prints:** Cheap factory screen prints use the "Kalamkari" name fraudulently, depressing artisan wages.
- **Digital & Linguistic Marketing Divide:** Elderly master artisans lack technical digital skills to write SEO product descriptions, Instagram marketing copy, or English customer narratives.

### The Kalamkari Connect Solution:
- Direct **Artisan-to-Consumer Marketplace** ensuring 100% transparent fair compensation.
- **Kalamkari Mitra AI:** An intelligent storytelling engine that generates authentic cultural descriptions and social media marketing copy based on the artisan's motif and natural dyes.
- **Natural Dye Transparency:** Explicit listings of plant and mineral ingredients (Myrobalan, Kasinam iron slag, Madder root, Indigo cake).
- **Simulated Demo Orders:** Safe educational testing without financial risk.

---

## 🛠️ 2. Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons
- **Backend:** Python 3.11+, Flask 3.1
- **Database:** SQLite with SQLAlchemy ORM (persistent file `kalamkari.db`)
- **Security:** Werkzeug password hashing, session-based role authorization (RBAC)
- **AI Engine:**
  - **Offline Demo Mode:** Built-in expert Kalamkari knowledge engine (no external API key needed, zero network failure).
  - **Live AI Mode:** Optional Google Gemini 1.5 Flash API integration via `GEMINI_API_KEY` in `.env`.

---

## 📂 3. Project Directory Structure

```text
csp/
├── app.py                     # Main Flask routing, business logic & controllers
├── config.py                  # Environment & database configuration
├── models.py                  # SQLAlchemy models (User, Product, CartItem, Order, OrderItem)
├── requirements.txt           # Python package dependencies
├── .env.example               # Template for environment variables
├── .gitignore                 # Files excluded from version control
├── README.md                  # Comprehensive documentation and viva guide
├── services/
│   ├── auth_service.py        # RBAC decorators (@login_required, @artisan_required, @admin_required)
│   ├── ai_service.py          # AI storytelling engine (Gemini API + smart offline fallback)
│   └── seed_data.py           # Preloaded realistic artisans, crafts, and orders
├── static/
│   ├── css/
│   │   └── style.css          # Traditional Kalamkari theme (Indigo, Terracotta, Cream, Gold)
│   ├── js/
│   │   └── main.js            # Client-side validation, AJAX AI tools, image preview, 1-click logins
│   └── images/
│       └── samples/           # Authentic Kalamkari SVG artworks (Tree of Life, Peacock, etc.)
├── templates/                 # 10 Responsive HTML/Jinja2 templates
│   ├── base.html              # Base layout with navbar, alerts, and cultural footer
│   ├── index.html             # Page 1: Home page (Heritage, styles, CSP spotlight)
│   ├── register.html          # Page 2: Registration page (Customer / Artisan role selection)
│   ├── login.html             # Page 3: Login page (1-Click demo credential buttons)
│   ├── artisan_dashboard.html # Page 4: Artisan studio (Product inventory & customer orders)
│   ├── product_form.html      # Page 5: Add / Edit Product (with inline AI Story Generator)
│   ├── marketplace.html       # Page 6: Marketplace (Search, category & style filters)
│   ├── product_detail.html    # Page 7: Product details (Craft story, dye specs, artisan bio)
│   ├── cart.html              # Page 8: Cart & Demo Checkout (COD, UPI, simulated payment)
│   ├── orders.html            # Order History & visual tracking timeline
│   ├── ai_assistant.html      # Page 9: Kalamkari Mitra AI (Storyteller, Marketing, Consultant)
│   └── admin_dashboard.html   # Page 10: Admin portal (Users, moderation, order status)
├── tests/
│   └── test_app.py            # Automated test suite (11 unit tests covering all features)
└── uploads/                   # Uploaded product photographs with file validation
```

---

## 🚀 4. Windows Setup & Run Guide (Step-by-Step for Beginners)

### Step 1: Open Terminal (PowerShell or Command Prompt)
Navigate to the project folder:
```powershell
cd c:\Users\soman\OneDrive\Documents\Desktop\csp
```

### Step 2: (Optional but Recommended) Create a Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If on standard CMD instead of PowerShell: `venv\Scripts\activate.bat`)*

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
> **Note:** The app works **100% offline out-of-the-box** using its built-in intelligent Kalamkari AI engine!  
> If you have a Google Gemini API key from [Google AI Studio](https://aistudio.google.com/), you can optionally paste it into `.env`:
> ```ini
> GEMINI_API_KEY=your_actual_key_here
> ```

### Step 5: Start the Application
```powershell
python app.py
```

### Step 6: Open the Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔑 5. Preloaded Demo Accounts (For Testing & Viva Evaluation)

The application automatically seeds realistic sample data on first start. On the **Login Page**, click any of the **Quick 1-Click Fill** buttons or enter:

| Role | Username / Email | Password | Description |
| :--- | :--- | :--- | :--- |
| **Artisan** | `artisan@kalamkari.org` | `artisan123` | Master S. Ramanaiah (Srikalahasti Pen Master, 28 yrs exp) |
| **Artisan (2)** | `lakshmi@kalamkari.org` | `lakshmi123` | Smt. Lakshmi Devi (Pedana Block Printing Master) |
| **Customer** | `customer@kalamkari.org` | `customer123` | Ananya Sharma (Conscientious Art Buyer) |
| **Admin** | `admin@kalamkari.org` | `admin123` | CSP Project Coordinator (Administrator) |

---

## 🧪 6. How to Test Every Major Feature

### Feature 1: Automated Unit Testing
Run the comprehensive test suite directly from your terminal:
```powershell
python -m unittest tests/test_app.py
```
*Expected Result:* All 11 tests pass with status `OK`.

### Feature 2: User Registration & Role Authorization (RBAC)
1. Go to `http://127.0.0.1:5000/register`.
2. Choose **Kalamkari Artisan / Craftsperson** from the dropdown. Notice the dynamic artisan fields appear (Craft Cluster, Years of Experience, Bio).
3. Register a new user and submit. You will be automatically redirected to your personalized **Artisan Dashboard**.
4. Log out and try accessing `/artisan/dashboard` directly — notice the route protection redirects you to login with a warning.

### Feature 3: Adding a Product with the AI Story Generator
1. Log in as an artisan (`artisan@kalamkari.org`).
2. Click **List Craft** in the top navigation or dashboard.
3. Fill in Title: `"Hand-Drawn Dancing Peacock Mangalagiri Silk Saree"`.
4. Select Style: *Srikalahasti Pen Kalamkari*, Motif: *Peacock & Swan*.
5. Click the golden **"✨ Generate Story with AI"** button.
6. Watch the AI instantly compose a rich cultural narrative detailing bamboo pen craftsmanship, peacock symbolism, and vegetable dye mordants right into the textarea!
7. Upload a photo or leave it blank (the system automatically assigns an authentic motif SVG pattern).
8. Click **Publish to Marketplace**.

### Feature 4: Marketplace Search & Multi-Faceted Filters
1. Go to `http://127.0.0.1:5000/marketplace`.
2. Type `"Tree of Life"` into the search bar and press Enter.
3. Filter by Style: `"Machilipatnam Block Kalamkari"`.
4. Sort by Price: *High to Low*.
5. Click **Clear Filters** to view all creations.

### Feature 5: Product Details, Natural Dye Transparency & Care Guide
1. Click on any product card (e.g. *Hand-Painted Tree of Life Sacred Wall Tapestry*).
2. Inspect the high-resolution artwork, artisan lineage, natural dye composition (*Myrobalan, Kasinam iron slag, Madder root*), and authentic wash care guide.
3. Click **Add to Handloom Bag**.

### Feature 6: Shopping Cart & Demo Order Checkout
1. Visit `http://127.0.0.1:5000/cart`.
2. Update item quantity using the stepper, verify subtotal recalculates.
3. Fill in the shipping details on the demo checkout form.
4. Select **Cash on Delivery (Demo Simulation)** or **Demo UPI Simulation**.
5. Click **Confirm Demo Order**.
6. The system generates an official order reference (e.g. `#KC-2026-XXXX`), deducts stock, empties the cart, and redirects to your **Order Tracking Timeline**.

### Feature 7: "Kalamkari Mitra" AI Assistant Page
1. Click **Kalamkari Mitra (AI)** in the navigation.
2. Note the banner displaying active AI mode (Smart Offline Demo Engine or Google Gemini Live API).
3. Test **Tab 1 (Storyteller):** Select a motif and title -> Click *Generate Heritage Story* -> Click *Copy Story*.
4. Test **Tab 2 (Marketing Generator):** Enter craft price -> Click *Generate Social Media Pack* -> Get ready-to-post Instagram, WhatsApp, and Facebook copy with hashtags (`#KalamkariConnect`, `#VocalForLocal`).
5. Test **Tab 3 (Heritage Buyer Consultant):** Click quick suggestion `"🏠 Living Room Decor"` -> Get recommendations on why the Tree of Life suits living spaces and view matching catalog products.

### Feature 8: Admin Management Portal
1. Log in as the administrator (`admin@kalamkari.org` / `admin123`).
2. Go to **Admin Portal** (`/admin/dashboard`).
3. View the system KPI metrics (Total Users, Crafts Listed, Total Orders, Gross Craft Value).
4. **Order Management Tab:** Change an order status from *Processing* to *Shipped* or *Delivered*.
5. **Craft Moderation Tab:** Delete any test or inappropriate listing across the entire platform.
6. **User Roles Tab:** Toggle user status between *Active* and *Deactivated*.

---

## 🚢 7. Complete Render Cloud Deployment Guide (Beginner Friendly)

Render is one of the easiest and most reliable platforms to host Python Flask applications. Follow these exact steps to deploy Kalamkari Connect:

### A. Pre-Deployment Repository Preparation (GitHub)
1. Initialize a Git repository if not already done:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit for Kalamkari Connect CSP deployment"
   ```
2. Create a new repository on [GitHub](https://github.com/) named `kalamkari-connect`.
3. Push your code to GitHub:
   ```powershell
   git remote add origin https://github.com/YOUR_GITHUB_USERNAME/kalamkari-connect.git
   git branch -M main
   git push -u origin main
   ```

---

### B. Creating the Web Service on Render
1. Go to [Render.com](https://render.com/) and create a free account or sign in with GitHub.
2. From the Render Dashboard, click **New +** and select **Web Service**.
3. Choose **Build and deploy from a Git repository**, click **Next**, and select your `kalamkari-connect` repository.
4. Fill in the deployment settings:
   - **Name:** `kalamkari-connect` (or any unique name you prefer)
   - **Region:** Choose the region closest to you (e.g., *Singapore* or *Frankfurt*)
   - **Branch:** `main`
   - **Root Directory:** Leave blank (defaults to root)
   - **Runtime:** `Python 3`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     gunicorn app:app
     ```
   - **Instance Type:** Select **Free** ($0/month)

---

### C. Configuring Environment Variables on Render
Scroll down to the **Environment Variables** section on Render and click **Add Environment Variable** for each:

| Key | Recommended Value | Purpose |
| :--- | :--- | :--- |
| `SECRET_KEY` | *(Click "Generate" or enter a secure random string)* | Used by Flask to securely sign session cookies. |
| `PYTHON_VERSION` | `3.11.9` | Ensures Render builds with Python 3.11. |
| `FLASK_ENV` | `production` | Declares production environment. |
| `FLASK_DEBUG` | `false` | Explicitly disables debug mode for security. |
| `GEMINI_API_KEY` | *(Optional)* | Your Google Gemini API key. If left blank, the built-in offline Kalamkari engine handles all requests. |

Click **Create Web Service**. Render will now automatically clone your repository, install dependencies, initialize the database, and launch Gunicorn!

---

### D. Database Persistence: SQLite vs. PostgreSQL on Render

Render's Free Web Service tier uses **ephemeral containers**. This means that when the free service spins down after 15 minutes of inactivity or is restarted, local file modifications are reset.

Here is how data persistence works for this project:

1. **Default Mode (SQLite with Auto-Seeding — Recommended for Viva & Demo):**
   - No external database setup is required.
   - Every time the application starts up or wakes from sleep on Render, `app.py` automatically initializes `kalamkari.db` and runs `seed_database()`.
   - All sample products, demo artisans, customers, and orders are guaranteed to be present and functional for examiners and reviewers at all times.
   - If an uploaded user image file is missing due to a container restart, the application automatically falls back to bundled authentic Kalamkari SVG patterns without broken links.

2. **Full Long-Term Persistence (Free Render PostgreSQL):**
   - If you want new registrations and orders to persist permanently even after months of inactivity, create a free **PostgreSQL Database** on Render:
     1. Click **New +** ➔ **PostgreSQL Database** on Render.
     2. Name it `kalamkari-db` and select the Free tier.
     3. Copy the **Internal Database URL** (e.g. `postgres://kalamkari:...@dpg-...`).
     4. Paste it as the `DATABASE_URL` environment variable in your Web Service settings.
   - Our `config.py` automatically detects Render PostgreSQL, normalizes the URL to `postgresql://`, and creates the tables on first launch!

3. **Persistent Disk (Paid Option):**
   - Render also offers Persistent Disks ($7/month) to mount `/data` or `/app/uploads`. For academic CSP projects, this is completely optional and not required.

---

### E. Verifying Your Live Deployment
1. Once Render displays **"Live"**, click on your onrender.com URL (e.g., `https://kalamkari-connect.onrender.com`).
2. Test the following on your live site:
   - Check the **Home Page** banner and GI craft comparisons.
   - Sign in using the **1-Click Demo Buttons** on the Login page (`artisan@kalamkari.org` or `customer@kalamkari.org`).
   - Check the **Marketplace** and test product filtering.
   - Test **Kalamkari Mitra AI Assistant**; confirm the mode indicator badge.
   - Add a product to the cart and confirm a demo order.
   - Log in as `admin@kalamkari.org` and view the **Admin Portal**.

---

## 🎓 8. Community Service Project (CSP) Viva Questions & Answers

**Q1: Why did you choose SQLite for this project?**  
*A:* SQLite is a serverless, zero-configuration, file-based relational database that stores all data persistently in `kalamkari.db`. It is ideal for local community field deployments and educational demonstrations without requiring heavy database server installations like MySQL or PostgreSQL.

**Q2: How does the AI Assistant work when there is no internet or no API key?**  
*A:* The system uses a graceful dual-mode architecture implemented in `services/ai_service.py`. When `GEMINI_API_KEY` is not present, the intelligent offline knowledge engine generates historically and culturally accurate Kalamkari descriptions and marketing copy based on the specific motif and style chosen. If an API key is provided, it seamlessly invokes the Google Gemini REST API.

**Q3: How are passwords protected?**  
*A:* Passwords are never stored in plain text. They are hashed using `werkzeug.security.generate_password_hash` utilizing secure PBKDF2/SHA-256 algorithms.

**Q4: How does this project benefit rural artisans?**  
*A:* It bridges the digital divide by giving non-technical artisans automated AI-powered marketing tools, eliminates predatory middlemen so artisans keep 100% of fair sales value, and promotes natural dye authenticity to fight synthetic counterfeit prints.

---

*Developed with passion for Andhra Pradesh Kalamkari Handloom Revival & College Community Service Project 2026.*
