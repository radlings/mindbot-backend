from google.cloud import firestore
db = firestore.Client()

category = []
title = []
description = []
source = []
url = []

for categ, tit, desc, src, u in zip(category, title, description, source, url):
	try:
		print(tit)
		category = categ
		tmp_json = {
			'title': tit,
			'description': desc,
			'source': src,
			'url': u,
			'helpful': 0,
			'not_helpful': 0,
			'impressions': 0,
			'discovery': 0 
		}
		doc_ref = db.collection('all_resources').document(category).collection('resources').document()
		doc_ref.set(tmp_json)
	except Exception as e:
		print("*Error: ", str(e))
