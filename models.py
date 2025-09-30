from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Credentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed password
    role = db.Column(db.String(20), nullable=False)  # student / teacher / staff
    credits = db.Column(db.Integer, nullable=False,default=0) 
    points = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Academic cohort info (for pods grouping)
    study_year = db.Column(db.Integer)  # e.g., 1,2,3,4
    department = db.Column(db.String(50))  # e.g., CSE, ECE
    section = db.Column(db.String(10))  # e.g., A, B, C

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)           # Sno
    from_user = db.Column(db.String(50), nullable=False)    # Sender's username
    date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)         # e.g., '2025-07-10'
    amount = db.Column(db.Integer, nullable=False)          # Amount transferred
    to_user = db.Column(db.String(50), nullable=False)   

    def __repr__(self):
        return f"<Transaction {self.from_user} -> {self.to_user}: {self.amount}>"

class CollegePayments(db.Model):
    __tablename__ = 'college_payments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), nullable=False)
    student_email = db.Column(db.String(120), nullable=False)
    student_phone = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    fee_type = db.Column(db.String(50), nullable=False)     # college, exam, library, lab, sports, other
    amount = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(10))                     # Optional
    academic_year = db.Column(db.String(20))                # Optional
    payment_method = db.Column(db.String(20), default='nfc')  # nfc, card, etc.
    nfc_reader_type = db.Column(db.String(20))             # external, mobile
    sender_username = db.Column(db.String(50), nullable=False)  # NFC card holder
    remarks = db.Column(db.Text)                            # Optional remarks
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')  # completed, pending, failed
    
    def __repr__(self):
        return f"<CollegePayment {self.student_name} ({self.student_id}): {self.fee_type} - ₹{self.amount}>"

class PaymentProof(db.Model):
    __tablename__ = 'payment_proofs'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)  # User who submitted the proof
    amount = db.Column(db.Integer, nullable=False)       # Amount requested
    proof_file = db.Column(db.String(255), nullable=False)  # File path/name
    note = db.Column(db.Text)                           # Optional note
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)                 # When admin reviewed it
    reviewed_by = db.Column(db.String(50))              # Admin who reviewed it
    review_note = db.Column(db.Text)                    # Admin's review note
    
    def __repr__(self):
        return f"<PaymentProof {self.username}: ₹{self.amount} - {self.status}>"

class RefundRequest(db.Model):
    __tablename__ = 'refund_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)  # User who requested refund
    amount = db.Column(db.Integer, nullable=False)       # Amount requested for refund
    reason = db.Column(db.Text, nullable=False)         # Reason for refund
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    requested_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)                 # When admin reviewed it
    reviewed_by = db.Column(db.String(50))              # Admin who reviewed it
    review_note = db.Column(db.Text)                    # Admin's review note
    
    def __repr__(self):
        return f"<RefundRequest {self.username}: ₹{self.amount} - {self.status}>"

class LibraryBook(db.Model):
    __tablename__ = 'library_books'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.String(50), unique=True, nullable=False)  # Unique book identifier
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20))
    category = db.Column(db.String(50))  # Fiction, Non-fiction, Academic, etc.
    publisher = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    location = db.Column(db.String(100))  # Shelf location
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<LibraryBook {self.book_id}: {self.title} by {self.author}>"

class LibraryTransaction(db.Model):
    __tablename__ = 'library_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50), unique=True, nullable=False)
    student_username = db.Column(db.String(50), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    student_roll_no = db.Column(db.String(50), nullable=False)
    student_email = db.Column(db.String(120), nullable=False)
    book_id = db.Column(db.String(50), nullable=False)
    book_title = db.Column(db.String(200), nullable=False)
    book_author = db.Column(db.String(100), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='issued')  # issued, returned, overdue
    fine_amount = db.Column(db.Integer, default=0)  # Fine in credits
    fine_paid = db.Column(db.Boolean, default=False)
    issued_by = db.Column(db.String(50), nullable=False)  # Library staff who issued
    returned_to = db.Column(db.String(50))  # Library staff who received return
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f"<LibraryTransaction {self.transaction_id}: {self.student_name} - {self.book_title}>"

class MockExam(db.Model):
    __tablename__ = 'mock_exams'
    
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.String(50), unique=True, nullable=False)
    student_username = db.Column(db.String(50), nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)
    syllabus = db.Column(db.Text, nullable=False)
    question_format = db.Column(db.String(50), nullable=False)  # multiple_choice, descriptive, mixed
    total_questions = db.Column(db.Integer, nullable=False)
    total_marks = db.Column(db.Integer, nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)  # in minutes
    difficulty_level = db.Column(db.String(20), default='medium')  # easy, medium, hard, mixed
    format_description = db.Column(db.Text)  # Custom format description for section-based exams
    questions = db.Column(db.Text, nullable=False)  # JSON string of questions
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='created')  # created, in_progress, completed, evaluated
    
    def __repr__(self):
        return f"<MockExam {self.exam_id}: {self.subject_name} - {self.student_username}>"

