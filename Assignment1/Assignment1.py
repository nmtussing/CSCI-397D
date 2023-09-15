"""
Assignment1.py
Author: Nicholas Tussing
A program that computes how much water would be contained in an elevation 
map based on a list of numbers. This solution utilizes memoization as an 
implementation of dynamic programming for an efficient solution
"""

def trap(heights):
    trapped_water = 0
    index = -1
    length = len(heights)
    for i in range(0,length):
        index +=1
        if i == 0 and heights[i] == 0:
            continue
        if index == length-1:
            return trapped_water
        if heights[i] >=1:
            for n in range(i+1,length):
                if heights[n]< heights[i]:
                    trapped_water += heights[i]-heights[n]
                elif heights[n]> heights[i]: 
                    break
    return trapped_water


# Testing with example elevation map
if __name__ == "__main__":
    elevationMapTest = [0,1,0,2,1,0,1,3,2,1,2,1]
    print(trap(elevationMapTest))
    print(trap([0,1,0,2,0,1,0,2,0,2]))
    

    


