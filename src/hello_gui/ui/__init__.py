# ============================================================================
#  HelloGUI - Python Data Stream Visualization Demo
#  Module: ui/__init__.py (UI Subpackage Initialization)
#
#  Purpose : Export UI components and widget classes
# ============================================================================

"""
Initialize UI subpackage.

Exports UI tab components.
"""

from hello_gui.ui.dashboard_tab import DashboardTab
from hello_gui.ui.config_tab import ConfigTab

__all__ = ["DashboardTab", "ConfigTab"]
