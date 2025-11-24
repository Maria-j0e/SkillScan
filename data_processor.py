import pandas as pd
import os
from typing import Dict, List, Tuple


class DataProcessor:
    """Process and normalize question bank CSV files"""

    def __init__(self, uploads_dir="uploads"):
        self.uploads_dir = uploads_dir
        # Create uploads directory if it doesn't exist
        os.makedirs(uploads_dir, exist_ok=True)

        self.courses = {
            'Data Science': os.path.join(uploads_dir, 'ds.csv'),
            'AI/ML': os.path.join(uploads_dir, 'aiml.csv'),
            'Cybersecurity': os.path.join(uploads_dir, 'cyber.csv'),
            'Full Stack': os.path.join(uploads_dir, 'fullstack.csv')
        }
        self.question_banks = {}
        self.load_all_courses()

    def load_all_courses(self):
        """Load all course question banks"""
        for course_name, file_path in self.courses.items():
            try:
                # Create sample data for all courses
                self.question_banks[course_name] = self._create_sample_data(course_name)
                print(f"Created sample data for {course_name}: {len(self.question_banks[course_name])} questions")
            except Exception as e:
                print(f"Error loading {course_name}: {e}")
                # Create empty DataFrame with required columns
                self.question_banks[course_name] = pd.DataFrame(columns=[
                    'id', 'course', 'topic', 'level', 'question',
                    'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer'
                ])

    def _create_sample_data(self, course_name: str) -> pd.DataFrame:
        """Create comprehensive sample data"""
        sample_data = []

        # Define course-specific topics and questions
        course_configs = {
            'Data Science': {
                'topics': ['Statistics', 'Python', 'Data Visualization', 'Machine Learning', 'Probability'],
                'questions': [
                    ("What is the mean of a dataset?", "Average", "Median", "Mode", "Range", 0),
                    ("Which library is used for data manipulation in Python?", "NumPy", "Pandas", "Matplotlib",
                     "Scikit-learn", 1),
                    ("What does PDF stand for in statistics?", "Probability Density Function",
                     "Portable Document Format", "Both", "Neither", 0),
                    ("What is regression analysis used for?", "Classification", "Predicting continuous values",
                     "Clustering", "Dimensionality reduction", 1),
                    ("Which plot is best for categorical data?", "Scatter plot", "Bar chart", "Line chart", "Histogram",
                     1)
                ]
            },
            'AI/ML': {
                'topics': ['Linear Algebra', 'Calculus', 'Neural Networks', 'Deep Learning', 'Algorithms'],
                'questions': [
                    ("What is a gradient in machine learning?", "Slope of a function", "Type of algorithm",
                     "Data structure", "Learning rate", 0),
                    ("What does ReLU stand for?", "Rectified Linear Unit", "Real Learning Update",
                     "Regression Linear Unit", "Random Learning Update", 0),
                    ("What is overfitting?", "Model too simple", "Model too complex", "Perfect fit", "Underperformance",
                     1),
                    ("What is backpropagation used for?", "Data preprocessing", "Training neural networks",
                     "Feature selection", "Model evaluation", 1),
                    ("What is a tensor?", "Multi-dimensional array", "Single value", "2D array only", "Database table",
                     0)
                ]
            },
            'Cybersecurity': {
                'topics': ['Network Security', 'Cryptography', 'Ethical Hacking', 'OS Security', 'Web Security'],
                'questions': [
                    ("What is a firewall used for?", "Network security", "Data backup", "Speed optimization",
                     "Memory management", 0),
                    ("What is encryption?", "Data scrambling", "Data compression", "Data deletion", "Data copying", 0),
                    ("What is phishing?", "Social engineering attack", "Virus type", "Firewall technique",
                     "Encryption method", 0),
                    ("What is two-factor authentication?", "Security verification", "Data encryption",
                     "Network protocol", "Backup method", 0),
                    ("What is a VPN?", "Virtual Private Network", "Visual Programming Network",
                     "Very Protected Network", "Virtual Protocol Network", 0)
                ]
            },
            'Full Stack': {
                'topics': ['HTML/CSS', 'JavaScript', 'React', 'Node.js', 'Databases'],
                'questions': [
                    ("What does HTML stand for?", "HyperText Markup Language", "HighTech Modern Language",
                     "Hyper Transfer Markup Language", "HighText Machine Language", 0),
                    ("What is CSS used for?", "Styling web pages", "Adding interactivity", "Database management",
                     "Server operations", 0),
                    ("What is JavaScript primarily used for?", "Client-side scripting", "Database management",
                     "Server configuration", "Graphic design", 0),
                    ("What is React?", "Frontend framework", "Backend framework", "Database", "Programming language",
                     0),
                    ("What is Node.js?", "JavaScript runtime", "Database system", "CSS framework", "Markup language", 0)
                ]
            }
        }

        config = course_configs[course_name]

        for i in range(25):  # Create 25 questions per course
            topic = config['topics'][i % len(config['topics'])]
            level = (i % 5) + 1  # Levels 1-5
            question_data = config['questions'][i % len(config['questions'])]

            sample_data.append({
                'id': f"{course_name[:2].lower()}_{i + 1}",
                'course': course_name,
                'topic': topic,
                'level': level,
                'question': question_data[0],
                'option_a': question_data[1],
                'option_b': question_data[2],
                'option_c': question_data[3],
                'option_d': question_data[4],
                'correct_answer': question_data[5]
            })

        return pd.DataFrame(sample_data)

    def get_questions_by_level(self, course: str, level: int, limit: int = None) -> pd.DataFrame:
        """Get questions for a specific course and level"""
        if course not in self.question_banks:
            return pd.DataFrame()

        df = self.question_banks[course]
        if len(df) == 0:
            return df

        filtered = df[df['level'] == level]

        if limit and len(filtered) > limit:
            filtered = filtered.sample(n=limit, random_state=42)

        return filtered.reset_index(drop=True)

    def get_all_topics(self, course: str) -> List[str]:
        """Get all unique topics for a course"""
        if course not in self.question_banks:
            return []

        df = self.question_banks[course]
        if len(df) == 0:
            return ['General']

        return df['topic'].unique().tolist()

    def get_level_distribution(self, course: str) -> Dict[int, int]:
        """Get count of questions per level"""
        if course not in self.question_banks:
            return {}

        df = self.question_banks[course]
        if len(df) == 0:
            return {1: 5, 2: 5, 3: 5, 4: 5, 5: 5}

        return df['level'].value_counts().sort_index().to_dict()