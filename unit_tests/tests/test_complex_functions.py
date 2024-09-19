import pytest

from functions.complex_functions import OccupationMatcher

import numpy as np

def test_full_class():
	occ_match = OccupationMatcher()
	occ_match.load_things()
	occ_match.get_all_embeddings()

	job_title = occ_match.occupation_names[0]

	single_embedding = occ_match.bert_model.encode([job_title])

	best_ix = occ_match.get_closest_embedding(occ_match.all_embeddings, single_embedding)

	# Since this job title comes from the dataset we are comparing to, 
	# it should exactly match with itself

	assert occ_match.occupation_names[best_ix] == job_title


# Test using Mocking

# class mock_bert_model(object):
# 	"""
# 	You can even make up mock classes if you want!
# 	"""
# 	def encode(text):
# 		return [[0, 1, 2, 3], [5, 5, 5, 5], [9, 8, 7, 6]]
		

def test_using_mocking():

	occ_match = OccupationMatcher()

	# Make them up so you don't need to load things unnecessary to perform the test

	# More transparent that get_closest_embedding is working as it should be
	best_ix = occ_match.get_closest_embedding(
		np.array([[0, 1, 2, 3], [5, 5, 5, 5], [9, 8, 7, 6]]),
		np.array([5.5, 5.4, 5.1, 5])
		)

	assert best_ix == 1



