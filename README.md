# Hotel / Room Booking Web Application (Django)

A fully responsive Hotel & Room Booking system built with **Django** (backend) and **Bootstrap 5**, HTML, and CSS (frontend). Users can search rooms by dates, view availability, book rooms, and receive booking confirmation.

## Features

### User Features
- **Authentication**: Register, login, logout
- **Search**: Search rooms by check-in and check-out date
- **Room listing**: View available rooms with image, type, price, amenities, availability
- **Room detail**: Multiple images, description, amenities, price, booking form
- **Booking**: Check-in/out dates, number of guests, automatic price calculation
- **Confirmation**: Booking summary page after submission
- **Booking history**: View past bookings (logged-in users)
- **Cancel booking**: Cancel a booking from history

### Admin Features (Django Admin)
- Admin login at `/admin/`
- Add / update / delete rooms and room images
- Manage room categories (Single, Double, Deluxe, Suite, Family)
- Manage hotels
- View all bookings and update status (confirmed / cancelled)
- Dashboard with links to all models

### Room Categories
- Single Room
- Double Room
- Deluxe Room
- Suite Room
- Family Room

## Project Structure

```
hotel booking/
├── config/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── accounts/               # User auth (register, login, logout)
├── rooms/                  # Hotels, room categories, rooms, search
├── bookings/               # Booking form, confirmation, history
├── templates/              # Base and app templates
├── static/
│   └── css/
│       └── style.css       # Custom branding CSS
├── media/                  # Uploaded images (created at runtime)
├── manage.py
└── requirements.txt
```

## Setup & Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run migrations (already applied if you ran them)

```bash
python manage.py migrate
```

### 3. Create default room categories

```bash
python manage.py create_categories
```

### 4. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

- **Home**: http://127.0.0.1:8000/
- **Hotels**: http://127.0.0.1:8000/hotels/
- **Rooms**: http://127.0.0.1:8000/rooms/
- **Admin**: http://127.0.0.1:8000/admin/ (use the superuser account)

### 6. Add sample data (optional)

Log in to the admin at `/admin/`, then:
- Add one or more **Hotels** (name, address, optional image)
- Add **Rooms** under each hotel (category, name, description, price per night, max guests, amenities)
- Optionally add **Room images** for each room (inline when editing a room)

## Tech Stack

- **Backend**: Django 4.x, SQLite
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Media**: Pillow (image uploads)

## UI Overview

- **Navbar**: Logo, Home / Hotels / Rooms links, date search (check-in/check-out), Login/Register or user dropdown
- **Footer**: Contact info, social links, support links
- **Room cards**: Hover effects, image, type, price, amenities, availability badge
- **Booking form**: HTML5 date pickers, guest count, automatic total calculation
- **Confirmation**: Success message and booking summary

All pages are responsive (mobile, tablet, desktop).