class ExamAttempt(db.Model):
    __tablename__ = 'exam_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.String(50), nullable=False)
    student_username = db.Column(db.String(50), nullable=False)
    answers = db.Column(db.Text, nullable=False)  # JSON string of answers
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    time_taken = db.Column(db.Integer, nullable=False)  # in minutes
    status = db.Column(db.String(20), default='submitted')  # submitted, evaluated
    
    def __repr__(self):
        return f"<ExamAttempt {self.exam_id}: {self.student_username}>"

class ExamResult(db.Model):
    __tablename__ = 'exam_results'
    
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.String(50), nullable=False)
    attempt_id = db.Column(db.Integer, nullable=False)
    student_username = db.Column(db.String(50), nullable=False)
    total_marks = db.Column(db.Integer, nullable=False)
    obtained_marks = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(5), nullable=False)  # A+, A, B+, B, C+, C, D, F
    detailed_feedback = db.Column(db.Text, nullable=False)  # JSON string of detailed feedback
    evaluated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ExamResult {self.exam_id}: {self.student_username} - {self.percentage}%>"

# Learning Pods Models
class LearningPod(db.Model):
    __tablename__ = 'learning_pods'
    
    id = db.Column(db.Integer, primary_key=True)
    pod_name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    cycle_number = db.Column(db.Integer, nullable=False, default=1)
    max_members = db.Column(db.Integer, default=4)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    teacher_username = db.Column(db.String(50))  # Optional teacher oversight

    # Cohort constraints for membership
    study_year = db.Column(db.Integer)
    department = db.Column(db.String(50))
    section = db.Column(db.String(10))
    
    def __repr__(self):
        return f"<LearningPod {self.pod_name}: {self.subject} (Cycle {self.cycle_number})>"

class PodMembership(db.Model):
    __tablename__ = 'pod_memberships'
    
    id = db.Column(db.Integer, primary_key=True)
    pod_id = db.Column(db.Integer, db.ForeignKey('learning_pods.id'), nullable=False)
    student_username = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), default='member')  # leader, member
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship
    pod = db.relationship('LearningPod', backref='memberships')
    
    def __repr__(self):
        return f"<PodMembership {self.student_username} in Pod {self.pod_id}>"

class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    
    # Learning Style Assessment
    learning_style = db.Column(db.String(50))  # visual, auditory, kinesthetic, reading
    preferred_pace = db.Column(db.String(20))  # fast, medium, slow
    collaboration_comfort = db.Column(db.String(20))  # high, medium, low
    
    # Academic Strengths/Weaknesses
    strong_subjects = db.Column(db.Text)  # JSON array
    weak_subjects = db.Column(db.Text)    # JSON array
    
    # Personality Traits
    leadership_tendency = db.Column(db.String(20))  # high, medium, low
    communication_style = db.Column(db.String(20))  # assertive, passive, balanced
    
    # Performance Data
    average_exam_score = db.Column(db.Float, default=0.0)
    attendance_rate = db.Column(db.Float, default=0.0)
    
    # Pod Preferences
    preferred_pod_size = db.Column(db.Integer, default=3)
    avoid_students = db.Column(db.Text)  # JSON array of usernames to avoid pairing with
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Digital resume fields (stored compactly as JSON + controls)
    resume_json = db.Column(db.Text)  # JSON blob containing resume data
    is_resume_public = db.Column(db.Boolean, default=False)
    public_slug = db.Column(db.String(64), unique=True)
    
    def __repr__(self):
        return f"<StudentProfile {self.username}: {self.learning_style} learner>"

class PodTask(db.Model):
    __tablename__ = 'pod_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    pod_id = db.Column(db.Integer, db.ForeignKey('learning_pods.id'), nullable=False)
    task_type = db.Column(db.String(50), nullable=False)  # micro_lesson, peer_challenge, reflection
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    
    # Task Content
    content = db.Column(db.Text)  # JSON with task details
    learning_objectives = db.Column(db.Text)  # JSON array
    
    # Timing
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    estimated_duration = db.Column(db.Integer)  # in minutes
    
    # Status
    status = db.Column(db.String(20), default='assigned')  # assigned, in_progress, completed, overdue
    
    # Relationship
    pod = db.relationship('LearningPod', backref='tasks')
    
    def __repr__(self):
        return f"<PodTask {self.title} for Pod {self.pod_id}>"

