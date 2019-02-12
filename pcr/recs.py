import numpy as np
from scipy.optimize import nnls
import csv

# parse courses file
course_list = [i.strip().split("\t\t") for i in open('./neo4jCourses copy.csv').readlines()]
course_list = course_list[1:]

course_map = {}
inverse_course_map = {}
course_rating_info = {}

# create maps of course names to ids and vice versa
count = 0
for i in course_list:
    for j in i:
        arr = j.split(',')
        course_map[count] = arr[0]
        inverse_course_map[arr[0]] = count
        course_rating_info[count] = [arr[6],arr[7],arr[8],arr[9],arr[10],arr[11],arr[12],arr[13]]
    count += 1

courseQualRating = {}
profQualRating = {}
diffRating = {}
amtLearnedRating = {}
workReqRating = {}
recToMaj = {}
recToNonMaj = {}
master = [courseQualRating, profQualRating, diffRating, amtLearnedRating, workReqRating, recToMaj, recToNonMaj]

#create rating distributiions by course by category
a = np.array([[1,2,3,4,5], [1,1,1,1,1]])
for item in course_rating_info:
    info = course_rating_info[item]
    if float(info[7]) > 0:
        for i in range(7):
            if float(info[i]) > 0:
                b = np.array([float(info[i])*float(info[7]),float(info[7])])
                pref = np.linalg.lstsq(a, b)
                l = []
                clear = True
                for j in pref[0]:
                    if j < 0:
                        clear = False
                        break
                if clear:
                    for k in pref[0]:
                        l.append(round(k))
                else:
                    sec = nnls(a, b)
                    for k in sec[0]:
                        l.append(round(k))
                master[i][item] = l
            else:
                master[i][item] = [0,0,0,0,0]

filenames = ['courseQualRating', 'profQualRating', 'diffRating', 'amtLearnedRating', 'workReqRating', 'recToMaj', 'recToNonMaj']
ind = 0
stud = 0
#write ratings by student and course
for map in master:
    with open(filenames[ind] + '.csv', 'w', newline='') as csvfile:
        wrtr = csv.writer(csvfile, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for key in map:
            li = map[key]
            for num in li:
                for k in range(int(num)):
                    wrtr.writerow([stud, key, li.index(num) + 1])
                    stud += 1
    ind += 1
