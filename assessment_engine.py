import pandas as pd
import random
from typing import Dict, List, Tuple
from data_processor import DataProcessor


class AssessmentEngine:
    """Adaptive quiz engine that adjusts difficulty based on performance"""

    def __init__(self, data_processor: DataProcessor):
        self.data_processor = data_processor
        self.min_questions = 15
        self.max_questions = 25

    def generate_adaptive_quiz(self, course: str, initial_level: int) -> List[Dict]:
        """
        Generate an adaptive quiz starting at the user's self-assessed level
        """
        quiz_questions = []

        # Get questions from different levels for comprehensive assessment
        for level in range(1, 6):
            questions = self.data_processor.get_questions_by_level(course, level, 5)
            for _, q_row in questions.iterrows():
                quiz_questions.append({
                    'question_data': q_row,
                    'adaptive_level': level,
                    'question_number': len(quiz_questions) + 1
                })

        # Shuffle questions
        random.shuffle(quiz_questions)

        # Limit to max questions
        quiz_questions = quiz_questions[:self.max_questions]

        # Re-number after shuffle
        for idx, q in enumerate(quiz_questions):
            q['question_number'] = idx + 1

        return quiz_questions

    def calculate_score(self, answers: Dict[int, int], quiz_questions: List[Dict]) -> Dict:
        """
        Calculate quiz score and detailed results
        """
        correct_count = 0
        total_count = len(quiz_questions)
        level_performance = {1: {'correct': 0, 'total': 0},
                             2: {'correct': 0, 'total': 0},
                             3: {'correct': 0, 'total': 0},
                             4: {'correct': 0, 'total': 0},
                             5: {'correct': 0, 'total': 0}}

        topic_performance = {}

        for q_dict in quiz_questions:
            q_num = q_dict['question_number']
            q_data = q_dict['question_data']
            level = q_dict['adaptive_level']
            topic = q_data['topic']

            if topic not in topic_performance:
                topic_performance[topic] = {'correct': 0, 'total': 0}

            level_performance[level]['total'] += 1
            topic_performance[topic]['total'] += 1

            if q_num in answers:
                user_answer = answers[q_num]
                correct_answer = q_data['correct_answer']

                if user_answer == correct_answer:
                    correct_count += 1
                    level_performance[level]['correct'] += 1
                    topic_performance[topic]['correct'] += 1

        score_percentage = (correct_count / total_count * 100) if total_count > 0 else 0

        return {
            'score_percentage': score_percentage,
            'correct_count': correct_count,
            'total_count': total_count,
            'level_performance': level_performance,
            'topic_performance': topic_performance
        }