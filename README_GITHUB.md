# Student-Teacher Matching Automation System

A comprehensive Python-based system that intelligently matches students with teachers for 1:1 and group lessons, considering subjects, availability, and preferences.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](README.md)

## 🚀 Quick Start

### Option 1: Run the Jupyter Notebook (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/student-teacher-matching.git
cd student-teacher-matching

# Install dependencies
pip install -r requirements.txt

# Open Jupyter notebook
jupyter notebook student_teacher_matching.ipynb
```

### Option 2: Run the Python Script
```bash
# Clone and setup
git clone https://github.com/yourusername/student-teacher-matching.git
cd student-teacher-matching
pip install -r requirements.txt

# Run the system
python student_teacher_matcher.py

# Check generated output files
ls *.csv *.json
```

### Option 3: Quick Demo
```bash
python demo.py
```

## 📁 Project Structure

```
├── students.csv                    # Sample student data
├── teachers.csv                    # Sample teacher data
├── student_teacher_matching.ipynb  # Interactive Jupyter notebook
├── student_teacher_matcher.py      # Standalone Python script
├── demo.py                        # Quick demonstration
├── test_matcher.py               # Testing script
├── sample_schedule_output.csv     # Example output (CSV)
├── sample_schedule_output.json    # Example output (JSON)
├── TECHNICAL_WRITEUP.md          # Detailed documentation
├── requirements.txt               # Dependencies
├── .gitignore                     # Git ignore rules
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

### Example Output
```csv
student_id,student_name,teacher_id,teacher_name,time_slot,lesson_type,subjects,compatibility_score
9,Chioma,4,Ms. Sarah,Morning,Group,"Math, English",0.667
5,Kemi,1,Mr. Obi,Morning,1:1,Math,0.5
1,Ada,4,Ms. Sarah,Morning,Group,"Math, English",0.667
```

## 🛠️ Technical Details

- **Language**: Python 3.8+
- **Key Libraries**: pandas, numpy, matplotlib, seaborn
- **Algorithm**: Greedy matching with Jaccard similarity scoring
- **Time Complexity**: O(n × m × s × t + k log k)
- **Scalable**: Handles 100s of students/teachers efficiently

## 📈 System Architecture

The system consists of several key components:

1. **Data Processing Module** - Handles loading, cleaning, and standardization
2. **Matching Algorithm** - Implements intelligent matching logic
3. **Schedule Generator** - Creates optimized schedules
4. **Evaluation Engine** - Provides comprehensive metrics
5. **Visualization Suite** - Generates analysis charts
6. **Feedback System** - Simulates and analyzes user feedback

## 🧪 Testing

Run the test suite to validate the system:

```bash
python test_matcher.py
```

## 📖 Documentation

- **[Technical Write-up](TECHNICAL_WRITEUP.md)** - Detailed technical documentation
- **[Completion Report](FINAL_COMPLETION_REPORT.md)** - Project summary and results

## 🔧 System Requirements

- Python 3.8 or higher
- 50MB free disk space
- RAM: 512MB minimum (for datasets up to 1000 students/teachers)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
```bash
# Clone the repo
git clone https://github.com/yourusername/student-teacher-matching.git
cd student-teacher-matching

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Built as a practical demonstration of algorithmic problem-solving
- Designed for educational institutions worldwide
- Implements industry best practices for production software

## 📞 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Project Link: [https://github.com/yourusername/student-teacher-matching](https://github.com/yourusername/student-teacher-matching)

---

**Built with ❤️ for educational institutions worldwide**
