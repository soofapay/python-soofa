# python soofa

This package is aimed at simplifying the process of integrating
soofapay payment solution to your python systems. You can check our
[website] for more

#### Installation
```sh
 $ pip install soofa
 ```

#### Usage

##### 1. Checking for a transaction
```python
from soofa import Soofa, Transaction

soofa = Soofa("you_soofa_till_number", "your_client_secret_here")
exists = soofa.find("tranaction_id_here")
if exists:
    transaction: Transaction = soofa.get_transaction()
    print(transaction.tid)
    print(transaction.sender)
    print(transaction.gross_amount)
else:
    print("No such transaction")
```
The expected response for transaction check is  `Transaction`
object with various keys and methods

There is an additional method for getting the entire json object.

> transaction.json()

```JSON
{
    "status": "SUCCESSFUL",
    "sender_currency": "KES",
    "receiver_currency": "KES",
    "tid": "QTMB3",
    "reference": "T5002",
    "receipt_no": "NFQ6U45W28",
    "timestamp": 1561499777.715254,
    "gross_amount": 5,
    "net_amount": 4.8605,
    "transacted_via": "mpesa",
    "is_money_in": true,
    "sender": "+254721732519",
    "receiver": "Dev Market"
}
```

The table below describes all the attributes of the transaction object.


| Key | Description |
| ------ | ------ |
| status | The state of the transaction, either `SUCCESSFUL` or `PENDING` |
| sender_currency | The currency of the person who performed the transaction  |
| receiver_currency | The currency of the business, if the transaction was Money in for the business |
| reference | The transaction reference passed when making a transaction |
| timestamp | Unix timestamp for the transaction |
| gross_amount | The amount of the transaction |
| net_amount | The amount received after deducting soofa |
| transacted_via | The service provider which facilitated the transaction eg. mpesa, visa, airtelmoney, mastercard, tkash ... |
| is_money_in | A boolean indicating if the money was to the business or out of the bsiness |
| sender | The performer of transaction |
| receiver | The receiver of the transaction which is the business if the transaction was inbound |


##### 2. Checking your soofa business account balance
```python
from soofa import Soofa

soofa = Soofa("you_soofa_till_number", "your_client_secret_here")
balance = soofa.get_balance()
print(balance)
```

The expected response for checking balance is a JSON with three fields:

[website]: <https://www.soofapay.com>


```JSON
{
    "balance": "1587.49",
    "currency": "KES",
    "timestamp": 1561820831.623298
}