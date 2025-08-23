#!/usr/bin/env python3
"""
Fix LaTeX compilation issues in lesson files
"""

import os
import re
import subprocess
from pathlib import Path

def fix_latex_file(filepath):
    """Fix common LaTeX issues in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix undefined control sequences
    fixes = {
        r'\\Rightarrow': r'\\rightarrow',
        r'\\RR': r'\\mathbb{R}',
        r'\\CC': r'\\mathbb{C}',
        r'\\NN': r'\\mathbb{N}',
        r'\\ZZ': r'\\mathbb{Z}',
        r'\\QQ': r'\\mathbb{Q}',
        r'⟨': r'\\langle',
        r'⟩': r'\\rangle',
        r'∘': r'\\circ',
    }
    
    for old, new in fixes.items():
        content = content.replace(old, new)
    
    # Fix missing math mode
    content = re.sub(r'([^$\\])_([a-zA-Z0-9]+)', r'\1$_{\2}$', content)
    content = re.sub(r'([^$\\])\^([a-zA-Z0-9]+)', r'\1$^{\2}$', content)
    
    # Add missing packages
    if '\\mathbb' in content and 'amssymb' not in content:
        content = content.replace('\\begin{document}', 
                                 '\\usepackage{amssymb}\n\\begin{document}')
    
    if '\\bmatrix' in content and 'amsmath' not in content:
        content = content.replace('\\begin{document}', 
                                 '\\usepackage{amsmath}\n\\begin{document}')
    
    # Fix environment issues
    content = re.sub(r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}', 
                     lambda m: m.group(0) if '$' not in m.group(1) else m.group(0).replace('$', ''),
                     content, flags=re.DOTALL)
    
    # Fix missing document structure
    if '\\documentclass' not in content:
        content = '\\documentclass[12pt]{article}\n' + content
    
    if '\\begin{document}' not in content and '\\title' in content:
        title_end = content.find('\\date')
        if title_end == -1:
            title_end = content.find('\\maketitle')
        if title_end > 0:
            content = content[:title_end+20] + '\n\\begin{document}\n\\maketitle\n' + content[title_end+20:]
    
    if '\\end{document}' not in content:
        content += '\n\\end{document}'
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def compile_latex(filepath):
    """Try to compile a LaTeX file."""
    directory = filepath.parent
    filename = filepath.name
    
    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', filename],
            cwd=directory,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except:
        return False

def process_lesson(lesson_num):
    """Fix and compile LaTeX files for a lesson."""
    base_dir = Path(f"/home/archer/Desktop/ODE 50 Lessons Plan/lesson_{lesson_num:02d}")
    if not base_dir.exists():
        return
    
    theory_file = base_dir / f"lesson_{lesson_num:02d}.tex"
    problems_file = base_dir / f"problems_{lesson_num:02d}.tex"
    
    fixed = False
    
    # Fix and compile theory
    if theory_file.exists():
        if fix_latex_file(theory_file):
            fixed = True
            print(f"Fixed lesson_{lesson_num:02d}.tex")
        
        if not (base_dir / f"lesson_{lesson_num:02d}.pdf").exists():
            if compile_latex(theory_file):
                print(f"Compiled lesson_{lesson_num:02d}.pdf")
            else:
                print(f"Failed to compile lesson_{lesson_num:02d}.pdf")
    
    # Fix and compile problems
    if problems_file.exists():
        if fix_latex_file(problems_file):
            fixed = True
            print(f"Fixed problems_{lesson_num:02d}.tex")
        
        if not (base_dir / f"problems_{lesson_num:02d}.pdf").exists():
            if compile_latex(problems_file):
                print(f"Compiled problems_{lesson_num:02d}.pdf")
            else:
                print(f"Failed to compile problems_{lesson_num:02d}.pdf")
    
    return fixed

def main():
    """Fix all lessons with compilation issues."""
    print("Fixing LaTeX compilation issues...")
    
    # List of lessons that had compilation issues
    problem_lessons = [20, 22, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 44, 47, 48, 49, 50]
    
    for lesson_num in problem_lessons:
        print(f"\nProcessing lesson {lesson_num}...")
        process_lesson(lesson_num)
    
    # Also check lesson 46 which had no content
    if not Path("/home/archer/Desktop/ODE 50 Lessons Plan/lesson_46").exists():
        print("\nLesson 46 needs manual processing")

if __name__ == "__main__":
    main()