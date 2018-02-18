import argparse
import trie


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_file",
                        help = "name of target_file")
    parser.add_argument("--dictionary_path",
                        help = "name of dictionary to create trie form")
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    trie = trie.create_trie(dictionary_path=args.dictionary_path,
                            to_be_saved=True,
                            save_as=args.target_file)
