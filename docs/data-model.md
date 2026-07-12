
Customers
Contains master data for all customers.
primary key - customer_id

| Column            | Type    | Description                    |
| ----------------- | ------- | ------------------------------ |
| customer_id       | string  | Unique customer identifier     |
| first_name        | string  | Customer first name            |
| last_name         | string  | Customer last name             |
| email             | string  | Email address                  |
| country           | string  | Customer country               |
| registration_date | date    | Registration date              |
| marketing_opt_in  | boolean | Marketing consent              |
| loyalty_tier      | string  | Bronze, Silver, Gold, Platinum |

Orders
primary key - order_id
 | Column      | Type    |
| ----------- | ------- |
| order_id    | string  |
| customer_id | string  |
| product_id  | string  |
| order_date  | date    |
| unit_price | decimal
| quantity	  | integer
| discount	  | decimal

Products
Contains the product catalog.

Primary key: `product_id`

| Column        | Type    | Description                       |
|---------------|---------|-----------------------------------|
| product_id    | string  | Unique product identifier         |
| category      | string  | Product category                  |
| brand         | string  | Product brand                     |
| product_name  | string  | Product name                      |
| unit_price    | decimal | Product price                     |

Marketing campaigns
primary key: campaign_id
| Column      | Type    |
| ----------- | ------- |
| campaign_id | string  |
| channel     | string  |
| cost        | decimal |


Website events
primary key: event_id
| Column      | Type      |
| ----------- | --------- |
| event_id    | string    |
| customer_id | string    |
| page        | string    |
| timestamp   | timestamp |
