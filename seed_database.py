from google.cloud import firestore


def write_quotes():
    db = firestore.Client()

    coll_ref = db.collection(u"quotes")
    coll_ref.add({
        u"text": u"Believe in yourself! Have faith in your abilities! Without a humble but reasonable confidence in your own powers you cannot be successful or happy.",
        u"author": u"Norman Vincent Peale"
    })

    quotes = [
        u"Your focus determines your reality.", "Do. Or do not. There is no try.",
        u"In my experience there is no such thing as luck.",
        u"Your eyes can deceive you. Don’t trust them.",
        u"The Force will be with you. Always.",
        u"There’s always a bigger fish.",
        u"You can’t stop the change, any more than you can stop the suns from setting.",
        u"Fear is the path to the dark side. Fear leads to anger; anger leads to hate; hate leads uto suffering. I sense much fear in you.",
        u"I’m one with the Force. The Force is with me."
    ]
    author = u"Star Wars"

    for q in quotes:
        quote = {
            "text": q,
            "author": author
        }
        coll_ref.add(quote)


def write_users():
    db = firestore.Client()

    coll_ref = db.collection(u"quotes")
    coll_ref.add({

    })


if __name__ == '__main__':
    write_quotes()
