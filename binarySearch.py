# Binary search function to find the key in the sorted collision list
def binarySearch(collisionList, keyToFind):
    low, high = 0, len(collisionList) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if collisionList[mid][0] == keyToFind:  # If the x-coordinate matches
            return collisionList[mid]
        elif collisionList[mid][0] < keyToFind:
            low = mid + 1
        else:
            high = mid - 1
    
    return -1  # Return -1 if not found
