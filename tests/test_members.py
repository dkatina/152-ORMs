from app import create_app
from app.models import db, Member
import unittest
from werkzeug.security import generate_password_hash
from app.utils.util import encode_token

class TestMember(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.member = Member(name="test_user", email="test@email.com", phone="1234567890", password=generate_password_hash('test'), role='admin')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.member)
            db.session.commit()
        self.token = encode_token(1, 'admin')
        self.client = self.app.test_client()

    def test_create_member(self):
        member_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "123-456-7890",
            "password": "123",
            "role": "general"
        }

        response = self.client.post('/members/', json=member_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")
    
    def test_invalid_creation(self):
        member_payload = {
            "name": "John Doe",
            "phone": "123-456-7890",
            "password": "123",
            "role": "general"
        }

        response = self.client.post('/members/', json=member_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

    def test_duplicate_member(self):
        member_payload = {
            "name": "test_user",
            "email": "test@email.com",
            "phone": "1234567890",
            "password": "test",
            "role": "admin"
        }

        response = self.client.post('/members/', json=member_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], "Account already associated with that email.")
        

    def test_login_member(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }

        response = self.client.post('/members/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']
    
    def test_invalid_login(self):
        credentials = {
            "email": "bad_email@email.com",
            "password": "bad_pw"
        }

        response = self.client.post('/members/login', json=credentials)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid email or password!')
     
    
    def test_get_member(self):

        response = self.client.get('/members/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'test_user')

    def test_get_all_members(self):
        response = self.client.get('/members/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test_user')


    def test_update_member(self):

        update_payload = {
            "name": "Peter",
            "phone": "",
            "email": "",
            "password": ""
        }

        headers = {'Authorization': "Bearer " + self.token}

        response = self.client.put('/members/', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Peter')
        self.assertEqual(response.json['email'], 'test@email.com')

    def test_delete_member(self):
        headers = {'Authorization': "Bearer " + self.token}
        response = self.client.delete('/members/', headers=headers)
        self.assertEqual(response.status_code, 200)