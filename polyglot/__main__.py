#!/usr/bin/env python3

import os
from argparse import ArgumentParser
from colorama import init, Fore

from polyglot.deepl import Deepl
from polyglot.managers import BaseManager, JSONManager, POManager

init()


def translate_or_print_data():

    parser: ArgumentParser = get_parser()
    args: dict = parser.parse_args()

    if not args.action:
        print(Fore.RED + f"No action selected.")
        os._exit(0)

    deepl: Deepl = Deepl(args.target_lang, args.source_lang)

    if args.action == 'translate':

        if args.source_file is None or args.target_lang is None:
            parser.error("translate requires --source_file and --target_lang.")

        name, extension = os.path.splitext(args.source_file)

        if extension == '.json':
            manager: JSONManager = JSONManager(deepl, args.source_file,
                                               args.output_directory)
        elif extension == '.po':
            manager: POManager = POManager(
                deepl, args.source_file, args.output_directory)
        else:
            manager: BaseManager = BaseManager(
                deepl, args.source_file, args.output_directory)

        manager.translate_source_file()

        print(Fore.GREEN + f'\nFinish.\n')

    elif args.action == 'print_supported_languages':
        deepl.print_supported_languages()

    elif args.action == 'print_usage_info':
        deepl.print_usage_info()


def get_parser():
    actions: list[str] = ['translate',
                          'print_supported_languages', 'print_usage_info']
    parser: ArgumentParser = ArgumentParser(
        description='Using the DeepL API, this script translate the given file.')
    parser.add_argument(
        'action', type=str, help="The action that will be exectued.", choices=actions)
    parser.add_argument('-p', '--source_file', type=str,
                        help='The file to be translated. Required if the action is "translate."', default=None)
    parser.add_argument('-t', '--target_lang', type=str,
                        help='the code of the language into which you want to translate the source file. Required if the action is "translate".', default=None)
    parser.add_argument('-o', '--output_directory', type=str,
                        help='The directory where the output file will be located. Will be used the working directory if this option is invalid or not used.', default=None)
    parser.add_argument('-s', '--source_lang', type=str,
                        help='Source file language code. Detected automatically by DeepL by default. Specifying it can increase performance and make translations more accurate.', default=None)
    return parser


if __name__ == '__main__':
    translate_or_print_data()