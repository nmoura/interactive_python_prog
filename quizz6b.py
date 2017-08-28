n = 1000
numbers = range(2,n)
results = []

while len(numbers) > 0:
    results.append(numbers[0])
    for i in numbers:
        if i % results[-1] == 0:
            numbers.remove(i)

print len(results)
