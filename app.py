#!/usr/bin/env python3
"""
NuBike - Flask Bike Rental Application

Sistema completo de aluguel de bicicletas com:
- Autenticação segura de usuários
- Mapa interativo com localização das bikes
- Sistema de reservas e pagamentos (Stripe)
- Geração de QR codes para desbloqueio
- Dashboard com histórico de aluguéis

Design inspirado no Nubank - Projeto Acadêmico
Autor: [Seu Nome]
Data: 2025
"""

# =============================================================================
# IMPORTS E CONFIGURAÇÕES
# =============================================================================
import os
import json
import uuid
import qrcode.main
import io
import base64
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import stripe

# =============================================================================
# CONFIGURAÇÃO DA APLICAÇÃO FLASK
# =============================================================================
app = Flask(__name__)

# Configuração de segurança - chave secreta para sessões
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')

# =============================================================================
# CONFIGURAÇÃO DO STRIPE (PAGAMENTOS)
# =============================================================================
STRIPE_KEY = os.environ.get('STRIPE_SECRET_KEY')
if STRIPE_KEY:
    stripe.api_key = STRIPE_KEY
    print("✅ Stripe configurado com sucesso")
else:
    print("⚠️  WARNING: STRIPE_SECRET_KEY not set. Payment functionality will be disabled.")

# Domínio da aplicação (para URLs do Stripe) 
# Em produção, será detectado automaticamente via request.host_url
YOUR_DOMAIN = os.environ.get('REPLIT_DEV_DOMAIN') or 'localhost:5000'

# =============================================================================
# ARMAZENAMENTO DE DADOS (MOCK)
# Em produção, substitua por um banco de dados (PostgreSQL, MySQL, etc.)
# =============================================================================

# Dicionário para armazenar usuários registrados
# Estrutura: {email: {id, name, email, password_hash, phone}}
users = {}

# =============================================================================
# CARREGAMENTO DE DADOS DAS BICICLETAS
# =============================================================================

