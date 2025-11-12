# Code that triggers actual BLOCKER issues in SonarQube

# Blocker: Division by zero
def divide_by_zero():
    x = 1 / 0
    return x

# Blocker: Infinite recursion
def infinite_loop():
    return infinite_loop()

# Blocker: Unreachable code after return
def unreachable():
    return True
    print("This will never execute")
    x = 5

# Blocker: Using exit() in production code
import sys
def bad_exit():
    sys.exit(1)

# Blocker: Empty except block that catches everything
try:
    risky_operation()
except:
    pass

# Blocker: Using assert in production
def use_assert(value):
    assert value > 0

# Blocker: Modifying list while iterating
def modify_during_iteration():
    items = [1, 2, 3, 4, 5]
    for item in items:
        items.remove(item)
