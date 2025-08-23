#!/usr/bin/env python3
"""
Script to fix common LaTeX issues in ODE lessons 19-50
"""

import os
import re
import glob

def fix_latex_issues(file_path):
    """Fix common LaTeX issues in a single file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remove nicematrix package
    content = re.sub(r'\\usepackage\{nicematrix\}\s*\n?', '', content)
    
    # Fix title format - add ODE prefix if missing
    content = re.sub(r'\\title\{Lesson (\d+):', r'\\title{ODE Lesson \1:', content)
    
    # Fix malformed subscripts: $_{n}$ -> _{n}
    content = re.sub(r'\$\_{([^}]+)}\$', r'_{\1}', content)
    content = re.sub(r'\$\^{([^}]+)}\$', r'^{\1}', content)
    
    # Fix malformed exponentials: $e^{-t$}$ -> e^{-t}
    content = re.sub(r'\$e\^\{([^}]+)\$\}\$', r'e^{\1}', content)
    content = re.sub(r'\$([^$]*)\$e\^\{([^}]+)\$\}\$', r'\1 e^{\2}', content)
    
    # Fix mixed math modes in matrices and equations
    content = re.sub(r'\$([^$]*e\^[^$]*)\$', lambda m: m.group(1), content)
    
    # Fix \times outside math mode in example titles
    content = re.sub(r'\\begin\{example\}\[(\d+)\\times(\d+)', r'\\begin{example}[\1$\\times$\2', content)
    
    # Fix complex malformed expressions
    content = re.sub(r'\$([^$]*)\$_\{([^}]+)\}\$([^$]*)\$', r'\1_{\2}\3', content)
    
    # Fix exponential expressions in matrices
    content = re.sub(r'(\d+)\$e\^\{([^}]+)\}\$', r'\1e^{\2}', content)
    content = re.sub(r'([+-])\$e\^\{([^}]+)\}\$', r'\1e^{\2}', content)
    
    # Fix plain exponentials not in math mode
    content = re.sub(r'([^$\\\w])e\^\{([^}]+)\}([^$\\\w])', r'\1$e^{\2}$\3', content)
    content = re.sub(r'W\(t\) = ([^$\n]+)e\^\{([^}]+)\}', r'W(t) = $\1e^{\2}$', content)
    content = re.sub(r'W\(0\) = (\d+)\$', r'W(0) = $\1$', content)
    
    return content, original_content != content

def process_lessons():
    """Process all lesson files in lessons 19-50"""
    base_dir = "/home/archer/Desktop/ODE 50 Lessons Plan"
    modified_files = []
    
    for lesson_num in range(19, 51):
        lesson_dir = os.path.join(base_dir, f"lesson_{lesson_num:02d}")
        if not os.path.exists(lesson_dir):
            continue
            
        tex_file = os.path.join(lesson_dir, f"lesson_{lesson_num:02d}.tex")
        if os.path.exists(tex_file):
            content, was_modified = fix_latex_issues(tex_file)
            if was_modified:
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                modified_files.append(tex_file)
                print(f"Fixed {tex_file}")
    
    return modified_files

if __name__ == "__main__":
    modified = process_lessons()
    print(f"\nTotal files modified: {len(modified)}")
    for f in modified:
        print(f"  - {f}")