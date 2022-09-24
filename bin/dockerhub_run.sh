FILE=Gemfile.lock
if [ -f "$FILE" ]; then
    rm $FILE
fi
docker run --rm -v "$PWD:/srv/jekyll/" -p "8088:8088" \
                    -it amirpourmand/al-folio bundler  \
                    exec jekyll serve --watch --port=8088 --host=0.0.0.0 
