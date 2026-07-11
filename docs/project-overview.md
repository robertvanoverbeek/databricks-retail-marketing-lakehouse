# NovaRetail - Retail Marketing Intelligence Platform

## Project Objective

Build an end-to-end Modern Data Platform using Databricks Free Edition to demonstrate modern Data Engineering best practices.

The platform simulates the data ecosystem of NovaRetail, a fictional international e-commerce company. Data from multiple business domains is ingested, transformed, and modeled using a Lakehouse architecture based on Delta Lake.

---

## Business Context

NovaRetail is a fictional international e-commerce company operating across multiple European countries.

The company aims to centralize data from various operational systems to improve reporting, marketing performance, and customer analytics.

Current business challenges include:

- Data scattered across multiple systems
- Limited visibility into marketing ROI
- No centralized customer analytics
- Manual reporting processes

---

## Data Sources

The platform processes data from multiple business domains:

- Customers
- Products
- Orders
- Website Events
- Marketing Campaigns

All datasets are synthetically generated using Python.

---

## Architecture

The solution follows the Medallion Architecture:

**Bronze**
- Raw data ingestion

**Silver**
- Cleansed, validated, and enriched data

**Gold**
- Business-ready analytical models and KPIs

---

## Key Business KPIs

- Revenue
- Marketing ROI
- Customer Lifetime Value (CLV)
- Conversion Rate
- Average Order Value (AOV)
- Repeat Purchase Rate

---

## Technology Stack

- Databricks Free Edition
- Delta Lake
- PySpark
- Spark SQL
- Python
- GitHub
- Visual Studio Code
- Faker

## Project Scope

This project demonstrates:

- End-to-end data ingestion
- Delta Lake and Medallion Architecture
- Data quality validation
- Incremental data processing
- PySpark transformations
- SQL analytics
- Git-based development workflow
- Documentation and software engineering best practices