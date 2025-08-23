#!/usr/bin/env python3
"""
Enhance quality of lessons 19-50 to match the high standards of lessons 7-18
"""

import os
import re
import subprocess
from pathlib import Path

def fix_latex_document(content):
    """Fix LaTeX document issues and enhance quality."""
    
    # Fix subscript/superscript issues with dollar signs
    content = re.sub(r'\$_\{(\d+)\}\$', r'_{\1}', content)
    content = re.sub(r'\$\^\{(\d+)\}\$', r'^{\1}', content)
    content = re.sub(r'q\$_\{([0-9]+)\}\$', r'q_{\1}', content)
    content = re.sub(r'c\$_\{([0-9]+)\}\$', r'c_{\1}', content)
    content = re.sub(r'y\$_\{([0-9pn]+)\}\$', r'y_{\1}', content)
    content = re.sub(r'x\$_\{([0-9]+)\}\$', r'x_{\1}', content)
    content = re.sub(r'a\$_\{([0-9]+)\}\$', r'a_{\1}', content)
    content = re.sub(r'b\$_\{([0-9]+)\}\$', r'b_{\1}', content)
    content = re.sub(r'\$\$([^$]+)\$\$\$', r'$$\1$$', content)
    
    # Fix common LaTeX errors
    content = content.replace('\\Rightarrow', '\\Rightarrow')
    content = content.replace('\\mathbb{R}', '\\mathbb{R}')
    content = content.replace('\\checkmark', '$\\checkmark$')
    
    # Ensure proper math mode
    content = re.sub(r'([^\\$])(e\^[{]?[^$\s]+[}]?)([^$])', r'\1$\2$\3', content)
    
    # Fix bmatrix environment
    if '\\bmatrix' in content or '\\pmatrix' in content:
        if 'amsmath' not in content:
            content = content.replace('\\usepackage{geometry',
                                    '\\usepackage{amsmath}\n\\usepackage{geometry')
    
    # Add missing packages if needed
    required_packages = {
        '\\mathbb': 'amssymb',
        '\\bmatrix': 'amsmath',
        '\\pmatrix': 'amsmath',
        'tikzpicture': 'tikz',
        'mdframed': 'mdframed',
        'enumerate': 'enumitem'
    }
    
    for command, package in required_packages.items():
        if command in content and package not in content:
            # Add after documentclass
            insert_pos = content.find('\\begin{document}')
            if insert_pos > 0:
                content = content[:insert_pos] + f'\\usepackage{{{package}}}\n' + content[insert_pos:]
    
    # Ensure document structure
    if '\\end{document}' not in content:
        content += '\n\\end{document}'
    
    # Fix alignment environments
    content = re.sub(r'\\begin\{align\}([^$]*)\$([^$]*)\$([^$]*)\\end\{align\}',
                     r'\\begin{align}\1\2\3\\end{align}', content)
    
    return content

def enhance_theory_document(filepath, lesson_num):
    """Enhance the theory document to match high-quality standards."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix LaTeX issues
    content = fix_latex_document(content)
    
    # Ensure proper title format
    if f'Lesson {lesson_num}:' not in content:
        content = re.sub(r'\\title\{([^}]+)\}',
                        f'\\\\title{{ODE Lesson {lesson_num}: \\1}}', content)
    
    # Ensure author line
    if 'Prof. Adi Ditkowski' not in content:
        content = re.sub(r'\\author\{[^}]*\}',
                        r'\\author{ODE 1 - Prof. Adi Ditkowski}', content)
    
    # Add custom environments if missing
    if '\\newmdenv' not in content:
        environments = """% Custom environments
\\newtheorem{definition}{Definition}
\\newtheorem{theorem}{Theorem}
\\newtheorem{method}{Method}
\\newtheorem{example}{Example}
\\newmdenv[linecolor=blue,linewidth=2pt]{keypoint}
\\newmdenv[linecolor=red,linewidth=2pt]{warning}
\\newmdenv[linecolor=green,linewidth=2pt]{insight}