class TaskSubmission(db.Model):
    __tablename__ = 'task_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('pod_tasks.id'), nullable=False)
    student_username = db.Column(db.String(50), nullable=False)
    
    # Submission Content
    submission_content = db.Column(db.Text)  # JSON with answers/responses
    reflection_notes = db.Column(db.Text)
    
    # Peer Feedback
    peer_feedback_given = db.Column(db.Text)  # JSON with feedback given to others
    peer_feedback_received = db.Column(db.Text)  # JSON with feedback received
    
    # AI Analysis
    ai_feedback = db.Column(db.Text)
    collaboration_score = db.Column(db.Float)
    learning_impact_score = db.Column(db.Float)
    
    # Timing
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    time_spent = db.Column(db.Integer)  # in minutes
    
    # Status
    status = db.Column(db.String(20), default='submitted')  # submitted, reviewed, graded
    awarded_points = db.Column(db.Integer, default=0)
    teacher_feedback = db.Column(db.Text)
    evaluated_at = db.Column(db.DateTime)
    evaluated_by = db.Column(db.String(50))
    
    # Relationship
    task = db.relationship('PodTask', backref='submissions')
    
    def __repr__(self):
        return f"<TaskSubmission {self.student_username} for Task {self.task_id}>"

class MeritBadge(db.Model):
    __tablename__ = 'merit_badges'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    badge_type = db.Column(db.String(50), nullable=False)  # helper, explainer, connector, leader, collaborator
    badge_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Earning Context
    earned_for = db.Column(db.String(100))  # what action earned this badge
    pod_id = db.Column(db.Integer, db.ForeignKey('learning_pods.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('pod_tasks.id'))
    
    # Credits Reward
    credits_earned = db.Column(db.Integer, default=0)
    
    # Timing
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    pod = db.relationship('LearningPod')
    task = db.relationship('PodTask')
    
    def __repr__(self):
        return f"<MeritBadge {self.username}: {self.badge_name}>"

class CollaborationEvent(db.Model):
    __tablename__ = 'collaboration_events'
    
    id = db.Column(db.Integer, primary_key=True)
    pod_id = db.Column(db.Integer, db.ForeignKey('learning_pods.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('pod_tasks.id'), nullable=False)
    
    # Event Details
    event_type = db.Column(db.String(50), nullable=False)  # help_given, help_received, explanation, question_asked
    from_student = db.Column(db.String(50), nullable=False)
    to_student = db.Column(db.String(50))  # None for general events
    
    # Content
    description = db.Column(db.Text)
    impact_rating = db.Column(db.Integer)  # 1-5 scale
    
    # Timing
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    pod = db.relationship('LearningPod', backref='collaboration_events')
    task = db.relationship('PodTask', backref='collaboration_events')
    
    def __repr__(self):
        return f"<CollaborationEvent {self.event_type}: {self.from_student} -> {self.to_student}>"

class NfcCard(db.Model):
    __tablename__ = 'nfc_cards'

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='active')  # active, inactive
    email = db.Column(db.String(120))
    roll_no = db.Column(db.String(50))
    pin = db.Column(db.String(4))  # 4-digit PIN for payments over 500 credits
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<NfcCard {self.card_id} ({self.username}) - {self.status}>"


class ResultDeclaration(db.Model):
    __tablename__ = 'result_declarations'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    pdf_path = db.Column(db.String(255), nullable=False)
    passed_rolls = db.Column(db.Text)  # JSON array of roll numbers
    uploaded_by = db.Column(db.String(50))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ResultDeclaration {self.title} ({self.uploaded_at})>"

class ExamContest(db.Model):
    __tablename__ = 'exam_contests'
    
    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject_name = db.Column(db.String(100), nullable=False)
    syllabus = db.Column(db.Text, nullable=False)
    question_format = db.Column(db.String(50), nullable=False)  # multiple_choice, descriptive, mixed
    total_questions = db.Column(db.Integer, nullable=False)
    total_marks = db.Column(db.Integer, nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)  # in minutes
    difficulty_level = db.Column(db.String(20), default='medium')
    format_description = db.Column(db.Text)
    questions = db.Column(db.Text, nullable=False)  # JSON string of questions
    created_by = db.Column(db.String(50), nullable=False)  # Teacher username
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ExamContest {self.contest_id}: {self.title} by {self.created_by}>"

class ContestParticipation(db.Model):
    __tablename__ = 'contest_participations'
    
    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.String(50), nullable=False)
    student_username = db.Column(db.String(50), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    student_roll_no = db.Column(db.String(50))
    student_email = db.Column(db.String(120))
    department = db.Column(db.String(50))
    section = db.Column(db.String(10))
    answers = db.Column(db.Text, nullable=False)  # JSON string of answers
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    time_taken = db.Column(db.Integer, nullable=False)  # in minutes
    total_marks = db.Column(db.Integer, nullable=False)
    obtained_marks = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(5), nullable=False)
    rank = db.Column(db.Integer)  # Calculated rank in contest
    detailed_feedback = db.Column(db.Text)  # JSON string of detailed feedback
    
    def __repr__(self):
        return f"<ContestParticipation {self.student_username} in {self.contest_id}: {self.percentage}%>"


class PinRecoveryOTP(db.Model):
    __tablename__ = 'pin_recovery_otp'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    card_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<PinRecoveryOTP {self.username} - {self.otp_code}>"
