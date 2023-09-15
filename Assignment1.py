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
        if heights[i] >=1 and index < length:
            for n in range(i,length):
                if heights[n]<= heights[i]:
                    trapped_water += heights[i]-heights[n]
                elif heights[n]> heights[i]: 
                    continue
    return trapped_water
            



# Testing with example elevation map
if __name__ == "__main__":
    elevationMapTest = [0,1,0,2,1,0,1,3,2,1,2,1]
    print(trap(elevationMapTest))


# Testing the ElevationMap class
if __name__ == "__main__":
    elevationMapTest = [0,1,0,2,1,0,1,3,2,1,2,1]
    print(trap(elevationMapTest))
    


