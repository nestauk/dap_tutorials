
def add_two_numbers(
	a: float,
	b: float
	) -> float:
	return a + b

def add_suffix_to_list(
	a: list,
	suffix: str,
	) -> list:

	return [a_i+suffix for a_i in a if isinstance(a_i, str)]

def return_first_suffixed_value(
	a: list,
	suffix: str,
	) -> str:

	suffixed_result = add_suffix_to_list(a, suffix)
	return suffixed_result[0]