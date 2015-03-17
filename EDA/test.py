import numpy as np

X = np.array([1.,2.,10.009201824123 ])

np.savetxt('%s/test.csv' %('/Volumes/hermanng_backup/Virginia_Capstone'),X, fmt = '%.8e')