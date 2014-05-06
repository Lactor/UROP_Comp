import numpy as np

res_folder = '../Data_Teste_2D/'

for i in range(1000):
    fil = open(res_folder + str(i)+".txt", "w")
    ra = np.random.rand(2)*(-30)
    fil.write("1 " + str(ra[0])+"\n")
    fil.write("2 " + str(ra[1])+ "\n")
    fil.close()
 
