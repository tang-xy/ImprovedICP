import math
#
import operator

x = [0 for i in range(20)]
x[0]=[0,0];
x[1]=[1,0];
x[2]=[0,1];
x[3]=[1,1];
x[4]=[2,1];
x[5]=[1,2];
x[6]=[2,2];
x[7]=[3,2];
x[8]=[6,6];
x[9]=[7,6];
x[10]=[8,6];
x[11]=[6,7];
x[12]=[7,7];
x[13]=[8,7];
x[14]=[9,7];
x[15]=[7,8];
x[16]=[8,8];
x[17]=[9,8];
x[18]=[8,9];
x[19]=[9,9];
#

def main(z, x):
	weight = {};
	tree = {};
	long = len(z)
	for i in range(0,long):
		weight[i]=x[z[i]];
	while(1):
		newweight = {};
		num = {};
		for j in range(0,long):
			newweight[j]=[0,0];
			num[j] = 0;
		for  i in range(0,len(x)):
			p_min = 10000;
			for j in range(0,long):
				temp = (x[i][0]-weight[j][0])*(x[i][0]-weight[j][0])+(x[i][1]-weight[j][1])*(x[i][1]-weight[j][1]);
				if(temp<p_min):
					p_min = temp;
					tree[i] = j;
			newweight[tree[i]][0]+=x[i][0];
			newweight[tree[i]][1]+=x[i][1];
			num[tree[i]]+=1;
		for j in range(0,long):
			newweight[j][0]/=num[j];
			newweight[j][1]/=num[j];
		if(operator.eq(newweight,weight)):
			return tree;
		weight = newweight;




if __name__ == "__main__":
	#import numpy as np
	#x = np.array(x)
	z = [1,10];
	main(z, x);