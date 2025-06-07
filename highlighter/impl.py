#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from typing import List, Dict

from PIL import Image, ImageChops
from pygments import highlight
from pygments.lexers import guess_lexer, get_all_lexers, find_lexer_class_by_name, find_lexer_class

from .formatter import Formatter

from docx import Document
from docx.shared import Inches
import zipfile
import os

import sqlglot
from sqlglot.dialects import TSQL
from sqlglot.errors import ParseError
import re


def get_formatter(dark):
    dark = False
    if dark:
        print('used monokai')
        return Formatter(
            style="monokai",
            format="png",
            line_numbers=False,
            font_name='Consolas-Regular',
            font_size=36,
            line_number_bg="#000000",
            line_number_fg="#888888",
            image_pad=8,
        )
    print('used tango')
    return Formatter(
        style="tango",
        format="png",
        line_numbers=False,
        font_name='Consolas-Regular',
        font_size=16,
        line_number_bg="#808000",
        line_number_fg="#999999",
        image_pad=8,
    )


def limit_input(content: str, max_lines=66) -> str:
    lines = content.splitlines()
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    else:
        lines = lines + [" "] * (max_lines - len(lines))
    return "\n".join(lines)


matrix_cache: Dict[str, List[int]] = {}


def get_matrix_file(background: str) -> str:
    return background.rsplit(".", maxsplit=1)[0] + ".json"


def get_matrix(bg):
    if bg not in matrix_cache:
        with open(get_matrix_file(bg)) as f:
            matrix_cache[bg] = json.load(f)["coefficients"]
    return matrix_cache[bg]


def transform(img, img_file, background, matrix=None):
    background_img_raw = Image.open(background)
    if matrix is None:
        matrix = get_matrix(background)

    foreground_img_raw = img
    foreground_img_raw = foreground_img_raw.transform(background_img_raw.size, method=Image.PERSPECTIVE, data=matrix,
                                                      resample=Image.BILINEAR, fillcolor=(255, 255, 255))

    ImageChops.multiply(foreground_img_raw, background_img_raw).convert("RGB").save(img_file)

def reformat_tsql(content):
    re_parameters = r'\((@P\d{1,3} (?:\w+(?:\(\d+\))?)\,?)+\)'
    param_replacement = ''
    sqltext_full = content
    sqltext_param = re.findall(re_parameters, sqltext_full)
    sqltext = re.sub(re_parameters, param_replacement, sqltext_full) # w/o params
    try:
        sql_ast = sqlglot.parse_one(sql=sqltext, read=sqlglot.dialects.TSQL)
        if type(sql_ast.root()) in (sqlglot.expressions.Select, sqlglot.expressions.Insert, sqlglot.expressions.Update, sqlglot.expressions.Delete):
            res = sqlglot.parse_one(sql=sqltext, read=sqlglot.dialects.TSQL).sql(pretty=True, dialect=sqlglot.dialects.TSQL)
            if sqltext_param:
                res =  '(' + sqltext_param[0] + ')\n' + res
        else:
            res = sqltext_full
        return res
    except ParseError:
        return content


def make_image(content, output, lang, background, dark=False, matrix=None):
    content = reformat_tsql(content)
    lexer = None
    if lang:
        lexer = find_lexer_class(lang)()
    if not lexer:
        lexer = guess_lexer(content)
    formatter = get_formatter(dark)
    highlight(limit_input(content), lexer, formatter, output)
    #debug formatter.image.save('/tmp/example.png')
    transform(formatter.image, output, background, matrix)


languages: List[str] = []


def get_languages() -> List[str]:
    if not languages:
        languages.extend(sorted([
            x[0] for x in get_all_lexers()
        ]))
    return languages



def make_doczip(path):
    doc = Document()
    doc.add_picture(path, width=Inches(6.0))
    base_filename = path.rpartition('.jpg')[0]
    doc_filename = base_filename + '.docx'
    zip_filename = base_filename + '.zip'
    doc.save(doc_filename )
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(doc_filename, os.path.basename(doc_filename))
