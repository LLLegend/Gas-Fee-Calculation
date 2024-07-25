# Gas-Fee-Calculation
## Project Architecture
### Overview
This project is for Tokka Labs Software Engineering Challenge. The system contains three main parts:    
1. Real-time WETH-USDC Uniswap pool transaction monitor.    
2. Backend Service for querying history WETH-USDC Uniswap pool transactions.
3. Database

This project used Python3 as programming language, MySQL as database, Flask for providing endpoint services, Docker-Compose for project set-up.

## Detailed Designs
### Docker
Docker Compose is used in this project. According to the config file `docker-compose.yaml`, services are split into backend service and database service. In this way, we will run two containers after deploying.  
1. `Backend`: The backend image is defined to run a flask app through Dockerfile. The Dockerfile defined how we initialize the container and the way we run the flask app. Besides, the port mapping with host machine and port expose defined in the Docker Compose config.
2. `Database`: The database image directly pull from official MySQL image repository. The database initialization and port mapping is well-defined.
### Backend
Since front-end is not provided, backend would be the most important part for this project. In order to fulfill the requirements of the project, we need:  
1. Database connector to add new data and query existing data from database.
2. Provide RESTful API.
3. HTTP/HTTPS logics to get data from other data services.   

The following modules are provided to implement the whole backend. 
#### db.py
In db.py, a class named DB is defiled. The class DB hold a connection with MySQL and provide useful functions for developers to easily interact with database. Functions are described as below.
1. `get_current_block_number`: Query the newest block number in database.
2. `get_current_price_date`: Query the newest price date in database.  
3. `get_price_by_date`: Query ETH price from a given date.  
4. `get_gas_by_txn`: Query gas price and gas used from a given transaction hash.
5. `get_histories`: Query historical transaction information from a given date range. 
6. `insert_transactions`: Insert transaction data into table `transactions`.
7. `insert_eth_history_prices`: Insert ETH Prices into table `prices`.

Also, The class DB would help a lot in code re-use when implementing more complex logics and building larger projects. 

#### backend.py
In backend.py, a complete flask application is defined to implement the RESTful API, which able to make responses for users who make requests. In this project, two function are used to respond to the request, which are   
1. `get_transaction_fee`: Provide arguments checking, data querying, and making responses for api `/api/v1.0/transaction-fees`
2. `get_histories`: Provide arguments checking, data querying, and making responses for api `/api/v1.0/histories`

It is note-worthy that the flask application run on backend service container's `0.0.0.0:5000`, but we can call the API through `127.0.0.1:5000` because of the setting for the port mapping `5000:5000` in the docker-compose.yaml.
#### data_providers
Data_providers is used for request data from other data api services. Each provider implemented http/https requests for given purpose. In this project, ETH price data is from Binance and token transfer data is from etherscan, so there are two providers are defined:
1. BinanceDataProvider:
   1. `get_daily_eth_price_by_timestamp`: Get ETH price from a given timestamp period.
2. EtherscanDataProvider: 
   1. `get_token_transfers`: Get transaction information from given sender, token address, and block number period.
   2. `get_newest_block`: Get the newest block in Ethereum main network.

#### monitor.py
monitor.py implemented real logics of data recording. The data recoding contains two modes:
1. Batch recording: When the system is at batch recording mode, it means the data in database has a great gap with updated data. The system need to update the record in high rate, which requires a huge amount data in every single request. For ETH price data, since the data volume is not big, we update the historical price in one request. For token transaction data, the block range is set to be 5000, which means we only request 5000 blocks data in one request. 
2. Real-time recording: The system monitor new block data every 5 seconds. Smaller latency would exceed the request quota that etherscan api have limitations per day, and is meaningless because Ethereum generate a new block every 12 seconds. Also, larger latency would destroy the real-time of the system. Hence, 5 seconds latency is nice.

**_The monitor.py is deployed in local host rather than Docker Container in this project because it is very complicated to make backend service container use VPN network that local host uses. But the VPN is required to connect to etherscan and Binance in mainland China._**

### RESTful API Instructions
This system provide 2 RESTful APIs
1. Get `/api/v1.0/transaction-fees`
   - arguments: 
     - `txn_hash`, type: string
   - response:
     - status_code: 
       - 200: Success
       - 400: Bad Request
       - 404: Not Found
     - message
     - results
2. Get `/api/v1.0/histories`
   - arguments: 
     - `start_date`, type: date
     - `end_date`, type: date
   - response:
     - status_code: 
       - 200: Success
       - 400: Bad Request
       - 404: Not Found
     - message
     - results
### Database
There are two tables initialized at the database:
1. `test_db.prices`
2. `test_db.transactions` 

## Build & Run Guide
Before build & run, please make sure you have anaconda and Docker in your computer and port 3306 and port 5000 are not occupied.  
1. Create environment for monitor under the project dir:
   1. create new environment: run `conda create -n Gas-Fee-Calculation python=3.9.7`
   2. switch to the environment: run `source activate Gas-Fee-Calculation`
   3. update pip: run `pip install --upgrade pip`
   4. install required packages: run `pip install -r requirements.txt`
2. Build and run database and backend api services using Docker-Compose under the project dir:
   1. run `docker compose up -d`
3. Run the monitor under the project dir:
   1. run `cd backend/`
   2. run `sh start.sh`

## Test Guide