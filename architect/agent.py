"""
Architect Agent
Main agent that analyzes codebase and suggests improvements
"""

import os
import ast
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class Improvement:
    """Represents a code improvement suggestion"""
    category: str  # 'performance', 'security', 'architecture', 'best_practices', 'testing'
    severity: str  # 'critical', 'high', 'medium', 'low'
    file_path: str
    line_number: Optional[int]
    issue: str
    suggestion: str
    impact: str
    priority: int  # 1-10, higher is more important


@dataclass
class CodeAnalysis:
    """Results of code analysis"""
    file_path: str
    complexity: int
    issues: List[Improvement]
    suggestions: List[str]
    metrics: Dict[str, Any]


class ArchitectAgent:
    """Architect agent that analyzes and improves codebase"""
    
    def __init__(self, project_root: str):
        """
        Initialize architect agent
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root)
        self.improvements: List[Improvement] = []
        self.analysis_results: List[CodeAnalysis] = []
        
    def analyze_project(self) -> Dict[str, Any]:
        """
        Analyze entire project and generate improvement suggestions
        
        Returns:
            Dictionary with analysis results and improvements
        """
        logger.info("Starting project analysis...")
        
        # Analyze backend
        backend_issues = self._analyze_backend()
        
        # Analyze frontend
        frontend_issues = self._analyze_frontend()
        
        # Analyze architecture
        architecture_issues = self._analyze_architecture()
        
        # Analyze security
        security_issues = self._analyze_security()
        
        # Analyze performance
        performance_issues = self._analyze_performance()
        
        # Combine all improvements
        all_improvements = (
            backend_issues + frontend_issues + 
            architecture_issues + security_issues + performance_issues
        )
        
        # Sort by priority
        all_improvements.sort(key=lambda x: x.priority, reverse=True)
        
        self.improvements = all_improvements
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_issues": len(all_improvements),
            "by_category": self._categorize_improvements(all_improvements),
            "by_severity": self._severity_breakdown(all_improvements),
            "improvements": [self._improvement_to_dict(imp) for imp in all_improvements],
            "recommendations": self._generate_recommendations(all_improvements)
        }
    
    def _analyze_backend(self) -> List[Improvement]:
        """Analyze backend code"""
        improvements = []
        backend_path = self.project_root / "backend"
        
        if not backend_path.exists():
            return improvements
        
        # Check for missing error handling
        for py_file in backend_path.rglob("*.py"):
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                    
                # Check for try-except blocks
                if "async def" in content or "def " in content:
                    if "try:" not in content and "except" not in content:
                        improvements.append(Improvement(
                            category="best_practices",
                            severity="medium",
                            file_path=str(py_file.relative_to(self.project_root)),
                            line_number=None,
                            issue="Missing error handling",
                            suggestion="Add try-except blocks for error handling",
                            impact="Unhandled exceptions can crash the application",
                            priority=6
                        ))
                
                # Check for logging
                if "import logging" not in content and "logger" not in content:
                    improvements.append(Improvement(
                        category="best_practices",
                        severity="low",
                        file_path=str(py_file.relative_to(self.project_root)),
                        line_number=None,
                        issue="Missing logging",
                        suggestion="Add logging for debugging and monitoring",
                        impact="Difficult to debug issues in production",
                        priority=4
                    ))
                
                # Check for type hints
                if "def " in content and "->" not in content:
                    improvements.append(Improvement(
                        category="best_practices",
                        severity="low",
                        file_path=str(py_file.relative_to(self.project_root)),
                        line_number=None,
                        issue="Missing type hints",
                        suggestion="Add type hints to function signatures",
                        impact="Better IDE support and code documentation",
                        priority=3
                    ))
                    
            except Exception as e:
                logger.warning(f"Error analyzing {py_file}: {e}")
        
        # Check for database connection handling
        if not (backend_path / "app" / "database.py").exists():
            improvements.append(Improvement(
                category="architecture",
                severity="high",
                file_path="backend/app/database.py",
                line_number=None,
                issue="Missing database module",
                suggestion="Create database.py with connection pooling and session management",
                impact="Database connections not properly managed",
                priority=8
            ))
        
        # Check for configuration management
        if not (backend_path / "app" / "config.py").exists():
            improvements.append(Improvement(
                category="architecture",
                severity="medium",
                file_path="backend/app/config.py",
                line_number=None,
                issue="Missing centralized configuration",
                suggestion="Create config.py using pydantic-settings for type-safe config",
                impact="Configuration scattered across files",
                priority=6
            ))
        
        return improvements
    
    def _analyze_frontend(self) -> List[Improvement]:
        """Analyze frontend code"""
        improvements = []
        frontend_path = self.project_root / "frontend"
        
        if not frontend_path.exists():
            return improvements
        
        # Check for error boundaries
        if not (frontend_path / "app" / "error.tsx").exists():
            improvements.append(Improvement(
                category="best_practices",
                severity="high",
                file_path="frontend/app/error.tsx",
                line_number=None,
                issue="Missing error boundary",
                suggestion="Create error.tsx for global error handling",
                impact="Unhandled errors can crash the entire app",
                priority=8
            ))
        
        # Check for loading states
        tsx_files = list(frontend_path.rglob("*.tsx")) + list(frontend_path.rglob("*.ts"))
        has_loading = any("loading.tsx" in str(f) for f in tsx_files)
        if not has_loading:
            improvements.append(Improvement(
                category="best_practices",
                severity="medium",
                file_path="frontend/app/loading.tsx",
                line_number=None,
                issue="Missing loading states",
                suggestion="Add loading.tsx for better UX during data fetching",
                impact="Users see blank screens during loading",
                priority=5
            ))
        
        # Check for environment variable validation
        if not (frontend_path / "lib" / "env.ts").exists():
            improvements.append(Improvement(
                category="security",
                severity="medium",
                file_path="frontend/lib/env.ts",
                line_number=None,
                issue="Missing environment variable validation",
                suggestion="Create env.ts to validate NEXT_PUBLIC_* variables",
                impact="Runtime errors from missing env vars",
                priority=6
            ))
        
        return improvements
    
    def _analyze_architecture(self) -> List[Improvement]:
        """Analyze overall architecture"""
        improvements = []
        
        # Check for API versioning
        api_path = self.project_root / "backend" / "app" / "api"
        if api_path.exists():
            if not any("v1" in str(p) for p in api_path.iterdir()):
                improvements.append(Improvement(
                    category="architecture",
                    severity="medium",
                    file_path="backend/app/api",
                    line_number=None,
                    issue="No API versioning",
                    suggestion="Implement API versioning (v1, v2) for future compatibility",
                    impact="Breaking changes will affect all clients",
                    priority=5
                ))
        
        # Check for rate limiting
        if not (self.project_root / "backend" / "app" / "middleware" / "rate_limit.py").exists():
            improvements.append(Improvement(
                category="security",
                severity="high",
                file_path="backend/app/middleware/rate_limit.py",
                line_number=None,
                issue="Missing rate limiting",
                suggestion="Implement rate limiting middleware to prevent abuse",
                impact="API vulnerable to DDoS and abuse",
                priority=9
            ))
        
        # Check for caching strategy
        if not (self.project_root / "backend" / "app" / "services" / "cache.py").exists():
            improvements.append(Improvement(
                category="performance",
                severity="medium",
                file_path="backend/app/services/cache.py",
                line_number=None,
                issue="No caching implementation",
                suggestion="Implement Redis or in-memory caching for frequently accessed data",
                impact="Unnecessary database/API calls slow down the app",
                priority=6
            ))
        
        # Check for monitoring/observability
        if not (self.project_root / "backend" / "app" / "monitoring").exists():
            improvements.append(Improvement(
                category="architecture",
                severity="medium",
                file_path="backend/app/monitoring",
                line_number=None,
                issue="Missing monitoring/observability",
                suggestion="Add Prometheus metrics, health checks, and structured logging",
                impact="Difficult to monitor app health and performance",
                priority=7
            ))
        
        return improvements
    
    def _analyze_security(self) -> List[Improvement]:
        """Analyze security issues"""
        improvements = []
        
        # Check for CORS configuration
        main_py = self.project_root / "backend" / "app" / "main.py"
        if main_py.exists():
            with open(main_py, 'r') as f:
                content = f.read()
                if "allow_origins=[\"*\"]" in content:
                    improvements.append(Improvement(
                        category="security",
                        severity="critical",
                        file_path="backend/app/main.py",
                        line_number=None,
                        issue="CORS allows all origins",
                        suggestion="Restrict CORS to specific domains in production",
                        impact="Security vulnerability - allows any origin to access API",
                        priority=10
                    ))
        
        # Check for authentication middleware
        if not (self.project_root / "backend" / "app" / "middleware" / "auth.py").exists():
            improvements.append(Improvement(
                category="security",
                severity="high",
                file_path="backend/app/middleware/auth.py",
                line_number=None,
                issue="Missing authentication middleware",
                suggestion="Implement JWT or OAuth2 authentication",
                impact="API endpoints are unprotected",
                priority=9
            ))
        
        # Check for input validation
        if not (self.project_root / "backend" / "app" / "middleware" / "validation.py").exists():
            improvements.append(Improvement(
                category="security",
                severity="high",
                file_path="backend/app/middleware/validation.py",
                line_number=None,
                issue="Missing input validation middleware",
                suggestion="Add request validation and sanitization",
                impact="Vulnerable to injection attacks",
                priority=8
            ))
        
        # Check for secrets management
        env_example = self.project_root / "backend" / ".env.example"
        if not env_example.exists():
            improvements.append(Improvement(
                category="security",
                severity="medium",
                file_path="backend/.env.example",
                line_number=None,
                issue="Missing .env.example",
                suggestion="Create .env.example with all required environment variables",
                impact="Developers may commit secrets or miss required config",
                priority=5
            ))
        
        return improvements
    
    def _analyze_performance(self) -> List[Improvement]:
        """Analyze performance issues"""
        improvements = []
        
        # Check for database query optimization
        if not (self.project_root / "backend" / "app" / "services" / "database" / "queries.py").exists():
            improvements.append(Improvement(
                category="performance",
                severity="medium",
                file_path="backend/app/services/database/queries.py",
                line_number=None,
                issue="No query optimization layer",
                suggestion="Implement query optimization with indexes and connection pooling",
                impact="Slow database queries",
                priority=6
            ))
        
        # Check for async operations
        main_py = self.project_root / "backend" / "app" / "main.py"
        if main_py.exists():
            with open(main_py, 'r') as f:
                content = f.read()
                # Check if using async properly
                if "async def" in content and "await" not in content:
                    improvements.append(Improvement(
                        category="performance",
                        severity="low",
                        file_path="backend/app/main.py",
                        line_number=None,
                        issue="Async functions not using await",
                        suggestion="Ensure async functions properly await async operations",
                        impact="Not leveraging async benefits",
                        priority=4
                    ))
        
        # Check for frontend code splitting
        frontend_path = self.project_root / "frontend"
        if frontend_path.exists():
            improvements.append(Improvement(
                category="performance",
                severity="medium",
                file_path="frontend",
                line_number=None,
                issue="No code splitting strategy",
                suggestion="Implement dynamic imports and route-based code splitting",
                impact="Large bundle size slows initial page load",
                priority=6
            ))
        
        return improvements
    
    def _categorize_improvements(self, improvements: List[Improvement]) -> Dict[str, int]:
        """Count improvements by category"""
        categories = {}
        for imp in improvements:
            categories[imp.category] = categories.get(imp.category, 0) + 1
        return categories
    
    def _severity_breakdown(self, improvements: List[Improvement]) -> Dict[str, int]:
        """Count improvements by severity"""
        severities = {}
        for imp in improvements:
            severities[imp.severity] = severities.get(imp.severity, 0) + 1
        return severities
    
    def _improvement_to_dict(self, imp: Improvement) -> Dict[str, Any]:
        """Convert Improvement to dictionary"""
        return {
            "category": imp.category,
            "severity": imp.severity,
            "file_path": imp.file_path,
            "line_number": imp.line_number,
            "issue": imp.issue,
            "suggestion": imp.suggestion,
            "impact": imp.impact,
            "priority": imp.priority
        }
    
    def _generate_recommendations(self, improvements: List[Improvement]) -> List[str]:
        """Generate high-level recommendations"""
        recommendations = []
        
        critical = [imp for imp in improvements if imp.severity == "critical"]
        if critical:
            recommendations.append(f"🚨 {len(critical)} critical security issues found - address immediately")
        
        high_priority = [imp for imp in improvements if imp.priority >= 8]
        if high_priority:
            recommendations.append(f"⚠️ {len(high_priority)} high-priority improvements identified")
        
        security_issues = [imp for imp in improvements if imp.category == "security"]
        if security_issues:
            recommendations.append(f"🔒 {len(security_issues)} security improvements recommended")
        
        performance_issues = [imp for imp in improvements if imp.category == "performance"]
        if performance_issues:
            recommendations.append(f"⚡ {len(performance_issues)} performance optimizations available")
        
        return recommendations
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate improvement report
        
        Args:
            output_path: Optional path to save report
            
        Returns:
            Report as string
        """
        analysis = self.analyze_project()
        
        report = f"""
# Architecture Improvement Report
Generated: {analysis['timestamp']}

## Summary
- Total Issues Found: {analysis['total_issues']}
- By Category: {json.dumps(analysis['by_category'], indent=2)}
- By Severity: {json.dumps(analysis['by_severity'], indent=2)}

## Recommendations
"""
        for rec in analysis['recommendations']:
            report += f"- {rec}\n"
        
        report += "\n## Detailed Improvements\n\n"
        
        # Group by category
        by_category = {}
        for imp in self.improvements:
            if imp.category not in by_category:
                by_category[imp.category] = []
            by_category[imp.category].append(imp)
        
        for category, imps in by_category.items():
            report += f"### {category.upper().replace('_', ' ')}\n\n"
            for imp in sorted(imps, key=lambda x: x.priority, reverse=True):
                report += f"**{imp.severity.upper()}** - {imp.file_path}\n"
                report += f"- Issue: {imp.issue}\n"
                report += f"- Suggestion: {imp.suggestion}\n"
                report += f"- Impact: {imp.impact}\n"
                report += f"- Priority: {imp.priority}/10\n\n"
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
        
        return report