def load_bikes_data():
    """
    Carrega dados das bicicletas do arquivo JSON
    Em caso de erro, usa dados fallback para desenvolvimento
    """
    try:
        with open('data/bicicletas.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            bikes = {}
            for bike in data['bicicletas']:
                bikes[str(bike['id'])] = {
                    'id': str(bike['id']),
                    'model': bike['model'],
                    'type': bike['type'].lower(),
                    'aro': '26',  # Padrão se não especificado
                    'lat': bike['location']['lat'],
                    'lng': bike['location']['lng'],
                    'available': bike['available'],
                    'battery': bike['battery'],
                    'image': bike.get('image', 'bike-default.jpg')
                }
            print(f"✅ Carregados {len(bikes)} bicicletas do arquivo JSON")
            return bikes
    except Exception as e:
        print(f"⚠️ Erro ao carregar bicicletas do JSON: {e}")
        print("📁 Usando dados fallback para desenvolvimento...")
        return {
            '1': {
                'id': '1',
                'model': 'Urban Pro',
                'type': 'urbana',
                'aro': '26',
                'lat': -23.550520,
                'lng': -46.633308,
                'available': True,
                'battery': 85,
                'image': 'bike1.jpg'
            },
            '2': {
                'id': '2',
                'model': 'Mountain Explorer',
                'type': 'mountain',
                'aro': '29',
                'lat': -23.551520,
                'lng': -46.634308,
                'available': True,
                'battery': 92,
                'image': 'bike2.jpg'
            }
        }

# Carrega dados das bicicletas na inicialização
bikes = load_bikes_data()

# Planos de aluguel disponíveis com preços e descrições
rental_plans = {
    'hourly': {
        'name': 'Por Hora',
        'description': 'Ideal para passeios curtos pela cidade',
        'price': 15.00,
        'unit': 'hora'
    },
    'daily': {
        'name': 'Diária',
        'description': 'Perfeito para um dia inteiro de aventura',
        'price': 80.00,
        'unit': 'dia'
    },
    'weekly': {
        'name': 'Semanal',
        'description': 'Para quem quer usar a bike por uma semana',
        'price': 300.00,
        'unit': 'semana'
    }
}

# Dicionário para armazenar reservas ativas
# Estrutura: {reservation_id: {user_id, bike_id, plan, created_at, ...}}
reservations = {}

# =============================================================================
# ROTAS PRINCIPAIS - PÁGINAS WEB
# =============================================================================

@app.route('/')
def index():
    """
    Página inicial do NuBike
    - Se usuário logado: redireciona para mapa
    - Se não logado: mostra landing page
    """
    if 'user_id' in session:
        return redirect(url_for('map_view'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registro de novos usuários
    - GET: Exibe formulário de cadastro
    - POST: Processa dados e cria conta
    - Validações: campos obrigatórios, senha mínima, email único
    """
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        phone = request.form.get('phone', '').strip()
        
        # Validação dos dados do formulário
        if not all([name, email, password, phone]):
            flash('Todos os campos são obrigatórios!', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres!', 'error')
            return render_template('register.html')
        
        if email in users:
            flash('Email já cadastrado!', 'error')
            return render_template('register.html')
        
        # Cria novo usuário com hash da senha para segurança
        user_id = str(uuid.uuid4())
        users[email] = {
            'id': user_id,
            'name': name,
            'email': email,
            'password': generate_password_hash(password),  # Hash seguro da senha
            'phone': phone
        }
        
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        
        if not email or not password:
            flash('Email e senha são obrigatórios!', 'error')
            return render_template('login.html')
        
        user = users.get(email)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('map_view'))
        else:
            flash('Email ou senha incorretos!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/map')
def map_view():
    """Interactive bike map"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('map.html', bikes=bikes)

@app.route('/api/bikes')
def api_bikes():
    """API endpoint for bike data"""
    bike_type = request.args.get('type', '')
    available_only = request.args.get('available', '').lower() == 'true'
    
    filtered_bikes = {}
    for bike_id, bike in bikes.items():
        if bike_type and bike['type'] != bike_type:
            continue
        if available_only and not bike['available']:
            continue
        filtered_bikes[bike_id] = bike
    
    return jsonify(filtered_bikes)

@app.route('/bike/<bike_id>')
def bike_details(bike_id):
    """Bike details page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    bike = bikes.get(bike_id)
    if not bike:
        flash('Bicicleta não encontrada!', 'error')
        return redirect(url_for('map_view'))
    
    return render_template('bike_details.html', bike=bike, plans=rental_plans)

@app.route('/reserve/<bike_id>', methods=['POST'])
def reserve_bike(bike_id):
    """Reserve a bike"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    bike = bikes.get(bike_id)
    if not bike or not bike['available']:
        flash('Bicicleta não disponível!', 'error')
        return redirect(url_for('map_view'))
    
    plan = request.form.get('plan')
    if plan not in rental_plans:
        flash('Plano inválido!', 'error')
        return redirect(url_for('bike_details', bike_id=bike_id))
    
    # Create reservation
    reservation_id = str(uuid.uuid4())
    reservations[reservation_id] = {
        'id': reservation_id,
        'user_id': session['user_id'],
        'bike_id': bike_id,
        'plan': plan,
        'status': 'pending_payment',
        'created_at': datetime.now().isoformat(),
        'price': rental_plans[plan]['price']
    }
    
    # Mark bike as reserved
    bikes[bike_id]['available'] = False
    
    return redirect(url_for('payment', reservation_id=reservation_id))

@app.route('/payment/<reservation_id>')
def payment(reservation_id):
    """Payment page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    reservation = reservations.get(reservation_id)
    if not reservation or reservation['user_id'] != session['user_id']:
        flash('Reserva não encontrada!', 'error')
        return redirect(url_for('map_view'))
    
    bike = bikes[reservation['bike_id']]
    plan = rental_plans[reservation['plan']]
    
    return render_template('payment.html', 
                         reservation=reservation, 
                         bike=bike, 
                         plan=plan)

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Create Stripe checkout session"""
    if not STRIPE_KEY:
        flash('Pagamento temporariamente indisponível. Entre em contato com o suporte.', 'error')
        return redirect(url_for('dashboard'))
    
    reservation_id = request.form.get('reservation_id')
    reservation = reservations.get(reservation_id)
    
    if not reservation:
        return "Reserva não encontrada", 400
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'brl',
                    'product_data': {
                        'name': f'Aluguel de Bicicleta - {rental_plans[reservation["plan"]]["name"]}',
                    },
                    'unit_amount': int(reservation['price'] * 100),  # Convert to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'{request.host_url}success/{reservation_id}',
            cancel_url=f'{request.host_url}payment/{reservation_id}',
            metadata={
                'reservation_id': str(reservation_id)
            }
        )
        if checkout_session.url:
            return redirect(checkout_session.url, code=303)
        else:
            flash('Erro ao criar sessão de pagamento', 'error')
            return redirect(url_for('payment', reservation_id=reservation_id))
    except Exception as e:
        flash(f'Erro no pagamento: {str(e)}', 'error')
        return redirect(url_for('payment', reservation_id=reservation_id))

@app.route('/success/<reservation_id>')
def payment_success(reservation_id):
    """Payment success page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    reservation = reservations.get(reservation_id)
    if not reservation:
        flash('Reserva não encontrada!', 'error')
        return redirect(url_for('map_view'))
    
    # Update reservation status
    reservation['status'] = 'paid'
    reservation['paid_at'] = datetime.now().isoformat()
    
    # Generate QR code for bike unlock
    qr_data = f"UNLOCK_BIKE:{reservation['bike_id']}:{reservation_id}"
    qr = qrcode.main.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Convert QR code to base64 string
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    bike = bikes[reservation['bike_id']]
    plan = rental_plans[reservation['plan']]
    
    return render_template('success.html', 
                         reservation=reservation,
                         bike=bike,
                         plan=plan,
                         qr_code=qr_code_base64)

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_reservations = {k: v for k, v in reservations.items() 
                        if v['user_id'] == session['user_id']}
    
    return render_template('dashboard.html', reservations=user_reservations, bikes=bikes, plans=rental_plans)

@app.route('/cancel/<reservation_id>')
def cancel_reservation(reservation_id):
    """Cancel a reservation"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    reservation = reservations.get(reservation_id)
    if reservation and reservation['user_id'] == session['user_id']:
        # Make bike available again
        bikes[reservation['bike_id']]['available'] = True
        # Remove reservation
        del reservations[reservation_id]
        flash('Reserva cancelada com sucesso!', 'success')
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)