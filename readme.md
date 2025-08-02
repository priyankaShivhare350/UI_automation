# UI Automation Testing Framework 

This project is a UI Automation Testing Framework built using **Python**, **Pytest**, and **Selenium WebDriver**. It supports multi-browser execution and generates beautiful HTML reports.

---

## Getting Started

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

---

### 2. Run Tests

####  Run All Tests
```bash
pytest
```

####  Run with HTML Report
```bash
pytest --html=reports/report.html --self-contained-html -v
```

####  Run with Specific Browser
```bash
pytest --browser_name=firefox
```

####  Headless Mode
```bash
pytest --browser_name=chrome --headless
```

---

### 3. Run Tests by Marker

Use `-m` to run tests with specific markers:

- **Cart Tests**
  ```bash
  pytest -m cart
  ```

- **Address Tests**
  ```bash
  pytest -m address
  ```

- **Register Tests**
  ```bash
  pytest -m register
  ```

- **Login Tests**
  ```bash
  pytest -m login
  ```

To run multiple markers:
```bash
pytest -m "cart or login"
```

---

## Default Configurations

Defined in `pytest.ini`:

```ini
[pytest]
pythonpath = .
addopts = --html=reports/report.html --self-contained-html -v
markers =
    cart: mark test as related to cart functionality
    address: mark test as related to address functionality
    register: mark test as related to user registration
    login: mark test as related to login functionality
```

---

##  Author

**Priyanka Shivhare**  
 GitHub: [priyankaShivhare350](https://github.com/priyankaShivhare350)  
 Email: Priyanka35063@gmail.com
