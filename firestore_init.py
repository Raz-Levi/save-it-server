import firebase_admin
from globals import database_configurations as config
from firebase_admin import credentials
from firebase_admin import firestore


def firestore_init():
    cred = credentials.Certificate(config.DatabaseConfigurations.get_service_account_key_path())
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    data = {
        "name": "Raz",
        "age": 26,
        "email": "john.doe@example.com",
    }
    db.collection("QA").document("QA").set(data)

    # Read data from Firestore
    user_ref = db.collection("QA").document("QA")
    user_data = user_ref.get().to_dict()
    print(user_data)


if __name__ == '__main__':
    firestore_init()
