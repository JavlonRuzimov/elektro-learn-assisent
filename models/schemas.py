from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Organization:
    id: str
    name: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Organization":
        return cls(
            id=data.get("id", ""),
            name=data.get("name", "")
        )

@dataclass
class UserProfile:
    id: str
    email: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    role: str = "USER"
    avatar_url: Optional[str] = None
    energo_id: Optional[str] = None
    must_change_password: bool = False
    organizations: List[Organization] = field(default_factory=list)

    @property
    def full_name(self) -> str:
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join([p for p in parts if p]).strip()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserProfile":
        orgs = [Organization.from_dict(o) for o in data.get("organizations", [])]
        return cls(
            id=data.get("id", ""),
            email=data.get("email", ""),
            first_name=data.get("firstName", ""),
            last_name=data.get("lastName", ""),
            middle_name=data.get("middleName"),
            role=data.get("role", "USER"),
            avatar_url=data.get("avatarUrl"),
            energo_id=data.get("energoId"),
            must_change_password=data.get("mustChangePassword", False),
            organizations=orgs
        )

@dataclass
class LevelSummary:
    id: str
    title: str
    order_index: int
    is_locked: bool
    is_completed: bool
    completion_percent: int
    correct_answers_count: int
    attempts_count: int
    completed_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LevelSummary":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            order_index=data.get("orderIndex", 0),
            is_locked=data.get("isLocked", True),
            is_completed=data.get("isCompleted", False),
            completion_percent=data.get("completionPercent", 0),
            correct_answers_count=data.get("correctAnswersCount", 0),
            attempts_count=data.get("attemptsCount", 0),
            completed_at=data.get("completedAt")
        )

@dataclass
class ProgressOverview:
    total_xp: int
    completed_levels: int
    badge_label: str
    badge_bolts: int
    levels: List[LevelSummary] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProgressOverview":
        badge = data.get("badge", {})
        levels = [LevelSummary.from_dict(l) for l in data.get("levels", [])]
        return cls(
            total_xp=data.get("totalXp", 0),
            completed_levels=data.get("completedLevels", 0),
            badge_label=badge.get("label", "Noma'lum"),
            badge_bolts=badge.get("bolts", 0),
            levels=levels
        )

@dataclass
class QuestionOption:
    id: str
    option_text: str
    order_index: int = 0
    match_text: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QuestionOption":
        return cls(
            id=data.get("id", ""),
            option_text=data.get("optionText", ""),
            order_index=data.get("orderIndex", 0),
            match_text=data.get("matchText", "")
        )

@dataclass
class Question:
    id: str
    prompt: str
    type: str  # e.g. "SINGLE_CHOICE", "MATCHING"
    order_index: int = 0
    options: List[QuestionOption] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Question":
        opts = [QuestionOption.from_dict(o) for o in data.get("options", [])]
        return cls(
            id=data.get("id", ""),
            prompt=data.get("prompt", ""),
            type=data.get("type", "SINGLE_CHOICE"),
            order_index=data.get("orderIndex", 0),
            options=opts
        )

@dataclass
class Theory:
    id: str
    title: str
    content: str
    order_index: int
    total_questions: int
    answered_questions: int
    quiz_theory_id: Optional[str] = None

    @property
    def is_complete(self) -> bool:
        return self.answered_questions >= self.total_questions and self.total_questions > 0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Theory":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            content=data.get("content", ""),
            order_index=data.get("orderIndex", 0),
            total_questions=data.get("totalQuestions", 0),
            answered_questions=data.get("answeredQuestions", 0),
            quiz_theory_id=data.get("quizTheoryId")
        )

@dataclass
class LevelDetail:
    id: str
    title: str
    order_index: int
    theories: List[Theory] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LevelDetail":
        theories = [Theory.from_dict(t) for t in data.get("theories", [])]
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            order_index=data.get("orderIndex", 0),
            theories=theories
        )

@dataclass
class DailyPlan:
    plan_date: str
    target_questions: int
    daily_goal_correct: int
    is_plan_day: bool
    answered_count: int
    correct_count: int
    wrong_count: int
    completion_percent: int
    completed: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DailyPlan":
        return cls(
            plan_date=data.get("planDate", ""),
            target_questions=data.get("targetQuestions", 10),
            daily_goal_correct=data.get("dailyGoalCorrect", 10),
            is_plan_day=data.get("isPlanDay", True),
            answered_count=data.get("answeredCount", 0),
            correct_count=data.get("correctCount", 0),
            wrong_count=data.get("wrongCount", 0),
            completion_percent=data.get("completionPercent", 0),
            completed=data.get("completed", False)
        )

@dataclass
class AnswerResult:
    is_correct: bool
    correct_option_id: Optional[str] = None
    xp_earned: int = 0
    xp_message: Optional[str] = None
    hearts: Optional[int] = None
    plan_correct_count: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AnswerResult":
        return cls(
            is_correct=data.get("isCorrect", False),
            correct_option_id=data.get("correctOptionId"),
            xp_earned=data.get("xpEarned", 0),
            xp_message=data.get("xpMessage"),
            hearts=data.get("hearts"),
            plan_correct_count=data.get("planCorrectCount"),
            raw=data
        )

