# Python Code Guidelines

## Python Version

* Python >= 3.11
* Use modern language features
* Avoid deprecated APIs

---

## Typing (Mandatory)

* All functions, methods, variables and returns must be typed
* Use strict typing
* `mypy --strict` required
* Avoid `Any`
* Avoid unnecessary `type: ignore`

### Preferred

```python
def create_user(name: str, age: int) -> User:
    ...
```

### Use modern typing

```python
list[str]
dict[str, int]
str | None
```

---

## Project Structure

```text
project/
├── app/
├── tests/
├── scripts/
├── pyproject.toml
└── README.md
```

---

## Naming

| Element         | Convention |
| --------------- | ---------- |
| Classes         | PascalCase |
| Functions       | snake_case |
| Variables       | snake_case |
| Constants       | UPPER_CASE |
| Private methods | _prefix    |

---

## Functions

* Single responsibility
* Small and focused
* Prefer early return
* Avoid deep nesting
* Avoid side effects

---

## Classes

* Single responsibility
* Prefer composition over inheritance
* Avoid god objects
* Use `dataclass(slots=True)` when applicable

---

## Imports

Order:

1. Standard library
2. Third-party
3. Internal imports

Rules:

* No `import *`
* Explicit imports only
* Avoid circular imports

---

## Error Handling

* Never use bare `except`
* Catch specific exceptions
* Never silently ignore errors

### Preferred

```python
try:
    process()
except ValueError as exc:
    logger.exception(exc)
```

---

## Logging

* Use `logging`
* No `print` in production

```python
import logging

logger = logging.getLogger(__name__)
```

---

## Configuration

* No hardcoded secrets
* Use environment variables
* Use `.env`

---

## Validation

* Validate all external input
* Prefer:

  * Pydantic
  * attrs
  * dataclasses + validators

---

## Database

* Use parameterized queries
* Never concatenate SQL manually
* Use migrations

---

## Testing

* Tests are written **after the application is working**, not during initial development.
* Test generation is **triggered explicitly by the user** — never generate tests automatically.
* Use `pytest`
* Minimum coverage: 80%

Structure:

```text
tests/
├── unit/
├── integration/
└── e2e/
```

---

## Code Quality Tools

Required:

* `black`
* `ruff`
* `mypy`
* `bandit`

---

## Documentation

* Self-explanatory code
* Minimal comments
* Public APIs require docstrings

---

## APIs

* Version APIs
* Explicit schemas/DTOs
* Do not expose internal entities

Example:

```text
/api/v1/users
```

---

## Async

* Use `async/await` only when necessary
* Avoid blocking operations in async code
* Avoid mixing sync and async unnecessarily

---

## Performance

* Avoid premature optimization
* Measure before optimizing
* Prefer simple comprehensions
* Avoid unnecessary loops

---

## Security

* Sanitize inputs
* Validate authentication and authorization
* Never log:

  * passwords
  * tokens
  * secrets
  * sensitive data

---

## Clean Code

Avoid:

* giant functions
* dead code
* duplication
* magic numbers
* excessive complexity
* redundant comments

---

## SOLID

Apply when appropriate:

* Single Responsibility
* Open/Closed
* Liskov Substitution
* Interface Segregation
* Dependency Inversion

---

## Dependencies

* Minimize external dependencies
* Pin versions
* Remove unused packages
* Prefer maintained libraries

---

## Commits

Use Conventional Commits:

```text
feat:
fix:
refactor:
test:
docs:
chore:
```

---

## Pull Requests

* Small
* Focused
* Reviewable
* Clear description

---

## Required Before Merge

```bash
ruff check .
black --check .
mypy .
pytest
```

No errors allowed.

---

## Principles

Priority order:

1. Clarity
2. Simplicity
3. Maintainability
4. Security
5. Testability
6. Consistency

---

## Zen of Python

```python
import this
```

Key principles:

* Explicit is better than implicit
* Simple is better than complex
* Readability counts
