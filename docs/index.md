## __Introduction__

### _Terminology_

The term **Inkosi** could sounds a little bit weird, indeed, it is actually coming from the _Zulu_ vocabulary, and it means "King" or "Chief" in English.

### _Inspiration_
The choice was inspiered by [Kubernetes](https://kubernetes.io/), a container orchestration system (It does completely different things). I just wanted to create a platform based on multiservices in order to simplify, accelerate and streamline the Financial Institution daily activies.

### _Definition_
The project aims to offer an Algorithmic Trading Platform, the idea is not meant to develop a trading strategy but, to build a reliable, eﬃcient and maintainable solution to open and close positions accordingly to algorithmic or manual trading signals, backtest your algorithmic trading strategies, manage commissions for all you investors, infer on the markets, manage risk efficiently, ...
<br>
<br>
As shown below, the platform has been structured to serve institution which generally follow the presented pattern:

- __Investment Firm__
    - A ﬁnancial institution that manages and invests money on behalf of individuals or organisations, with the objective of generating ﬁnancial returns.
- __Funds__
    - All the money collected through an initial campaign of the Investment Firm are distributed and assigned to diﬀerent funds according to diﬀerent features such as:
        - __Liquidity__
        - __Asset__
        - __Investment Objectives__
        - ...
- __Portfolio Manager__ (Numerous and various assigned to different funds)
    - He is a ﬁnancial professional or an entity responsible for managing an investment portfolio on behalf of funds
    - For each funds are generally assigned a diﬀerent number of portfolio managers in accordance with their prior experiences, ﬁnancial knowledge, etc.
- __ATS__ (Algorithmic Trading Strategies)
    - A simple application able to send trading signals to the main platform accordingly to strategies based on an empirical approach, machine learning models, etc.

![Alt text](resources/images/Scenario_trasparency.svg "Scenario")

### _Definition_

It is a __OMS__ (Order Management System) written in _Python_ which interacts, through the MetaTrader5 library, with the MetaTrader5 Client. The project aims to offers a solid and reliable infrastructure able to quickly open and close trading positions.

## __Libraries__

Here you will find the list with all the libraries implemented on the platform with its explanation:

- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) - Version (2.0.21)
    - It has been used for interactions with the PostgreSQL database (going forward with the documentation, it is possible to analyze these aspects more thoroughly) 
- [Beartype](https://beartype.readthedocs.io/en/latest/) - Version 0.16.2
    - Beartype is an open-source pure-Python runtime type checker emphasizing efficiency, portability, and thrilling puns.
    - Used to check if some methods parameters have been correctly typed
- [FastAPI](https://fastapi.tiangolo.com/) - Version 0.103.2
    - FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
    - All the endpoints, both for Investors and Administrators, have been developed and organised through FastAPI
- [NumPy](https://numpy.org/doc/stable/) - Version 1.26.0
    - NumPy is the fundamental package for scientific computing in Python.
    - Most of the operation on backtesting are performed through NumPy (God saves Cython)
- [OmegaConf](https://omegaconf.readthedocs.io/en/2.3_branch/) - Version 2.3.0
    - OmegaConf is a YAML based hierarchical configuration system, with support for merging configurations from multiple sources providing a consistent API regardless of how the configuration was created.
    - All the settings are loaded through this library
- [Pandas](https://pandas.pydata.org/) - Version 2.1.2
    - Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language.
    - Used to work with Financial Data Frames
- [Pandas TA](https://github.com/twopirllc/pandas-ta) - Version 0.3.14b0
    - Pandas Technical Analysis (Pandas TA) is an easy to use library that leverages the Pandas package with more than 130 Indicators and Utility functions and more than 60 TA Lib Candlestick Patterns.
    - Used to compute different technical indicators on prices in order to provide backtesting tools
- [Psycopg](https://www.psycopg.org/docs/)
    - Psycopg is the most popular PostgreSQL database adapter for the Python programming language.
    - Auxiliar to SQLAlchemy
- [PyDantic](https://docs.pydantic.dev/latest/api/base_model/) - Version 2.4.2
    - Pydantic is the most widely used data validation library for Python.
    - Fast and extensible, Pydantic plays nicely with your linters/IDE/brain.
    - Written in Rust!
    - Used to validate specific settings coming from .env file (Auxiliar to PyDantic Settings, another library used)
- [PyMongo](https://pymongo.readthedocs.io/en/stable/) - Version 4.5.0
    - PyMongo is a Python distribution containing tools for working with MongoDB, and is the recommended way to work with MongoDB from Python.
    - Used to interact with the MongoDB Instance
    - Further information available in both the Databases and Code Analysis parts
- [Streamlit](https://streamlit.io/)
    - Streamlit turns data scripts into shareable web apps in minutes. All in pure Python.
    - Investor and Administrators Frontend experiences have been developed using this library
    - Backtesting Frontend experience has been developed using this Library
- [yfinance](https://pypi.org/project/yfinance/)
    - yfinance offers a threaded and Pythonic way to download market data from
    - All the markets data are downloaded through this library
- [PyTorch](https://pytorch.org/docs/stable/index.html)
    - PyTorch is a machine learning framework based on the Torch library
    - Originally developed by Meta AI and now part of the Linux Foundation
    - Together with TensorFlow, the most important Machine Learning development framework
    - Used to load pre-trained Risk Management Model

## __Installation__

### _General Information_

At the state of art, the platform could only interacts with markets on Windows, due to MetaTrader API.
<br>
<br>
MetaTrader 5 (MT5) is a versatile trading platform offering advanced tools for forex and stock trading. It provides real-time market analysis, automated trading, and customizable features for traders.
<br>
<br>
Currenty, it is a platform widely used by different brokers, and it is also free to use compared to Trader Workstation. In the future, I would really like to implement TWS API (Trader WorkStation API to render Inkosi versatile)
<br>
<br>
I apologise for the incovenience.


### _Advanced Python Programming For Economics, Management And Finance Exam_

At the moment a _Compute Engine_ instance, a simple virtual machine running on Microsoft Server 2022, here are contained all the needed tools (expect from MetaTrader 5) to interact with the platform.
<br><br>

__Tools__:

- _Visual Studio Code_
    - Here the latest version of the code has been loaded, you will be able to have a closer look to it
- _Postman_
    - Postman is an API platform for developers
    - All the API Endpoints are available on this platform, divided by features
- _Mongo Compass_
    - Compass is a free interactive tool for querying, optimizing, and analyzing MongoDB data
    - A connection has already been created
- _HeidiSQL_
    - HeidiSQL is a free and open-source administration tool for MariaDB, MySQL, as well as Microsoft SQL Server, PostgreSQL and SQLite
- _Google Chrome_
    - Most widely used internet browser
    - You will have access to Frontend experiences

All the information needed to use the Virtual Machine have been inserted in the README.txt file of the uploaded folder.
<br><br>
Two databases have been created to respectively interact to PostgreSQL and MongoDB (Access only available through the Virtual Machine, IP Address restriction has been implemented. Credentials avaiable in the uploaded folder on BlackBoard)

## __Issues & Suggestions Tracker__

### _GitHub Issues_

For any issues, please refers to [GitHub Issues](https://github.com/BopaxDev/Inkosi/issues)

## __Contact__

- [GitHub](https://github.com/BopaxDev)
- [LinkedIn](https://www.linkedin.com/in/mario-nicolo-de-matteis)
- [X](https://twitter.com/MDMatteis)
- [E-mail Address](mailto:marionicdematteis@gmail.com)