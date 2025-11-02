# Trading Tools Server

This project is a FastAPI application designed to read and analyze trade data exported from MetaTrader 4 (MT4). It provides a web interface for visualizing trade data over various time frames, including yearly, monthly, weekly, and daily.

## Features

- Support for reading MT4 export files in .htm format.
- Data analysis for the last 3 to 9 months.
- Visualization of trade data through interactive charts.
- HTML rendering for a user-friendly dashboard.

## Project Structure

```
trading-tools-server
├── src
│   ├── main.py                # Entry point for the FastAPI application
│   ├── api
│   │   ├── __init__.py        # API module initialization
│   │   ├── routes.py          # API route definitions
│   │   └── handlers.py        # Request handlers for the API
│   ├── services
│   │   ├── __init__.py        # Services module initialization
│   │   ├── mt4_parser.py      # Functions for parsing MT4 export files
│   │   ├── data_analyzer.py   # Functions for analyzing trade data
│   │   └── visualization.py    # Functions for visualizing trade data
│   ├── models
│   │   ├── __init__.py        # Models module initialization
│   │   └── trade.py           # Data model for trade attributes
│   ├── templates
│   │   ├── base.html          # Base HTML template
│   │   ├── dashboard.html      # Dashboard template for visualizations
│   │   ├── yearly.html        # Yearly data visualization template
│   │   ├── monthly.html       # Monthly data visualization template
│   │   ├── weekly.html        # Weekly data visualization template
│   │   └── daily.html         # Daily data visualization template
│   └── static
│       ├── css
│       │   └── style.css      # CSS styles for the application
│       └── js
│           └── charts.js      # JavaScript for rendering charts
├── tests
│   ├── __init__.py            # Tests module initialization
│   └── test_mt4_parser.py     # Unit tests for MT4 parser functions
├── data
│   └── exports                 # Directory for storing MT4 export files
├── pyproject.toml              # Project configuration for UV package manager
├── uv.lock                     # Dependency lock file for UV
└── README.md                   # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd trading-tools-server
   ```

2. Install dependencies using the UV package manager:
   ```
   uv install
   ```

## Usage

To run the FastAPI application, execute the following command:
```
uv run src/main.py
```

Visit `http://localhost:8000` in your web browser to access the dashboard and visualize your trade data.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.