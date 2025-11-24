class GapAnalyzer:
    def __init__(self):
        self.mastery_threshold = 70
        self.weak_threshold = 50

    def analyze_gaps(self, results, course, initial_level):
        level_performance = results['level_performance']
        topic_performance = results['topic_performance']

        # Analyze topic performance
        strong_topics = []
        weak_topics = []
        moderate_topics = []

        for topic, perf in topic_performance.items():
            if perf['total'] > 0:
                percentage = (perf['correct'] / perf['total'] * 100)
                topic_data = {
                    'topic': topic,
                    'percentage': percentage,
                    'correct': perf['correct'],
                    'total': perf['total']
                }

                if percentage >= 80:
                    strong_topics.append(topic_data)
                elif percentage < 60:
                    weak_topics.append(topic_data)
                else:
                    moderate_topics.append(topic_data)

        # Determine readiness level
        overall_score = results['score_percentage']
        if overall_score >= 80:
            readiness = "Excellent"
            readiness_message = "You have excellent prerequisite knowledge for this course."
        elif overall_score >= 70:
            readiness = "Good"
            readiness_message = "You have solid foundational knowledge. Minor improvements needed."
        elif overall_score >= 60:
            readiness = "Satisfactory"
            readiness_message = "You have basic understanding. Focus on key improvement areas."
        else:
            readiness = "Needs Improvement"
            readiness_message = "Significant preparation recommended before starting the course."

        # Calculate actual level
        actual_level = self._calculate_actual_level(level_performance)
        level_gap = initial_level - actual_level

        return {
            'overall_score': overall_score,
            'readiness': readiness,
            'readiness_message': readiness_message,
            'strong_topics': strong_topics,
            'weak_topics': weak_topics,
            'moderate_topics': moderate_topics,
            'actual_level': actual_level,
            'self_assessed_level': initial_level,
            'level_gap': level_gap,
            'level_gap_message': self._get_level_gap_message(level_gap),
            'level_performance': level_performance,
            'topic_performance': topic_performance
        }

    def _calculate_actual_level(self, level_performance):
        actual_level = 1
        for level in range(5, 0, -1):
            perf = level_performance[level]
            if perf['total'] > 0:
                percentage = (perf['correct'] / perf['total'] * 100)
                if percentage >= self.mastery_threshold:
                    actual_level = level
                    break
        return actual_level

    def _get_level_gap_message(self, gap):
        if gap > 2:
            return "Your self-assessment was significantly higher than your actual performance. Focus on fundamentals."
        elif gap > 0:
            return "Your self-assessment was slightly optimistic. Review the recommended materials."
        elif gap == 0:
            return "Your self-assessment matches your performance. Great self-awareness!"
        else:
            return "You're performing above your self-assessment. Consider challenging yourself more!"

    def generate_priority_list(self, gap_analysis):
        priorities = []

        # High priority: Weak topics
        for topic in gap_analysis['weak_topics']:
            priorities.append({
                'priority': 'High',
                'area': topic['topic'],
                'type': 'Topic',
                'score': topic['percentage'],
                'reason': f"Low performance ({topic['percentage']:.1f}%) - needs immediate attention"
            })

        # Medium priority: Moderate topics
        for topic in gap_analysis['moderate_topics']:
            priorities.append({
                'priority': 'Medium',
                'area': topic['topic'],
                'type': 'Topic',
                'score': topic['percentage'],
                'reason': f"Room for improvement ({topic['percentage']:.1f}%)"
            })

        return priorities