# Full-Stack Django E-Commerce Application 📱🛒

A robust, production-ready e-commerce platform built from scratch utilizing Python, full-stack Django components, and SQLite. This application bridges a sleek customer-facing catalog frontend with a powerful, dynamic Django Administration dashboard.

## 🚀 Core Features

- **User Authentication Pipeline**: Integrated custom user creation structures alongside secure login/logout session states.
- **Dynamic Shopping Cart**: Full database-backed logic managing multi-item selections, automatic quantity handling, and real-time calculation totals.
- **Stripe Checkout Integration**: Configured secure end-to-end sandbox payment flows reading dynamically from environment variables.
- **Media Asset Pipeline**: Integrated image upload capabilities straight from the administrative control panel to frontend inventory card views using Pillow.
- **Inventory Safety Triggers**: Automated database updates to process item subtractions upon successful payment sessions and block out-of-stock items.

## 🛠️ Tech Stack

- **Backend Framework**: Python 3, Django
- **Database Architecture**: SQLite (Development)
- **Payment Processing**: Stripe API SDK
- **Styling UI Layout**: Responsive CSS Grids
- **Environment Security**: Python-Dotenv

## 🔧 Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd MY_DJANGO_PROJECT
   ```

2. **Initialize Environment Variables:**
   Create a `.env` file in the root directory and add your credentials:
   ```text
   STRIPE_PUBLIC_KEY=your_stripe_public_key
   STRIPE_SECRET_KEY=your_stripe_secret_key
   ```

3. **Install Dependencies & Sync Database:**
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   ```

4. **Launch Local Server:**
   ```bash
   python manage.py runserver
   ```
