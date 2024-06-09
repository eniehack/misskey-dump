#!/bin/sh

ADMIN_TOKEN="${MISSKEY_ADMIN_TOKEN}"
MKHOST="${MISSKEY_HOST=misskey.until.tsukuba.one}"
POETRY=$(which poetry)

USERID_LIST_FILE=$(mktemp)
echo "USERID_LIST_FILE: $USERID_LIST_FILE" 1>&2
"$POETRY" run python3 src/fetchuserlists.py --host "$MKHOST" --token "$ADMIN_TOKEN" \
    | python3 -c 'import sys,json; d=json.load(sys.stdin); [print(i["id"]) for i in d]' \
    > "$USERID_LIST_FILE"

NOTEID_LIST_FILE=$(mktemp)
echo "NOTEID_LIST_FILE: $NOTEID_LIST_FILE" 1>&2
cat "$USERID_LIST_FILE"  \
    | xargs -I {} -P 4 -t sh -c 'sleep 1 && '"$POETRY"' run python3 src/fetchusernotes.py -u {} --host '"$MKHOST"' >> '"$NOTEID_LIST_FILE"
"$POETRY" run python3 src/filternotes.py "$NOTEID_LIST_FILE" | xargs -I {} -P 4 echo "https://$MKHOST/notes/"{}
        #"$POETRY"' run python3 src/fetchusernotes.py -u {} --host '"$MISSKEY_HOST"' | '"$POETRY"' run python3 -c '\''import sys,json; print(json.load(sys.stdin))'\'
        #"$POETRY"' run python3 src/fetchusernotes.py -u {} --host '"$MISSKEY_HOST"
#while read user; do
#    echo "$user"
#    $POETRY run python3 src/fetchusernotes.py \
#        -u "$user" --host "$MISSKEY_HOST" \
#        >> "$NOTEID_LIST_FILE"
#    sleep 1
#done < "$USERID_LIST_FILE"

#while read note; do
#    echo "https://$MISSKEY_HOST/notes/$NOTEID"
#done < "$NOTEID_LIST_FILE"

#rm "$NOTEID_LIST_FILE"
#rm "$USERID_LIST_FILE"

