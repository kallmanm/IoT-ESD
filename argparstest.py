import yaml
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
                '-c',
                dest='config_file',
                type=argparse.FileType(mode='r'))
    parser.add_argument(
                '--config-file',
                dest='config_file',
                type=argparse.FileType(mode='r'))
    args = parser.parse_args()
    data = yaml.load(args.config_file, Loader=yaml.FullLoader)
    print(data)
    exit()
