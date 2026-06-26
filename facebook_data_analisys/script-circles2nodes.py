"""
Trasforma un file .circles nel formato:
    node_id, circle1, circle2, ...

Input:  ogni riga  ->  <circle_name> <node1> <node2> ...
Output: ogni riga  ->  <node_id>,<circle1>,<circle2>,...
"""

import sys
from collections import defaultdict

def trasforma(input_path: str, output_path: str) -> None:
    nodo_circoli: dict[str, list[str]] = defaultdict(list)

    with open(input_path, "r") as f:
        for riga in f:
            parti = riga.strip().split()
            if len(parti) < 2:
                continue
            circle = parti[0]
            nodi = parti[1:]
            for nodo in nodi:
                nodo_circoli[nodo].append(circle)

    num_colonne_circoli = 6

    with open(output_path, "w") as f:
        f.write("Id,primary,secondary,other_3,other_4,other_5,other_6\n")
        for nodo in sorted(nodo_circoli, key=lambda x: int(x)):
            circoli = nodo_circoli[nodo][:num_colonne_circoli]
            circoli += [""] * (num_colonne_circoli - len(circoli))
            riga = ",".join([nodo] + circoli)
            f.write(f"{riga}\n")

    print(f"Fatto! {len(nodo_circoli)} nodi scritti in '{output_path}'")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        input_file  = sys.argv[1]
        output_file = sys.argv[2]
    elif len(sys.argv) == 2:
        input_file  = sys.argv[1]
        output_file = input_file.rsplit(".", 1)[0] + "_trasformato.csv"
    else:
        # default per test locale
        input_file  = "3437.circles"
        output_file = "3437_trasformato.csv"

    trasforma(input_file, output_file)
