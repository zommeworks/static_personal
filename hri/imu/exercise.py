import sys
import os
import re
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R

acc_in = [[0.0161], [-1.0002], [0.0105]]
acc_g = [[0], [-1], [0]]
angle = [-3.0218, 1.5012, -2.4253]

r_ex = R.from_euler('xyz', angle, degrees=False)
r_in = R.from_euler('XYZ', angle, degrees=False)

m_ex = r_ex.as_matrix()
m_in = r_in.as_matrix()

print('>>> m_ex, acc_in :')
print(m_ex @ acc_in)
print('>>> m_in, acc_in :')
print(m_in @ acc_in)
print('>>> m_ex, acc_g :')
print(m_ex @ acc_g)
print('>>> m_in, acc_g :')
print(m_in @ acc_g)
'''
def main():
	df = pd.DataFrame(columns = ['Timestamp', 'pose_X', 'pose_Y', 'pose_Z'])
	for i in range(5):
		ni = i//2
		print(ni)
		df.loc[i] = [2020, 1, 2, 3]
	print(df)

if __name__ == '__main__':
    main()
'''