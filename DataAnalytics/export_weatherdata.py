from bson.json_util import dumps
from db import DB


def main():
    weatherDB = DB()
    data = weatherDB.read()
    data = list(data)
    data = dumps(data, indent=2)

    with open("weatherdata.json", "w") as file:
        file.write(data)


if __name__ == "__main__":
    main()
