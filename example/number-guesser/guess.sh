#!/bin/bash

number=20
guess={{ guess_number }}
diff=$((number > guess ? number - guess : guess - number))
sleep 1
echo "$diff" >result
