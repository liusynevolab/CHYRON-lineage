import pickle
import sys
import pprint
import re

# with open('green_LT_insDict.pkl', 'rb') as pkl:
# 	insDict = pickle.load(pkl)

# insDict = {
	# insertion:{		
# 		"counts": {
#			"well" : int()
#		}
# 	}
# }
## sysargv[1] = "exp"_well_data_file.txt
def writestuff(file, numA, numC, numG, numT,combinations,combcount):
	file.write('\n')
	file.write(f"A: {numA}")
	file.write('\n')
	file.write(f"C: {numC}")
	file.write('\n')
	file.write(f"G: {numG}")
	file.write('\n')
	file.write(f"T: {numT}")
	file.write('\n')
	i = 0
	while i < len(combinations):
		file.write(f"{combinations[i]}: {combcount[i]}")
		file.write('\n')
		i += 1

lengthcount = int(input("Enter the lengthcount:(input 16 for default) "))
if lengthcount> 16:
	lengthcount = 16
if lengthcount< 1:
	lengthcount = 1
insDict = {}
open('base_count_wells.txt','w').close()
with open(sys.argv[1]) as samples:
	for line in samples:
		counter = 0
		c = 0
		count = 0
		insCount = 0
		line = line.strip().split(' ')
		withlengths = line[0]
		well_regex = re.search('(?<=_).*?(?=[.])', line[0]) ## finds well number between '_' and '.' of file name
		well = f"well_{str(int(well_regex.group())+1)}" 
		print(f"Working on {well}")

		with open(withlengths) as lengths:
			numA,numC,numG,numT = 0,0,0,0
			combinations = ["AA","AC","AG","AT","CA","CC","CG","CT","GA","GC","GG","GT","TA","TC","TG","TT"]
			combcount = [0] * 16
			for line in lengths:
				insInfo = line.strip().split('\t')
				insertion = insInfo[1][:lengthcount] #slider1; the number after ":" should go from 1-15, the number after ":" indicates number of letters you want;
				insLen = insInfo[2]
				insCount = int(insInfo[3])
				insPerc = insInfo[4]
				numA += insertion.count('A')
				numC += insertion.count('C')
				numG += insertion.count('G')
				numT += insertion.count('T')
				i = 0
				while i < len(combcount):
					combcount[i] += insertion.count(combinations[i])
					i += 1
				#if insertion == 'ROOT':
					#print("found one")
				if insertion not in insDict: ## have we seen this insertion?
					insDict[insertion] = {"counts":{well:insCount}}
					c += 1
					continue
				if well in insDict[insertion]["counts"]: ## have we seen this insertion in this well?
					insDict[insertion]["counts"][well] += insCount
				else:
					insDict[insertion]["counts"][well] = insCount
			with open('base_count_wells.txt','a') as base_count:
					base_count.write(f"{well}")
					writestuff(base_count, numA, numC, numG, numT,combinations,combcount) #create a new text file and put stuff in it
					#continue
			# print(f"{c} unique insertions in {well}")
			# print(f"{insCount} non-unique in {well}")

countDict = {}

for key in insDict:
	for w in insDict[key]["counts"]:
		if not w in countDict:
			countDict[w] = 1
		else:
			countDict[w] += 1


pp = pprint.PrettyPrinter(indent=4)
pp.pprint(countDict)

with open('darkgreenLT_percinsDict.pkl', 'wb') as file:
	pickle.dump(insDict, file)
