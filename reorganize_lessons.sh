#!/bin/bash

# Reorganize all lesson directories
# Move .tex and .aux files to src/ subdirectory
# Keep .pdf files and lesson_script.txt in main directory

echo "Reorganizing lesson directories..."

# Process lessons 7-50
for i in {7..50}; do
    # Format lesson number with leading zero if needed
    if [ $i -lt 10 ]; then
        lesson_dir="lesson_0${i}"
        lesson_num="0${i}"
    else
        lesson_dir="lesson_${i}"
        lesson_num="${i}"
    fi
    
    # Check if lesson directory exists
    if [ -d "$lesson_dir" ]; then
        echo "Processing $lesson_dir..."
        
        # Create src directory if it doesn't exist
        mkdir -p "$lesson_dir/src"
        
        # Move LaTeX source files to src/
        if [ -f "$lesson_dir/lesson_${lesson_num}.tex" ]; then
            mv "$lesson_dir/lesson_${lesson_num}.tex" "$lesson_dir/src/"
            echo "  Moved lesson_${lesson_num}.tex to src/"
        fi
        
        if [ -f "$lesson_dir/problems_${lesson_num}.tex" ]; then
            mv "$lesson_dir/problems_${lesson_num}.tex" "$lesson_dir/src/"
            echo "  Moved problems_${lesson_num}.tex to src/"
        fi
        
        # Move auxiliary files to src/
        if [ -f "$lesson_dir/lesson_${lesson_num}.aux" ]; then
            mv "$lesson_dir/lesson_${lesson_num}.aux" "$lesson_dir/src/"
        fi
        
        if [ -f "$lesson_dir/problems_${lesson_num}.aux" ]; then
            mv "$lesson_dir/problems_${lesson_num}.aux" "$lesson_dir/src/"
        fi
        
        # Move any .log files to src/
        if ls "$lesson_dir"/*.log 1> /dev/null 2>&1; then
            mv "$lesson_dir"/*.log "$lesson_dir/src/"
        fi
        
        # Verify PDFs remain in main directory
        if [ -f "$lesson_dir/lesson_${lesson_num}.pdf" ]; then
            echo "  ✓ lesson_${lesson_num}.pdf remains in main directory"
        fi
        
        if [ -f "$lesson_dir/problems_${lesson_num}.pdf" ]; then
            echo "  ✓ problems_${lesson_num}.pdf remains in main directory"
        fi
        
        # Verify audio script remains in main directory
        if [ -f "$lesson_dir/lesson_script.txt" ]; then
            echo "  ✓ lesson_script.txt remains in main directory"
        fi
        
        echo ""
    fi
done

echo "Reorganization complete!"
echo ""
echo "Final structure for each lesson:"
echo "  lesson_XX/"
echo "    ├── lesson_script.txt     (audio script)"
echo "    ├── lesson_XX.pdf         (theory PDF)"
echo "    ├── problems_XX.pdf       (problems PDF)"
echo "    └── src/"
echo "        ├── lesson_XX.tex     (theory LaTeX source)"
echo "        ├── problems_XX.tex   (problems LaTeX source)"
echo "        └── *.aux, *.log      (auxiliary files)"