import abstract_recommender

def calculate_recommendations_for(user):
	client_id = client['id']
	client_name = client['name']
	for content in client['contents']:
		content_type = content['content']
		content_url = content['url']
		abstract_recommender.calculate(client_id, client_name, content_type, content_url)