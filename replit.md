# NuBike - Flask Bike Rental Application

## Overview

NuBike is a comprehensive web application for bicycle rentals, built with Flask (Python) and featuring a modern, Nubank-inspired design. The application allows users to register, find available bikes on an interactive map, make reservations, process payments, and unlock bikes using QR codes. It provides a complete bike-sharing solution with real-time bike tracking, multiple rental plans, and secure payment processing.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **CSS Framework**: Bootstrap 5.3.0 for responsive design and components
- **JavaScript**: Vanilla JavaScript with page-specific initialization
- **Map Integration**: Leaflet.js for interactive bike location mapping
- **Icons**: Font Awesome 6.4.0 for consistent iconography
- **Design System**: Custom CSS with Nubank-inspired color palette (purple themes)

### Backend Architecture
- **Web Framework**: Flask (Python) with session-based authentication
- **Data Storage**: In-memory dictionaries for mock data (users, bikes, reservations)
- **Authentication**: Werkzeug's security functions for password hashing
- **Session Management**: Flask sessions with configurable secret key
- **QR Code Generation**: qrcode library for bike unlock codes
- **Payment Processing**: Stripe integration for secure transactions

### Key Components
- **User Management**: Registration, login, and session handling
- **Bike Management**: Location tracking, availability status, and specifications
- **Reservation System**: Multiple rental plans (time/distance-based) with pricing
- **Payment Integration**: Stripe checkout with success/failure handling
- **QR Code System**: Unique codes generated for bike unlocking after payment

### Data Models (Mock Implementation)
- **Users**: ID, name, email, phone, hashed password
- **Bikes**: ID, model, type, location coordinates, availability, battery level
- **Reservations**: User association, bike selection, pricing, payment status

## External Dependencies

### Payment Services
- **Stripe**: Credit card processing and secure payment handling
- Environment variable: `STRIPE_SECRET_KEY`

### Frontend Libraries
- **Bootstrap 5.3.0**: UI framework via CDN
- **Font Awesome 6.4.0**: Icon library via CDN
- **Google Fonts (Poppins)**: Typography via CDN
- **Leaflet 1.9.4**: Interactive maps via CDN

### Python Packages
- **Flask**: Web application framework
- **Werkzeug**: Security utilities for password hashing
- **qrcode**: QR code generation for bike unlocking
- **stripe**: Payment processing integration

### Infrastructure
- **Replit Environment**: Configured for `REPLIT_DEV_DOMAIN` detection
- **Session Management**: Uses environment variable `SESSION_SECRET` with fallback

Note: The current implementation uses mock in-memory data storage. For production deployment, this would typically be replaced with a persistent database solution like PostgreSQL with an ORM such as SQLAlchemy or Drizzle.