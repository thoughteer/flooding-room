read -p 'Press <ENTER> to stop... ' -n 1 -s
echo 'now give it a second...'
kill `jobs -p`
wait `jobs -p` 2>/dev/null
