"""
Implementation of byte ring buffer

(c) Aleksei Tiulpin, 2016

Center for Machine Vision and Signal Analysis,
University of Oulu, Finland

"""

class RingBuffer:
    """
    Ring buffer of bytes. By the default has zeros everywhere

    """
    def __init__(self, l=10):
        self._l = l
        self._buf = bytearray([0]*l)
        self._pos = 0
        self._full = False
        
    def append(self, b):
        self._buf[self._pos] = b
        if not ((self._pos+1) % self._l) and not self._full:
            self._full = True
        self._pos = (self._pos+1) % self._l
    
    def _get_one(self, idx):
         if self._full:
            return self._buf[(self._pos + idx) % self._l]
         return self._buf[idx]
    
    def __getitem__(self, given):
        if isinstance(given, slice):
            tmp = []
            inds = range(self._l).__getitem__(given)
            for i in inds   :
                tmp.append(self._get_one(i))
            return bytearray(tmp)
            
        else:
            return self._get_one(given)
        
    def full(self):
        return self._full
        
    def __str__(self):
        return str(bytearray([self.__getitem__(i) for i in range(self._l)]))
        
        
        
        
if __name__ == "__main__":
    b = RingBuffer(10)
    print(b)
    for i in range(1, 27):
        b.append(i+40)
        print(b)
        
    print("===================")
    for i in range(10):
        print(b[i], b[i] == ord("?"))
        
    print("===================")
    print(b[-1])
    print(b[-2])
    print(b[:1])
    print(b[:3])
    print(b[:7])
   
   
    
    
    
    
    
