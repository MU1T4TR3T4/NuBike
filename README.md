# 🚴‍♂️ NuBike - Sistema de Aluguel de Bicicletas

Sistema completo de aluguel de bicicletas desenvolvido com Flask, inspirado no design do Nubank. Permite aos usuários encontrar, reservar e alugar bicicletas através de uma interface moderna e intuitiva.

## ✨ Funcionalidades

- **Autenticação**: Sistema seguro de cadastro e login
- **Mapa Interativo**: Visualização de bicicletas disponíveis com Leaflet.js
- **Catálogo de Bicicletas**: Diferentes tipos e modelos com detalhes
- **Sistema de Reservas**: Múltiplos planos de aluguel (tempo/distância)
- **Pagamento Seguro**: Integração com Stripe para processamento
- **QR Code**: Geração automática para desbloqueio das bikes
- **Dashboard**: Histórico de aluguéis e estatísticas
- **Design Responsivo**: Interface otimizada para mobile e desktop

## 🎨 Design

Interface inspirada no Nubank com:
- **Cores**: Roxo escuro (#820AD1), Lilás (#BA68C8), Branco (#FFFFFF)
- **Componentes**: Cards modernos, botões arredondados, gradients
- **Layout**: Responsivo com Bootstrap 5
- **Tipografia**: Font Poppins do Google Fonts

## 🛠️ Tecnologias

### Backend
- **Flask**: Framework web Python
- **Flask-Session**: Gerenciamento de sessões
- **Stripe**: Processamento de pagamentos
- **QRCode**: Geração de códigos QR
- **Werkzeug**: Utilitários de segurança

### Frontend
- **HTML5/CSS3**: Estrutura e estilização
- **JavaScript**: Interatividade e funcionalidades
- **Bootstrap 5**: Framework CSS responsivo
- **Leaflet.js**: Mapas interativos
- **Font Awesome**: Biblioteca de ícones

## 📁 Estrutura do Projeto

```
/
├── app.py                  # Aplicação principal Flask
├── requirements.txt        # Dependências Python
├── Procfile               # Configuração para Render
├── README.md              # Este arquivo
├── replit.md              # Documentação técnica
├── /templates/            # Templates HTML
│   ├── base.html          # Template base
│   ├── index.html         # Página inicial
│   ├── login.html         # Login
│   ├── register.html      # Cadastro
│   ├── map.html           # Mapa de bicicletas
│   ├── bike_details.html  # Detalhes da bike
│   ├── payment.html       # Página de pagamento
│   ├── success.html       # Confirmação
│   └── dashboard.html     # Dashboard do usuário
├── /static/               # Arquivos estáticos
│   ├── /css/
│   │   └── style.css      # Estilos customizados
│   ├── /js/
│   │   └── main.js        # Scripts JavaScript
│   └── /img/              # Imagens
└── /data/
    └── bicicletas.json    # Mock de dados das bikes
```

## 🚀 Instalação e Execução Local

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/nubike.git
cd nubike
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**
```bash
export SESSION_SECRET="sua-chave-secreta-aqui"
export STRIPE_SECRET_KEY="sk_test_sua_chave_stripe"  # Opcional para desenvolvimento
```

5. **Execute a aplicação:**
```bash
python app.py
```

6. **Acesse no navegador:**
```
http://localhost:5000
```

## 🌐 Deploy no Render

### Passo a Passo

1. **Faça fork/clone do projeto no GitHub**

2. **Conecte sua conta do Render ao GitHub**

3. **Crie um novo Web Service no Render:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3

4. **Configure as variáveis de ambiente no Render:**
   - `SESSION_SECRET`: Chave secreta para sessões
   - `STRIPE_SECRET_KEY`: Chave do Stripe (opcional)

5. **Deploy automático**: O Render fará deploy automaticamente a cada push

### Variáveis de Ambiente Necessárias

- `SESSION_SECRET`: Chave secreta para Flask sessions (obrigatória)
- `STRIPE_SECRET_KEY`: Chave da API do Stripe (opcional para desenvolvimento)

**Exemplo de configuração no Render:**
```bash
SESSION_SECRET=sua-chave-secreta-super-segura-aqui-min-32-chars
STRIPE_SECRET_KEY=sk_test_sua_chave_stripe_aqui  # Opcional
```

## 📊 Dados de Demonstração

O sistema utiliza dados mockados armazenados em `/data/bicicletas.json` para demonstração, incluindo:

- **Localizações**: Pontos em São Paulo (Paulista, Vila Madalena, etc.)
- **Tipos de Bikes**: Urbana, Elétrica, Mountain Bike, Speed
- **Preços**: Diferentes planos por tempo e distância
- **Status**: Disponível, Em uso, Manutenção

## 🔧 Desenvolvimento

### Estrutura do Código

- **Rotas principais**: `/`, `/login`, `/register`, `/map`, `/dashboard`
- **API endpoints**: `/api/bikes`, `/create-checkout-session`
- **Autenticação**: Sistema baseado em sessões Flask
- **Pagamentos**: Stripe Checkout (modo sandbox)

### Customização

1. **Cores e Estilo**: Edite `/static/css/style.css`
2. **Funcionalidades JS**: Modifique `/static/js/main.js`
3. **Templates**: Personalize arquivos em `/templates/`
4. **Dados**: Ajuste `/data/bicicletas.json`

## 📝 Licença

Este é um projeto acadêmico desenvolvido para fins educacionais.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abrir um Pull Request

## 📞 Suporte

Para dúvidas ou suporte, entre em contato através das issues do GitHub.

---

**NuBike** - Mobilidade urbana simples e sustentável 🌱