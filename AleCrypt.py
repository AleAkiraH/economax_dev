def ale_encrypt(message, key):
    message = message.lower()
    encrypted_message = ""
    numLetter = 0
    for char in key:
        numLetter = numLetter + ord(char)
        if (str(numLetter)[-1] == '0'):
            numLetter = numLetter - 1
    for char in message:
        if char.isalpha():
            encrypted_char = chr((ord(char) - ord('a') + numLetter) % 26 + ord('a'))
        elif char.isdigit():
            encrypted_char = str((int(char) + numLetter) % 10)
        else:
            encrypted_char = char
        encrypted_message += encrypted_char
    return encrypted_message

def ale_decrypt(encrypted_message, key):
    decrypted_message = ""
    numLetter = 0
    for char in key:
        numLetter = numLetter + ord(char)
        if (str(numLetter)[-1] == '0'):
            numLetter = numLetter - 1
    for char in encrypted_message:
        if char.isalpha():
            decrypted_char = chr((ord(char) - numLetter - ord('a')) % 26 + ord('a'))
        elif char.isdigit():
            decrypted_char = str((int(char) - numLetter) % 10)
        else:
            decrypted_char = char
        decrypted_message += decrypted_char
    return decrypted_message

result = ale_encrypt('aleakirah','aleakirah')
print(result)
result2 = ale_decrypt(result,'aleakirah')
print(result2)