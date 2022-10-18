from flask import Flask

api = Flask(__name__)

@api.route('/')
def my_profile():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body

if __name__ == '__main__':
    api.run(host='127.0.0.1', port=8080, debug=True)