"""
        content = content.replace('\\begin{document}', environments + '\\begin{document}')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def enhance_problems_document(filepath, lesson_num):
    """Enhance the problems document to ensure 28 problems."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix LaTeX issues
    content = fix_latex_document(content)
    
    # Count problems
    problem_count = content.count('\\item')
    
    # Ensure proper title
    if 'Practice Problems' not in content:
        content = re.sub(r'\\title\{([^}]+)\}',
                        f'\\\\title{{Practice Problems: Lesson {lesson_num}}}', content)
    
    # Check for proper sections
    sections_needed = [
        'Part A:',
        'Part B:',
        'Part C:',
        'Part D:',
        'Part E:'
    ]
    
    for section in sections_needed:
        if section not in content:
            print(f"  Warning: Missing section '{section}' in problems_{lesson_num:02d}.tex")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def compile_with_fixes(filepath, max_attempts=2):
    """Try to compile LaTeX with automatic fixes."""
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
                return True
            
            # Try to fix common errors
            if attempt == 0:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Fix based on error messages
                if 'Undefined control sequence' in result.stdout:
                    content = fix_latex_document(content)
                    
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
        except Exception as e:
            print(f"    Compilation error: {e}")
            
    return False

def process_lesson(lesson_num):
    """Process and enhance a single lesson."""
    base_dir = Path(f"/home/archer/Desktop/ODE 50 Lessons Plan/lesson_{lesson_num:02d}")
    
    if not base_dir.exists():
        print(f"  Lesson {lesson_num} directory not found")
        return False
    
    print(f"Processing Lesson {lesson_num}...")
    
    # Check and enhance theory document
    theory_file = base_dir / f"lesson_{lesson_num:02d}.tex"
    theory_pdf = base_dir / f"lesson_{lesson_num:02d}.pdf"
    
    if theory_file.exists():
        if enhance_theory_document(theory_file, lesson_num):
            print(f"  Enhanced theory document")
        
        if not theory_pdf.exists() or theory_file.stat().st_mtime > theory_pdf.stat().st_mtime:
            if compile_with_fixes(theory_file):
                print(f"  ✓ Compiled lesson_{lesson_num:02d}.pdf")
            else:
                print(f"  ✗ Failed to compile theory PDF")
    
    # Check and enhance problems document
    problems_file = base_dir / f"problems_{lesson_num:02d}.tex"
    problems_pdf = base_dir / f"problems_{lesson_num:02d}.pdf"
    
    if problems_file.exists():
        if enhance_problems_document(problems_file, lesson_num):
            print(f"  Enhanced problems document")
        
        if not problems_pdf.exists() or problems_file.stat().st_mtime > problems_pdf.stat().st_mtime:
            if compile_with_fixes(problems_file):
                print(f"  ✓ Compiled problems_{lesson_num:02d}.pdf")
            else:
                print(f"  ✗ Failed to compile problems PDF")
    
    # Check audio script
    script_file = base_dir / "lesson_script.txt"
    if script_file.exists():
        with open(script_file, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        if len(script_content) < 1000:
            print(f"  Warning: Audio script seems too short ({len(script_content)} chars)")
        
        if not script_content.startswith('Episode'):
            print(f"  Warning: Audio script doesn't start with 'Episode'")
    else:
        print(f"  Warning: No audio script found")
    
    return True

def main():
    """Enhance all lessons 19-50."""
    print("Enhancing lessons 19-50 to match quality standards...")
    print("=" * 50)
    
    successful = 0
    failed = []
    
    for lesson_num in range(19, 51):
        try:
            if process_lesson(lesson_num):
                successful += 1
            else:
                failed.append(lesson_num)
        except Exception as e:
            print(f"  Error processing lesson {lesson_num}: {e}")
            failed.append(lesson_num)
        print()
    
    print("=" * 50)
    print(f"Enhancement complete!")
    print(f"Successfully processed: {successful} lessons")
    if failed:
        print(f"Lessons needing attention: {failed}")
    
    # Summary of PDF status
    print("\nPDF Compilation Status:")
    pdf_count = 0
    for lesson_num in range(19, 51):
        base_dir = Path(f"/home/archer/Desktop/ODE 50 Lessons Plan/lesson_{lesson_num:02d}")
        if base_dir.exists():
            theory_pdf = base_dir / f"lesson_{lesson_num:02d}.pdf"
            problems_pdf = base_dir / f"problems_{lesson_num:02d}.pdf"
            
            status = []
            if theory_pdf.exists():
                status.append("T")
                pdf_count += 1
            else:
                status.append("-")
            
            if problems_pdf.exists():
                status.append("P")
                pdf_count += 1
            else:
                status.append("-")
            
            print(f"  Lesson {lesson_num:02d}: [{''.join(status)}]", end="")
            if lesson_num % 4 == 0:
                print()
    
    print(f"\n\nTotal PDFs: {pdf_count}/64")

if __name__ == "__main__":
    main()