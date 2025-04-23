# 🍽️ **Restaurant System – ER Diagram Design (Conceptual)**

## 🧾 `MenuItem`

- `id` (PK)
- `name`
- `description`
- `price`
- `category` (FK → `MenuCategory`)
- `is_available`

## 📂 `MenuCategory`

- `id` (PK)
- `name`

## 🪑 `Table`

- `id` (PK)
- `table_number`
- `seats`
- `status` (`available`, `occupied`, `reserved`)

## 🛒 `Order`

- `id` (PK)
- `table` (FK → `Table`)
- `created_at`
- `updated_at`
- `status` (`pending`, `in_progress`, `served`, `paid`, `cancelled`)
- `total` (calculated)

## 🍽️ `OrderItem`

- `id` (PK)
- `order` (FK → `Order`)
- `menu_item` (FK → `MenuItem`)
- `quantity`
- `unit_price`
- `note`

## 💳 `Sale`

- `id` (PK)
- `order` (FK → `Order`)
- `payment_method` (`cash`, `card`, `pix`)
- `amount`
- `payment_time`

## 💰 `Expense`

- `id` (PK)
- `description`
- `amount`
- `category` (`inventory`, `salary`, `maintenance`, `other`)
- `date`

## 📊 `Report`

(Not a model — but views/logic to summarize: total sales, expenses, best sellers, etc.)

## 👤 (Optional) `User`

- Extend later with roles (admin, waiter, etc.) if needed

## 🔗 Relationships

- One `MenuCategory` → many `MenuItems`
- One `Table` → many `Orders`
- One `Order` → many `OrderItems`
- One `Order` → one `Sale`
- Expenses are standalone, for accounting only
