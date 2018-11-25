# seldon-api
Client libraries for API provided by Seldon.

## Supported products
- Seldon Basis with `BasisClient`

## Usage example
### Prepare virtual environemnt
```bash
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install git+https://github.com/agladkov/seldon-api.git
```
### Run some python code
```python
>>> from seldon import BasisClient
>>> cl = BasisClient("_YOUR_BASIS_USER_", "_YOUR_BASIS_PASS_")
>>> orgs = cl.check_balance()
..(balance output)..
>>> org = cl.get_company_card(ogrn="_YOUR_OGRN_")
>>> print(org)
```

## Testing
You can run some tests with API key provided for testing purpose.
```bash
$ git clone git@github.com:agladkov/seldon-api.git
$ cd seldon-api
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install pytest pytest-flake8
$ export SELDON_USER="_YOUR_BASIS_USER_"
$ export SELDON_PASS="_YOUR_BASIS_PASS_"
$ pytest
```
