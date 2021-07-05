import numpy as np
import pandas as pd


s = np.random.randn(1000)
df = pd.DataFrame(s)
df[0].plot(kind = 'hist')