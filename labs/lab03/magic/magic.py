# check whether duplicates exist in matrix
def duplicates(square):
    new_list = []
    size = len(square)
    # Make 2d array (sqaure)
    for x in range(size):
        for y in range(size):
            newItem = int(square[x][y])
            new_list.append(newItem)
    # A set has no duplicates so duplicates are removed
    if len(new_list) != len(set(new_list)):
        return True
    
    return False

def is_magic(square):
    
    # first diagonal sum
    sum = 0 
    size = len(square)
    for i in range(0, size): 
        sum += square[i][i]
    
    # second diagonal sum
    sum2 = 0
    for i in range(0, size): 
        sum2 += square[i][size-i-1] 
    
    # if the sums differ not a magic square
    if (sum != sum2): 
        return False
    
    # sum of rows   
    for x in range(0, size) : 
        row = 0;      
        for y in range(0, size) : 
            row += square[x][y] 
      
        # check if every row sum is equal to the sum of diagonal 
        if (row != sum) : 
            return False
            
    # sum of cols 
    for x in range(0, size): 
        col = 0
        for y in range(0, size) : 
            col += square[y][x] 
  
        # check if every col sum is equal to the sum of diagonal 
        if (sum != col) : 
            return False
  
    return True     

# check whether there is a missing number
def is_matrix(square):
    size = len(square)
    for row in square:
        if len(row) != size:
            return False
            
    return True

# return the correct phrase
def magic(square):
    if is_matrix(square) == False:
        result = 'Invalid data: missing or repeated number'
        return result
    if duplicates(square) == True:
        result = 'Invalid data: missing or repeated number'
        return result
    if is_magic(square) == False:
        result = 'Not a magic square'
        return result
    if is_magic(square) == True:
        result = 'Magic square'
        return result
