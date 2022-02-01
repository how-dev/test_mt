# Howard's Technical Test

> Context 1:
> 
> __Me__ as MaisTODOS client
> 
> __I want__ to be able to create cashback for my customers
> 
> __If__ I have permissions to do so.

> Context 2:
> 
> __Me__ as an employee of MaisTODOS
> 
> __I want__ to manage all generate cashbacks
> 
> __If__ I have permissions to do so.
 
> !Rules:
> 
> If the total field is lower than 50, the cashback is 0
> 
> If the total field is between 50 and 99, the cashback is 5%
> 
> If the total field is between 100 and 200, the cashback is 10%
> 
> If the total field is greater than 200, the cashback is 15%
> 
> Cashback will __never__ exceed 150

## Running the project locally with Docker

1. Create a volume called "persist_db"
2. Create the .env file in `core_api` module according to `example.env` file
3. Run docker-compose up --build
4. Access the Docker's machine in another terminal with:

```commandline
docker exec -it test_mt_api_1 /bin/bash
```
or (to zsh system):

```commandline
docker exec -it test_mt_api_1 /bin/sh
```
5. Run this commands in Docker's machine:

```commandline
python manage.py makemigrations
python manage.py migrate
python manage.py start
```

> The last command `python manage.py start` creates 3 users to manually test the API:

```json
{
  "email": "test1@mail.com",
  "password": "test"
}
```

```json
{
  "email": "test2@mail.com",
  "password": "test"
}
```

```json
{
  "email": "test3@mail.com",
  "password": "test"
}
```

> The first user has the user_type field "Interno MaisTODOS" and his token has more permissions than the others. He can use the complete CRUD of the endpoint `api/v1/cashback/`

> The second user has the user_type field "Empresa X" and his token is only allowed to create a cashback. 

> The third user has the user_type field "Empresa Y" and their token is not allowed to create a cashback. This case simulates a customer where we at MaisTODOS do not offer the possibility of cashback, but we may include this possibility in the future. It also demonstrates that we can disable some customers from generating cashback.

## Endpoints

`base_url` = http://localhost:8000/api/v1/

### Login

`endpoint`: login/

`method`: POST

`body`:
```json
{
  "email": "example@mail.com",
  "password": "example"
}
```

`return's example`:
```json
{
  "status": 200,
  "result": {
    "id": 1,
    "last_login": "2022-02-01T18:02:20.604246-03:00",
    "email": "example@mail.com",
    "name": "Example",
    "document": "00000000000",
    "user_type": "Interno MaisTODOS",
    "token": "72ddd93c0e975c3e7a9df18160585ca947f43481"
  }
}
```

> This token reset after 1 hour on you login.

### Cashback

`endpoint`: cashback/

`method`: GET

`body`: No body

`header`: Authorization = Bearer < token >

`user_type`: Interno MaisTODOS

`return's example`:
```json
[
  {
    "sold_at": "2022-01-02T00:00:00-03:00",
    "customer": {
      "document": "00000000000",
      "name": "Example Example"
    },
    "total": "2000.00",
    "products": [
      {
        "type": "C",
        "value": "10.00",
        "qty": 100
      },
      {
        "type": "A",
        "value": "10.00",
        "qty": 100
      }
    ]
  },
  {
    "sold_at": "2022-01-02T00:00:00-03:00",
    "customer": {
      "document": "00000000000",
      "name": "Example Example"
    },
    "total": "50.00",
    "products": [
      {
        "type": "C",
        "value": "10.00",
        "qty": 5
      }
    ]
  },
  {
    "sold_at": "2022-01-02T00:00:00-03:00",
    "customer": {
      "document": "00000000000",
      "name": "Example Example"
    },
    "total": "1000.00",
    "products": [
      {
        "type": "C",
        "value": "10.00",
        "qty": 100
      }
    ]
  }
]
```

`endpoint`: cashback/< int:cashback_id >/

`method`: GET

`body`: No body

`header`: Authorization = Bearer < token >

`user_type`: Interno MaisTODOS

`return's example`:
```json
{
  "sold_at": "2022-01-02T00:00:00-03:00",
  "customer": {
    "document": "00000000000",
    "name": "Example Example"
  },
  "total": "2000.00",
  "products": [
    {
      "type": "C",
      "value": "10.00",
      "qty": 100
    },
    {
      "type": "A",
      "value": "10.00",
      "qty": 100
    }
  ]
}
```

`endpoint`: cashback/< int:cashback_id >/

`method`: PATCH

`body`: 
```json
{
  "sold_at": "2020-01-02T00:00:00-03:00"
}
```

`header`: Authorization = Bearer < token >

`user_type`: Interno MaisTODOS

`return's example`:
```json
{
  "sold_at": "2020-01-02T00:00:00-03:00",
  "customer": {
    "document": "00000000000",
    "name": "Example Example"
  },
  "total": "2000.00",
  "products": [
    {
      "type": "C",
      "value": "10.00",
      "qty": 100
    },
    {
      "type": "A",
      "value": "10.00",
      "qty": 100
    }
  ]
}
```
`endpoint`: cashback/< int:cashback_id >/

`method`: PUT

`body`: 
```json
{
  "sold_at": "2020-01-02T00:00:00-03:00",
  "customer": {
    "document": "00000000000",
    "name": "Example Example"
  },
  "total": "2000.00",
  "products": [
    {
      "type": "C",
      "value": "10.00",
      "qty": 100
    },
    {
      "type": "A",
      "value": "10.00",
      "qty": 100
    }
  ]
}
```

`header`: Authorization = Bearer < token >

`user_type`: Interno MaisTODOS

`return's example`:
```json
{
  "sold_at": "2020-01-02T00:00:00-03:00",
  "customer": {
    "document": "00000000000",
    "name": "Example Example"
  },
  "total": "2000.00",
  "products": [
    {
      "type": "C",
      "value": "10.00",
      "qty": 100
    },
    {
      "type": "A",
      "value": "10.00",
      "qty": 100
    }
  ]
}
```

`endpoint`: cashback/< int:cashback_id >/

`method`: DELETE

`body`: No body

`header`: Authorization = Bearer < token >

`user_type`: Interno MaisTODOS

`return's example`: 
```json
No content
```

`endpoint`: cashback/

`method`: POST

`body`:
```json
{
  "sold_at": "2020-01-02T00:00:00-03:00",
  "customer": {
    "document": "00000000000",
    "name": "Example Example"
  },
  "total": "2000.00",
  "products": [
    {
      "type": "C",
      "value": "10.00",
      "qty": 100
    },
    {
      "type": "A",
      "value": "10.00",
      "qty": 100
    }
  ]
}
```

`header`: Authorization = Bearer < token >

`user_type`: Interno MaisTODOS, Empresa X or Empresa Z

`return's example`: 

```json
{
  "createdAt": "2022-02-01T17:05:16.854Z",
  "message": "Cashback criado com sucesso!",
  "id": "01",
  "document": "00000000000",
  "cashback": 150
}
```

> !Remember:
> 
> If the total field is lower than 50, the cashback is 0
> 
> If the total field is between 50 and 99, the cashback is 5%
> 
> If the total field is between 100 and 200, the cashback is 10%
> 
> If the total field is greater than 200, the cashback is 15%
> 
> Cashback will __never__ exceed 150
