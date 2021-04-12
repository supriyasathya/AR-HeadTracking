
# script to compute error or change in pose between two transformation matrices. In the accuracy measurement experiments, A1 is the tracked pose of a game object and A2 is the pose after any manual adjustment that was
# needed by the user to make the virtual rendering align well with the real-world counterpart.
# The function "compute_error" computes the translation and rotation error between A1 and A2. 
# Replace the csv file with the csv file containing the poses from the MagicLeap debug log.


import numpy as np 
from math import sqrt 
from sklearn.metrics import mean_squared_error
from scipy.spatial.transform import Rotation as R
from numpy.linalg import inv
from csv import reader
import csv

def compute_error(A1,A2):
	A1 = np.array(A1)
	A2 = np.array(A2)
	A1 = A1.reshape(4,4)
	A2 = A2.reshape(4,4)

	A1rot = A1[:3,:3]
	A2rot = A2[:3,:3]

	A1tra = A1[:3,3]
	A2tra = A2[:3,3]

	A1R = R.from_matrix(A1rot)
	A2R = R.from_matrix(A2rot)
    #to compute rotation error form rotation matrix
	err_rot = A1rot*inv(A2rot)

	rot_R = R.from_matrix(err_rot)
	err_rot = rot_R.as_euler('xyz', degrees = True)
	#compute translation error from the translation vector
	rmstra = sqrt(mean_squared_error(A1tra,A2tra))
	# Following lines will print the rotation error and translation error in the terminal. Replace the following lines to write to a csv file.
	print(err_rot)
	print(rmstra)
	print(' ')



def main():
	data = []
   # replace with a csv file containing the tracked pose and pose after manual alignment adjustment taken from the MagicLeap debuglog via "The Lab". Consecutive rows should contain
   # the pose before and after manual adjustment
	with open('DebugLogCSVFile.csv', 'r') as read_obj:
		csv_reader = csv.reader(read_obj)

		for row in csv_reader:
			if len(row) != 0:
				row = list(map(float, row[0].split(",")))
				data.append(row)

		# Read every two rows at a time - first row is the tracked pose and secon row is pose after any adjustment.
		for i in range(0,len(data)+1,2):
			#print(i)
			A1 = data[i]
			A2 = data[i+1]
			compute_error(A1,A2)


if __name__ == '__main__':
    main()




