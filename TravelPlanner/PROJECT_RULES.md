# Project Development Rules: TravelPlanner

This document defines the core coding guidelines and constraints for the TravelPlanner project. All AI agents assisting with this project must strictly adhere to these rules.

## Core Directives
- **Follow Django best practices**: Maintain standard Django folder structures, name models/views standardly, and leverage built-in framework features.
- **Use Class-Based Views (CBVs)**: Unless specifically instructed or unless function-based views (FBVs) are cleaner for a specific edge-case, prefer Django's built-in class-based views (e.g., `ListView`, `DetailView`, `CreateView`).
- **Keep code modular and reusable**: Avoid monolithic functions or duplicate logic. Use clean mixins, helper methods, or services where appropriate.
- **Follow PEP 8**: Ensure all Python code matches Python's styling guidelines.
- **Write clean, commented code**: Document complex logic, views, models, and custom methods. Keep comments concise and useful.
- **Keep functions small**: Each function or method should serve a single clear purpose.

## Templates & Styling
- **Never duplicate HTML**: Reuse templates, layouts, and components.
- **Use template inheritance**: Extend `base.html` for all front-facing pages. Use `{% include %}` for sub-template components.
- **Use Bootstrap 5 only**: All responsive design, layout styling, grid systems, and spacing utilities should utilize Bootstrap 5 components and utility classes. Do not introduce custom stylesheet utilities unless Bootstrap does not support them.

## Safety & Modification Constraints
- **Do not modify existing working functionality unless explicitly instructed**: Respect the existing state of models, routes, templates, and configurations.
- **Never remove existing code**: Refactor or extend existing blocks safely instead of deleting functional components.
