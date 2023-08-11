from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'  # SQLite database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(db.String(20), nullable=False)

@app.route('/api/users', methods=['GET'])
def search_users():
    first_name = request.args.get('first_name')
    matching_users = User.query.filter(User.first_name.startswith(first_name)).all()

    if matching_users:
        result = []
        for user in matching_users:
            result.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': user.age,
                'gender': user.gender,
                'email': user.email,
                'phone': user.phone,
                'birth_date': user.birth_date
            })
        return jsonify(result)
    else:
        # Call external API to get users
        external_api_url = f"https://dummyjson.com/users/search?q={first_name}"
        response = requests.get(external_api_url)
        external_users = response.json()

        for ext_user in external_users:
            new_user = User(
                first_name=ext_user['first_name'],
                last_name=ext_user['last_name'],
                age=ext_user['age'],
                gender=ext_user['gender'],
                email=ext_user['email'],
                phone=ext_user['phone'],
                birth_date=ext_user['birth_date']
            )
            db.session.add(new_user)
            db.session.commit()

        return jsonify(external_users)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
