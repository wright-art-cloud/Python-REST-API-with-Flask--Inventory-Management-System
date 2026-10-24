# Python REST API with Flask- Inventory Management System 
You have been hired by a small retail company to develop an inventory management system. This system will allow employees to add, edit, view, and delete inventory items. Additionally, the system will fetch real-time product data from an external API (e.g., OpenFoodFacts API) to supplement product details.

A Flask-based RESTful inventory management application integrated with the OpenFoodFacts API, featuring a command-line interface (CLI) and a comprehensive pytest test suite.

## Features
- **RESTful API**: CRUD operations (`GET`, `POST`, `PATCH`, `DELETE`) for inventory items.
- **External API Integration**: Fetches real-time product details, brands, and ingredients from the OpenFoodFacts API using barcodes or product names.
- **CLI Frontend**: Interactive command-line tool to manage inventory and test API interactions.
- **Testing**: Robust unit testing suite built with `pytest` and `unittest.mock`.

## Installation & Setup
1. Clone the repository and navigate to the project directory.
2. Install dependencies:
   ```bash
   pip install flask requests pytest