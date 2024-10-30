# Project Exodus - Advanced Forex Trading Algorithm (PAfTA) Backend Engine

## Overview

Project Exodus is a sophisticated backend engine for an advanced forex trading algorithm. It leverages real-time market data, historical analysis, and machine learning techniques to make informed trading decisions in the foreign exchange market. The project also includes a web interface for user interaction and management.

## Features

- Real-time forex market data integration
- Advanced algorithmic trading strategies
- Machine learning models for market prediction
- Risk management and position sizing
- Backtesting capabilities
- Performance analytics and reporting
- RESTful API for integration with front-end applications
- Scalable architecture for high-frequency trading
- User authentication and account management
- Web interface for user interaction

## Tech Stack

- Python 3.9+
- MongoDB for data storage
- Redis for caching and real-time data
- MetaTrader5 for forex data and trading
- Flask for RESTful API and web server
- Pandas and NumPy for data manipulation
- JWT for authentication
- Bootstrap for frontend styling

## Prerequisites

- Python 3.9+
- MongoDB
- Redis
- MetaTrader5
- Access to a forex data feed (e.g., OANDA, FXCM, MetaTrader)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/godwins3/PAfTA.git
   cd PAfTA
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your MongoDB and Redis instances and update the connection strings in `config/config.py`.

5. Configure your forex data feed API keys and other settings in `config/config.py`.

## Usage

1. Start the main engine and web server:

   ```bash
   python server.py
   ```

2. Access the web interface at `http://localhost:8000`.

3. Use the API endpoints for programmatic access. Refer to the API documentation for available endpoints and their usage.

## Configuration

- Adjust trading parameters in `config/config.py`
- Modify risk management settings in `exodus/engine.py`
- Fine-tune machine learning models in the `ml_models` directory (if applicable)

## Key Components

- `exodus/engine.py`: Main trading engine
- `users/auth/`: User authentication and management
- `notification_service/`: Email and SMS notification services
- `location_service/`: Geolocation services
- `middleware/service.py`: API middleware for authentication and logging
- `server.py`: Flask-based web server and API

## Security

- JWT-based authentication for API access
- Secure password hashing using bcrypt
- HTTPS recommended for production deployment
- Regular security audits and dependency updates

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## Disclaimer

This software is for educational purposes only. Trading forex carries a high level of risk and may not be suitable for all investors. Please ensure you fully understand the risks involved before using this system for live trading.

## License

[MIT]
