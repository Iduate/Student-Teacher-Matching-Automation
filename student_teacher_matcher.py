#!/usr/bin/env python3
"""
Student-Teacher Matching Automation System

A comprehensive system that matches students with teachers for 1:1 and group lessons,
taking into account subjects, availability, and preferences.

Author: AI Assistant
Date: September 2025
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple, Set
import warnings
warnings.filterwarnings('ignore')

class StudentTeacherMatcher:
    """
    Main class for student-teacher matching automation system.
    
    This class handles data preprocessing, matching algorithm implementation,
    schedule generation, and performance evaluation.
    """
    
    def __init__(self):
        """Initialize the matcher with empty data structures."""
        self.students_df = None
        self.teachers_df = None
        self.processed_students = None
        self.processed_teachers = None
        self.schedule = []
        self.metrics = {}
        self.feedback_data = []
    
    def load_data(self, students_file: str, teachers_file: str) -> bool:
        """
        Load student and teacher data from CSV files.
        
        Args:
            students_file: Path to students CSV file
            teachers_file: Path to teachers CSV file
            
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        try:
            self.students_df = pd.read_csv(students_file)
            self.teachers_df = pd.read_csv(teachers_file)
            print(f"✅ Loaded {len(self.students_df)} students and {len(self.teachers_df)} teachers")
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def display_data_info(self):
        """Display information about the loaded data."""
        print("\n" + "="*50)
        print("                DATA OVERVIEW")
        print("="*50)
        
        print("\n📚 STUDENTS DATA:")
        print(self.students_df.head())
        print(f"\nShape: {self.students_df.shape}")
        print(f"Missing values:\n{self.students_df.isnull().sum()}")
        
        print("\n👨‍🏫 TEACHERS DATA:")
        print(self.teachers_df.head())
        print(f"\nShape: {self.teachers_df.shape}")
        print(f"Missing values:\n{self.teachers_df.isnull().sum()}")
    
    def preprocess_data(self):
        """
        Clean and standardize the data for processing.
        
        Returns:
            tuple: (processed_students_df, processed_teachers_df)
        """
        def standardize_time_slots(time_str):
            """Standardize time slot strings."""
            if pd.isna(time_str):
                return []
            slots = [slot.strip().title() for slot in str(time_str).split(',')]
            return [slot for slot in slots if slot in ['Morning', 'Afternoon', 'Evening']]
        
        def standardize_subjects(subject_str):
            """Standardize subject strings."""
            if pd.isna(subject_str):
                return []
            subjects = [subj.strip().title() for subj in str(subject_str).split(',')]
            return subjects
        
        # Process students data
        students_processed = self.students_df.copy()
        students_processed['time_slots'] = students_processed['preferred_time_slots'].apply(standardize_time_slots)
        students_processed['subject_list'] = students_processed['subjects'].apply(standardize_subjects)
        
        # Process teachers data
        teachers_processed = self.teachers_df.copy()
        teachers_processed['time_slots'] = teachers_processed['available_time_slots'].apply(standardize_time_slots)
        teachers_processed['subject_list'] = teachers_processed['subjects'].apply(standardize_subjects)
        
        # Handle missing values
        students_processed = students_processed.dropna(subset=['student_id', 'name'])
        teachers_processed = teachers_processed.dropna(subset=['teacher_id', 'name'])
        teachers_processed['max_students_per_slot'] = teachers_processed['max_students_per_slot'].fillna(2)
        
        self.processed_students = students_processed
        self.processed_teachers = teachers_processed
        
        print("✅ Data preprocessing completed!")
        print(f"Processed {len(self.processed_students)} students and {len(self.processed_teachers)} teachers")
        
        return students_processed, teachers_processed
    
    def calculate_subject_compatibility(self, student_subjects: List[str], teacher_subjects: List[str]) -> float:
        """
        Calculate compatibility score between student and teacher subjects using Jaccard similarity.
        
        Args:
            student_subjects: List of student's subjects
            teacher_subjects: List of teacher's subjects
            
        Returns:
            float: Compatibility score between 0 and 1
        """
        if not student_subjects or not teacher_subjects:
            return 0.0
        
        student_set = set(student_subjects)
        teacher_set = set(teacher_subjects)
        
        intersection = student_set.intersection(teacher_set)
        union = student_set.union(teacher_set)
        
        return len(intersection) / len(union) if union else 0.0
    
    def find_common_time_slots(self, student_slots: List[str], teacher_slots: List[str]) -> List[str]:
        """Find common available time slots between student and teacher."""
        return list(set(student_slots).intersection(set(teacher_slots)))
    
    def create_matches(self):
        """
        Create student-teacher matches based on subjects and availability.
        
        Returns:
            list: List of match dictionaries
        """
        matches = []
        teacher_capacity = {}
        
        # Initialize teacher capacity tracking
        for _, teacher in self.processed_teachers.iterrows():
            teacher_id = teacher['teacher_id']
            teacher_capacity[teacher_id] = {}
            for time_slot in teacher['time_slots']:
                teacher_capacity[teacher_id][time_slot] = teacher['max_students_per_slot']
        
        # Create potential matches with scores
        potential_matches = []
        
        for _, student in self.processed_students.iterrows():
            student_id = student['student_id']
            student_subjects = student['subject_list']
            student_time_slots = student['time_slots']
            
            for _, teacher in self.processed_teachers.iterrows():
                teacher_id = teacher['teacher_id']
                teacher_subjects = teacher['subject_list']
                teacher_time_slots = teacher['time_slots']
                
                # Calculate compatibility and find common slots
                subject_score = self.calculate_subject_compatibility(student_subjects, teacher_subjects)
                common_slots = self.find_common_time_slots(student_time_slots, teacher_time_slots)
                
                if subject_score > 0 and common_slots:
                    for time_slot in common_slots:
                        potential_matches.append({
                            'student_id': student_id,
                            'teacher_id': teacher_id,
                            'time_slot': time_slot,
                            'subject_score': subject_score,
                            'common_subjects': list(set(student_subjects).intersection(set(teacher_subjects)))
                        })
        
        # Sort by compatibility score (descending)
        potential_matches.sort(key=lambda x: x['subject_score'], reverse=True)
        
        # Assign matches respecting capacity constraints
        assigned_students = set()
        
        for match in potential_matches:
            student_id = match['student_id']
            teacher_id = match['teacher_id']
            time_slot = match['time_slot']
            
            # Skip if student already assigned
            if student_id in assigned_students:
                continue
            
            # Check teacher capacity
            if teacher_capacity[teacher_id][time_slot] > 0:
                # Determine lesson type
                current_capacity = teacher_capacity[teacher_id][time_slot]
                max_capacity = self.processed_teachers[
                    self.processed_teachers['teacher_id'] == teacher_id
                ]['max_students_per_slot'].iloc[0]
                
                lesson_type = "1:1" if max_capacity == 1 or current_capacity == max_capacity else "Group"
                
                # Create final match
                final_match = {
                    'student_id': student_id,
                    'teacher_id': teacher_id,
                    'time_slot': time_slot,
                    'lesson_type': lesson_type,
                    'subjects': ', '.join(match['common_subjects']),
                    'compatibility_score': round(match['subject_score'], 3)
                }
                
                matches.append(final_match)
                assigned_students.add(student_id)
                teacher_capacity[teacher_id][time_slot] -= 1
        
        self.schedule = matches
        print(f"✅ Created {len(matches)} student-teacher matches")
        return matches
    
    def generate_schedule_dataframe(self) -> pd.DataFrame:
        """Generate a detailed schedule DataFrame with student and teacher names."""
        if not self.schedule:
            return pd.DataFrame()
        
        schedule_df = pd.DataFrame(self.schedule)
        
        # Add names
        student_names = self.processed_students.set_index('student_id')['name'].to_dict()
        teacher_names = self.processed_teachers.set_index('teacher_id')['name'].to_dict()
        
        schedule_df['student_name'] = schedule_df['student_id'].map(student_names)
        schedule_df['teacher_name'] = schedule_df['teacher_id'].map(teacher_names)
        
        # Reorder columns
        column_order = ['student_id', 'student_name', 'teacher_id', 'teacher_name', 
                       'time_slot', 'lesson_type', 'subjects', 'compatibility_score']
        
        return schedule_df[column_order]
    
    def export_schedule(self, format_type: str = 'csv', filename: str = None) -> str:
        """
        Export the schedule to CSV or JSON format.
        
        Args:
            format_type: 'csv' or 'json'
            filename: Optional custom filename
            
        Returns:
            str: Generated filename
        """
        if not self.schedule:
            print("❌ No schedule to export. Please create matches first.")
            return ""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type.lower() == 'csv':
            filename = filename or f'schedule_{timestamp}.csv'
            schedule_df = self.generate_schedule_dataframe()
            schedule_df.to_csv(filename, index=False)
            print(f"📁 Schedule exported to {filename}")
            
        elif format_type.lower() == 'json':
            filename = filename or f'schedule_{timestamp}.json'
            with open(filename, 'w') as f:
                json.dump(self.schedule, f, indent=2)
            print(f"📁 Schedule exported to {filename}")
        
        return filename
    
    def calculate_metrics(self) -> Dict:
        """Calculate comprehensive performance metrics for the matching system."""
        if not self.schedule:
            return {}
        
        total_students = len(self.processed_students)
        matched_students = len(set(match['student_id'] for match in self.schedule))
        total_teachers = len(self.processed_teachers)
        
        # Basic metrics
        metrics = {
            'total_students': total_students,
            'matched_students': matched_students,
            'unmatched_students': total_students - matched_students,
            'matching_rate': round((matched_students / total_students) * 100, 2),
            'total_lessons': len(self.schedule),
            'lesson_types': Counter(match['lesson_type'] for match in self.schedule)
        }
        
        # Teacher utilization
        teacher_usage = Counter(match['teacher_id'] for match in self.schedule)
        utilized_teachers = len(teacher_usage)
        
        metrics['teacher_utilization'] = {
            'total_teachers': total_teachers,
            'utilized_teachers': utilized_teachers,
            'utilization_rate': round((utilized_teachers / total_teachers) * 100, 2)
        }
        
        # Time slot distribution
        time_slot_distribution = Counter(match['time_slot'] for match in self.schedule)
        metrics['time_slot_distribution'] = dict(time_slot_distribution)
        
        # Compatibility scores
        compatibility_scores = [match['compatibility_score'] for match in self.schedule]
        metrics['average_compatibility_score'] = round(np.mean(compatibility_scores), 3)
        metrics['min_compatibility_score'] = round(min(compatibility_scores), 3)
        metrics['max_compatibility_score'] = round(max(compatibility_scores), 3)
        
        # Subject coverage
        all_subjects = set()
        for _, student in self.processed_students.iterrows():
            all_subjects.update(student['subject_list'])
        
        covered_subjects = set()
        for match in self.schedule:
            if match['subjects']:
                covered_subjects.update(match['subjects'].split(', '))
        
        metrics['subject_coverage'] = {
            'total_subjects': len(all_subjects),
            'covered_subjects': len(covered_subjects),
            'coverage_rate': round((len(covered_subjects) / len(all_subjects)) * 100, 2) if all_subjects else 0
        }
        
        self.metrics = metrics
        return metrics
    
    def print_metrics_report(self):
        """Print a detailed metrics report."""
        if not self.metrics:
            self.calculate_metrics()
        
        print("\n" + "="*60)
        print("         MATCHING SYSTEM PERFORMANCE REPORT")
        print("="*60)
        
        print(f"\n📊 STUDENT MATCHING:")
        print(f"   • Total Students: {self.metrics['total_students']}")
        print(f"   • Matched Students: {self.metrics['matched_students']}")
        print(f"   • Unmatched Students: {self.metrics['unmatched_students']}")
        print(f"   • Matching Rate: {self.metrics['matching_rate']}%")
        
        print(f"\n👩‍🏫 TEACHER UTILIZATION:")
        print(f"   • Total Teachers: {self.metrics['teacher_utilization']['total_teachers']}")
        print(f"   • Utilized Teachers: {self.metrics['teacher_utilization']['utilized_teachers']}")
        print(f"   • Utilization Rate: {self.metrics['teacher_utilization']['utilization_rate']}%")
        
        print(f"\n📚 LESSONS:")
        print(f"   • Total Lessons: {self.metrics['total_lessons']}")
        for lesson_type, count in self.metrics['lesson_types'].items():
            print(f"   • {lesson_type} Lessons: {count}")
        
        print(f"\n⏰ TIME SLOT DISTRIBUTION:")
        for time_slot, count in self.metrics['time_slot_distribution'].items():
            print(f"   • {time_slot}: {count} lessons")
        
        print(f"\n🎯 COMPATIBILITY SCORES:")
        print(f"   • Average: {self.metrics['average_compatibility_score']}")
        print(f"   • Range: {self.metrics['min_compatibility_score']} - {self.metrics['max_compatibility_score']}")
        
        print(f"\n📖 SUBJECT COVERAGE:")
        print(f"   • Total Subjects: {self.metrics['subject_coverage']['total_subjects']}")
        print(f"   • Covered Subjects: {self.metrics['subject_coverage']['covered_subjects']}")
        print(f"   • Coverage Rate: {self.metrics['subject_coverage']['coverage_rate']}%")
    
    def create_visualizations(self):
        """Create comprehensive visualizations for the matching results."""
        if not self.schedule or not self.metrics:
            print("❌ No data available for visualization")
            return
        
        # Set up the plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Student-Teacher Matching Analysis', fontsize=16, fontweight='bold')
        
        # 1. Matching Rate Pie Chart
        ax1 = axes[0, 0]
        labels = ['Matched', 'Unmatched']
        sizes = [self.metrics['matched_students'], self.metrics['unmatched_students']]
        colors = ['#2ecc71', '#e74c3c']
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Student Matching Rate')
        
        # 2. Time Slot Distribution
        ax2 = axes[0, 1]
        time_slots = list(self.metrics['time_slot_distribution'].keys())
        counts = list(self.metrics['time_slot_distribution'].values())
        bars = ax2.bar(time_slots, counts, color=['#3498db', '#f39c12', '#9b59b6'])
        ax2.set_title('Lessons by Time Slot')
        ax2.set_ylabel('Number of Lessons')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        # 3. Lesson Type Distribution
        ax3 = axes[1, 0]
        lesson_types = list(self.metrics['lesson_types'].keys())
        lesson_counts = list(self.metrics['lesson_types'].values())
        colors = ['#1abc9c', '#e67e22']
        ax3.pie(lesson_counts, labels=lesson_types, colors=colors, autopct='%1.1f%%', startangle=90)
        ax3.set_title('Lesson Type Distribution')
        
        # 4. Compatibility Score Distribution
        ax4 = axes[1, 1]
        scores = [match['compatibility_score'] for match in self.schedule]
        ax4.hist(scores, bins=10, color='#34495e', alpha=0.7, edgecolor='black')
        ax4.set_title('Compatibility Score Distribution')
        ax4.set_xlabel('Compatibility Score')
        ax4.set_ylabel('Number of Matches')
        ax4.axvline(self.metrics['average_compatibility_score'], color='red', 
                    linestyle='--', label=f'Mean: {self.metrics["average_compatibility_score"]}')
        ax4.legend()
        
        plt.tight_layout()
        plt.savefig('matching_analysis.png', dpi=300, bbox_inches='tight')
        print("📊 Saved matching_analysis.png")
        plt.show()
        
        # Create teacher utilization chart
        self._create_teacher_utilization_chart()
    
    def _create_teacher_utilization_chart(self):
        """Create a detailed chart showing teacher utilization."""
        teacher_usage = Counter(match['teacher_id'] for match in self.schedule)
        teacher_names = self.processed_teachers.set_index('teacher_id')['name'].to_dict()
        
        # Create data for all teachers
        all_teachers = []
        usage_counts = []
        
        for _, teacher in self.processed_teachers.iterrows():
            teacher_id = teacher['teacher_id']
            all_teachers.append(teacher_names[teacher_id])
            usage_counts.append(teacher_usage.get(teacher_id, 0))
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(all_teachers, usage_counts, 
                       color=['#2ecc71' if count > 0 else '#e74c3c' for count in usage_counts])
        plt.title('Teacher Utilization - Number of Students Assigned', fontsize=14, fontweight='bold')
        plt.xlabel('Teachers')
        plt.ylabel('Number of Students')
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('teacher_utilization.png', dpi=300, bbox_inches='tight')
        print("📊 Saved teacher_utilization.png")
        plt.show()
    
    def simulate_feedback(self, positive_rate: float = 0.8):
        """
        Simulate feedback for the matching system.
        
        Args:
            positive_rate: Expected rate of positive feedback
            
        Returns:
            list: Feedback data
        """
        if not self.schedule:
            print("❌ No matches to provide feedback for")
            return []
        
        feedback_data = []
        
        for match in self.schedule:
            # Base satisfaction on compatibility score with some randomness
            base_satisfaction = match['compatibility_score']
            random_factor = np.random.normal(0, 0.1)
            final_satisfaction = max(0, min(1, base_satisfaction + random_factor))
            
            # Convert to 1-5 rating scale
            rating = max(1, min(5, int(final_satisfaction * 5)))
            
            feedback = {
                'student_id': match['student_id'],
                'teacher_id': match['teacher_id'],
                'time_slot': match['time_slot'],
                'rating': rating,
                'satisfaction_score': round(final_satisfaction, 3),
                'feedback_positive': rating >= 4
            }
            
            feedback_data.append(feedback)
        
        self.feedback_data = feedback_data
        
        # Calculate feedback metrics
        avg_rating = np.mean([f['rating'] for f in feedback_data])
        positive_feedback_rate = sum(f['feedback_positive'] for f in feedback_data) / len(feedback_data)
        
        print(f"\n🔄 FEEDBACK SIMULATION RESULTS:")
        print(f"   • Average Rating: {avg_rating:.2f}/5.0")
        print(f"   • Positive Feedback Rate: {positive_feedback_rate:.1%}")
        
        return feedback_data
    
    def analyze_feedback_trends(self):
        """Analyze feedback trends to improve future matching."""
        if not self.feedback_data:
            print("❌ No feedback data available")
            return None
        
        feedback_df = pd.DataFrame(self.feedback_data)
        
        # Analyze by teacher
        teacher_feedback = feedback_df.groupby('teacher_id').agg({
            'rating': ['mean', 'count'],
            'satisfaction_score': 'mean'
        }).round(2)
        
        print("\n📈 TEACHER PERFORMANCE ANALYSIS:")
        teacher_names = self.processed_teachers.set_index('teacher_id')['name'].to_dict()
        
        for teacher_id in teacher_feedback.index:
            avg_rating = teacher_feedback.loc[teacher_id, ('rating', 'mean')]
            num_students = teacher_feedback.loc[teacher_id, ('rating', 'count')]
            teacher_name = teacher_names.get(teacher_id, f'Teacher {teacher_id}')
            print(f"   • {teacher_name}: {avg_rating}/5.0 (from {num_students} students)")
        
        # Analyze by time slot
        timeslot_feedback = feedback_df.groupby('time_slot')['rating'].mean().round(2)
        
        print("\n⏰ TIME SLOT SATISFACTION:")
        for time_slot, avg_rating in timeslot_feedback.items():
            print(f"   • {time_slot}: {avg_rating}/5.0")
        
        return feedback_df
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report."""
        print("\n" + "="*70)
        print("           STUDENT-TEACHER MATCHING SYSTEM")
        print("                 SUMMARY REPORT")
        print("="*70)
        
        print(f"\n🎯 SYSTEM PERFORMANCE OVERVIEW:")
        print(f"   ✓ Successfully matched {self.metrics['matched_students']}/{self.metrics['total_students']} students ({self.metrics['matching_rate']}%)")
        print(f"   ✓ Utilized {self.metrics['teacher_utilization']['utilized_teachers']}/{self.metrics['teacher_utilization']['total_teachers']} teachers ({self.metrics['teacher_utilization']['utilization_rate']}%)")
        print(f"   ✓ Created {self.metrics['total_lessons']} total lessons")
        print(f"   ✓ Average compatibility score: {self.metrics['average_compatibility_score']}")
        
        if self.feedback_data:
            avg_rating = np.mean([f['rating'] for f in self.feedback_data])
            print(f"   ✓ Average satisfaction rating: {avg_rating:.2f}/5.0")
        
        print(f"\n📊 KEY INSIGHTS:")
        
        # Most popular time slot
        popular_slot = max(self.metrics['time_slot_distribution'], 
                          key=self.metrics['time_slot_distribution'].get)
        print(f"   • Most popular time slot: {popular_slot} ({self.metrics['time_slot_distribution'][popular_slot]} lessons)")
        
        # Lesson type breakdown
        for lesson_type, count in self.metrics['lesson_types'].items():
            percentage = (count / self.metrics['total_lessons']) * 100
            print(f"   • {lesson_type} lessons: {count} ({percentage:.1f}%)")
        
        # Subject coverage
        coverage_rate = self.metrics['subject_coverage']['coverage_rate']
        print(f"   • Subject coverage: {coverage_rate}%")
        
        print(f"\n💡 RECOMMENDATIONS:")
        
        if self.metrics['unmatched_students'] > 0:
            print(f"   1. Consider adding more teachers or expanding time slots for {self.metrics['unmatched_students']} unmatched students")
        
        if self.metrics['teacher_utilization']['utilization_rate'] < 100:
            unused_teachers = (self.metrics['teacher_utilization']['total_teachers'] - 
                              self.metrics['teacher_utilization']['utilized_teachers'])
            print(f"   2. {unused_teachers} teachers are underutilized - consider adjusting availability")
        
        if coverage_rate < 100:
            print(f"   3. Some subjects need additional teacher coverage")
        
        if self.metrics['average_compatibility_score'] < 0.5:
            print(f"   4. Consider expanding teacher subject expertise")
        
        print("="*70)

def main():
    """Main function to run the student-teacher matching system."""
    print("🎓 Student-Teacher Matching Automation System")
    print("=" * 50)
    
    # Initialize the system
    matcher = StudentTeacherMatcher()
    
    # Load data
    if not matcher.load_data('students.csv', 'teachers.csv'):
        print("❌ Failed to load data. Exiting.")
        return
    
    # Display data overview
    matcher.display_data_info()
    
    # Preprocess data
    matcher.preprocess_data()
    
    # Create matches
    matches = matcher.create_matches()
    
    if not matches:
        print("❌ No matches could be created. Please check your data.")
        return
    
    # Display schedule
    print("\n📅 GENERATED SCHEDULE:")
    schedule_df = matcher.generate_schedule_dataframe()
    print(schedule_df.to_string(index=False))
    
    # Export schedule
    csv_file = matcher.export_schedule('csv', 'final_schedule.csv')
    json_file = matcher.export_schedule('json', 'final_schedule.json')
    
    # Calculate and display metrics
    matcher.calculate_metrics()
    matcher.print_metrics_report()
    
    # Create visualizations
    try:
        matcher.create_visualizations()
    except Exception as e:
        print(f"⚠️ Could not create visualizations: {e}")
    
    # Simulate feedback
    matcher.simulate_feedback()
    matcher.analyze_feedback_trends()
    
    # Generate summary report
    matcher.generate_summary_report()
    
    print("\n✅ Student-Teacher Matching System completed successfully!")
    print(f"📁 Check the generated files: {csv_file}, {json_file}")

if __name__ == "__main__":
    main()
