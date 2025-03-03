from tinyec.ec import SubGroup, Curve
from os import urandom
from tqdm import tqdm, trange
import time

# Function for multiplying a point by a scalar on the elliptic curve
def multiplyNum(scalar, point):
    """Multiply a point by a scalar on the elliptic curve."""
    return scalar * point

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

# Input public key coordinates
X = int(input("Please Enter Your Public Key X Coordinate In Hexadecimal Format: "), 16)
Y = int(input("Please Enter Your Public Key Y Coordinate In Hexadecimal Format: "), 16)

# secp256k1 curve parameters
name = 'secp256k1'
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
a = 0x0000000000000000000000000000000000000000000000000000000000000000
b = 0x0000000000000000000000000000000000000000000000000000000000000007
g = (X, Y)
h = 1

# Validate public key
if ((X * X * X) % p + 7) != (Y * Y) % p:
    print("The Public Key X and Y Coordinates You Entered Are NOT Valid...")
    print("NOTE: Do not include 02, 03, or 04 at the beginning of the X Coordinate.")
    print("Ensure you're using hexadecimal format.")
    exit()

# Define elliptic curve and subgroup
curve1 = Curve(a, b, SubGroup(p, g, n, h), name)
EnteredPublicKey = curve1.g * 1  # Identity point (0, 0) is not the public key

# Initialize lists for collision points
CollisionList = []
PosOneList = []

# Predefined values for scalar multiplication
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
half = 57896044618658097711785492504343953926418782139537452191302581570759080747169

# Get user input for collision list size
AA = int(input("Please Enter the Size of the Collision List you would like to Create (Best Performance around 10,000):"))
AAA = (AA * 2)
BB = AA

print("Creating Collision List...Please Wait...")
place = EnteredPublicKey * ((half ** AA) % N)
PosOneList.append(place.x)
PosOneList.append(-AA)
tuplePosOneList = tuple(PosOneList)
CollisionList.append(tuplePosOneList)
AA = -AA + 1

# Generate collision list
for iterationMultiples in trange(AAA, total=AAA, ascii=True, ncols=100, colour='#00ff00', unit='Keys Stored', desc='Keys Stored In Memory...'):
    PosTwoList = []
    iteratedMultiple = place + place
    PosTwoList.append(iteratedMultiple.x)
    PosTwoList.append(AA)
    tuplePosTwoList = tuple(PosTwoList)
    CollisionList.append(tuplePosTwoList)
    place = iteratedMultiple
    AA += 1

# Sorting the collision list
print("Sorting List...Please Wait...")
CollisionList.sort(key=lambda i: i[0])
tupleCollisionList = tuple(CollisionList)
print("List Sorted...Searching For Key")
print("Creating Easy Count List...Please Wait...")

# Start key finding process
keyFound = False
while not keyFound:
    t = time.process_time()
    privKey = int(urandom(32).hex(), 16) % N  # Generate random private key
    privateKey1 = (privKey * (half ** BB)) % N
    newKey = multiplyNum(privateKey1, curve1.g)  # Multiply scalar with curve generator

    # Search for matching keys in the collision list
    for hashIteration in trange(AAA, total=AAA, ascii=True, ncols=100, colour='#00ff00', unit='Comparisons', desc='Searching...'):
        keyToFind = int(newKey.x)
        result = binarySearch(tupleCollisionList, keyToFind)  # Use binary search to find a match
        if result != -1:
            if result[1] <= 0:
                RecFunct = ((privateKey1 * (2 ** hashIteration)) * (2 ** (abs(result[1])))) % N
            else:
                RecFunct = ((privateKey1 * (half ** hashIteration)) * (2 ** (abs(result[1])))) % N
            recoveredKey = multiplyNum(RecFunct, curve1.g)

            # Ensure the recovered Y-coordinate matches the entered public key
            if recoveredKey.y != EnteredPublicKey.y:
                RecFunct = N - RecFunct

            print("X-Coordinate Found of Collision Key Found:", result)
            print("Collision PrivateKey:", privateKey1)
            print("Here is the Private Key for the PublicKey that you Entered:", RecFunct)
            keyFound = True
            exit()
        else:
            newKey += newKey  # Double the key if not found

    # Performance and round time metrics
    elapsed_time = time.process_time() - t
    print("Average Random Key Strings Created Per Second:", (AAA // elapsed_time))
    print("Average Seconds per Round:", elapsed_time)
