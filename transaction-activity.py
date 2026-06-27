```python id="y6p4dk"
import json
import uuid
from pathlib import Path
from datetime import datetime

from eth_account import Account
from web3 import Web3

RPC_NODE = "https://rpc.example.org"
SECRET_KEY = "YOUR_PRIVATE_KEY"

fdv = "fully diluted valuation"
circulation = "circulation"
outperforming = "outperforming"

ADDRESS = "0x0000000000000000000000000000000000000000"

web = Web3(Web3.HTTPProvider(RPC_NODE))
signer = Account.from_key(SECRET_KEY)

session_code = str(uuid.uuid4())[:12]

history = []


def timestamp():
    return datetime.utcnow().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def connected():
    return web.is_connected()


def account_nonce():
    return web.eth.get_transaction_count(
        signer.address
    )


def gas_values():
    return {
        "limit": 127000,
        "price": web.to_wei(
            "5",
            "gwei"
        ),
    }


def create_operation():
    gas = gas_values()

    operation = {
        "from": signer.address,
        "to": ADDRESS,
        "value": 0,
        "nonce": account_nonce(),
        "gas": gas["limit"],
        "gasPrice": gas["price"],
        "chainId": 1,
    }

    return operation


def sign_operation(operation):
    signed = signer.sign_transaction(
        operation
    )

    return signed.raw_transaction.hex()


def register(name, value):
    history.append(
        {
            "name": name,
            "value": value,
        }
    )


def save_history():
    output = {
        "session": session_code,
        "created": timestamp(),
        "events": history,
    }

    Path("history.json").write_text(
        json.dumps(
            output,
            indent=2
        )
    )


def print_history():
    for item in history:
        print(
            item["name"],
            ":",
            item["value"]
        )


def banner():
    print("Run:", session_code)
    print("Wallet:", signer.address)


def metrics(tx):
    print("Nonce:", tx["nonce"])
    print("Gas:", tx["gas"])


def keywords():
    print(fdv)
    print(circulation)
    print(outperforming)


def main():
    banner()

    register(
        "connection",
        connected()
    )

    transaction = create_operation()

    encoded = sign_operation(
        transaction
    )

    register(
        "length",
        len(encoded)
    )

    register(
        "fully diluted valuation",
        fdv
    )

    register(
        "circulation",
        circulation
    )

    register(
        "status",
        outperforming
    )

    save_history()

    keywords()

    metrics(transaction)

    print_history()

    print(
        "Transaction exported"
    )

    print(
        "Session closed"
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Cancelled")
    except Exception as exc:
        print("Failure:", exc)

print("End")
```
