from funcs import sign
from controller import get_private_key

print("Your name: ", end='')
name = input()

print("Your password: ", end='')
password = input()

print("To Whom: ", end='')
recipient = input()

print("Amount: ", end='')
amount = input()

data = [
    str(name),
    str(amount),
    str(recipient),
]

data_string = ";".join(data)

# getting encrypted private key
pk = get_private_key(name)

try:
    signature = sign(data_string, pk, password)

    transaction = {
        'sender': name,
        'recipient': recipient,
        'amount': amount,
        'signature': signature.hex()
    }
except ValueError:
    print('The password is wrong!')
    transaction = None

print(transaction)
