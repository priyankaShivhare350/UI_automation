# UI Automation Testing Framework 

This project is a UI Automation Testing Framework built using **Python**, **Pytest**, and **Selenium WebDriver**. It supports multi-browser execution and generates beautiful HTML reports.

---
##  Test Cases Automated

Below is the summary of all the test cases covered in the framework, categorized by module:

###  Login Module
- **Verify successful login with valid credentials**
- **Verify error message for invalid credentials**
- **Verify login fails with blank email and password fields**

###  Register Module
- **Verify successful user registration with valid details**
- **Verify registration fails when required fields are blank**
- **Verify error messages for invalid inputs (e.g., weak password, invalid email)**

###  Cart Module
- **Verify product is added to cart successfully**
- **Verify product is removed from cart**
- **Verify cart reflects correct product details and quantity**
- **Verify cart total updates correctly when quantity is changed**

###  Billing Address Module
- **Add new billing address from profile page**
- **Edit existing billing address and verify updated details**
- **Verify mandatory field validations during billing address submission**

###  Shipping Address Module
- **Add new shipping address from profile page**
- **Edit existing shipping address and verify updated details**
- **Verify shipping address form shows correct state and country values**

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
