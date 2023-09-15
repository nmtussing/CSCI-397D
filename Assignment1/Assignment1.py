"""
Assignment1.py
Author: Nicholas Tussing
A program that computes how much water would be contained in an elevation 
map based on a list of numbers. This solution utilizes memoization as an 
implementation of dynamic programming for an efficient solution
"""

def trap(map):
    trapped_water = 0
    index = -1
    length = len(map)
    #Creating arrays for the mamximum heights to the left and right position 
    leftMax = [0] * length  
    rightMax = [0] * length  
    
    #finding the left maximum 
    leftMax[0] = map[0]
    for i in range(1,length):
        leftMax[i] = max(leftMax[i-1],map[i])
    
    #finding the right maximum, iterating from the right side of the array
    rightMax [length-1] = map[length -1]
    for i in range(length -2, -1, -1):
        rightMax[i] = max(rightMax[i+1], map[i])
        
    #Calculating the water trapped based on the max heights for each position 
    for i in range(length):
        minMax = min(leftMax[i], rightMax[i])
        trapped_water += max(minMax - map[i], 0)
    return trapped_water


# Testing with example elevation map
if __name__ == "__main__":
    print("Testing the function")
    print(trap("Expected: 6 \n Result: " [0,1,0,2,1,0,1,3,2,1,2,1],))
    print(trap([0,1,0,2,0,1,0,2,0,2]))
    

    


