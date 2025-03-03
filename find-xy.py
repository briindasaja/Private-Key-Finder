# Prompt user to choose between uncompressed or compressed public key
key_type = input("Enter 'u' for uncompressed public key or 'c' for compressed public key: ")

if key_type == 'u':
    # Prompt user to enter the uncompressed public key as a hexadecimal string
    public_key_hex = input("Enter the uncompressed public key as a hexadecimal string (starting with '04'): ")

    # Check if the entered public key starts with '04'
    if not public_key_hex.startswith('04'):
        print("Invalid public key! An uncompressed public key should start with '04'.")
    else:
        # Remove the '04' prefix which indicates an uncompressed public key
        public_key_bytes = bytes.fromhex(public_key_hex[2:])

        # The first 32 bytes represent the X coordinate
        x_coordinate = public_key_bytes[:32]
        # The next 32 bytes represent the Y coordinate
        y_coordinate = public_key_bytes[32:]

        # Convert the byte values to integers
        x_int = int.from_bytes(x_coordinate, byteorder='big')
        y_int = int.from_bytes(y_coordinate, byteorder='big')

        # Print the X and Y coordinates
        print("Uncompressed Public Key Coordinates:")
        print("X:", hex(x_int))
        print("Y:", hex(y_int))

elif key_type == 'c':
    # Prompt user to enter the compressed public key as a hexadecimal string
    public_key_hex = input("Enter the compressed public key as a hexadecimal string (starting with '02' or '03'): ")

    # Check if the entered public key starts with '02' or '03'
    if not (public_key_hex.startswith('02') or public_key_hex.startswith('03')):
        print("Invalid public key! A compressed public key should start with '02' or '03'.")
    else:
        # The compressed public key only includes the X coordinate
        public_key_bytes = bytes.fromhex(public_key_hex[2:])
        
        # The first 32 bytes represent the X coordinate
        x_coordinate = public_key_bytes[:32]

        # Convert the byte values to an integer
        x_int = int.from_bytes(x_coordinate, byteorder='big')

        # Print the X coordinate
        print("Compressed Public Key Coordinates:")
        print("X:", hex(x_int))

        # Determine the parity of Y (even for '02', odd for '03')
        parity = "even" if public_key_hex.startswith('02') else "odd"
        print("Y-coordinate parity:", parity)
else:
    print("Invalid option! Please enter 'u' for uncompressed or 'c' for compressed.")
