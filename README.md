Cleancopy for LaTeX documents
===============================

This repository contains a tool ``cleancopy.py`` to identify all dependencies for compilation of a top-level LaTeX document.
Its main purpose is to quickly create clean copy of a LaTeX document and its dependencies for camera-ready submissions, ArXiV submissions and so on.

Optionally, comments inside the LaTeX documents can be stripped/redacted as well.

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
Install ``python3`` and the following python dependencies on your system:

- numpy
- pandas

Checkout this repository and copy the script ``cleancopy.py`` into the working directory of your LaTeX document

## Usage
For the examples we assume ``manuscript.tex`` to be the top-level LaTeX file we want to operate on.

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

### Create a Copy for ArXiV (-A)

- Identify dependencies with pdfLaTeX
- Include ``manuscript.bbl`` and ``manuscript.bib``
- Copy to subdirectory ``[outdir]`` (-o)
- Strip all comments from ``.tex``-files in ``[outdir]`` (-s)

```sh
python3 cleancopy.py -A -s -o [outdir] manuscript.tex
```

### Create a Camera-Ready Copy for Paper Submissions (-C)

- Identify dependencies with LaTeX
- Include ``manuscript.dvi`` and ``manuscript.bib``
- Copy to subdirectory ``[outdir]`` (-o)
- Strip all comments from ``.tex``-files in ``[outdir]`` (-s)
 
```sh
python3 cleancopy.py -C -s -o [outdir] manuscript.tex
```

## Contact
In case of any questions contact Robert Falkenberg <robert.falkenberg@tu-dortmund.de>.