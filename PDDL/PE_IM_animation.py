"""
==========================================================
ANIMAZIONE DEL SATELLITE
==========================================================

Visualizzazione semplice step-by-step del piano.

L'obiettivo NON è creare un videogioco,
ma rendere visibile:

- orientamento
- foto scattate
- invii
- energia
- memoria

==========================================================
"""

import time


def animate_plan(plan):

    print("\n======================================")
    print("ANIMAZIONE PIANO")
    print("======================================")

    for i, action in enumerate(plan, 1):

        print(f"\nSTEP {i}")
        print("AZIONE:", action)

        time.sleep(1)

    print("\nMISSIONE COMPLETATA")