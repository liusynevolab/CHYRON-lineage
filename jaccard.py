import pickle
import pandas as pd
from itertools import combinations, product
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from scipy.stats import norm
import operator
import numpy as np
import tkinter as tk

class Main:
        def __init__(self,parent):
                
          
           self.parent=parent
           '''
           self.geometry("200x200") 
           self.minsize(100,100)
           ''' 


           
           self.v2 = tk.IntVar()
           self.v2.set(1)
           self.v3 = tk.DoubleVar()
           self.v3.set(0.0139)
           self.v4 = tk.DoubleVar()
           self.v4.set(1.0)

                     
           self.text1=tk.Label(self.parent,text="LENGTH CUTOFF")
           self.text1=self.text1.place(x=0,y=0)
          
           self.text2=tk.Label(self.parent,text="COUNT CUTOFF")
           self.text2=self.text2.place(x=0,y=20)
           
           
           self.text3=tk.Label(self.parent,text="RECOVERY EFFICIENCY")
           self.text3=self.text3.place(x=0,y=40)
                        
                        
           self.entry0 = tk.Entry(self.parent,textvariable=str(self.v2))
           self.entry0.place(x=130,y=0)
          
           
           self.entry1 = tk.Entry(self.parent,textvariable=str(self.v3))
           self.entry1.place(x=130,y=20)
          
           
           self.entry2 = tk.Entry(self.parent,textvariable=str(self.v4))
           self.entry2.place(x=130,y=40)
           
           
             
           B = tk.Button(self.parent, text = "QUIT", command = self.get)
           B.place(x=50,y=70)
           B.config(width=15,height=1,font=("Times New Roman",11))

         
           
          
           

        def get(self):                

            global val2, val3, val4 
            val2,val3,val4=int(self.entry0.get()),float(self.entry1.get()),float(self.entry2.get())
            self.parent.destroy() 


with open('darkgreenLT_percinsDict.pkl', 'rb') as file:
        insDict = pickle.load(file)

root=tk.Tk()
app = Main(root)
root.mainloop()

val3= val3*1000000


LENGTH_CUTOFF = (val2,16) ## slider 2; the 2nd number should go from 2-16, inclusive, exclusive
COUNT_CUTOFF = val3 #can we make this value a float rather than an integer? this would be slider 3
RECOVERY_EFFICIENCY = val4 #slider 4, should go from 0.05-1

#def update():
#       global val2, val3, val4
#       vel2 = e1.get()
#       val3 = e2.get()*1000000
#       val4 = e3.get()

#master = tk.Tk()
#tk.Label(master, text="LENGTH CUTOFF").grid(row=0)
#tk.Label(master, text="COUNT CUTOFF(%)").grid(row=1)
#tk.Label(master, text="RECOVERY EFFICIENCY").grid(row=2)
#e1 = tk.Entry(master)
#e2 = tk.Entry(master)
#e3 = tk.Entry(master)
#e1.insert(10,16)
#e2.insert(10,0.0139)
#e3.insert(10,1)

#e1.grid(row=0, column=1)
#e2.grid(row=1, column=1)
#e3.grid(row=2, column=1)
#tk.Button(master,text="Set",command=update()).grid(row=3)
#tk.mainloop()


def jaccard_calc(l1,l2):
        a,b,c,d = (0,0,0,0)
        for i in range(len(l1)):
                if l1[i] == l2[i]:
                        if l1[i] == 1:
                                a+=1
                                continue
                        else:
                                d+=1
                                continue
                else:
                        if l1[i] == 1:
                                b+=1
                                continue
                        else:
                                c+=1
                                continue
        # print(a,b,c,d)
        return (a)/(a+b+c)

def insertionFinder(wellPairs, vectors):
        for pair in wellPairs:
                with open(f"{pair[0]}_{pair[1]}_insertions.txt",'w') as file:
                        insertions = vectors["wells"][pair[0]][0].intersection(vectors["wells"][pair[1]][0])
                        for insertion in insertions:
                                file.write(insertion+'\n')

def nextLevelInsertionFinder(wellPairs2, vectors):
        for pair in wellPairs2:
                with open(f"{pair[0]}_{pair[1]}_{pair[2]}_{pair[3]}_insertions.txt",'w') as file:
                        set1 = vectors["wells"][pair[0]][0].intersection(vectors["wells"][pair[1]][0])
                        set2 = vectors["wells"][pair[2]][0].intersection(vectors["wells"][pair[3]][0])
                        insertions = set1.intersection(set2)
                        for insertion in insertions:
                                file.write(insertion+'\n')


# c =0
# for ins in insDict:
#       print(ins, insDict[ins])
#       c +=1
#       if c >=10:
#               break
# exit()

