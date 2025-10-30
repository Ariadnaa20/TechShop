# 🛒 TechShop – Aplicació Web MVC amb Flask i SQLite

**Autora:** Ariadna Pascual i Hugo Torres
**Data:** 2025  

---

## 📘 Descripció del projecte

**TechShop** és una aplicació web de comerç electrònic desenvolupada amb **Python, Flask i SQLite** que permet gestionar un carretó de compres en línia.  
Aquesta pràctica posa en pràctica els principis del patró **Model–Vista–Controlador (MVC)** i de l’**arquitectura en tres capes**: presentació, lògica de negoci i accés a dades.

L’aplicació permet als usuaris:
- Veure una llista de productes disponibles.
- Afegir i eliminar productes del carretó.
- Crear un compte d’usuari o iniciar sessió.
- Finalitzar la compra amb una comanda guardada a la base de dades.

---

## 🎯 Objectius

- Comprendre la importància de separar responsabilitats entre vista, negoci i dades.
- Implementar una base de dades relacional amb **SQLite**.
- Aplicar el patró **MVC** amb **Flask**.
- Afegir validacions tant al servidor com al client.
- Integrar un **assistent d’intel·ligència artificial (ChatGPT)** per millorar la codificació i documentació.

---

## 🧩 Estructura del projecte

```
Practica_TechShop/
│
├── app.py                        # Arrel principal de Flask
│
├── models/                       # Capa de dades (ORM SQLAlchemy)
│   ├── __init__.py
│   ├── product.py
│   ├── user.py
│   ├── order.py
│   ├── order_item.py
│
├── services/                     # Capa de lògica de negoci
│   ├── cart_service.py
│   └── order_service.py
│
├── routes/                       # Capa de presentació/controladors
│   └── routes.py
│
├── database/                     # Inicialització i dades de prova
│   └── db_seed.py
│
├── templates/                    # Plantilles HTML (Jinja2)
│   ├── checkout.html
│   ├── products.html
│   ├── cart.html
│   └── order_succes.html
│
├── static/                       # Recursos estàtics
│   ├── css/style.css
│   └── js/main.js
│
├── instance/
│   └── techshop.db               # Base de dades SQLite
│
└── README.md                     # Documentació del projecte
```

---

## 🧱 Disseny de la base de dades

| Taula | Descripció | Camps principals |
|-------|-------------|------------------|
| **Product** | Llista de productes disponibles | id, name, price, stock |
| **User** | Informació dels usuaris | id, username, password_hash, email, created_at |
| **Order** | Comandes creades pels usuaris | id, total, created_at, user_id |
| **OrderItem** | Línies de cada comanda | id, order_id, product_id, quantity |

**Relacions:**
- Un `User` pot tenir moltes `Order`.
- Una `Order` pot tenir molts `OrderItem`.
- Cada `OrderItem` fa referència a un `Product`.

---

## ⚙️ Lògica de negoci

Els serveis gestionen la lògica principal de TechShop:

### `CartService`
- `add_to_cart(product, quantity)`: afegeix productes al carretó.
- `remove_from_cart(product_id)`: elimina productes.
- `validate_stock(product, quantity)`: comprova disponibilitat d’estoc.

### `OrderService`
- `create_order(cart, user_id)`: crea una nova comanda i els seus detalls (`OrderItem`).

---

## 🌐 Rutes principals

| Ruta | Mètode | Descripció |
|------|---------|------------|
| `/` | GET | Redirigeix al formulari de checkout |
| `/checkout` | GET/POST | Formulari d’usuari i validació inicial |
| `/products` | GET | Mostra la llista de productes |
| `/add_to_cart/<product_id>/<quantity>` | GET/POST | Afegeix productes al carretó |
| `/cart` | GET | Mostra el carretó actual |
| `/remove_from_cart/<product_id>` | GET | Elimina productes del carretó |
| `/finish_checkout` | GET | Finalitza la compra i desa la comanda |

---

## 🧠 Validacions implementades

### 🔹 Al **frontend** (HTML)
- `required`, `minlength`, `maxlength` i `pattern` als inputs del checkout.
- `<input type="number" min="1" max="5">` per les quantitats.
- Missatges d’error visuals amb `flash`.

### 🔹 Al **backend** (Python)
- Comprovació d’usuari existent.
- Validació d’estoc disponible.
- Límits màxims de 5 unitats per producte.
- Contrasenyes hashades amb `werkzeug.security`.

---

## 🧑‍💻 Instal·lació i execució

### 1️⃣ Crear un entorn virtual
```bash
python -m venv venv
source venv/Scripts/activate  # (Windows)
```

### 2️⃣ Instal·lar dependències
```bash
pip install flask flask_sqlalchemy werkzeug
```

### 3️⃣ Crear la base de dades amb dades de prova
```bash
python database/db_seed.py
```

### 4️⃣ Executar el servidor
```bash
python app.py
```

### 5️⃣ Obrir al navegador
```
http://127.0.0.1:5000
```

---

## 🧩 Exemple d’ús

1. L’usuari accedeix al **formulari de checkout** i introdueix les seves dades.  
2. Un cop validat, veu els **productes disponibles**.  
3. Afegeix alguns productes al **carretó**.  
4. Prem “💳 Finalitzar compra” → es crea una nova comanda a la base de dades.  
5. Es mostra la pantalla de **Compra Finalitzada**.

---

## 🧠 Ús d’intel·ligència artificial (IA)

S’ha utilitzat **ChatGPT (OpenAI GPT-5)** per:
- Optimitzar el codi Python i separar responsabilitats segons el patró MVC.
- Generar documentació tècnica i el present `README.md`.
- Corregir errors de dependències i millorar la interfície d’usuari (`HTML + CSS`).

---

## 📸 Captures de pantalla

### ✅ Llista de productes
*(Exemple visual de la pàgina /products)*

### 🛒 Carretó de compra
*(Exemple amb productes afegits)*

### 💳 Compra finalitzada
*(Pantalla `order_succes.html` amb total i confirmació)*

---

## 🧾 Llicència

Aquest projecte es distribueix sota llicència **MIT** per a ús educatiu.

© 2025 TechShop – Desenvolupat per **Ariadna Pascual i Hugo Torres** 🩵
