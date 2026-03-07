# UI Layout Specification

## Design Style

Modern SaaS-style dashboard.

Clean layout with card-based internship display.

---

# Layout Structure

Top navigation bar
Sidebar navigation
Main content area

---

# Sidebar Navigation

Dashboard
Application Tracker
Saved Internships

---

# Dashboard Page

Sections:

Search bar
Filters
Internship grid

---

# Internship Card

Each card displays:

Role
Company
Location
Skills tags
Apply button
Save button

Cards arranged in responsive grid.

Desktop
3 cards per row

Tablet
2 cards per row

Mobile
1 card per row

---

# Application Tracker Page

Kanban-style board.

Columns:

Saved
Applied
Interview
Rejected
Offer

Users can move internships between columns.

Status updates automatically update the database.

---

# Filters

Filter internships by:

Role
Category
Skills
Remote

---

# Search

Search matches:

role
company
skills

---

# Empty State

If no internships match search:

"No internships found."

---

# Loading State

Use skeleton loaders while fetching data.

---

# Mobile Design

Sidebar collapses into menu.

Internship cards stack vertically.
