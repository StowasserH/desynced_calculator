# desynced_calculator
A small script that calculates the required factories in Desynced and outputs them as a graphviz diagram.

I first created a hierarchy of the necessary factories in Desynced with the small Python script.
And then this generated by Graphviz:

![alt tree](./desynct_1.svg)

That's a good step in the right direction. The unbundling of DOT works quite well.
If you don't have Graphviz installed, no problem here is an online interpreter:
https://dreampuf.github.io/GraphvizOnline/

Then I did the layout with yEd, because that way you can move the proportions and relationships around with the mouse and disentangle them.

![alt layout](./desynct_1.gif)

btw: If someone finds a spelling mistake: Don't complain but correct it. This is a public repository!

# ToDo List:
- [o] Add all components
- [X] Add multiple components to the tree
- [ ] Use correct names


