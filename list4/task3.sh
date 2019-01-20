#!/bin/sh
swipl -c list4/task1.pl <list4/phrases > ok
echo "Good phrases"
grep GOOD ok | wc -l
swipl -c list4/task1.pl <list4/bad_phrases > no_ok
echo "bad phrases"
grep GOOD no_ok | wc -l

