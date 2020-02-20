#!/usr/bin/python

import os
import shutil

import pandas as pd
import subprocess
import argparse
import sys
import platform
import re

regex = re.compile(r"(^|[^\\])%.*")

COMPILER_LATEX = "latex"
COMPILER_PDFLATEX = "pdflatex"
COMPILER_DEFAULT = COMPILER_PDFLATEX

EXTENSIONS = [
    'pdf',
    'pdf_tex',
    'png'
    ]

# Exclude all files with the following extensions (if not added explicitly)
EXCLUDE_EXT = [
    'aux',
    'auxlock',
    'bbl',
    'blg',
    'log',
    'out',
    'synctex.gz',
    'synctex(busy)',
    'upa',
    'upb'
    ]

# Also copy all files with "texname".{ADDITIONAL_EXT}
ADDITIONAL_EXT = []     # removed 'bib' from here
# Conditional extensions
ADDITIONAL_EXT_ARXIV = ['bbl']
ADDITIONAL_EXT_CAMERAREADY = ['dvi']

# Strip comments from tex files with the following extensions
STRIP_COMMENTS_TEX_EXT = ['tex', 'tikz']

def scan_dependencies(tex_filename, compiler):
    args = [
        compiler,
        "-quiet",
	    "-interaction=nonstopmode",
	    "-shell-escape",
        ]
    system = platform.system()
    if system == "Linux":
        args.append("-record")
    elif system == "Windows":
        args.append("-recorder")
    elif system == "Darwin":
        args.append("-record")
    else:
        print("Platform not supported: " + system, file=sys.stderr)
        exit(1)

    args.append(tex_filename)

    FNULL = open(os.devnull, 'w')
    popen = subprocess.Popen(args, stdout=FNULL, stderr=subprocess.STDOUT)
    popen.wait()
    FNULL.close()

def change_extension(filename, extension):
    pre, ext = os.path.splitext(filename)
    return pre + "." + extension

def get_fls_filename(tex_filename):
    return change_extension(tex_filename, "fls")

def get_dependencies(fls_filename):
    x = pd.read_csv(fls_filename,sep=" ",header=None)
    
    # filter only inputs, and remove duplicates
    filenames = x.loc[x[0]=="INPUT",1].unique()
    
    # remove absolute paths (system libraries, classes, packages)
    filenames = [f for f in filenames if not os.path.isabs(f)]

    # normalize paths (e.g. A/foo/../B -> A/B)
    filenames = [os.path.normpath(f) for f in filenames]

    return filenames

def strip_comments_tex(src, dst):
    lines = []
    with open(src) as f:
        for line in f:
            line = regex.sub(r"\1%", line)
            lines.append(line)
    with open(dst, mode="w") as f:
        for line in lines:
            f.write(line)

def copy_files(files, outputpath, stripcomments=False):
    for filename in files:
        print(filename)
        destination = os.path.join(outputpath, filename)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        if stripcomments:
            _, ext = os.path.splitext(filename)
            ext = ext.lower()[1:]
            if ext in STRIP_COMMENTS_TEX_EXT:
                strip_comments_tex(filename, destination)
            else:
                shutil.copy(filename, destination)
        else:
            shutil.copy(filename, destination)

def main():

    #defaults
    compiler = COMPILER_DEFAULT
    additional_ext = ADDITIONAL_EXT

    parser = argparse.ArgumentParser()

    preset = parser.add_argument_group("Output format")
    grp = preset.add_mutually_exclusive_group()
    grp.add_argument("-P", "--pdflatex", help="scan dependencies with pdflatex (default)", action="store_true")
    grp.add_argument("-L", "--latex", help="scan dependencies with latex", action="store_true")
    grp.add_argument("-A", "--arxiv", help="scan dependencies for ArXiV", action="store_true")
    grp.add_argument("-C", "--cameraready", help="scan dependencies for DVI-based submissions", action="store_true")
    
    strip = parser.add_argument_group("Redact comments")
    grp = strip.add_mutually_exclusive_group()
    grp.add_argument("-s", "--strip-comments", help="strip comments from tex files (default)", action="store_true", default=True)
    grp.add_argument(      "--no-strip-comments", help="do not strip comments from tex files", action="store_false", dest="strip_comments")

    parser.add_argument("-c", "--compiler", help="override TeX/LaTeX compiler")
    parser.add_argument("-o", "--outputpath", help="copy all dependencies into directory (otherwise only print deps to stdout)")
    parser.add_argument("texname", nargs=1, help="basename of top-level tex file")
    parser.add_argument("extra_files", nargs='*', help="additional files to copy, e.g. bibliography")
    args = parser.parse_args()

    if args.texname is None:
        print("Please provide a top-level tex file", file=sys.stderr)
        exit(1)
    texname = args.texname[0]

    # Presets
    if args.pdflatex:
        compiler = COMPILER_PDFLATEX
    if args.latex:
        compiler = COMPILER_LATEX
    if args.arxiv:
        compiler = COMPILER_PDFLATEX
        additional_ext.extend(ADDITIONAL_EXT_ARXIV)
    if args.cameraready:
        compiler = COMPILER_LATEX
        additional_ext.extend(ADDITIONAL_EXT_CAMERAREADY)
    
    # manual override for compiler
    if args.compiler is not None:
        compiler = args.compiler

    # run compiler to obtain dependency file
    scan_dependencies(texname, compiler)

    # parse dependency file
    files = get_dependencies(get_fls_filename(texname))

    # remove excluded extensions
    tmp = []
    for f in files:
        _, ext = os.path.splitext(f)
        ext = ext.lower()[1:]
        if ext not in EXCLUDE_EXT:
            tmp.append(f)
    files = tmp

    # add additional extensions (global)
    files.extend([change_extension(texname, ext) for ext in additional_ext])
    
    # add extra files explicitly
    files.extend(args.extra_files)
    
    if args.outputpath is not None:
        copy_files(files, args.outputpath, args.strip_comments)
    else:
        print(*files, sep = "\n")
        

if __name__ == '__main__':
    main()
