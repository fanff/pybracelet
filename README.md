# pybracelet


This project models the Brazilian bracelet problem, a pattern-based system for constructing woven bracelets using knotted cotton wires. The output is a grid-like canvas made of interlinked nodes, forming a ribbon that wraps around the wrist.

## 🧶 Overview

A Brazilian bracelet is built by knotting wires in specific patterns. The resulting structure is a canvas of nodes organized in columns (lengthwise) and rows (widthwise). This canvas simulates how wires interact over time, with each node determining wire order and color as the bracelet is built.

* Columns: ~150 (length around the wrist)

* Rows: N, where N = W / 2 and W is the number of wires

The bracelet alternates between even and odd columns with differing node counts, creating a zig-zag weaving effect.
### 🔗 Node Types

Each node is formed by two wires:

    L: Left wire

    R: Right wire

There are 4 possible node combinations:

| Input Wires | Node Color | Output Wires   |
| ----------- | ---------- | -------------- |
| LL          | R (Right)  | R L (Reversed) |
| LR          | R (Right)  | L R (Same)     |
| RR          | L (Left)   | R L (Reversed) |
| RL          | L (Left)   | R L (Same)     |



Each node alters the order of wires and determines the color based on a simple rule set.


### 🧱 Canvas Structure

The canvas is constructed as follows:

* Even columns contain N nodes

* Odd columns contain N - 1 nodes

       Even Column (C)      Odd Column (C+1)      Even Column     (C+2)
    
       [ ]                                        [ ]
       [ ]                  [ ]                   [ ]
       [ ]                  [ ]                   [ ]
       [ ]                  [ ]                   [ ]
       [ ]                  [ ]                   [ ]


This alternating pattern offsets nodes so that:

* Nodes in column C are aligned vertically using the current wire arrangement

* Nodes in column C + 1 are placed between nodes from column C

* Nodes in column C + 1 use the output wires from column C as their input

At each odd column, the two topmost wires pass through unknotted to the next even column, effectively skipping that row.

### 📐 Example Parameters

    W = 12 wires → N = 6 rows

    Canvas width = 6 rows

    Canvas length = ~150 columns (customizable)