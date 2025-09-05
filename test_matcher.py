"""
Simple Test Script for Student-Teacher Matching System
This script tests the core functionality without visualizations.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter
import json

# Simple version of the matcher for testing
class SimpleStudentTeacherMatcher:
    def __init__(self):
        self.students_df = None
        self.teachers_df = None
        self.schedule = []
    
    def load_data(self, students_file, teachers_file):
        try:
            self.students_df = pd.read_csv(students_file)
            self.teachers_df = pd.read_csv(teachers_file)
            print(f"✅ Loaded {len(self.students_df)} students and {len(self.teachers_df)} teachers")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def preprocess_data(self):
        # Simple preprocessing
        def clean_list(text):
            if pd.isna(text):
                return []
            return [item.strip().title() for item in str(text).split(',')]
        
        self.students_df['time_slots'] = self.students_df['preferred_time_slots'].apply(clean_list)
        self.students_df['subject_list'] = self.students_df['subjects'].apply(clean_list)
        self.teachers_df['time_slots'] = self.teachers_df['available_time_slots'].apply(clean_list)
        self.teachers_df['subject_list'] = self.teachers_df['subjects'].apply(clean_list)
        
        print("✅ Data preprocessing completed")
    
    def create_matches(self):
        matches = []
        teacher_capacity = {}
        
        # Initialize capacity
        for _, teacher in self.teachers_df.iterrows():
            teacher_id = teacher['teacher_id']
            teacher_capacity[teacher_id] = {}
            for slot in teacher['time_slots']:
                teacher_capacity[teacher_id][slot] = teacher['max_students_per_slot']
        
        assigned_students = set()
        
        for _, student in self.students_df.iterrows():
            if student['student_id'] in assigned_students:
                continue
                
            student_subjects = set(student['subject_list'])
            student_slots = set(student['time_slots'])
            
            best_match = None
            best_score = 0
            
            for _, teacher in self.teachers_df.iterrows():
                teacher_subjects = set(teacher['subject_list'])
                teacher_slots = set(teacher['time_slots'])
                
                # Check subject overlap
                common_subjects = student_subjects.intersection(teacher_subjects)
                if not common_subjects:
                    continue
                
                # Check time availability
                common_slots = student_slots.intersection(teacher_slots)
                if not common_slots:
                    continue
                
                # Check capacity
                available_slot = None
                for slot in common_slots:
                    if teacher_capacity[teacher['teacher_id']][slot] > 0:
                        available_slot = slot
                        break
                
                if not available_slot:
                    continue
                
                # Calculate score (Jaccard similarity)
                score = len(common_subjects) / len(student_subjects.union(teacher_subjects))
                
                if score > best_score:
                    best_score = score
                    best_match = {
                        'student_id': student['student_id'],
                        'teacher_id': teacher['teacher_id'],
                        'time_slot': available_slot,
                        'subjects': ', '.join(common_subjects),
                        'compatibility_score': round(score, 3)
                    }
            
            if best_match:
                matches.append(best_match)
                assigned_students.add(best_match['student_id'])
                teacher_id = best_match['teacher_id']
                slot = best_match['time_slot']
                teacher_capacity[teacher_id][slot] -= 1
        
        self.schedule = matches
        print(f"✅ Created {len(matches)} matches")
        return matches
    
    def print_schedule(self):
        if not self.schedule:
            print("No matches created")
            return
        
        print("\n📅 GENERATED SCHEDULE:")
        print("-" * 80)
        
        for i, match in enumerate(self.schedule, 1):
            student_name = self.students_df[self.students_df['student_id'] == match['student_id']]['name'].iloc[0]
            teacher_name = self.teachers_df[self.teachers_df['teacher_id'] == match['teacher_id']]['name'].iloc[0]
            
            print(f"{i:2d}. {student_name:<10} -> {teacher_name:<10} | {match['time_slot']:<9} | {match['subjects']:<20} | Score: {match['compatibility_score']}")
    
    def calculate_basic_metrics(self):
        total_students = len(self.students_df)
        matched_students = len(self.schedule)
        matching_rate = (matched_students / total_students) * 100
        
        print(f"\n📊 BASIC METRICS:")
        print(f"   • Total Students: {total_students}")
        print(f"   • Matched Students: {matched_students}")
        print(f"   • Matching Rate: {matching_rate:.1f}%")
        
        if self.schedule:
            avg_score = np.mean([m['compatibility_score'] for m in self.schedule])
            print(f"   • Average Compatibility Score: {avg_score:.3f}")
    
    def export_simple_schedule(self):
        if not self.schedule:
            return
        
        # Add names to schedule
        enhanced_schedule = []
        for match in self.schedule:
            enhanced = match.copy()
            enhanced['student_name'] = self.students_df[self.students_df['student_id'] == match['student_id']]['name'].iloc[0]
            enhanced['teacher_name'] = self.teachers_df[self.teachers_df['teacher_id'] == match['teacher_id']]['name'].iloc[0]
            enhanced_schedule.append(enhanced)
        
        # Export to CSV
        df = pd.DataFrame(enhanced_schedule)
        df.to_csv('simple_schedule.csv', index=False)
        print("📁 Schedule exported to simple_schedule.csv")
        
        # Export to JSON
        with open('simple_schedule.json', 'w') as f:
            json.dump(enhanced_schedule, f, indent=2)
        print("📁 Schedule exported to simple_schedule.json")

def main():
    print("🎓 Student-Teacher Matching System - Test Run")
    print("=" * 50)
    
    matcher = SimpleStudentTeacherMatcher()
    
    # Load and process data
    if matcher.load_data('students.csv', 'teachers.csv'):
        matcher.preprocess_data()
        matches = matcher.create_matches()
        
        if matches:
            matcher.print_schedule()
            matcher.calculate_basic_metrics()
            matcher.export_simple_schedule()
            print("\n✅ Test completed successfully!")
        else:
            print("❌ No matches could be created")
    else:
        print("❌ Failed to load data")

if __name__ == "__main__":
    main()
