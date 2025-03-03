from tinyec.ec import Point

def multiplyNum(privateKey):
    """
    Simulates an elliptic curve point multiplication.
    
    Args:
        privateKey (int): The private key value to be used for generating a public key.
    
    Returns:
        Point: An elliptic curve point representing the generated public key.
    """
    # Define the curve parameters for secp256k1
    from tinyec.ec import SubGroup, Curve
    
    p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
    n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    a = 0x0
    b = 0x7
    g = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 
         0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
    
    subgroup = SubGroup(p, g, n, 1)
    curve = Curve(a, b, subgroup, "secp256k1")
    
    # Multiply private key by generator point
    public_key = privateKey * curve.g
    return public_key
