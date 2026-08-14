def calculate_avg(numbers=[]):
    total=0
    for n in numbers:
        total+=n
    return total/len(numbers)

print(calculate_avg)    