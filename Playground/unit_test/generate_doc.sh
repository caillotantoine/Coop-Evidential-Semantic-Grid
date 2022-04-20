path_from_here="$(dirname "$0")"

# files_projection=bbox.py vec3.py projection.py matrix_utils.py dataset_reader.py
files_projection="$(ls ./projection/*.py)"

cd $path_from_here


rm -rf ./Doc
mkdir ./Doc
mkdir ./Doc/html
mkdir ./Doc/md
mkdir ./Doc/pdf

# rm -rf projection/__pycache__
pdoc3 --html -o ./Doc/html -c latex_math=True projection/*.py --force

for f in ./projection/*.py
do
    filename="$(basename $f | cut -d. -f1)"
    echo $filename
    pdoc3 --pdf -c latex_math=True projection/$filename.py > ./Doc/md/$filename.md
    sed -i '' -e "s/-----=/------\\n/" ./Doc/md/$filename.md
    pandoc --metadata=title:"Projection" --from=markdown --pdf-engine=xelatex ./Doc/md/$filename.md -o ./Doc/pdf/$filename.pdf
done
# rm -rf projection/__pycache__


# pandoc --metadata=title:"MyProject Documentation"               \
#        --from=markdown+abbreviations+tex_math_single_backslash  \
#        --pdf-engine=xelatex --variable=mainfont:"DejaVu Sans"   \
#        --toc --toc-depth=4 --output=pdf.pdf  pdf.md