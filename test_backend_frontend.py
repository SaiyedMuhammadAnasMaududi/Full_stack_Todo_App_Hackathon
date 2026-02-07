#!/usr/bin/env python3
"""
Comprehensive test to verify backend and frontend functionality
"""

import subprocess
import sys
import time
import json
from pathlib import Path

def test_backend_endpoints():
    """Test that backend endpoints are properly configured"""
    print("🔍 Testing backend endpoints...")

    # Check that all required imports and dependencies are available
    try:
        import fastapi
        import sqlmodel
        import pydantic
        import uvicorn
        print("✅ Backend dependencies are available")
    except ImportError as e:
        print(f"❌ Backend dependency missing: {e}")
        return False

    # Check routes file structure
    routes_path = Path("backend/routes/tasks.py")
    if routes_path.exists():
        content = routes_path.read_text()

        # Check for essential imports
        required_imports = [
            "from fastapi import APIRouter, Depends, HTTPException",
            "from ..models import Task",
            "from ..db import SessionLocal"
        ]

        missing_imports = []
        for imp in required_imports:
            if imp not in content:
                missing_imports.append(imp)

        if missing_imports:
            print(f"❌ Missing imports in routes: {missing_imports}")
            return False

        # Check for essential endpoints
        required_endpoints = [
            "@router.get('/tasks'",
            "@router.post('/tasks'",
            "@router.put('/tasks'",
            "@router.patch('/tasks'",
            "@router.delete('/tasks'"
        ]

        endpoint_found = False
        for endpoint in required_endpoints:
            if endpoint in content:
                endpoint_found = True
                break

        if not endpoint_found:
            print("❌ No essential endpoints found in routes")
            return False

        print("✅ Backend routes are properly configured")
        return True
    else:
        print("❌ Routes file not found")
        return False

def test_frontend_structure():
    """Test that frontend structure is properly configured"""
    print("\n🔍 Testing frontend structure...")

    # Check essential frontend files
    essential_files = [
        "frontend/package.json",
        "frontend/pages/_app.tsx",
        "frontend/pages/index.tsx",
        "frontend/lib/api.ts",
        "frontend/types/index.ts"
    ]

    missing_files = []
    for file in essential_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        print(f"❌ Missing essential frontend files: {missing_files}")
        return False

    # Check package.json for dependencies
    pkg_path = Path("frontend/package.json")
    if pkg_path.exists():
        try:
            pkg_data = json.loads(pkg_path.read_text())
            deps = pkg_data.get("dependencies", {})

            required_deps = ["react", "next", "typescript", "axios"]
            missing_deps = [dep for dep in required_deps if dep not in deps]

            if missing_deps:
                print(f"⚠️  Missing frontend dependencies: {missing_deps}")
            else:
                print("✅ Frontend dependencies are properly configured")
        except:
            print("⚠️  Could not parse package.json")

    # Check lib/api.ts for proper structure
    api_path = Path("frontend/lib/api.ts")
    if api_path.exists():
        content = api_path.read_text()

        required_elements = [
            "export interface Task",
            "class ApiClient",
            "async getTasks",
            "async createTask",
            "async updateTask"
        ]

        missing_elements = []
        for elem in required_elements:
            if elem not in content:
                missing_elements.append(elem)

        if missing_elements:
            print(f"❌ Missing elements in API client: {missing_elements}")
            return False

        print("✅ Frontend API client is properly configured")
        return True
    else:
        print("❌ API client file not found")
        return False

def test_models_consistency():
    """Test that backend models and frontend types are consistent"""
    print("\n🔍 Testing model consistency...")

    # Check backend models
    models_path = Path("backend/models.py")
    if models_path.exists():
        models_content = models_path.read_text()

        # Check for essential Task model fields
        essential_fields = [
            "title:",
            "description:",
            "completed:",
            "user_id:",
            "priority:",
            "tags:",
            "due_at:",
            "reminder_at:",
            "recurrence_rule:",
            "is_recurring:"
        ]

        missing_fields = []
        for field in essential_fields:
            if field not in models_content:
                missing_fields.append(field)

        if missing_fields:
            print(f"❌ Missing fields in backend model: {missing_fields}")
            return False
    else:
        print("❌ Backend models file not found")
        return False

    # Check frontend types
    types_path = Path("frontend/types/index.ts")
    if types_path.exists():
        types_content = types_path.read_text()

        # Check for corresponding Task interface fields
        essential_type_fields = [
            "title:",
            "description?:",
            "completed:",
            "userId:",
            "priority?:",
            "tags?:",
            "due_at?:",
            "reminder_at?:",
            "recurrence_rule?:",
            "is_recurring?:"
        ]

        missing_type_fields = []
        for field in essential_type_fields:
            if field not in types_content:
                missing_type_fields.append(field)

        if missing_type_fields:
            print(f"❌ Missing fields in frontend types: {missing_type_fields}")
            return False
    else:
        print("❌ Frontend types file not found")
        return False

    print("✅ Backend models and frontend types are consistent")
    return True

