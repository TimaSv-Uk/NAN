# **DONE**:
- refactor encode,decode algorithsms **to class based** approach 
- refactor **encode_decode.py** so it fits class based algorithsms
- refactor **tests** so it fits class based algorithsms
- redo **finite_field precalc** Fn with no 0, exclude 0
    - HINT: fiead of 255 only odd numbers,z2^6 -> z2^7

    - PROBLEM: I can not map 254 numbers to 255, if i remove zero from the table and then try to encode and decode without zero condition, i figure i wont be able to decode enything 
    (Table would only have indices from 0 to 254. If  data contains the byte 255, the code will try to look up row or column 255, crash, and throw an "index out of bounds" error.)
- make encoding classes : - to +, or - to *, group of 255 with no 0
    - encode_decode.py modification
    - test them


# **TODO**:
- refactor remove repetion of encode_decode encode_algo,decode_algo with Genrators, Registry or other pattern

---------
- d_mod_range: precompute so there is no 0 (for F8_MULT_BASED class)

