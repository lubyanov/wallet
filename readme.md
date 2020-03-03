### Run project via `docker-compose`

1. Assure database name and user name in script `init.sql` is the same as `$POSTGRES_NAME` and `$POSTGRES_USER` in `.env.compose` [**IT'S THE SAME BY DEFAULT**]


2. Run ``docker-compose up --build``

3. Open ``http://localhost:8080/api/v1/customers/`` to create wallet 

4. Open ``http://localhost:8080/api/v1/transfer/`` to do a transfer with body:

```
{
    "customer_from": <customer_from_id>,
    "customer_to": <customer_from_id>, // optional
    "account_from": <account_from_uuid>,
    "account_to": <account_to_uuid>,
    "amount": <amount>
}
```

5. Open ``http://localhost:8080/api/v1/transactions/`` to see history transactions

```
// sorting
?ordering=-created_at&action=[INITIAL|TRANSFER]

// filtering
?action=[INITIAL|TRANSFER]
?account_from_uuid=<uuid>
?account_to_uuid=<uuid>
```


### Assumptions

1. Assumes currencies are equal (1 USD = 1 EUR = 1 CNY)

2. Assumes fee is calculates, but not stores in database