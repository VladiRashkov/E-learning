

# E-Learning Platform
Project Description

This project is an e-learning platform that allows students to search for and enroll in online courses, and teachers to publish and manage the courses. Admins manage the platform by assigning teachers, approving students' enrollment to premium courses, and managing content visibility. The platform includes user roles (students, teachers, and admins), course management, and premium/public course subscriptions, with built-in search, progress tracking, and rating features.

## Features
- Users
Students, teachers, and admins are supported.
Admins assign teachers and manage user access.
Teachers manage courses, approve enrollments, and generate student reports.
Students can enroll in courses, track progress, rate courses, and more.
- Courses
Courses include a title, description, objectives, tags, and sections.
Teachers can create and manage course content.
Courses can be public or premium, with enrollment and subscription options.
Course ratings are calculated based on student feedback.
- Sections
Courses can be divided into sections, each with its own title, content, and optional description.
Sections can be sorted by ID or name.
Authentication and User Management
Anonymous users can browse courses but must register to access detailed content.
Users can log in and manage their accounts (students cannot change their email).
Admins and teachers have specific privileges to manage users, courses, and sections.
Course Subscriptions and Progress Tracking
Students can subscribe to a limited number of premium courses (up to 5) and an unlimited number of public courses.
Students can track their progress through the course sections.
Subscriptions can be managed (subscribed/unsubscribed) by students.
Search and Filter
Search functionality is available for courses by name, tag, and rating.
Pagination and sorting are supported.
Admin Features
Approve teacher registrations and course enrollments.
Deactivate/reactivate users.
Delete/hide courses and manage notifications for students.
Technologies Used
Framework: FastAPI
Database: Relational Database (PostgreSQL/MySQL/SQLite) for storing user and course information
Authentication: JWT Tokens for user authentication and role management
Deployment: Docker and AWS for containerization and cloud hosting
Documentation: Swagger for REST API documentation
Testing: Unit tests with at least 60% code coverage for the service layer
Version Control: Git for code management and collaboration
- Database
The project uses a relational database that follows normalization principles, avoiding data duplication and ensuring efficient data storage.

## Database Structure
Users: Information about students, teachers, and admins.
Courses: Each course has a unique title, description, tags, and sections.
Sections: A course can be divided into multiple sections with optional external resources.
Enrollment: Tracks students' enrollment and course progress.
Scripts
Database Creation Script: A script to create the database schema.
Data Population Script: A script to populate the database with initial data.
API Endpoints
The platform provides a RESTful API for managing users, courses, sections, and enrollments.

User Endpoints: CRUD operations for students, teachers, and admins.
Course Endpoints: Create, update, delete, and manage courses and sections.
Enrollment Endpoints: Enroll in courses, rate courses, and track progress.
For detailed API documentation, please refer to the Swagger Documentation.