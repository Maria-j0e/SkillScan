import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List


class SkillTreeBuilder:
    """Build and visualize skill trees for courses"""

    def __init__(self):
        self.skill_hierarchies = self._define_skill_hierarchies()

    def _define_skill_hierarchies(self) -> Dict:
        """Define skill hierarchies for each course"""
        return {
            'Data Science': {
                'Foundation': ['Basic Statistics', 'Python Basics', 'Data Types'],
                'Intermediate': ['Probability', 'Data Manipulation', 'Visualization'],
                'Advanced': ['Hypothesis Testing', 'Machine Learning', 'Big Data'],
                'Expert': ['Statistical Modeling', 'Deep Learning', 'Data Engineering']
            },
            'AI/ML': {
                'Foundation': ['Mathematics', 'Calculus', 'Linear Algebra'],
                'Intermediate': ['Supervised Learning', 'Unsupervised Learning', 'Neural Networks'],
                'Advanced': ['Deep Learning', 'NLP', 'Computer Vision'],
                'Expert': ['Reinforcement Learning', 'GANs', 'Transformers']
            },
            'Cybersecurity': {
                'Foundation': ['OS Basics', 'Linux', 'Networking'],
                'Intermediate': ['Network Security', 'Cryptography', 'Web Security'],
                'Advanced': ['Penetration Testing', 'Malware Analysis', 'Incident Response'],
                'Expert': ['Security Architecture', 'Threat Hunting', 'Zero-day Research']
            },
            'Full Stack': {
                'Foundation': ['HTML', 'CSS', 'JavaScript'],
                'Intermediate': ['React/Vue', 'Node.js', 'Databases'],
                'Advanced': ['API Design', 'Authentication', 'Cloud Deployment'],
                'Expert': ['Microservices', 'DevOps', 'System Design']
            }
        }

    def build_skill_tree(self, course: str, gap_analysis: Dict) -> go.Figure:
        """Build an interactive skill tree visualization"""

        if course not in self.skill_hierarchies:
            return self._create_empty_tree()

        hierarchy = self.skill_hierarchies[course]

        # Create nodes for the tree
        labels = []
        parents = []
        values = []
        colors = []

        # Root node
        labels.append(course)
        parents.append("")
        values.append(100)
        colors.append('lightblue')

        # Add hierarchy levels
        level_names = ['Foundation', 'Intermediate', 'Advanced', 'Expert']
        level_colors = ['lightgreen', 'yellow', 'orange', 'red']

        actual_level = gap_analysis['actual_level']

        for idx, level_name in enumerate(level_names):
            level_num = idx + 1
            skills = hierarchy[level_name]

            # Add level node
            labels.append(level_name)
            parents.append(course)
            values.append(len(skills) * 10)

            # Color based on mastery
            if level_num <= actual_level:
                colors.append('lightgreen')  # Mastered
            elif level_num == actual_level + 1:
                colors.append('yellow')  # In progress
            else:
                colors.append('lightcoral')  # Not yet mastered

            # Add skill nodes
            for skill in skills:
                labels.append(skill)
                parents.append(level_name)
                values.append(10)

                # Check if this skill is in weak/strong topics
                skill_status = self._get_skill_status(skill, gap_analysis)
                if skill_status == 'strong':
                    colors.append('darkgreen')
                elif skill_status == 'weak':
                    colors.append('darkred')
                else:
                    colors.append('lightyellow')

        # Create sunburst chart
        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            marker=dict(colors=colors),
            branchvalues="total",
            hovertemplate='<b>%{label}</b><br>Click to focus<extra></extra>'
        ))

        fig.update_layout(
            title=f"{course} Skill Tree",
            width=800,
            height=800,
            margin=dict(t=50, l=0, r=0, b=0)
        )

        return fig

    def _get_skill_status(self, skill: str, gap_analysis: Dict) -> str:
        """Determine if a skill is strong, weak, or moderate"""
        skill_lower = skill.lower()

        # Check in strong topics
        for topic in gap_analysis['strong_topics']:
            if skill_lower in topic['topic'].lower() or topic['topic'].lower() in skill_lower:
                return 'strong'

        # Check in weak topics
        for topic in gap_analysis['weak_topics']:
            if skill_lower in topic['topic'].lower() or topic['topic'].lower() in skill_lower:
                return 'weak'

        return 'moderate'

    def _create_empty_tree(self) -> go.Figure:
        """Create an empty tree for unknown courses"""
        fig = go.Figure()
        fig.add_annotation(
            text="Skill tree not available for this course",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False
        )
        return fig

    def create_performance_radar(self, gap_analysis: Dict) -> go.Figure:
        """Create a radar chart showing performance across levels"""

        levels = []
        scores = []

        for level in range(1, 6):
            perf = gap_analysis['level_performance'][level]
            if perf['total'] > 0:
                levels.append(f"Level {level}")
                scores.append(perf['correct'] / perf['total'] * 100)
            else:
                levels.append(f"Level {level}")
                scores.append(0)

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=levels,
            fill='toself',
            name='Your Performance',
            line=dict(color='blue')
        ))

        # Add target line at 70%
        fig.add_trace(go.Scatterpolar(
            r=[70] * 5,
            theta=levels,
            fill='toself',
            name='Target (70%)',
            line=dict(color='green', dash='dash'),
            opacity=0.3
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            title="Performance Across Difficulty Levels"
        )

        return fig