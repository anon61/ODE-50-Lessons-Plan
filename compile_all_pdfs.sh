#!/bin/bash

# Compile all missing PDFs for lessons 19-50

echo "Compiling PDFs for lessons 19-50..."
echo "=================================="

successful=0
failed=0

for i in {19..50}; do
    lesson_dir="lesson_${i}"
    
    if [ -d "$lesson_dir" ]; then
        echo -n "Lesson $i: "
        
        # Check if lesson PDF exists, if not compile it
        if [ ! -f "$lesson_dir/lesson_${i}.pdf" ]; then
            if [ -f "$lesson_dir/src/lesson_${i}.tex" ]; then
                cd "$lesson_dir/src"
                pdflatex -interaction=nonstopmode lesson_${i}.tex > /dev/null 2>&1
                if [ -f "lesson_${i}.pdf" ]; then
                    mv lesson_${i}.pdf ../
                    echo -n "[L✓] "
                    ((successful++))
                else
                    echo -n "[L✗] "
                    ((failed++))
                fi
                cd ../..
            else
                echo -n "[L-] "
            fi
        else
            echo -n "[L✓] "
        fi
        
        # Check if problems PDF exists, if not compile it
        if [ ! -f "$lesson_dir/problems_${i}.pdf" ]; then
            if [ -f "$lesson_dir/src/problems_${i}.tex" ]; then
                cd "$lesson_dir/src"
                pdflatex -interaction=nonstopmode problems_${i}.tex > /dev/null 2>&1
                if [ -f "problems_${i}.pdf" ]; then
                    mv problems_${i}.pdf ../
                    echo "[P✓]"
                    ((successful++))
                else
                    echo "[P✗]"
                    ((failed++))
                fi
                cd ../..
            else
                echo "[P-]"
            fi
        else
            echo "[P✓]"
        fi
    fi
done

echo ""
echo "=================================="
echo "Compilation Summary:"
echo "Successful: $successful"
echo "Failed: $failed"
echo ""

# Count total PDFs
total_pdfs=$(find . -name "*.pdf" -type f | wc -l)
echo "Total PDFs in project: $total_pdfs"

# Show which lessons are missing PDFs
echo ""
echo "Missing PDFs:"
for i in {19..50}; do
    lesson_dir="lesson_${i}"
    if [ -d "$lesson_dir" ]; then
        missing=""
        if [ ! -f "$lesson_dir/lesson_${i}.pdf" ]; then
            missing="lesson "
        fi
        if [ ! -f "$lesson_dir/problems_${i}.pdf" ]; then
            missing="${missing}problems"
        fi
        if [ -n "$missing" ]; then
            echo "  Lesson $i: $missing"
        fi
    fi
done