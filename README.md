# python-pco

Python wrapper for Planning Center Online API

## Installation

```bash
# Using uv (recommended)
uv add python-pco

# Using pip
pip install python-pco
```

## Quick Start

### OAuth 2.0 Authentication

```python
from pco import OAuth2Client, PCOClient

# Initialize OAuth client
oauth_client = OAuth2Client(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="http://localhost:8000/callback"
)

# Get authorization URL
auth_url = oauth_client.get_authorization_url()
print(f"Visit: {auth_url}")

# After user authorizes, exchange code for token
token = oauth_client.exchange_code_for_token(authorization_code)

# Create PCO client
client = PCOClient(oauth_client=oauth_client)

# Or use token directly
from pco import OAuth2Token
token = OAuth2Token(access_token="your_token")
client = PCOClient(token=token)
```

### Using the API

#### People Module

```python
from pco import PCOClient, OAuth2Token

client = PCOClient(token=OAuth2Token(access_token="your_token"))
people = client.people

# List all people
people_list = people.list_people()

# Get a specific person
person = people.get_person("person_id")

# Create a person
new_person = people.create_person({
    "data": {
        "type": "Person",
        "attributes": {
            "first_name": "John",
            "last_name": "Doe"
        }
    }
})

# Update a person
updated = people.update_person("person_id", {
    "data": {
        "attributes": {
            "first_name": "Jane"
        }
    }
})

# Delete a person
people.delete_person("person_id")

# Get households for a person
households = people.get_person_households("person_id")
```

#### Services Module

```python
# List service plans
plans = client.services.list_plans()

# Get a specific plan
plan = client.services.get_plan("plan_id")

# Get items for a plan
items = client.services.get_plan_items("plan_id")

# Get teams for a plan
teams = client.services.get_plan_teams("plan_id")
```

#### Check-Ins Module

```python
# List check-in events
events = client.checkins.list_events()

# Get a specific event
event = client.checkins.get_event("event_id")

# Get locations for an event
locations = client.checkins.get_event_locations("event_id")
```

#### Giving Module

```python
# List giving funds
funds = client.giving.list_funds()

# List donations
donations = client.giving.list_donations()

# Get donations for a batch
batch_donations = client.giving.get_batch_donations("batch_id")
```

#### Resources Module

```python
# List resource items
items = client.resources.list_items()

# Get checkouts for an item
checkouts = client.resources.get_item_checkouts("item_id")
```

## Error Handling

The library provides custom exceptions for different error scenarios:

```python
from pco import (
    PCOError,
    PCOAuthError,
    PCOAPIError,
    PCONotFoundError,
    PCORateLimitError,
    PCOValidationError
)

try:
    person = client.people.get_person("invalid_id")
except PCONotFoundError:
    print("Person not found")
except PCORateLimitError:
    print("Rate limit exceeded")
except PCOAPIError as e:
    print(f"API error: {e}")
```

## Context Manager Support

Both `PCOClient` and `OAuth2Client` support context managers:

```python
with OAuth2Client(client_id="id", client_secret="secret") as oauth:
    token = oauth.exchange_code_for_token(code)
    with PCOClient(oauth_client=oauth) as client:
        people = client.people.list_people()
```

## Query Parameters

All list methods support query parameters for filtering, pagination, and sorting:

```python
# Pagination
people = client.people.list_people({"per_page": 50, "offset": 0})

# Filtering
people = client.people.list_people({"where[name]": "John"})

# Sorting
people = client.people.list_people({"order": "name"})
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/python-pco.git
cd python-pco

# Install dependencies with uv
uv sync

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src/pco --cov-report=term-missing
```

### Code Quality

```bash
# Run Ruff linter
uv run ruff check .

# Format code
uv run ruff format .
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
