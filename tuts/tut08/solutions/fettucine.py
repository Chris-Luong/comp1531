import math

def generateNumber(i):
  return (i * (3 + i)) * (1 if i % 2 == 0 else -1)

def calc(m):
  nums = [generateNumber(i) for i in range(m)]
  retStr = f"""
Middle item: {nums[int(math.floor(m - 1) / 2)]}
Min item: {min(nums)}
Max item: {max(nums)}
Sum: {sum(nums)}"""
  return retStr

if __name__ == '__main__':
  print(calc(int(input())))