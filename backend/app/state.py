"""Workflow state management for Medical Multi-Agents"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class WorkflowPhase(str, Enum):
    """Workflow execution phases"""
    INITIAL = "initial"
    DIAGNOSTIC = "diagnostic"
    REVIEW = "review"
    REPORT = "report"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class PatientData:
    """Patient information"""
    patient_id: str
    symptoms: List[str] = field(default_factory=list)
    vitals: Dict[str, Any] = field(default_factory=dict)
    medical_history: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DiagnosticResult:
    """Diagnostic result from diagnostic agent"""
    diagnosis: str
    confidence: float
    reasoning: str
    differential_diagnoses: List[str] = field(default_factory=list)
    recommended_tests: List[str] = field(default_factory=list)


@dataclass
class ReviewResult:
    """Review result from physician agent"""
    approved: bool
    reviewer_notes: str
    modifications: Optional[str] = None
    confidence: float = 0.0


@dataclass
class FinalReport:
    """Final medical report"""
    workflow_id: str
    patient_id: str
    diagnosis: str
    treatment_plan: List[str]
    follow_up: str
    created_at: str
    reviewed_by: str
    status: str = "completed"


@dataclass
class WorkflowState:
    """Complete workflow state"""
    workflow_id: str
    phase: WorkflowPhase = WorkflowPhase.INITIAL
    patient_data: Optional[PatientData] = None
    diagnostic_result: Optional[DiagnosticResult] = None
    review_result: Optional[ReviewResult] = None
    final_report: Optional[FinalReport] = None
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_error(self, error: str) -> None:
        """Add error to workflow"""
        self.errors.append(error)
        if self.phase != WorkflowPhase.FAILED:
            self.phase = WorkflowPhase.FAILED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary"""
        return {
            "workflow_id": self.workflow_id,
            "phase": self.phase.value,
            "patient_data": self.patient_data.__dict__ if self.patient_data else None,
            "diagnostic_result": self.diagnostic_result.__dict__ if self.diagnostic_result else None,
            "review_result": self.review_result.__dict__ if self.review_result else None,
            "final_report": self.final_report.__dict__ if self.final_report else None,
            "errors": self.errors,
            "metadata": self.metadata
        }