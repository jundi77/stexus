#!/bin/bash

number=55
multiplicand={{ multiplicand }}
substractor={{ substractor }}
multiplicator=5
guess=$((multiplicand * multiplicator - substractor))
diff=$((number > guess ? number - guess : guess - number))
sleep 1
echo "$diff" >result
