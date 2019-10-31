import pyrebase
from config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Dont Run. Data has already entered

# quote = {"text": "Believe in yourself! Have faith in your abilities! Without a humble but reasonable confidence in your own powers you cannot be successful or happy.", "author": "Norman Vincent Peale"}
# db.child("quotes").push(quote)

# quotes = ["Your focus determines your reality.", "Do. Or do not. There is no try.", "In my experience there is no such thing as luck.", "Your eyes can deceive you. Don’t trust them.", "The Force will be with you. Always.", "There’s always a bigger fish.", "You can’t stop the change, any more than you can stop the suns from setting.", "Fear is the path to the dark side. Fear leads to anger; anger leads to hate; hate leads to suffering. I sense much fear in you.", "I’m one with the Force. The Force is with me."]
# author = 'Star Wars'

# for q in quotes:
#     quote = {
#         "text": q,
#         "author": author
#     }
#     db.child("quotes").push(quote)