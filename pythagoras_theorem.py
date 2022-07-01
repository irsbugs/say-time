#!/usr/bin/env python3
#!
# pythagoras_theorem.py
import math

def calculate_hypotenuse(adjacent=3, opposite=4):
    # Use Pythagorean theorem to calculate hypotenuse.
    hypotenuse = math.sqrt(float(adjacent)**2 + float(opposite)**2)   
    return hypotenuse

if __name__ == "__main__":
    # For testing...
    #adjacent = input("Enter the length of the adjacent side: ")
    #opposite = input("Enter the length of the opposite side: ")
    #hypotenuse = calculate_hypotenuse(adjacent, opposite)
    hypotenuse = calculate_hypotenuse()
    print("Length of hypotenuse: {:g}". format(hypotenuse))
