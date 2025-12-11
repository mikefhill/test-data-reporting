from dataclasses import dataclass, field
from datetime import datetime as dt
from typing import Dict, Any, Optional
from enum import Enum

class Status(Enum):
    """The status of a test outcome."""
    PASS = "PASS"
    FAIL = "FAIL"
    ABORTED = "ABORTED"
    UNKNOWN = "UNKNOWN"

@dataclass
class PhaseSummary:
    """A summary of a phase."""
    name: str
    status: str
    start_time: Optional[dt] = None
    end_time: Optional[dt] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TestStageSummary:
    """A summary of a test stage."""
    name: str
    status: str
    start_time: Optional[dt] = None
    end_time: Optional[dt] = None
    phases: Dict[str, PhaseSummary] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DeviceReport:
    """A report for a single device."""
    device_id: str
    fw_version: str
    status: Status
    test_stages: Dict[str, TestStageSummary] = field(default_factory=dict)
    attachments: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FullAssemblyReport:
    """A report for a full assembly."""
    device_id: str
    status: str
    device_reports: Dict[str, DeviceReport] = field(default_factory=dict)
    attachments: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: dt = field(default_factory=dt.now)
    schema_version: str = "1.0.0"

    @property
    def overall_status(self) -> Status:
        """The overall status of the report."""
        if any(device_report.status == Status.FAIL for device_report in self.device_reports.values()):
            return Status.FAIL
        if any(device_report.status == Status.ABORTED for device_report in self.device_reports.values()):
            return Status.ABORTED
        if any(device_report.status == Status.UNKNOWN for device_report in self.device_reports.values()):
            return Status.UNKNOWN
        return Status.PASS
