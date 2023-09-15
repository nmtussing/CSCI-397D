"""
Assignment1.py
Author: Nicholas Tussing
A program that computes how much water would be contained in an elevation 
map based on a list of numbers. This solution utilizes memoization as an 
implementation of dynamic programming for an efficient solution
"""
length = len(heights)
def trap(heights):
    for i in range(0,length):
        if heights[i] == 0:

            
    


# Testing the ElevationMap class
if __name__ == "__main__":
    elevation_map = ElevationMap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    trapped_water = elevation_map.trap_water()
    print("Trapped Water:", trapped_water)


