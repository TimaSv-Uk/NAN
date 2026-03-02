
5. Implementation of the algorithms.

Algorithm 5. 1.
    We select K=Z_q, q=2^s, s ≥8. So Z*_q  of order 2^{s-1}consists on
odd residues. We take parameter k, k:>0 and  symbolic word w from the subsemigroup S(Z_q)
of kind w=(α_1, β_1. α_2, β_2, …, α_k, β_k) whee
 α_1ϵK. β_1ϵK*, α_{i+1}- α_iϵK* , β_{i+1}- β_i ϵK*  
We select intrger n to work with the space of plaintexts
K^n and linear transformations L_i  such that L_i()=x_1
+a_2(i)x_2 +a_3(i)x_3+… a_n(i)x_n, i=1,2 and
L_i(x_j)=x_j for j>1. where a_j(i) are elements of K*.
We  refer to the pair k, w as active password and
L_i are passive password data.

The degree of encryption transformation E=L_1FL_2 is 3.
For the computation of homomorphism \phi_n we select graph A(K).
Under condition that k≤[n/4] active  distinct passwords of kind
k, w produce different ciphertext from the selected password. The totality of active passwords with symbolic word of length k has
cardinality q(q/2)^{2k-1}.
If adversary has no access to unencrypted data he/she
has to conduct brut force search via the space of active
passwords.

In case of the possibility of  interceptions of pairs of kind (plaintext , corresponding ciphertext) adversary has to intercept O(n^3) such pairs and restore the encryption map E in time O(n^{10}).


```
    import numpy as np
    from numba import njit

    def encode_bites(
        bites: np.ndarray,
        char_ecncode_mod: int,
        d_mod: int,
        seed: int,
        noise_ratio: float = 0.00,
    ) -> np.ndarray:
        """
        High-level wrapper for the encryption process.
        Generates the dynamic password (random_d_mod_range) and applies
        the algebraic graph transformation.
        """
        # Pre-processing: Noise injection and initial vector transformation
        # (Corresponds to preliminary linear transformations L_i)
        bites = add_noise(bites, char_ecncode_mod, seed, noise_ratio)
        file_bites = change_first_symbol_based_on_random_vector(bites, seed)
        
        # Generate the symbolic word (sequence of active parameters)
        random_d_mod_range = randomize_d_mod(d_mod, seed)
        
        # Apply the core graph walk
        encoded_bites = encode_v5(file_bites, char_ecncode_mod, random_d_mod_range)
        return encoded_bites

    def decode_bites(
        bites: np.ndarray,
        char_ecncode_mod: int,
        d_mod: int,
        seed: int,
        noise_ratio: float = 0.00,
    ) -> np.ndarray:
        """
        High-level wrapper for the decryption process.
        Reverses the graph walk and removes pre-processing artifacts.
        """
        random_d_mod_range = randomize_d_mod(d_mod, seed)
        
        # Reverse the graph walk
        decoded_bites = decode_v5(bites, char_ecncode_mod, random_d_mod_range)
        
        # Inverse linear transformation and noise removal
        decoded_bites = reverse_change_first_symbol_based_on_random_vector(
            decoded_bites, seed
        )
        decoded_bites = remove_noise(decoded_bites, char_ecncode_mod, seed, noise_ratio)
        return decoded_bites

    @njit
    def randomize_d_mod(d_mod: int, seed: int) -> np.ndarray:
        range_d_mod = np.arange(d_mod, dtype=np.int64)

        if d_mod == 0:
            return range_d_mod

        index = seed % d_mod
        new_val = (seed * 1664525 + 1013904223) % d_mod  # LCG hash

        if new_val == index:
            new_val = (new_val + 1) % d_mod

        range_d_mod[index] = new_val
        return range_d_mod

    def encode_v5(
        chars: np.ndarray, char_encode_mod: int, d_mod_range: np.ndarray
    ) -> np.ndarray:
        """
        Iteratively applies the neighbor-finding map F according to the 
        sequence defined in d_mod_range.
        """
        current_state = chars.astype(np.uint8).copy()
        next_state = np.empty_like(current_state)

        for a in d_mod_range:
            find_neighbors_v5(current_state, next_state, a, char_encode_mod)
            # Swap buffers to move to the next node in the walk
            current_state, next_state = next_state, current_state

        return current_state

    def decode_v5(
        chars: np.ndarray, char_encode_mod: int, d_mod_range: np.ndarray
    ) -> np.ndarray:
        """
        Reverses the graph walk by applying the inverse map in reverse order 
        of the parameter sequence.
        """
        current_state = chars.astype(np.uint8).copy()
        next_state = np.empty_like(current_state)

        # Traverse the path backwards
        for i in range(len(d_mod_range) - 1, -1, -1):
            a = d_mod_range[i]
            reverse_find_neighbors_v5(current_state, next_state, a, char_encode_mod)
            current_state, next_state = next_state, current_state

        return current_state

    @njit
    def find_neighbors_v5(
        point_in: np.ndarray, point_out: np.ndarray, a: int, mod: int
    ) -> None:
        """
        Implements the algebraic relations of the graph edge.
        Maps input vector X to neighbor Y given parameter a.
        
        Equations:
        y_1 = x_1 + a
        y_i = x_i - y_1 * x_{i-1} (even i)
        y_i = x_i - x_1 * y_{i-1} (odd i)
        """
        n = len(point_in)
        point_out[0] = (point_in[0] + a) % mod
        x0 = point_in[0]

        for i in range(1, n):
            # Using implicit modulo 256 via uint8 overflow for efficiency
            if i % 2 == 0:
                point_out[i] = np.uint8(point_in[i] - point_out[0] * point_in[i - 1])
            else:
                point_out[i] = np.uint8(point_in[i] - x0 * point_out[i - 1])

    @njit
    def reverse_find_neighbors_v5(
        point_in: np.ndarray, point_out: np.ndarray, a: int, mod: int
    ) -> None:
        """
        Implements the inverse algebraic relations.
        Maps vector Y back to X given parameter a.
        
        Equations:
        x_1 = y_1 - a
        x_i = y_i + y_1 * x_{i-1} (even i)
        x_i = y_i + x_1 * y_{i-1} (odd i)
        """
        n = len(point_in)
        point_out[0] = (point_in[0] - a) % mod
        x0 = point_out[0] 
        y0 = point_in[0]  

        for i in range(1, n):
            if i % 2 == 0:
                point_out[i] = np.uint8(point_in[i] + y0 * point_out[i - 1])
            else:
                point_out[i] = np.uint8(point_in[i] + x0 * point_in[i - 1])
```
