from pybin import itoc

def netint(value):
    """Return a four byte string containing the integer in network byte order."""

    value = int(value)
    output = ''
    
    # store bytes in a stack
    stack = []
    for i in range(4):
        stack.append( value % 256 )
        value /= 256

    # pop bytes off of stack into output string
    for i in stack[:]:
        output += itoc(stack.pop())
    return output

