from flask import render_template, url_for, redirect, request
from app import app, db, bcrypt
from app.models import User
from app.forms import RegisterForm, SearchForm
import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
    form = SearchForm()
    return render_template('index.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/parse', methods=['POST'])
def parse():
    category = request.form['category']
    url = f'https://www.divan.ru/{category}/'
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        products = []
        for item in soup.find_all('div', class_='product_item'):
            title = item.find('div', class_='title').get_text(strip=True)
            price = item.find('div', class_='price').get_text(strip=True)
            products.append({'title': title, 'price': price})

        if not products:
            return render_template('index.html', message="Товары не найдены. Попробуйте другую категорию.", form=SearchForm())

        return render_template('results.html', products=products)
    except requests.exceptions.RequestException as e:
        return render_template('index.html', message="Ошибка при подключении к сайту. Попробуйте позже.", form=SearchForm())
