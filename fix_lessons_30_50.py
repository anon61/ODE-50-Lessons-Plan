#!/usr/bin/env python3
"""
Fix all LaTeX compilation issues for lessons 30-50
"""

import os
import re
import subprocess
from pathlib import Path

def fix_latex_content(content, lesson_num):
    """Fix common LaTeX issues in content."""
    
    # Remove unavailable packages
    content = re.sub(r'\\usepackage\{nicematrix[^}]*\}', '', content)
    content = re.sub(r'\\usepackage\{[^}]*nicematrix[^}]*\}', '', content)
    content = re.sub(r'\\usepackage\{[^}]*systeme[^}]*\}', '', content)
    
    # Fix the package line if it becomes empty
    content = re.sub(r'\\usepackage\{\s*,\s*', r'\\usepackage{', content)
    content = re.sub(r',\s*\}', r'}', content)
    content = re.sub(r'\\usepackage\{\s*\}', '', content)
    
    # Fix math mode issues
    # Fix subscripts outside math mode
    content = re.sub(r'([^$\\])_\{([^}]+)\}([^$])', r'\1$_{\2}$\3', content)
    content = re.sub(r'([^$\\])\^\{([^}]+)\}([^$])', r'\1$^{\2}$\3', content)
    
    # Fix specific patterns like q$_{0}$
    content = re.sub(r'([a-zA-Z])\$_\{([^}]+)\}\$', r'\1_{\2}', content)
    content = re.sub(r'([a-zA-Z])\$\^\{([^}]+)\}\$', r'\1^{\2}', content)
    
    # Fix double dollar signs in align
    content = re.sub(r'\\begin\{align\}([^$]*)\$\$([^$]*)\$\$([^$]*)\\end\{align\}',
                     r'\\begin{align}\1\2\3\\end{align}', content, flags=re.DOTALL)
    
    # Replace nicematrix environments with standard ones
    content = re.sub(r'\\begin\{bNiceMatrix\}', r'\\begin{bmatrix}', content)
    content = re.sub(r'\\end\{bNiceMatrix\}', r'\\end{bmatrix}', content)
    content = re.sub(r'\\begin\{pNiceMatrix\}', r'\\begin{pmatrix}', content)
    content = re.sub(r'\\end\{pNiceMatrix\}', r'\\end{pmatrix}', content)
    
    # Replace systeme commands with aligned environment
    content = re.sub(r'\\systeme\{([^}]+)\}', 
                     lambda m: r'\\begin{aligned}' + m.group(1).replace(',', r'\\\\') + r'\\end{aligned}', 
                     content)
    
    # Ensure amsmath is included if we use bmatrix
    if 'bmatrix' in content or 'pmatrix' in content or 'aligned' in content:
        if 'amsmath' not in content:
            content = re.sub(r'(\\documentclass[^}]+\})',
                           r'\1\n\\usepackage{amsmath}', content)
    
    # Fix specific issues for certain lessons
    if lesson_num == 32:
        # Complex eigenvalues lesson - ensure proper formatting
        content = re.sub(r'\\lambda = \\alpha \\pm i\\beta',
                        r'$\\lambda = \\alpha \\pm i\\beta$', content)
    
    if lesson_num == 35:
        # Duhamel's principle - fix matrix exponentials
        content = re.sub(r'e\^\{At\}', r'e^{At}', content)
        content = re.sub(r'e\^\{A\(t-s\)\}', r'e^{A(t-s)}', content)
    
    return content

def compile_latex(filepath, max_attempts=2):
    """Try to compile a LaTeX file."""
    directory = filepath.parent
    filename = filepath.name
    
    for attempt in range(max_attempts):
        try:
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', filename],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                pdf_name = filename.replace('.tex', '.pdf')
                # Move PDF to parent directory if in src/
                if directory.name == 'src':
                    src_pdf = directory / pdf_name
                    dest_pdf = directory.parent / pdf_name
                    if src_pdf.exists():
                        src_pdf.rename(dest_pdf)
                return True
            
            # If first attempt failed, try to fix more issues
            if attempt == 0 and 'Undefined control sequence' in result.stdout:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Additional fixes based on error
                content = re.sub(r'\\mathbb\{([A-Z])\}', r'\\mathbb{\1}', content)
                content = re.sub(r'\\times(?![a-z])', r'\\times ', content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
        except Exception as e:
            print(f"  Error during compilation: {e}")
    
    return False

def process_lesson(lesson_num):
    """Process and fix a single lesson."""
    print(f"\nProcessing Lesson {lesson_num}...")
    
    base_dir = Path(f"/home/archer/Desktop/ODE 50 Lessons Plan/lesson_{lesson_num}")
    if not base_dir.exists():
        print(f"  Lesson {lesson_num} directory not found")
        return False
    
    theory_tex = base_dir / 'src' / f'lesson_{lesson_num}.tex'
    theory_pdf = base_dir / f'lesson_{lesson_num}.pdf'
    
    # Only process if PDF is missing
    if not theory_pdf.exists() and theory_tex.exists():
        print(f"  Fixing LaTeX for lesson_{lesson_num}.tex...")
        
        # Read and fix content
        with open(theory_tex, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content = fix_latex_content(content, lesson_num)
        
        # Write fixed content
        with open(theory_tex, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        # Try to compile
        if compile_latex(theory_tex):
            print(f"  ✓ Successfully compiled lesson_{lesson_num}.pdf")
            return True
        else:
            print(f"  ✗ Failed to compile lesson_{lesson_num}.pdf")
            return False
    elif theory_pdf.exists():
        print(f"  ✓ lesson_{lesson_num}.pdf already exists")
        return True
    else:
        print(f"  ✗ lesson_{lesson_num}.tex not found")
        return False

def main():
    """Fix all problematic lessons."""
    print("Fixing LaTeX compilation issues for lessons 30-50...")
    print("=" * 50)
    
    # List of lessons that need fixing
    lessons_to_fix = [32, 33, 34, 35, 38, 48, 49, 50]
    
    successful = 0
    failed = []
    
    for lesson_num in lessons_to_fix:
        if process_lesson(lesson_num):
            successful += 1
        else:
            failed.append(lesson_num)
    
    print("\n" + "=" * 50)
    print(f"Results:")
    print(f"  Successfully fixed: {successful}/{len(lessons_to_fix)}")
    if failed:
        print(f"  Failed lessons: {failed}")
    
    # Also check other lessons in range
    print("\nChecking all lessons 30-50 for completeness...")
    missing_pdfs = []
    for lesson_num in range(30, 51):
        base_dir = Path(f"/home/archer/Desktop/ODE 50 Lessons Plan/lesson_{lesson_num}")
        if base_dir.exists():
            theory_pdf = base_dir / f'lesson_{lesson_num}.pdf'
            problems_pdf = base_dir / f'problems_{lesson_num}.pdf'
            
            if not theory_pdf.exists():
                missing_pdfs.append(f"lesson_{lesson_num}")
            if not problems_pdf.exists():
                missing_pdfs.append(f"problems_{lesson_num}")
    
    if missing_pdfs:
        print(f"Still missing PDFs: {missing_pdfs}")
    else:
        print("All lessons 30-50 have complete PDFs!")

if __name__ == "__main__":
    main()