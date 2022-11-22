import numpy as np

def highlight_min(s):
    if s.dtype == np.object:
        is_min = [False for _ in range(s.shape[0])]
    else:
        is_min = s == s.min()

    return ["background: powderblue" if cell else "" for cell in is_min]