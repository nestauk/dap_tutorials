"""
A class to find the standardised occupation name (SOC) given an inputted job title
"""

import pandas as pd

import numpy as np

class OccupationMatcher(object):

	def load_things(self):

		from sentence_transformers import SentenceTransformer

		# Load some data
		data = pd.read_csv("s3://open-jobs-indicators/prinz/occupation_aggregated_data_20240314_extra_gjeformat.csv")
		self.occupation_names = data['SOC_2020_EXT_name'].tolist()

		# Load a sentence transformer model
		self.bert_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

	def embed_texts(self, texts):

		return self.bert_model.encode(texts)

	def get_all_embeddings(self):
		
		self.all_embeddings = self.embed_texts(self.occupation_names)

		return self.all_embeddings

	def get_closest_embedding(self, all_embeddings, single_embedding):
		for i, embedding in enumerate(all_embeddings):
			dist = np.linalg.norm(single_embedding - embedding)
			if (i == 0) or (dist < closest_dist):
				best_ix = i
				closest_dist = dist
		return best_ix

	def find_closest_occupation_name(self, job_title):

		single_embedding = self.bert_model.encode([job_title])

		best_ix = self.get_closest_embedding(self.all_embeddings, single_embedding)

		return self.occupation_names[best_ix]


if __name__ == '__main__':
	
	occ_match = OccupationMatcher()
	occ_match.load_things()
	occ_match.get_all_embeddings()

	print(occ_match.find_closest_occupation_name("plumber"))
	print(occ_match.find_closest_occupation_name("data wrangler"))
