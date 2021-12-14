import argparse
from colorama import init, Fore

from deepl import Deepl
from translation import JSONManager

init()

def translate(args):
    deepl = Deepl(args.target_lang, args.source_lang)  
    translation_manager = JSONManager(deepl, args.source_file, args.target_path)
    translation_manager.translate_source_file()
    # TODO: PO files support

def print_data_or_translate(args):
    if args.action == 'translate':
        translate(args)
    else:
        deepl = Deepl()
        if args.action == 'print_supported_languages':
            deepl.print_supported_languages()
        elif args.action == 'print_usage_info':
            deepl.print_usage_info()
        else:
            print(Fore.YELLOW + f"No action selected.")
    
ACTIONS = [ 'translate', 'print_supported_languages', 'print_usage_info']

parser = argparse.ArgumentParser(description='Using the Deepl APIs, this script translate the given json or po file')

parser.add_argument('action', type=str, help="The action that will be exectued.", choices=ACTIONS)
parser.add_argument('-p', '--source_file', type=str, help='The JSON or PO file to be translated. Required if the action is "translate"', default=None)
parser.add_argument('-t', '--target_lang', type=str, help='The language code of the output file. Required if the action is "translate"', default=None)
parser.add_argument('-s', '--source_lang', type=str, help='Source language code. Detected automatically by Deepl by default. Specifying it manually can increase performance and make translations more accurate.', default=None)
parser.add_argument('-o', '--target_path', type=str, help='The directory where the output file will be located. The working directory will be used if target_path is empty or not valid.', default=None)

args = parser.parse_args()

if args.action == 'translate' and (args.source_file is None or args.target_lang is None):
    parser.error("translate requires --source_file and --target_lang.")

print_data_or_translate(args)