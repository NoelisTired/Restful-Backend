# NoelP X Backend 2023

A Python based project combining a RESTful API with a Discord Bot. The API serves to handle user authentication and data management while the Discord Bot provides a conversational interface to the service.

## Installation

Clone the repository:

git clone [https://github.com/](https://github.com/)`<NoelisTired>`/NoelP-X.git

Install the dependencies:

pip install -r setup/requirements.txt

## Usage

Edit the configuration file `conf.json` to reflect your desired setup.

Start the project:

$ python main.py

## Configuration

The configuration file `conf.json` is in JSON format and contains settings for the API and Discord Bot.

Api settings:

- `Enabled`: Enable or disable the API
- `Host`: The hostname or IP to bind the API to
- `Port`: The port number to listen on
- `Debug`: A description of the API
- `Info`: Version and last updated date

Discord settings:

- `Enabled`: Enable or disable the Discord Bot to run at startup
- `Token`: Your Discord Bot Token
- `Prefix`: The prefix to use for bot commands
- `OwnerID`: The Discord User ID of the Bot owner

Database settings:

- `Host`: The hostname or IP of the MySQL server
- `Port`: The port number of the MySQL server
- `Login`:
  - `Username`: The MySQL username
  - `Password`: The MySQL password
  - `Database`: The name of the database

## Features

- RESTful API for user authentication and data management
- Discord Bot for conversational interaction with the service
- Graceful exit on `CTRL + C`

## Contributing

Feel free to contribute to this project by submitting pull requests or by reporting issues.

## License

This project is licensed under the MIT License.
