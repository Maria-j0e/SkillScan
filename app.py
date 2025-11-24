import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os
import random

# Page configuration
st.set_page_config(
    page_title="Prerequisite Knowledge Assessment Tool",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .info-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        color: #000000;
    }
    .info-box h3, .info-box h4, .info-box p, .info-box ul, .info-box li {
        color: #000000 !important;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #28a745;
        color: #000000;
    }
    .success-box h2, .success-box h3, .success-box p {
        color: #000000 !important;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #ffc107;
        color: #000000;
    }
    .warning-box h2, .warning-box h3, .warning-box p {
        color: #000000 !important;
    }
    .danger-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #dc3545;
        color: #000000;
    }
    .danger-box h2, .danger-box h3, .danger-box p {
        color: #000000 !important;
    }
    /* Ensure all text in main content area is visible */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, 
    .stMarkdown h3, .stMarkdown h4, .stMarkdown li {
        color: inherit;
    }
</style>
""", unsafe_allow_html=True)



# Define all classes in the same file to avoid import issues
class DataProcessor:
    def __init__(self):
        self.courses = ['Data Science', 'AI/ML', 'Cybersecurity', 'Full Stack']
        self.question_banks = {}
        self.load_all_courses()

    def load_all_courses(self):
        for course in self.courses:
            self.question_banks[course] = self._create_sample_data(course)

    def _create_sample_data(self, course_name):
        sample_data = []
        course_configs = {
            'Data Science': {
                'topics': ['Statistics', 'Python', 'Data Visualization', 'Machine Learning'],
                'questions': [
                    ("What is the mean of a dataset?", "Average", "Median", "Mode", "Range", 0),
                    ("Which library is used for data manipulation?", "NumPy", "Pandas", "Matplotlib", "Scikit-learn",
                     1),
                    ("What does PDF stand for in statistics?", "Probability Density Function",
                     "Portable Document Format", "Both", "Neither", 0),
                    ("What is regression analysis used for?", "Classification", "Predicting continuous values",
                     "Clustering", "Dimensionality reduction", 1),
                ]
            },
            'AI/ML': {
                'topics': ['Linear Algebra', 'Calculus', 'Neural Networks', 'Deep Learning'],
                'questions': [
                    ("What is a gradient in machine learning?", "Slope of a function", "Type of algorithm",
                     "Data structure", "Learning rate", 0),
                    ("What does ReLU stand for?", "Rectified Linear Unit", "Real Learning Update",
                     "Regression Linear Unit", "Random Learning Update", 0),
                    ("What is overfitting?", "Model too simple", "Model too complex", "Perfect fit", "Underperformance",
                     1),
                    ("What is backpropagation used for?", "Data preprocessing", "Training neural networks",
                     "Feature selection", "Model evaluation", 1),
                ]
            },
            'Cybersecurity': {
                'topics': ['Network Security', 'Cryptography', 'Ethical Hacking', 'OS Security'],
                'questions': [
                    ("What is a firewall used for?", "Network security", "Data backup", "Speed optimization",
                     "Memory management", 0),
                    ("What is encryption?", "Data scrambling", "Data compression", "Data deletion", "Data copying", 0),
                    ("What is phishing?", "Social engineering attack", "Virus type", "Firewall technique",
                     "Encryption method", 0),
                    ("What is two-factor authentication?", "Security verification", "Data encryption",
                     "Network protocol", "Backup method", 0),
                ]
            },
            'Full Stack': {
                'topics': ['HTML/CSS', 'JavaScript', 'React', 'Node.js'],
                'questions': [
                    ("What does HTML stand for?", "HyperText Markup Language", "HighTech Modern Language",
                     "Hyper Transfer Markup Language", "HighText Machine Language", 0),
                    ("What is CSS used for?", "Styling web pages", "Adding interactivity", "Database management",
                     "Server operations", 0),
                    ("What is JavaScript primarily used for?", "Client-side scripting", "Database management",
                     "Server configuration", "Graphic design", 0),
                    ("What is React?", "Frontend framework", "Backend framework", "Database", "Programming language",
                     0),
                ]
            }
        }

        config = course_configs[course_name]
        for i in range(20):
            topic = config['topics'][i % len(config['topics'])]
            level = (i % 5) + 1
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

    def get_questions_by_level(self, course, level, limit=None):
        if course not in self.question_banks:
            return pd.DataFrame()
        df = self.question_banks[course]
        filtered = df[df['level'] == level]
        if limit and len(filtered) > limit:
            filtered = filtered.sample(n=limit)
        return filtered

    def get_level_distribution(self, course):
        if course not in self.question_banks:
            return {}
        df = self.question_banks[course]
        return df['level'].value_counts().sort_index().to_dict()


class AssessmentEngine:
    def __init__(self, data_processor):
        self.data_processor = data_processor

    def generate_adaptive_quiz(self, course, initial_level):
        quiz_questions = []
        for level in range(1, 6):
            questions = self.data_processor.get_questions_by_level(course, level, 4)
            for _, q_row in questions.iterrows():
                quiz_questions.append({
                    'question_data': q_row,
                    'adaptive_level': level,
                    'question_number': len(quiz_questions) + 1
                })
        random.shuffle(quiz_questions)
        for idx, q in enumerate(quiz_questions):
            q['question_number'] = idx + 1
        return quiz_questions[:20]

    def calculate_score(self, answers, quiz_questions):
        correct_count = 0
        level_performance = {1: {'correct': 0, 'total': 0}, 2: {'correct': 0, 'total': 0},
                             3: {'correct': 0, 'total': 0}, 4: {'correct': 0, 'total': 0},
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

        score_percentage = (correct_count / len(quiz_questions) * 100) if quiz_questions else 0
        return {
            'score_percentage': score_percentage,
            'correct_count': correct_count,
            'total_count': len(quiz_questions),
            'level_performance': level_performance,
            'topic_performance': topic_performance
        }


class GapAnalyzer:
    def __init__(self):
        self.mastery_threshold = 70
        self.weak_threshold = 50

    def analyze_gaps(self, results, course, initial_level):
        level_performance = results['level_performance']
        topic_performance = results['topic_performance']

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

        for topic in gap_analysis['weak_topics']:
            priorities.append({
                'priority': 'High',
                'area': topic['topic'],
                'type': 'Topic',
                'score': topic['percentage'],
                'reason': f"Low performance ({topic['percentage']:.1f}%) - needs immediate attention"
            })

        for topic in gap_analysis['moderate_topics']:
            priorities.append({
                'priority': 'Medium',
                'area': topic['topic'],
                'type': 'Topic',
                'score': topic['percentage'],
                'reason': f"Room for improvement ({topic['percentage']:.1f}%)"
            })

        return priorities


class LearningPathGenerator:
    def generate_learning_path(self, course, gap_analysis, priorities):
        learning_path = {
            'immediate_focus': [],
            'short_term': [],
            'long_term': [],
            'estimated_hours': 0
        }

        for item in priorities[:3]:
            learning_path['immediate_focus'].append({
                'area': item['area'],
                'current_score': f"{item['score']:.1f}%",
                'target_score': '70%+',
                'resources': [
                    f'Online tutorials on {item["area"]}',
                    f'Practice exercises for {item["area"]}',
                    f'Video courses covering {item["area"]} fundamentals',
                    f'Interactive coding challenges'
                ],
                'estimated_hours': 6
            })
            learning_path['estimated_hours'] += 6

        return learning_path

    def generate_study_schedule(self, learning_path, weeks=4):
        schedule = []
        for i in range(weeks):
            focus_areas = {
                1: "Foundation Building & Core Concepts",
                2: "Practice & Skill Development",
                3: "Advanced Topics & Projects",
                4: "Review & Final Assessment"
            }
            schedule.append({
                'week': i + 1,
                'focus': focus_areas[i + 1],
                'activities': [
                    'Complete all assigned readings and tutorials',
                    'Solve daily practice problems',
                    'Participate in discussion forums',
                    'Work on mini-projects',
                    'Take weekly progress assessment'
                ],
                'hours': 8
            })
        return schedule


class SkillTreeBuilder:
    def build_skill_tree(self, course, gap_analysis):
        labels = [course, "Foundation", "Intermediate", "Advanced", "Expert"]
        parents = ["", course, course, course, course]
        values = [100, 25, 25, 25, 25]
        colors = ['lightblue', 'lightgreen', 'yellow', 'orange', 'lightcoral']

        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            marker=dict(colors=colors),
            branchvalues="total"
        ))
        fig.update_layout(title=f"{course} Skill Tree", width=600, height=600)
        return fig

    def create_performance_radar(self, gap_analysis):
        levels = [f"Level {i}" for i in range(1, 6)]
        scores = [70, 65, 60, 55, 50]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=levels,
            fill='toself',
            name='Your Performance'
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
        return fig


# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()
if 'selected_course' not in st.session_state:
    st.session_state.selected_course = None
if 'selected_level' not in st.session_state:
    st.session_state.selected_level = 3
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False
if 'results' not in st.session_state:
    st.session_state.results = None
if 'gap_analysis' not in st.session_state:
    st.session_state.gap_analysis = None

# Initialize engines
assessment_engine = AssessmentEngine(st.session_state.data_processor)
gap_analyzer = GapAnalyzer()
learning_path_gen = LearningPathGenerator()
skill_tree_builder = SkillTreeBuilder()

# Sidebar navigation
st.sidebar.title("📚 Navigation")
page = st.sidebar.radio("Go to:", ["🏠 Home", "📝 Take Assessment", "📊 View Results", "🎯 Learning Path", "🌳 Skill Tree"])

if page == "🏠 Home":
    st.session_state.page = 'home'
elif page == "📝 Take Assessment":
    st.session_state.page = 'assessment'
elif page == "📊 View Results" and st.session_state.quiz_completed:
    st.session_state.page = 'results'
elif page == "🎯 Learning Path" and st.session_state.quiz_completed:
    st.session_state.page = 'learning_path'
elif page == "🌳 Skill Tree" and st.session_state.quiz_completed:
    st.session_state.page = 'skill_tree'

# HOME PAGE
if st.session_state.page == 'home':
    st.markdown('<h1 class="main-header">🎓 Automated Prerequisite Knowledge Assessment</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    <h3>Welcome to Your Personalized Learning Journey!</h3>
    <p>This tool helps you:</p>
    <ul>
        <li>📊 Assess your current knowledge level</li>
        <li>🔍 Identify specific knowledge gaps</li>
        <li>📚 Get personalized learning recommendations</li>
        <li>🎯 Track your progress with visual skill trees</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📋 Available Courses")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔬 Data Science**")
        st.markdown("**🤖 AI/ML**")
    with col2:
        st.markdown("**🔒 Cybersecurity**")
        st.markdown("**💻 Full Stack**")

    st.markdown("---")
    st.markdown("### 🚀 Get Started")
    st.info("Select 'Take Assessment' to begin!")

# ASSESSMENT PAGE
elif st.session_state.page == 'assessment':
    st.markdown('<h1 class="main-header">📝 Knowledge Assessment</h1>', unsafe_allow_html=True)

    if not st.session_state.selected_course:
        st.markdown("### Step 1: Select Your Course")
        course_options = st.session_state.data_processor.courses
        selected = st.selectbox("Choose a course:", course_options)
        if st.button("Select Course"):
            st.session_state.selected_course = selected
            st.rerun()

    elif not st.session_state.quiz_questions:
        st.markdown(f"### Step 2: Self-Assess Your Level")
        st.markdown(f"**Selected Course:** {st.session_state.selected_course}")

        level = st.slider("Rate your knowledge level (1-5):", 1, 5, 3)
        st.session_state.selected_level = level

        if st.button("Start Assessment"):
            with st.spinner('Generating quiz...'):
                st.session_state.quiz_questions = assessment_engine.generate_adaptive_quiz(
                    st.session_state.selected_course, level
                )
                st.rerun()

    elif not st.session_state.quiz_completed:
        total_questions = len(st.session_state.quiz_questions)
        current_idx = st.session_state.current_question

        progress = current_idx / total_questions
        st.progress(progress, text=f"Question {current_idx + 1} of {total_questions}")

        q_dict = st.session_state.quiz_questions[current_idx]
        q_data = q_dict['question_data']

        st.markdown(f"### Question {current_idx + 1}")
        st.markdown(f"**Level:** {q_dict['adaptive_level']} | **Topic:** {q_data['topic']}")
        st.markdown(f"**{q_data['question']}**")

        options = [q_data['option_a'], q_data['option_b'], q_data['option_c'], q_data['option_d']]
        selected_option = st.radio("Select your answer:", options, key=f"q_{current_idx}")

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if current_idx > 0 and st.button("Previous"):
                st.session_state.current_question -= 1
                st.rerun()
        with col3:
            if current_idx < total_questions - 1 and st.button("Next"):
                st.session_state.answers[q_dict['question_number']] = options.index(selected_option)
                st.session_state.current_question += 1
                st.rerun()
            elif current_idx == total_questions - 1 and st.button("Submit"):
                st.session_state.answers[q_dict['question_number']] = options.index(selected_option)
                st.session_state.results = assessment_engine.calculate_score(
                    st.session_state.answers, st.session_state.quiz_questions
                )
                st.session_state.gap_analysis = gap_analyzer.analyze_gaps(
                    st.session_state.results, st.session_state.selected_course, st.session_state.selected_level
                )
                st.session_state.quiz_completed = True
                st.success("Assessment completed!")
                st.balloons()
                st.rerun()

# RESULTS PAGE
elif st.session_state.page == 'results' and st.session_state.gap_analysis:
    st.markdown('<h1 class="main-header">📊 Assessment Results</h1>', unsafe_allow_html=True)

    if st.session_state.gap_analysis:
        gap = st.session_state.gap_analysis

        # Overall score with better styling
        score = gap['overall_score']
        if score >= 80:
            box_class = "success-box"
            emoji = "🎉"
            status = "Excellent - Strong Potential"
        elif score >= 70:
            box_class = "success-box"
            emoji = "👍"
            status = "Good - Well Prepared"
        elif score >= 60:
            box_class = "warning-box"
            emoji = "⚠️"
            status = "Satisfactory - Close to Cutoff"
        else:
            box_class = "danger-box"
            emoji = "🔴"
            status = "Needs Improvement"

        st.markdown(f"""
        <div class="{box_class}">
        <h2>{emoji} Overall Score: {score:.1f}%</h2>
        <h3>Status: {status}</h3>
        <p>{gap['readiness_message']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Key metrics in a more organized way
        st.markdown("### 📈 Performance Summary")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Questions Answered", st.session_state.results['total_count'])
        with col2:
            st.metric("Correct Answers", st.session_state.results['correct_count'])
        with col3:
            st.metric("Accuracy Rate", f"{score:.1f}%")
        with col4:
            st.metric("Performance Level", f"Level {gap['actual_level']}")

        # Level performance
        st.markdown("---")
        st.markdown("### 🎯 Difficulty Level Analysis")

        level_data = []
        for level, perf in st.session_state.results['level_performance'].items():
            if perf['total'] > 0:
                level_score = (perf['correct'] / perf['total'] * 100)
                level_data.append({
                    'Difficulty Level': f"Level {level}",
                    'Questions': perf['total'],
                    'Correct': perf['correct'],
                    'Score': f"{level_score:.1f}%",
                    'Status': 'Mastered' if level_score >= 70 else 'Learning' if level_score >= 50 else 'Needs Work'
                })

        if level_data:
            for row in level_data:
                col1, col2, col3 = st.columns([2, 1, 2])
                with col1:
                    st.write(f"**{row['Difficulty Level']}**")
                with col2:
                    st.write(f"{row['Correct']}/{row['Questions']}")
                with col3:
                    if row['Status'] == 'Mastered':
                        st.success(f"{row['Score']} ✅")
                    elif row['Status'] == 'Learning':
                        st.warning(f"{row['Score']} ⚠️")
                    else:
                        st.error(f"{row['Score']} ❌")

        # Topic performance with progress bars
        st.markdown("---")
        st.markdown("### 📊 Topic-wise Performance")

        for topic, perf in st.session_state.results['topic_performance'].items():
            if perf['total'] > 0:
                percentage = (perf['correct'] / perf['total'] * 100)
                col1, col2, col3 = st.columns([3, 1, 2])
                with col1:
                    st.write(f"**{topic}**")
                with col2:
                    st.write(f"{perf['correct']}/{perf['total']}")
                with col3:
                    st.progress(percentage / 100, text=f"{percentage:.1f}%")

        # Quick recommendations
        st.markdown("---")
        st.markdown("### 💡 Quick Recommendations")

        if gap['weak_topics']:
            st.warning("**Immediate Focus Areas:**")
            for topic in gap['weak_topics'][:3]:
                st.write(f"- Review and practice **{topic['topic']}** concepts")
        else:
            st.success("**You're doing great!** Consider exploring advanced topics.")

        if gap['actual_level'] < gap['self_assessed_level']:
            st.info(
                "**Self-Assessment Note:** Your actual performance is below your self-assessment. Focus on building stronger foundations.")
        else:
            st.success("**Self-Assessment Note:** Great self-awareness! Your assessment matches your performance.")

        # Navigation to detailed learning path
        st.markdown("---")
        st.markdown("### 🚀 Next Steps")
        if st.button("📚 View Detailed Learning Path", type="primary"):
            st.session_state.page = 'learning_path'
            st.rerun()

# LEARNING PATH PAGE
elif st.session_state.page == 'learning_path' and st.session_state.gap_analysis:
    st.markdown('<h1 class="main-header">🎯 Personalized Learning Path</h1>', unsafe_allow_html=True)

    if st.session_state.gap_analysis:
        gap = st.session_state.gap_analysis
        priorities = gap_analyzer.generate_priority_list(gap)
        learning_path = learning_path_gen.generate_learning_path(
            st.session_state.selected_course,
            gap,
            priorities
        )

        # Candidate Information
        st.markdown("""
        <div class="info-box">
        <h3>📋 Gap Analysis Report</h3>
        <h4>Candidate Information</h4>
        <p><strong>Candidate Name:</strong> Student</p>
        <p><strong>Test Date:</strong> {}</p>
        <p><strong>Score:</strong> {}/{} ({:.1f}%)</p>
        <p><strong>Overall Status:</strong> {}</p>
        </div>
        """.format(
            datetime.now().strftime('%Y-%m-%d'),
            st.session_state.results['correct_count'],
            st.session_state.results['total_count'],
            gap['overall_score'],
            gap['readiness']
        ), unsafe_allow_html=True)

        # Section-wise Performance
        st.markdown("---")
        st.markdown("### 📊 Section-wise Performance")

        # Create performance table
        performance_data = []
        for topic, perf in st.session_state.results['topic_performance'].items():
            if perf['total'] > 0:
                percentage = (perf['correct'] / perf['total'] * 100)
                if percentage >= 80:
                    strength = "Excellent"
                    remarks = "Strong understanding of this topic"
                elif percentage >= 70:
                    strength = "Good"
                    remarks = "Good performance, minor improvements needed"
                elif percentage >= 60:
                    strength = "Satisfactory"
                    remarks = "Basic understanding, needs practice"
                else:
                    strength = "Needs Improvement"
                    remarks = "Significant improvement required"

                performance_data.append({
                    'Section': topic,
                    'Correct': perf['correct'],
                    'Incorrect': perf['total'] - perf['correct'],
                    'Unattempted': 0,
                    'Strength Level': strength,
                    'Remarks': remarks
                })

        # Display as table
        perf_df = pd.DataFrame(performance_data)
        st.table(perf_df)

        # Strengths and Improvement Areas
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Strengths Identified")
            if gap['strong_topics']:
                for topic in gap['strong_topics']:
                    st.success(f"• Excellent knowledge of {topic['topic']} ({topic['percentage']:.1f}%)")
            else:
                st.info("• Solid foundation in core concepts")
                st.info("• Good problem-solving approach")

        with col2:
            st.markdown("### 📈 Improvement Areas")
            if gap['weak_topics']:
                for topic in gap['weak_topics']:
                    st.error(f"• Improve understanding of {topic['topic']} ({topic['percentage']:.1f}%)")
            else:
                st.success("• No major improvement areas identified")

        # Detailed Learning Path
        st.markdown("---")
        st.markdown("### 🎯 Next Steps Recommended")

        # Immediate focus
        st.markdown("#### 🔥 Immediate Focus (Next 2 Weeks)")
        for i, item in enumerate(learning_path['immediate_focus']):
            with st.expander(f"📌 {item['area']} - Priority: High", expanded=i == 0):
                st.markdown(f"**Current Performance:** {item['current_score']}")
                st.markdown(f"**Target:** {item['target_score']}")
                st.markdown(f"**Time Commitment:** {item['estimated_hours']} hours")
                st.markdown("**Action Plan:**")
                for resource in item['resources']:
                    st.markdown(f"- {resource}")
                st.markdown("**Expected Outcomes:**")
                st.markdown("- Solid understanding of core concepts")
                st.markdown("- Ability to solve intermediate problems")
                st.markdown("- Improved confidence in this area")

        # Study schedule
        st.markdown("---")
        st.markdown("### 📆 4-Week Study Plan")

        weeks_plan = [
            {"Week": 1, "Focus": "Foundation Building", "Topics": "Core concepts & basics", "Hours": "10-12"},
            {"Week": 2, "Focus": "Skill Development", "Topics": "Practice & application", "Hours": "8-10"},
            {"Week": 3, "Focus": "Advanced Topics", "Topics": "Complex problems & projects", "Hours": "6-8"},
            {"Week": 4, "Focus": "Review & Assessment", "Topics": "Final review & mock tests", "Hours": "4-6"}
        ]

        for week in weeks_plan:
            with st.expander(f"Week {week['Week']}: {week['Focus']}"):
                st.markdown(f"**Main Topics:** {week['Topics']}")
                st.markdown(f"**Recommended Hours:** {week['Hours']}")
                st.markdown("**Weekly Goals:**")
                st.markdown("- Complete all assigned readings")
                st.markdown("- Solve practice problems daily")
                st.markdown("- Participate in discussion forums")
                st.markdown("- Take weekly progress quiz")

        # Download comprehensive report
        st.markdown("---")
        st.markdown("### 📥 Download Full Report")

        report_data = {
            'candidate_name': 'Student',
            'course': st.session_state.selected_course,
            'test_date': datetime.now().strftime('%Y-%m-%d'),
            'score': f"{st.session_state.results['correct_count']}/{st.session_state.results['total_count']}",
            'percentage': gap['overall_score'],
            'status': gap['readiness'],
            'performance_breakdown': performance_data,
            'strengths': [f"Excellent knowledge of {topic['topic']}" for topic in gap['strong_topics']],
            'improvement_areas': [f"Improve understanding of {topic['topic']}" for topic in gap['weak_topics']],
            'recommendations': [
                "Review and practice core concepts",
                "Take advanced courses on weak areas",
                "Practice with real-world projects",
                "Participate in coding exercises",
                "Engage in peer learning activities"
            ]
        }

        report_json = json.dumps(report_data, indent=2)
        st.download_button(
            label="📄 Download Detailed Gap Analysis Report",
            data=report_json,
            file_name=f"gap_analysis_report_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

# SKILL TREE PAGE
elif st.session_state.page == 'skill_tree' and st.session_state.gap_analysis:
    st.markdown('<h1 class="main-header">🌳 Skill Tree</h1>', unsafe_allow_html=True)
    fig = skill_tree_builder.build_skill_tree(st.session_state.selected_course, st.session_state.gap_analysis)
    st.plotly_chart(fig)

# Footer
st.markdown("---")
st.markdown("Automated Prerequisite Knowledge Assessment Tool | Built with Streamlit")