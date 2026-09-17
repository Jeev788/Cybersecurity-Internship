def caesar_cipher_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():  # Only shift letters
            shift_base = ord('A') if char.isupper() else ord('a')
            # Apply Caesar Cipher formula: (x + shift) mod 26
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char  # Non-alphabet characters remain unchanged
    return result
def caesar_cipher_decrypt(text, shift):
    # Decryption is just encryption with negative shift
    return caesar_cipher_encrypt(text, -shift)
if __name__ == "__main__":
    message = input("Enter your message: ")
    shift = int(input("Enter shift value (e.g., 3): "))
    encrypted = caesar_cipher_encrypt(message, shift)
    decrypted = caesar_cipher_decrypt(encrypted, shift)
    print("\n--- Results ---")
    print(f"Original Message : {message}")
    print(f"Encrypted Message: {encrypted}")
    print(f"Decrypted Message: {decrypted}")