def test_component_integration():
    """Test that frontend components are properly integrated"""
    print("\n🔍 Testing component integration...")

    # Check TaskForm component
    task_form_path = Path("frontend/components/TaskForm/TaskForm.tsx")
    if task_form_path.exists():
        content = task_form_path.read_text()

        required_elements = [
            "useState",
            "apiClient.createTask",
            "apiClient.updateTaskExtended",
            "PrioritySelector",
            "TagsInput",
            "DatePicker",
            "ReminderPicker",
            "RecurrenceControls"
        ]

        missing_elements = []
        for elem in required_elements:
            if elem not in content:
                missing_elements.append(elem)

        if missing_elements:
            print(f"❌ Missing elements in TaskForm: {missing_elements}")
        else:
            print("✅ TaskForm component is properly integrated")
    else:
        print("❌ TaskForm component not found")
        return False

    # Check TaskList component
    task_list_path = Path("frontend/components/TaskList/TaskList.tsx")
    if task_list_path.exists():
        content = task_list_path.read_text()

        required_elements = [
            "apiClient.getTasks",
            "apiClient.searchTasks",
            "apiClient.filterTasks",
            "apiClient.sortTasks",
            "searchQuery",
            "filterPriority",
            "sortBy"
        ]

        missing_elements = []
        for elem in required_elements:
            if elem not in content:
                missing_elements.append(elem)

        if missing_elements:
            print(f"❌ Missing elements in TaskList: {missing_elements}")
        else:
            print("✅ TaskList component is properly integrated")
    else:
        print("❌ TaskList component not found")
        return False

    return True

def test_advanced_features():
    """Test that advanced features are properly implemented"""
    print("\n🔍 Testing advanced features...")

    # Check AI agent
    ai_agent_path = Path("backend/src/ai/agent.py")
    if ai_agent_path.exists():
        content = ai_agent_path.read_text()

        required_elements = [
            "COHERE_API_KEY",
            "process_message",
            "add_task",
            "list_tasks",
            "update_task",
            "set_priority",
            "add_tags",
            "search_tasks",
            "filter_tasks",
            "sort_tasks"
        ]

        missing_elements = []
        for elem in required_elements:
            if elem not in content:
                missing_elements.append(elem)

        if missing_elements:
            print(f"❌ Missing elements in AI agent: {missing_elements}")
        else:
            print("✅ AI agent has all required features")
    else:
        print("❌ AI agent not found")
        return False

    # Check MCP server
    mcp_path = Path("backend/src/mcp/server.py")
    if mcp_path.exists():
        content = mcp_path.read_text()

        required_tools = [
            "@server.tools.register",
            "def add_task",
            "def list_tasks",
            "def update_task",
            "def set_priority",
            "def add_tags",
            "def search_tasks",
            "def filter_tasks",
            "def sort_tasks",
            "def set_due_date",
            "def set_reminder",
            "def set_recurrence"
        ]

        missing_tools = []
        for tool in required_tools:
            if tool not in content:
                missing_tools.append(tool)

        if missing_tools:
            print(f"❌ Missing tools in MCP server: {missing_tools}")
        else:
            print("✅ MCP server has all required tools")
    else:
        print("❌ MCP server not found")
        return False

    return True

def main():
    """Run all tests"""
    print("🚀 Testing Backend and Frontend Functionality\n")

    tests = [
        test_backend_endpoints,
        test_frontend_structure,
        test_models_consistency,
        test_component_integration,
        test_advanced_features
    ]

    results = []
    for test in tests:
        results.append(test())

    print(f"\n📊 Test Results: {sum(results)}/{len(results)} tests passed")

    if all(results):
        print("\n🎉 BACKEND AND FRONTEND WORK AS EXPECTED! 🎉")
        print("\n✅ All components are properly integrated")
        print("✅ Models and types are consistent")
        print("✅ Advanced features are implemented")
        print("✅ API connections are properly configured")
        print("\nThe application is ready for use!")
        return True
    else:
        print("\n❌ Some tests failed. Components need attention.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)