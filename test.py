numberList = [(1, 2, 3),
              (4, 5, 6),
              (7, 8, 9)]
strList = ['one', 'two', 'three']

# No iterables are passed
result = zip()

# Converting itertor to list
resultList = list(result)
print(resultList)

# Two iterables are passed
result = zip(numberList, strList)

# Converting itertor to set
resultList = list(result)
print(resultList)

# print(sum(n for l, m, n in numberList))
