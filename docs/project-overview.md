# NovaRetail - Retail Marketing Intelligence Platform

## Project Objective

NovaRetail is an end-to-end Data Engineering portfolio project built with Databricks Free Edition.

The project demonstrates the design and implementation of a modern Lakehouse platform using the Medallion architecture (Bronze, Silver, Gold), with a focus on data ingestion, transformation, data quality, incremental processing, and analytical data modelling.

---

## Business Context

NovaRetail is a fictional international e-commerce company operating across multiple European countries.

The company wants to centralize customer, product, and order data in a scalable analytical platform to support reporting and customer and sales analytics.

The project simulates how operational retail data can be transformed into reliable, business-ready datasets using a modern Lakehouse architecture.

---

## Data Sources

The current implementation contains three core business domains:

- **Customers** — customer profile, country, marketing opt-in status, and loyalty tier
- **Products** — product information including product name, category, brand, and price
- **Orders** — transactional order data including customer, product, quantity, price, discount, and revenue

All source datasets are synthetically generated using Python. Configuration files are used to control the generation process, allowing reproducible datasets and incremental order batches to be created.

The generated CSV files simulate source-system extracts that are subsequently ingested into Databricks.

---

## Architecture

The solution follows the Medallion architecture and separates data processing into Bronze, Silver, and Gold layers.

### Source Data

Python-based data generators create synthetic customer, product, and order datasets. Order data can be generated in separate batches to simulate the incremental arrival of source files.

The generated source files are copied to a Unity Catalog Volume before ingestion.

### Bronze Layer

The Bronze layer contains ingested source data with minimal transformation.

Customers and products are loaded from their respective source files, while orders support incremental file-based ingestion.

Additional ingestion metadata is captured for orders:

- `_source_file`
- `_ingested_at`

A `processed_order_files` Delta table tracks which order files have already been processed.

New files are identified by comparing the files available in the Volume with the processing metadata. Only previously unprocessed files are selected for ingestion.

Delta Lake `MERGE` operations are used to make both order ingestion and file tracking idempotent. This allows pipeline runs to be safely retried without creating duplicate orders or duplicate file-processing records.

### Silver Layer

The Silver layer transforms the Bronze data into cleaned and validated datasets suitable for downstream use.

Processing includes:

- Data type validation and transformation
- Duplicate checks
- Order date validation
- Quantity, price, discount, and revenue validation
- Revenue consistency checks
- General data quality validation

The resulting Silver tables provide trusted customer, product, and order datasets for analytical processing.

### Gold Layer

The Gold layer contains business-ready analytical datasets derived from the Silver layer.

The current implementation includes:

- **`customer_product_sales_gold`** — combines orders with customer and product attributes to provide a detailed analytical sales dataset
- **`sales_by_category_year_gold`** — aggregates order count, quantity, and revenue by product category and year

These datasets provide a foundation for reporting, dashboards, and further business analysis.

---

## Incremental Processing and Idempotency

Incremental order ingestion is implemented explicitly to demonstrate the underlying principles of incremental data processing.

The process:

1. Lists available `orders_*.csv` files in the Unity Catalog Volume.
2. Reads previously processed file names from `processed_order_files`.
3. Uses a left anti join to identify new files.
4. Reads only the unprocessed order files.
5. Merges new orders into the Bronze Delta table using `order_id`.
6. Merges successfully processed file names into the processing metadata table.

Using Delta Lake `MERGE` operations makes the process idempotent at both the order and file-tracking level.

For example, if the orders are successfully written but updating the processing metadata fails, the file will be selected again during the next run. The order `MERGE` prevents the existing orders from being duplicated, after which the processing metadata can be updated successfully.

The initial implementation intentionally avoids Databricks Auto Loader to demonstrate these underlying concepts before introducing platform-specific ingestion automation.

---

## Data Quality

Data quality checks are performed as part of Silver processing.

Examples include:

- Duplicate order IDs
- Future order dates
- Non-positive quantities
- Negative unit prices
- Discounts outside the expected range
- Negative revenue
- Revenue inconsistencies based on quantity, unit price, and discount

These checks help ensure that only reliable data is propagated to the analytical layer.

---

## Repository Structure

```text
config/
    YAML configuration for synthetic data generation

data/
    generated/
        Generated CSV source files

docs/
    Project documentation and data model

images/
    Architecture diagrams and project screenshots

notebooks/
    bronze/
        Setup and Bronze ingestion
    silver/
        Data cleansing and validation
    gold/
        Analytical transformations

src/
    config/
        Configuration loading utilities
    generators/
        Synthetic data generators

tests/
    Development and testing utilities