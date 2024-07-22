str_dep_time = str(0.0)
str_dep_time = str_dep_time.strip()
str_dep_time = str_dep_time.replace(".0", "")

for i in range(4 - len(str_dep_time)):
    str_dep_time = "0" + str_dep_time

print(str_dep_time)