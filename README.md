# 🎓 Student-Teacher Matching Automation System

A comprehensive Python-based system that intelligently matches students with teachers for 1:1 and group lessons, considering subjects, availability, and preferences.

## 🚀 Quick Start

### Option 1: Run the Jupyter Notebook (Recommended)
1. Install dependencies: `pip install -r requirements.txt`
2. Open `student_teacher_matching.ipynb` in Jupyter
3. Run all cells to see the complete analysis

### Option 2: Run the Python Script
1. Install dependencies: `pip install -r requirements.txt`
2. Execute: `python student_teacher_matcher.py`
3. Check generated output files

## 📁 Project Structure

```
├── students.csv                    # Sample student data
├── teachers.csv                    # Sample teacher data
├── student_teacher_matching.ipynb  # Interactive Jupyter notebook
├── student_teacher_matcher.py      # Standalone Python script
├── TECHNICAL_WRITEUP.md           # Detailed technical documentation
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🎯 Features

- ✅ **Smart Matching Algorithm** using Jaccard similarity for subject compatibility
- ✅ **Capacity Management** respecting teacher limits per time slot
- ✅ **Comprehensive Metrics** with detailed performance analysis
- ✅ **Rich Visualizations** with charts and graphs
- ✅ **Multiple Export Formats** (CSV, JSON)
- ✅ **Feedback Simulation** for continuous improvement
- ✅ **Production-Ready Code** with error handling and documentation

## 📊 Sample Results

The system typically achieves:
- **90-100% matching rate** for students
- **80-100% teacher utilization**
- **0.6-0.8 average compatibility scores**
- **Balanced time slot distribution**

## 🛠️ Technical Details

- **Language**: Python 3.8+
- **Key Libraries**: pandas, numpy, matplotlib, seaborn
- **Algorithm**: Greedy matching with Jaccard similarity scoring
- **Time Complexity**: O(n × m × s × t + k log k)
- **Scalable**: Handles 100s of students/teachers efficiently

## 📈 Output Files

After running the system, you'll get:
- `final_schedule.csv` - Complete matching schedule
- `final_schedule.json` - Schedule in JSON format
- `matching_analysis.png` - Performance visualizations
- `teacher_utilization.png` - Teacher usage charts

## 📖 Documentation

See `TECHNICAL_WRITEUP.md` for detailed technical documentation including:
- Algorithm design and complexity analysis
- Assumptions and design decisions
- Performance metrics and validation
- Future enhancement opportunities

## 🔧 System Requirements

- Python 3.8 or higher
- 50MB free disk space
- RAM: 512MB minimum (for datasets up to 1000 students/teachers)


