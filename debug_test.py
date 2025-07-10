#!/usr/bin/env python3
"""
Simple test script to verify VS Code debugger is working with Python 3.13
"""

def main():
    print("Testing VS Code debugger with Python 3.13")
    
    # Set a breakpoint on the next line
    x = 10
    y = 20
    result = x + y
    
    print(f"x = {x}")
    print(f"y = {y}")
    print(f"result = {result}")
    
    # Test with a loop
    for i in range(3):
        print(f"Loop iteration: {i}")
        value = i * 2
        print(f"Value: {value}")
    
    print("Debugger test completed!")

if __name__ == "__main__":
    main()
