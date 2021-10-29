# Thistlethwaite
Rubik's cube solver based on Thistlethwaite's algorithm combined with Bidirectional breadth first search

https://en.wikipedia.org/wiki/Morwen_Thistlethwaite

Usage:
You can pass a mix as a string of moves ( F R B L U D notation https://www.francocube.com/notation )

./rubik.py "F R L' U B D2 F' R"
output: "D R' F' L' B' F' U' R' D' L' U' B2 U' B2 U L2 D B2 R2 U D2 R2 D2 R2 F2 L2 U2 B2 U2 B2 L2 F2"

./rubik.py -vr  for a random mix (42 moves) and unity visual.

options:
-h usage
-r for random mix
-v for a Unity visual (Mac build)
-t for detailed phases

Unity code: https://github.com/Fervac/rubiks
