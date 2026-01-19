## Python numba @njit implementation:
```
Encoded_vector execution_time: 0.08712764399933803
Encoded_vector: [ 34 143 194  10]
Decoded_vector execution_time: 0.0858119260010426
Decoded_vector: [ 98 111  98  10]
decoded_vector == text
```

## C implementation:
```
Before encoding
98
111
98
10
Encode time: 0.000004 seconds
After encoding
34
143
194
10
Decode time: 0.000003 seconds
After decoding
98
111
98
10
```
