#!/bin/bash

# Simple script to run planning for all problems and generate animations

PROBLEMS="easy medium hard hardHD extreme"
DOMAIN="domain.pddl"
SEARCH_STRATEGY="astar(lmcut())"

mkdir -p plans planimation_exports

for problem in $PROBLEMS; do
    echo ""
    echo "=========================================="
    echo "PLANNING: $problem"
    echo "=========================================="

    problem_file="problem_${problem}.pddl"

    # Run planner
    ./downward/fast-downward.py "$DOMAIN" "$problem_file" --search "$SEARCH_STRATEGY" > "plans/plan_${problem}.txt" 2>&1

    if [ $? -eq 0 ]; then
        echo "✅ Plan saved to: plans/plan_${problem}.txt"

        # Generate animation
        echo ""
        echo "Generating animation..."
        python3 animations/generate_planimation.py "$problem" "plans/plan_${problem}.txt" --output "planimation_exports/${problem}.json"

        if [ $? -eq 0 ]; then
            echo "✅ Animation saved to: planimation_exports/${problem}.json"
        else
            echo "❌ Animation generation failed for $problem"
        fi
    else
        echo "❌ Planning failed for $problem"
    fi
done

echo ""
echo "=========================================="
echo "Done!"
echo "=========================================="

