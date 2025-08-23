# ODE 50 Lessons Plan - Processing Guide

## Project Overview
This project contains 50 comprehensive ODE lessons designed for Prof. Adi Ditkowski's course. Each lesson includes:
- Audio script (lesson_script.txt)
- Theory document (lesson_XX.tex → lesson_XX.pdf)
- Practice problems (problems_XX.tex → problems_XX.pdf)

## Completed Lessons
- ✅ Lesson 07: Non-Unique Solutions
- ✅ Lesson 08: Parameter-Dependent Existence Problems
- ✅ Lesson 09: Direction Fields and Isoclines
- ✅ Lesson 10: Qualitative Analysis Without Solving

## Systematic Processing Plan for Lessons 11-18

### Lesson Structure Template
Each lesson follows this consistent structure:
1. **lesson_script.txt**: Audio-friendly conversational script
2. **lesson_XX.tex**: Formal theory with definitions, theorems, examples
3. **problems_XX.tex**: 28 practice problems (Basic, Core, Applications, Advanced, Exam-style)

### Processing Steps for Each Lesson

#### Step 1: Extract Content from Raw Text
- Read `lesson_XX/lesson_XX_raw.txt`
- Identify three main sections:
  1. Episode XX: [Title] (audio script)
  2. Theory document content
  3. Practice problems content

#### Step 2: Create Audio Script
- Extract Episode section → `lesson_script.txt`
- Keep conversational tone
- Preserve Prof. Ditkowski references
- Include memory tricks and exam tips

#### Step 3: Create Theory LaTeX Document
- Structure: Title, Definitions, Theorems, Methods, Examples
- Add custom environments (keypoint, warning, insight)
- Include TikZ diagrams where applicable
- Use consistent formatting from lessons 07-10

#### Step 4: Create Problems LaTeX Document
- Part A: Basic Concepts (6 problems)
- Part B: Core Techniques (6 problems)
- Part C: Applications (5 problems)
- Part D: Advanced/Theoretical (5 problems)
- Part E: Exam-Style Questions (6 problems)
- Include Answer Key with hints

#### Step 5: Compile PDFs
```bash
cd lesson_XX
pdflatex lesson_XX.tex
pdflatex problems_XX.tex
```

#### Step 6: Verify Output
- Check all files created
- Ensure PDFs compile without errors
- Verify problem count (28 total)

### Lessons to Process

#### Lesson 11: Systems of First-Order ODEs
- Topics: Converting higher-order to systems, matrix form, phase portraits
- Key focus: System representation and basic analysis

#### Lesson 12: Linear Systems - Eigenvalue Method
- Topics: Eigenvalues/eigenvectors, fundamental matrix, matrix exponential
- Key focus: Solution techniques for linear systems

#### Lesson 13: Phase Portraits for 2x2 Systems
- Topics: Classification (nodes, saddles, centers, spirals), stability
- Key focus: Geometric behavior visualization

#### Lesson 14: Nonhomogeneous Linear Systems
- Topics: Variation of parameters, undetermined coefficients for systems
- Key focus: Forcing terms in systems

#### Lesson 15: Fundamental Matrices and Matrix Exponentials
- Topics: Properties, computation methods, applications
- Key focus: Advanced linear algebra techniques

#### Lesson 16: Nonlinear Systems and Stability
- Topics: Linearization, Lyapunov methods, limit cycles
- Key focus: Local vs global behavior

#### Lesson 17: Applications - Coupled Oscillators
- Topics: Mechanical/electrical systems, normal modes
- Key focus: Physical modeling

#### Lesson 18: Applications - Population Dynamics
- Topics: Predator-prey, competition, cooperation models
- Key focus: Biological modeling

### Automation Commands

#### Extract all lessons (11-18):
```bash
for i in {11..18}; do
    echo "Processing Lesson $i"
    cd lesson_$i
    # Process raw text into three files
    # Compile LaTeX documents
    pdflatex lesson_$i.tex
    pdflatex problems_$i.tex
    cd ..
done
```

### Quality Checklist
- [ ] Audio script maintains conversational tone
- [ ] Theory document includes all mathematical rigor
- [ ] Problems span difficulty levels appropriately
- [ ] PDFs compile without errors
- [ ] File naming convention consistent
- [ ] Git commits after each lesson

### Git Workflow
```bash
# After processing each lesson
git add lesson_XX/
git commit -m "Add Lesson XX: [Title] - complete with PDFs"
```

### Common LaTeX Packages Required
```latex
\usepackage{amsmath, amssymb, amsthm}
\usepackage{tikz, pgfplots}
\usepackage{geometry, enumitem}
\usepackage{mdframed, xcolor}
```

### Notes
- Maintain consistency with Prof. Ditkowski's teaching style
- Include exam-specific tips and warnings
- Use memory aids and mnemonics where helpful
- Ensure mathematical accuracy while keeping accessibility

## Next Steps
1. Process Lesson 11 following the template
2. Continue sequentially through Lesson 18
3. Final review of all lessons for consistency
4. Push complete repository to GitHub