import argparse


def get_arguments_dict():
    parser = argparse.ArgumentParser()
    parser.add_argument("db_name",
                        help="name of database with texts")

    parser.add_argument("-h", "--host",
                        dest="host",
                        help="mysql user's name")

    parser.add_argument("-u", "--user",
                        dest="user",
                        help="mysql user's name")

    parser.add_argument("-p", "--password",
                        dest="password",
                        help="mysql user's password")

    parser.add_argument("-db", "--database",
                        dest="database",
                        help="name of database")

    parser.add_argument("-u", "--user",
                        dest="user",
                        help="mysql user's name")

    parser.add_argument("-c", "--coding",
                        dest="charset",
                        help="coding tom use",
                        required=False,
                        default="utf8")

    args = {}
    try:
        args = parser.parse_args()
    except argparse.ArgumentError:
        print("argparse.ArgumentError:")
        exit()
    return args


if __name__ == "__main__":
    pass
