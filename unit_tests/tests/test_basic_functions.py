import pytest

from functions.basic_functions import add_two_numbers, add_suffix_to_list, return_first_suffixed_value

def test_add_two_numbers():

	assert add_two_numbers(1, 2) == 3

def test_add_suffix_to_list():

	str_list = ["cat", "dog"]
	suffix = "_animal"

	result = add_suffix_to_list(str_list, suffix)

	assert result == ["cat_animal", "dog_animal"]
	assert len(result) == len(str_list)

def test_mixed_input_add_suffix_to_list():

	str_list = [15, "cat"]
	suffix = "_animal"

	result = add_suffix_to_list(str_list, suffix)

	assert result == ["15_animal", "cat_animal"]
	assert len(result) == len(str_list)


def test_return_first_suffixed_value():

	str_list = [15, "cat"]
	suffix = "_animal"

	result = return_first_suffixed_value(str_list, suffix)

	assert isinstance(result, str)