wells = []
vectors = {}
vectors["pool"] = [set(),[]]
vectors["wells"] = {}

for x in range(1,17):
        wells.append(f"well_{str(x)}")
        vectors["wells"][f"well_{str(x)}"] = [set(),[]]
print(vectors["wells"][f"well_{str(x)}"])
# for i in range(1,5):
#       vectors["wells"][f"well_{str(i)}"] = [set(),[]]
#       wells.append(f"well_{str(i)}")
        # print(vectors["wells"])

# for _ in group_2:
#       vectors["wells"][f"well_{_}"] = [set(),[]]
#       wells.append(f"well_{_}")

for ins in insDict:
        if not ins == 'ROOT':
                if len(ins) in range(*LENGTH_CUTOFF):
                        for well in insDict[ins]["counts"]:
                                if well in wells:
                                        if insDict[ins]["counts"][well] >= COUNT_CUTOFF:
                                                if np.random.choice([0,1], p=[1-RECOVERY_EFFICIENCY, RECOVERY_EFFICIENCY]):
                                                        vectors["pool"][0].add(ins)
                                                        vectors["wells"][well][0].add(ins)
                                else:
                                        print("couldnt find well")
# nextLevelInsertionFinder(wellPairs_2, vectors)

distDF = pd.DataFrame(columns=[x for x in wells], index=[x for x in wells], dtype='float64')


for ins in vectors["pool"][0]:
        for well in vectors["wells"]:
                if ins in vectors["wells"][well][0]:
                        vectors["wells"][well][1].append(1)
                else:
                        vectors["wells"][well][1].append(0)

for well in vectors["wells"]:
        print(f'{well} length {len(vectors["wells"][well][0])}')

# for well in vectors["wells"]:
        # print(f'{well} length {len(vectors["wells"][well][1])}')


wellsAndDistances = {}
for x,y in combinations(wells, 2):
        d = jaccard_calc(vectors["wells"][x][1],vectors["wells"][y][1])
        distDF.at[x, y] = d #round(d,1)
        distDF.at[y, x] = d #round(d,1)
        distDF.at[y, y] = 1
        distDF.at[x, x] = 1
        wellsAndDistances[x+'-'+y] = d

orderedPairs = sorted(wellsAndDistances.items(), key=operator.itemgetter(1), reverse=True)
seenWells = []
final = []
stderror = {}

for wells,dist in orderedPairs:
                well1,well2 = wells.split('-')
                if well1 not in seenWells and well2 not in seenWells:
                        final.append(wells) # Wells is the string of both wells
                        seenWells.append(well1)
                        seenWells.append(well2)
                        col = [x for x in distDF.loc[well1] if x > 0]
                        row = [y for y in distDF.loc[well2] if y > 0]
                        row_col = []
                        row_col.extend(row+col)
                        # row_col.remove(dist)
                        if len(col) > 1 and len(row) > 1:
                                std = np.std(row_col)
                                mean = np.mean(row_col)
                                error = (dist-mean)/std
                                stderror[wells] = error
                        else:
                                stderror[wells] = 0

distDF.index=(['2-1-1','2-2-2','3-1-2','1-1-2','4-1-1','4-2-1','1-2-1','4-1-2','1-1-1','2-1-2','2-2-1','3-2-1','4-2-2','3-2-2','3-1-1','1-2-2'])
print(distDF)
print("**********Lowest Level***************")
totalStd = 0
for winnerWells in final:
        print(f"{winnerWells} with a standard err of {stderror[winnerWells]}")
        totalStd += stderror[winnerWells]
print(f"Average Standard Err: {round(totalStd / (len(final)-1),2)}")
print(f"Final confidence of {round(norm.cdf(totalStd / len(final)) * 100,2)}%")
# if SYSTEM["SHOW_DENDROGRAM"]:
# distDF = distDF.replace(np.nan,1)
        # print(z)
        # print(dn)
        # plt.savefig("static/results.jpg")
        # return (returnString,distDF)
distDF.to_csv(f'jaccard_darkgreenLT_C{str(COUNT_CUTOFF)}_L{str(LENGTH_CUTOFF[0])}-{str(LENGTH_CUTOFF[1])}_Recovery_{str(int(RECOVERY_EFFICIENCY*100))}.csv')
z = hierarchy.linkage(distDF, 'average') ##there are a few clustering choices here. for UPGMA, a standard algorithm, use 'average' instead of 'ward'
# plt.figure(figsize=(14,6),dpi=100)
hierarchy.set_link_color_palette(['k'])
dn = hierarchy.dendrogram(z, labels=distDF.index, above_threshold_color='#bbbbbb', orientation='left')

plt.show()
