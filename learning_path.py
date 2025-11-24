import pandas as pd
from typing import Dict, List


class LearningPathGenerator:
    """Generate personalized learning paths based on gap analysis"""

    def __init__(self):
        # Learning resources mapped to topics and levels
        self.resource_library = self._build_resource_library()

    def _build_resource_library(self) -> Dict:
        """Build a library of learning resources"""
        return {
            'Data Science': {
                'Stati': {
                    1: ['Khan Academy: Basic Statistics', 'Coursera: Statistics Fundamentals'],
                    2: ['DataCamp: Intermediate Statistics', 'YouTube: StatQuest'],
                    3: ['Coursera: Inferential Statistics', 'edX: Probability and Statistics'],
                    4: ['MIT OpenCourseWare: Advanced Statistics', 'Coursera: Bayesian Statistics'],
                    5: ['Research Papers on Statistical Methods', 'Advanced Statistical Modeling']
                },
                'Python': {
                    1: ['Codecademy: Python Basics', 'Python.org Tutorial'],
                    2: ['Real Python: Intermediate Python', 'DataCamp: Python Programming'],
                    3: ['Effective Python by Brett Slatkin', 'Advanced Python Features'],
                    4: ['Fluent Python by Luciano Ramalho', 'Python Design Patterns'],
                    5: ['Python Core Development', 'Contributing to Python Projects']
                }
            },
            'AI/ML': {
                'calculus': {
                    1: ['Khan Academy: Calculus Basics', 'Paul\'s Online Math Notes'],
                    2: ['MIT OCW: Single Variable Calculus', 'Coursera: Calculus One'],
                    3: ['MIT OCW: Multivariable Calculus', 'Advanced Calculus Concepts'],
                    4: ['Vector Calculus Applications', 'Optimization Theory'],
                    5: ['Research-level Calculus', 'Mathematical Analysis']
                },
                'machine learning': {
                    1: ['Google: Machine Learning Crash Course', 'Coursera: ML for Beginners'],
                    2: ['Andrew Ng: Machine Learning Course', 'Fast.ai: Practical ML'],
                    3: ['Deep Learning Specialization', 'Hands-on Machine Learning'],
                    4: ['Advanced ML Algorithms', 'Research Papers'],
                    5: ['Cutting-edge ML Research', 'Novel Algorithm Development']
                }
            },
            'Cybersecurity': {
                'os_linux -cybersecurtiy': {
                    1: ['Linux Journey', 'Introduction to Linux'],
                    2: ['Linux Command Line Basics', 'Linux System Administration'],
                    3: ['Advanced Linux Security', 'Linux Hardening Guide'],
                    4: ['Linux Kernel Security', 'Security Auditing'],
                    5: ['Linux Security Research', 'Kernel Development']
                },
                'network security': {
                    1: ['Network Security Basics', 'Introduction to Cybersecurity'],
                    2: ['CompTIA Security+', 'Network Security Fundamentals'],
                    3: ['Ethical Hacking Course', 'Penetration Testing'],
                    4: ['Advanced Network Security', 'Security Architecture'],
                    5: ['Security Research', 'Zero-day Analysis']
                }
            },
            'Full Stack': {
                'Web Fundamentals-HTML & CSS': {
                    1: ['MDN: HTML Basics', 'W3Schools: CSS Tutorial'],
                    2: ['Responsive Web Design', 'CSS Flexbox & Grid'],
                    3: ['Advanced CSS Techniques', 'CSS Animations'],
                    4: ['CSS Architecture', 'Performance Optimization'],
                    5: ['Web Standards Development', 'Browser Engine Internals']
                },
                'JavaScript': {
                    1: ['JavaScript.info', 'Codecademy: JavaScript'],
                    2: ['You Don\'t Know JS', 'JavaScript: The Good Parts'],
                    3: ['Async JavaScript', 'Modern JavaScript Features'],
                    4: ['JavaScript Design Patterns', 'Performance Optimization'],
                    5: ['V8 Engine Internals', 'TC39 Proposals']
                }
            }
        }

    def generate_learning_path(self, course: str, gap_analysis: Dict, priorities: List[Dict]) -> Dict:
        """
        Generate a personalized learning path

        Args:
            course: Course name
            gap_analysis: Gap analysis results
            priorities: Prioritized list of areas to focus on

        Returns:
            Dict with structured learning path
        """
        learning_path = {
            'immediate_focus': [],
            'short_term': [],
            'long_term': [],
            'estimated_hours': 0
        }

        # Process high priority items (immediate focus)
        high_priority = [p for p in priorities if p['priority'] == 'High']
        for item in high_priority[:3]:  # Top 3 high priority items
            resources = self._get_resources(course, item['area'], gap_analysis['actual_level'])
            learning_path['immediate_focus'].append({
                'area': item['area'],
                'current_score': f"{item['score']:.1f}%",
                'target_score': '70%+',
                'resources': resources,
                'estimated_hours': 5
            })
            learning_path['estimated_hours'] += 5

        # Process medium priority items (short-term)
        medium_priority = [p for p in priorities if p['priority'] == 'Medium']
        for item in medium_priority[:3]:
            resources = self._get_resources(course, item['area'], gap_analysis['actual_level'] + 1)
            learning_path['short_term'].append({
                'area': item['area'],
                'current_score': f"{item['score']:.1f}%",
                'target_score': '80%+',
                'resources': resources,
                'estimated_hours': 3
            })
            learning_path['estimated_hours'] += 3

        # Add long-term goals (strong areas to maintain)
        for topic in gap_analysis['strong_topics'][:2]:
            resources = self._get_resources(course, topic['topic'], min(5, gap_analysis['actual_level'] + 2))
            learning_path['long_term'].append({
                'area': topic['topic'],
                'current_score': f"{topic['percentage']:.1f}%",
                'goal': 'Maintain and deepen expertise',
                'resources': resources,
                'estimated_hours': 2
            })
            learning_path['estimated_hours'] += 2

        return learning_path

    def _get_resources(self, course: str, area: str, level: int) -> List[str]:
        """Get learning resources for a specific area and level"""
        # Clean up area name
        area_clean = area.replace(' concepts', '').replace('Level ', '').strip()

        # Try to find exact match
        if course in self.resource_library:
            course_resources = self.resource_library[course]

            # Try exact topic match
            if area_clean in course_resources:
                level_resources = course_resources[area_clean].get(level, [])
                if level_resources:
                    return level_resources

            # Try partial match
            for topic_key in course_resources.keys():
                if topic_key.lower() in area_clean.lower() or area_clean.lower() in topic_key.lower():
                    level_resources = course_resources[topic_key].get(level, [])
                    if level_resources:
                        return level_resources

        # Generic resources if no specific match
        return [
            f'Online search: "{area_clean} tutorial level {level}"',
            f'YouTube: "{area_clean} explained"',
            f'Practice exercises on {area_clean}'
        ]

    def generate_study_schedule(self, learning_path: Dict, weeks: int = 4) -> List[Dict]:
        """Generate a week-by-week study schedule"""
        total_hours = learning_path['estimated_hours']
        hours_per_week = total_hours / weeks

        schedule = []
        current_week = 1
        hours_allocated = 0

        # Week 1-2: Immediate focus
        for item in learning_path['immediate_focus']:
            schedule.append({
                'week': current_week,
                'focus': item['area'],
                'activities': [
                    f"Study: {item['resources'][0] if item['resources'] else 'Recommended materials'}",
                    f"Practice problems and exercises",
                    f"Self-assessment quiz"
                ],
                'hours': item['estimated_hours']
            })
            hours_allocated += item['estimated_hours']
            if hours_allocated >= hours_per_week * current_week:
                current_week += 1

        # Week 3: Short-term goals
        for item in learning_path['short_term']:
            if current_week > weeks:
                break
            schedule.append({
                'week': current_week,
                'focus': item['area'],
                'activities': [
                    f"Study: {item['resources'][0] if item['resources'] else 'Recommended materials'}",
                    f"Hands-on projects"
                ],
                'hours': item['estimated_hours']
            })
            hours_allocated += item['estimated_hours']
            if hours_allocated >= hours_per_week * current_week:
                current_week += 1

        # Final week: Review and long-term
        if current_week <= weeks:
            schedule.append({
                'week': weeks,
                'focus': 'Review and Advanced Topics',
                'activities': [
                    'Review all weak areas',
                    'Complete practice assessments',
                    'Explore advanced topics'
                ],
                'hours': hours_per_week
            })

        return schedule