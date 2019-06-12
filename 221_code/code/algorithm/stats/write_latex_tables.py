fin = open("stats_results.csv", "r")
data = fin.read()
fin.close()

rookie_table = ""

veteran_table = ""

for line in data.split("\n")[1:-1]:
    results = line.split(", ")
    
    rookie_table += results[0] + " & " + results[1][:9] + " & " + results[2][:9] + " & " + results[3][:9] + " & " + results[4][:9] + "\n\\\\ \myline \n"
    
    veteran_table += results[0][:9] + " & " + results[5][:9] + " & " + results[6][:9] + " & " + results[7][:9] + " & " + results[8][:9] +  " & " + results[9][:9] + "\n\\\\ \myline \n"

#print rookie_table

#print ""
#print ""

#print veteran_table

counter = 0.
total = 0.
for line in data.split("\n")[1:-1]:
    results = line.split(", ")
    
    if float(results[5]) > float(results[8]):
        counter += 1.
    total += 1.

print counter, total
