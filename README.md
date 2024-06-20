# Crypto Trading Engineering: Scalable Backtesting Infrastructure

## Installation

- Fork the repository
- Clone the repository you just forked using `git clone`

- In your terminal:

```bash
cd Backtesting-Infrastructure-CryptoTrading
pip install -r requirements.txt
```

## Usage

In your terminal run:

```bash
make up
```

This will start the services in compose.yaml file. You can check the status of
the services by running:

```bash
docker ps
```

To check the logs of a service, run:

```bash
docker compose logs -f <service_name>
```

* Example of checking the logs of the api service:

  ```bash
  docker compose logs -f api
  ```

Where the service_name is the name of the service found in the compose.yaml
file.
