import random
import time
import csv
x = 0
y = random.randint(0,20)
while True:
    with open("temp.csv", "a")as output:
        data = [x,y]
        writer = csv.writer(output, delimiter=",", lineterminator='\n')
        writer.writerow(data)
        y = random.randint(0,20)
        x+=1
        time.sleep(1)
