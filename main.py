from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
import json

app = Flask(__name__)
api = Api(app)


class GetLiveStatus(Resource):
    def get(self):
        return 'FrontEnd Server: Alive'


# Add the resource to the API
api.add_resource(GetLiveStatus, '/getlivestatus')

# Configure Swagger UI
API_URL = 'http://127.0.0.1:5000/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    '',
    API_URL,
    config={
        'app_name': "SaveIt"
    }
)
app.register_blueprint(swaggerui_blueprint)


@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))


if __name__ == '__main__':
    app.run(debug=True)
