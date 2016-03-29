# -*- coding: utf-8 -*-

import argparse


class CliArgs:
    def __init__(self):
        p = argparse.ArgumentParser(prog='elastic_funnel')
        p.add_argument('--path', nargs='+', help='Path of stages')
        p.add_argument('--country', nargs='+', help='Path of stages')
        p.add_argument('--start', nargs='+', help='Start time for ')
        p.add_argument('--end', nargs='+', help='The end-time of log')
        args = p.parse_args()

        self.path = args.path


def main():
    cli_args = CliArgs()

    print cli_args.path


if __name__ == '__main__':
    main()
