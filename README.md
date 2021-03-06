Cleancopy for LaTeX documents
===============================

This repository contains a tool ``cleancopy.py`` to identify all dependencies for compilation of a top-level LaTeX document.
Its main purpose is to quickly create clean copy of a LaTeX document and its dependencies for camera-ready submissions, ArXiV submissions and so on.

By default, comments inside the LaTeX documents are stripped/redacted as well.

## How it works
Running ``latex`` or ``pdflatex`` with the command ``-record``/``-recorder`` brings the compilers to print the paths of all accessed files during a run (for input or output) into a ``.fls`` file.
The cleancopy script triggers such a translation and reads the provided file to obtain a list of dependencies.
Only relative paths are assumed as necessary dependencies, while absolute paths are discarded as they are assumed to be libraries/fonts/etc. that come with the LaTeX installation on the system.

## Caution
This script potentially (over)writes and modifies files on your disk. Ensure you have backups of your documents you plan to run this script on, e.g. a remote GIT repository. Do not apply this script on your backup copy.

You have been warned.

## Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## License
This package is released under MIT license.

## Compatible Systems
This tool succesfully tested with:

- Linux + TexLive
- Windows + MikTeX

## Installation

- Install compilers for LaTeX (e.g. TexLive or MikTeX)
- Install ``python3`` and the following python packages on your system:
    - pandas

- Checkout this repository and link or copy the script ``cleancopy.py`` into the working directory of your LaTeX document

## Usage Examples
For the following examples we assume ``manuscript.tex`` to be the top-level LaTeX file we want to operate on.

### List dependencies only
Print a list of dependencies to ``stdout`` without creating any copy. Note that the script triggers the translation of the top-level tex file with the predefined TeX compiler.
This mode is useful, if you wish to do other fancy stuff with the dependencies.

For pdfLaTeX dependencies:
```sh
python3 cleancopy.py manuscript.tex
```

For LaTeX dependencies:
```sh
python3 cleancopy.py -L manuscript.tex
```

### Create a copy for ArXiV (-A)

- Identify dependencies with pdfLaTeX
- Include ``manuscript.bbl``
- Copy to subdirectory ``[outdir]`` (-o)
- Strip all comments from ``.tex`` and ``.tikz`` files in ``[outdir]``

```sh
python3 cleancopy.py -A -o [outdir] manuscript.tex
```

### Create a Camera-Ready Copy (CRC) for Paper Submissions (-C)

- Identify dependencies with LaTeX
- Include ``manuscript.dvi``
- Copy to subdirectory ``[outdir]`` (-o)
- Strip all comments from ``.tex`` and ``.tikz`` files in ``[outdir]``

```sh
python3 cleancopy.py -C -o [outdir] manuscript.tex
```

### Note: Bibliography
Generally, no ``.bib`` files are required for the compilation with latex/pdflatex if a ``.bbl`` file is found. I you wish to include your ``.bib`` files, you can add it to the list of additional files at the end of the command line:

```sh
python3 cleancopy.py -A -o [outdir] manuscript.tex Bibliography.bib AnotherExtraFile.foo
```

## Contact
In case of any questions contact Robert Falkenberg <robert.falkenberg@tu-dortmund.de>.