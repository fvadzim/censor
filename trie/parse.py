from argparse import ArgumentParser
class DBArgsParser(ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument("-hst", "--host",
                            dest="host",
                            help="mysql host's name")

        self.add_argument("-u", "--user",
                            dest="user",
                            help="mysql user's name")

        self.add_argument("-p", "--password",
                            dest="password",
                            help= "mysql user's password")

        self.add_argument("-db", "--database",
                            dest="database",
                            help="name of database")


        self.add_argument("-c","--coding",
                            dest="charset",
                            help="coding tom use",
                            required=False,
                            default="utf8")
    def get_args_dict(self):
        return vars(self.parse_args())


class LexiconCheckerAgsParser(DBArgsParser):
    def __init__(self):
        super().__init__()
        self.add_argument("-t","--table",
                            dest="table",
                            help="table to use",
                            default="utf8")

        self.add_argument("-f","--field",
                            dest="field",
                            help="field name",
                            required=False,
                            default="utf8")

if __name__ =="__main__":
    print(get_arguments_dict())
