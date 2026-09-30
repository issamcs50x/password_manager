# Simple Encryption Simulation

A lightweight educational simulation demonstrating fundamental cryptographic concepts, including salt generation, key derivation, shift cipher encryption, and master password verification.

> ⚠️ **Disclaimer:** This project is strictly for learning and educational simulation purposes. It relies on simplified custom algorithms (such as Caesar cipher and modulo arithmetic) and must **not** be used in production for real-world security.

---

## 🚀 How It Works

The application follows a step-by-step cryptographic workflow to securely handle user input, derive keys, and verify credentials:

### 1. Master Password Prompt
Upon launching, the program prompts the user to enter a **Master Password**.

### 2. Random Salt Generation & Persistence
* Generates a random alphanumeric **Salt**.
* Saves the salt locally to a file so it can be reused in future sessions.
* **Purpose:** Ensures uniqueness. Even if multiple users choose identical passwords, adding a unique salt prevents identical key generation and pattern analysis attacks.

### 3. Password & Salt Combination
* Combines the Master Password with the stored Salt.
* Mitigates password collisions and precomputed dictionary attacks (e.g., rainbow tables).

### 4. Custom Key Derivation & Encryption Algorithm
* **Key Derivation Function (KDF):** Sums the ASCII (`ord()`) values of all characters in the combined string and computes the modulo 26 (`sum(ord(c)) % 26`) to derive a numerical key offset.
* **Caesar Cipher:** Implements a simple shift cipher mechanism that shifts character positions based on the derived numerical key.

### 5. Master Password Verification (`VALID_KEY`)
* Encrypts a predefined constant string (`VALID_KEY`) and stores the ciphertext locally.
* **Authentication Check:** On subsequent logins, the system attempts to decrypt the stored ciphertext using the derived key:
  * **Correct Password:** Yields the matching `VALID_KEY` string $\rightarrow$ Access Granted.
  * **Incorrect Password:** Produces an incorrect key, resulting in corrupted output instead of `VALID_KEY` $\rightarrow$ Access Denied.

---

## 💡 Cryptographic Concepts Simulated
* **Salting:** Preventing password reuse vulnerability and rainbow table lookups.
* **Key Derivation (KDF):** Mapping arbitrary length secrets to fixed key values.
* **Symmetric Encryption:** Demonstrating basic substitution/shift cipher mechanics.
* **Credential Verification:** Validating master secrets via encrypted reference tokens without storing plaintext passwords.