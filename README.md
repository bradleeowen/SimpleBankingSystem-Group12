# Simple Banking System (Django REST Framework)

## Group Members
150140-Owen Kipkosgei
121238-Ogole Edgar
151751-Mary Ng'ang'a 
145768-Ogato Deborah Kerubo 
94944-Antony Wanderi
169648-Kamau Joseph Manene

---

## 1. Step-by-Step Project Implementation

### Step 1: Project Setup
- Created Django project `project_name` and app `banking`.
- Installed dependencies: `django`, `djangorestframework`, and `djangorestframework-authtoken`.
- Configured `INSTALLED_APPS` to include `rest_framework`, `rest_framework.authtoken`, and `banking`.

### Step 2: Models and Relationships
We designed **six models** representing the core entities of the banking system:
1. **Branch** – Represents a bank branch (fields: `name`, `location`).
2. **Customer** – Holds customer personal details (`first_name`, `last_name`, `email`, `phone`).
3. **Account** – Linked to a `Customer` and `Branch` via foreign keys. Tracks account number, type, and balance.
4. **Transaction** – Linked to an `Account`. Records type (`deposit`, `withdrawal`), amount, and timestamp.
5. **Loan** – Linked to a `Customer`. Stores loan type, amount, interest rate, and repayment period.
6. **Staff** – Linked to a `Branch`. Stores staff member details and role.

**Relationships:**
- **One-to-Many:**  
  - One `Branch` → Many `Accounts`  
  - One `Customer` → Many `Accounts`  
  - One `Account` → Many `Transactions`
- **One-to-One:**  
  - N/A (all customer and staff relations are many-to-one)
- **Foreign Keys** ensure relational integrity.

### Step 3: Serializers and Validation Rules
- Each model has a corresponding **ModelSerializer**.
- Validation rules include:
  - **Unique Email** for `Customer`.
  - **Non-negative balance** in `Account`.
  - **Positive transaction amounts** in `Transaction`.
  - **Loan amount > 0** and **interest rate between 0–100** in `Loan`.

### Step 4: Views/ViewSets
- **ModelViewSets** are used for CRUD operations.
- **Custom actions** for:
  - Deposit and withdraw in `TransactionViewSet` (updates account balance atomically).
- **Permissions**:
  - Authenticated users can access endpoints.
  - Staff-only access for certain administrative actions.

### Step 5: URL Patterns
- Used DRF `DefaultRouter` to auto-generate RESTful URLs:
  - `/api/branches/`
  - `/api/customers/`
  - `/api/accounts/`
  - `/api/transactions/`
  - `/api/loans/`
  - `/api/staff/`
- `/api-auth/login/` enabled for session authentication.