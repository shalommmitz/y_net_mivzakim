#!/usr/bin/env python3

import shutil, textwrap
from bidi.algorithm import get_display
RTL_START = u'\u202B'
PDF = '\u202C'  # Pop Directional Formatting

def get_text_as_lines(text, term_width):

    paragraphs = text.strip().split('\n\n')

    output_lines = []
    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        for line in lines:
            wrapped_lines = textwrap.wrap(
                line,
                width=term_width,
                break_long_words=False,
                break_on_hyphens=False
            )
            for line in wrapped_lines:
                #print("b", line)
                start_of_line_natrual_chars = ""
                while get_char_type(line[0])=="natrual":
                    start_of_line_natrual_chars += line[0]
                    line = line[1:]
                end_of_line_natrual_chars = ""
                while get_char_type(line[-1])=="natrual":
                    end_of_line_natrual_chars += line[-1]
                    line = line[:-1]
                line = end_of_line_natrual_chars + line + start_of_line_natrual_chars
                visual = get_display(line)
                #print("a", visual)
                visual_len = len(visual)
                padding = max(0, term_width - visual_len)
                output_lines.append(' ' * padding + visual[::-1] )
           #     # Force RTL rendering by wrapping with RTL_START ... PDF
           #    print(' ' * padding + RTL_START + visual[::-1] + PDF)
        output_lines.append("")
    return output_lines

def send_to_terminal(text: str):
    term_width = shutil.get_terminal_size((80, 20)).columns
    lines = get_text_as_lines(text, term_width)
    for line in lines:
        print(line)
        
def old_send_to_terminal(text: str):
    term_width = shutil.get_terminal_size((80, 20)).columns
    paragraphs = text.strip().split('\n\n')


    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        for line in lines:
            wrapped_lines = textwrap.wrap(
                line,
                width=term_width,
                break_long_words=False,
                break_on_hyphens=False
            )
            for line in wrapped_lines:
                #print("b", line)
                start_of_line_natrual_chars = ""
                while get_char_type(line[0])=="natrual":
                    start_of_line_natrual_chars += line[0]
                    line = line[1:]
                end_of_line_natrual_chars = ""
                while get_char_type(line[-1])=="natrual":
                    end_of_line_natrual_chars += line[-1]
                    line = line[:-1]
                line = end_of_line_natrual_chars + line + start_of_line_natrual_chars
                visual = get_display(line)
                #print("a", visual)
                visual_len = len(visual)
                padding = max(0, term_width - visual_len)
                print(' ' * padding + visual[::-1] )
           #     # Force RTL rendering by wrapping with RTL_START ... PDF
           #    print(' ' * padding + RTL_START + visual[::-1] + PDF)
        print()


def get_char_type(c):
    o = ord(c)
    if o>=32 and o<=47: return "natrual"
    if o>=48 and o<=57: return "LTR"
    if o>=58 and o<=64: return "natrual"
    if o>=65 and o<=90: return "LTR"
    if o>=91 and o<=96: return "natrual"
    if o>=97 and o<=122: return "LTR"
    if o>=123 and o<=126: return "natrual"
    if o>=0x5D0 and o<=0x5EA: return "RTL"

def is_next_seq_is_RTL(text, start):
    i = start +1
    while i<len(text):
         char_type = get_char_type(text[i])
         i += 1
         if char_type=="natrual": continue
         if char_type=="LTR": return False
         if char_type=="RTL": return True
    return False

def reverse_LTR(text):
    t = ""
    LTR_seq = ""
    for idx, c in enumerate(text):
        char_type = get_char_type(c)
        match char_type:
            case "natrual":
                if LTR_seq!="":
                    if is_next_seq_is_RTL(text, idx):
                        t += LTR_seq[::-1]
                        LTR_seq = ""
                        t += c
                    else:
                        LTR_seq += c
                else:
                    t += c
            case "LTR":
                LTR_seq += c
            case "RTL":
                if LTR_seq!="":
                    t += LTR_seq[::-1]
                    LTR_seq = ""
                t+= c
    return t
    
def display_rtl_on_terminal(text):
        #open("item.txt", 'wb').write(text.encode('utf8'))
        text = reverse_LTR(text)
        send_to_terminal(text)

if __name__=="__main__":
    text = open("item.txt", 'rb').read().decode('utf8')
    display_rtl_on_terminal(text)
