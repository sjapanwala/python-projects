import random
DAYS = 365
values = []
for day in range(DAYS):
    value = random.randint(0,3)
    values.append(value)
values_colorized = []
for i in values:
    if i == 0:
        values_colorized.append("\033[0m██\033[0m")
    elif i == 1:
        values_colorized.append("\033[32m██\033[0m")
    elif i == 2:
        values_colorized.append("\033[92m██\033[0m")
counter = 0
exec_counter = 0
week_count = 1
string = f" {week_count} "
for i in values_colorized:
    counter +=1
    exec_counter +=1
    if counter > 40:
        week_count +=1
        string += f"\n {week_count} "
        counter = 0
    else:
        string += i
print("\n   Jan    Feb    Mar    Apr    May    Jun    Jul    Aug    Sep    Oct    Nov    Dec")
print(f"{string}")
print(f"Commits; {exec_counter}")
