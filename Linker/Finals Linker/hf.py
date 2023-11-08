#hf.py

def int2bs(s, n, signed=0):
    """ Converts an integer string to a 2s complement binary string.

        Args:
            s: Integer string to convert to 2s complement binary.
            n: Length of outputted binary string.
            signed: Flag indicating whether the input is a signed integer or not (default: 0).
        
        Example Input: int2bs("4", 4)
        Example Output: "0100"

        Example Input: int2bs("-3", 16, 1)
        Example Output: "1111111111111101"
    """
    x = int(s)                              # Convert string to integer, store in x.
    if x >= 0:                              # If not negative, use python's binary converter and strip the "0b"
        ret = str(bin(x))[2:]
        return ("0"*(n-len(ret)) + ret)     # Pad with 0s to length.
    else:
        if signed:                          # If signed flag is set, convert to 2s complement integer
            ret = 2**n - abs(x)
            return bin(ret)[2:]             # Convert to binary using python's binary converter and strip the "0b"
        else:                               # If unsigned, raise ValueError
            raise ValueError("Unsigned integer must be positive.")
    
def bs2hex(v):
    """ Converts a binary string into hex.

        Args: v = Binary string to convert to hex

        Example Input: bs2hex("1010000010001111") 
        Example Output: "a08f" """
    return(hex(int(v,2))[2:])
