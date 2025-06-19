# Product Requirements Document (PRD)

## 1. Introduction/Overview

The product is a web application designed to simplify the process of creating, managing, and analyzing surveys. Built with Streamlit for the front end, a Flask REST API for middleware, and backed by a PostgreSQL database, this application caters to businesses and individuals who need a straightforward platform to gather feedback, conduct research, or collect data. The application addresses the problem of cumbersome survey creation and analysis by providing an intuitive interface and robust backend for seamless survey management and insightful data visualization.

## 2. Goals & Objectives

### Business Goals:
- Provide a reliable and user-friendly platform for survey creation and management.
- Facilitate quick feedback collection and data-driven decision-making for businesses and individuals.
- Establish a scalable and secure application that can grow with user demand.

### User Goals:
- Enable users to easily create and customize surveys with various question types.
- Allow users to efficiently manage their surveys and view results in real-time.
- Provide respondents with a simple and straightforward survey completion experience without requiring authentication.

## 3. User Stories/Personas

### Primary User Roles:
1. **Survey Creator:** A business or individual user who creates and manages surveys.
2. **Survey Respondent:** An unauthenticated user who participates in surveys by providing responses.

### User Stories:
1. As a **Survey Creator**, I want to register and log into the application so that I can securely access my dashboard and manage my surveys.
2. As a **Survey Creator**, I want to create a new survey with a custom title, description, and various question types so that I can tailor it to my specific needs.
3. As a **Survey Creator**, I want to share a survey link with potential respondents so that I can collect their feedback easily.
4. As a **Survey Creator**, I want to view real-time responses in charts and graphs so that I can quickly analyze the data.
5. As a **Survey Respondent**, I want to access a survey via a link without logging in so that I can easily submit my responses.

## 4. Functional Requirements

### Front End Features:
- **User Registration and Login:** Interface for users to sign up and log in to access the survey dashboard.
- **Survey Dashboard:** A central hub for authenticated users to create, view, edit, activate/deactivate, and delete surveys.
- **Survey Creation Interface:** Allows defining survey title, description, and adding questions (multiple choice, open-ended, rating scales).
- **Survey Management:** Options to activate, deactivate, edit, or delete surveys.
- **Real-Time Response Display:** Graphical representation of survey responses for analysis.
- **Responsive Design:** Ensures accessibility on both desktop and mobile devices.

### Middleware Services:
- **User Authentication API:** Endpoints for registration, login, logout, and token management.
- **Survey Management API:** CRUD operations for surveys and associated questions.
- **Response Collection API:** Endpoints for collecting responses from unauthenticated users.
- **Data Validation and Sanitization:** Ensures all incoming data is clean and safe.
- **Rate Limiting:** Prevents abuse of public-facing endpoints for response submission.
- **Session Management:** Secure handling of user sessions and authentication tokens.

### Backend Capabilities:
- **User Table Management:** Handles user data including authentication credentials and roles.
- **Survey and Question Storage:** Maintains survey definitions and associated questions.
- **Response Handling:** Stores user responses and processes aggregated data for analysis.
- **Data Integrity:** Enforces relationships and constraints within the PostgreSQL database.
- **Security Measures:** Implements password hashing and protection against web vulnerabilities.

## 5. Non-Functional Requirements

- **Performance:** Supports hundreds of concurrent users with efficient data processing.
- **Security:** Implements basic security measures including password hashing and input validation.
- **Scalability:** Can be expanded in future phases to accommodate more users and features.
- **Usability:** Intuitive and easy-to-navigate user interface for both creators and respondents.
- **Reliability:** Ensures data accuracy and consistent uptime for user access.

## 6. Scope & Exclusions

### In Scope:
- Basic survey creation and management features.
- User registration and authentication.
- Real-time response visualization.
- Secure data handling and storage.

### Out of Scope:
- Advanced data analytics and reporting features.
- Integration with third-party applications (e.g., email, social media).
- Localization and multi-language support.

## 7. Assumptions & Constraints

### Assumptions:
- Users have basic internet access and can use a web browser.
- Initial deployment will support a limited number of concurrent users with room for scalability.

### Constraints:
- Limited to basic security measures; advanced security features will be considered in future phases.
- Initial deployment on a cloud infrastructure with constraints on budget and resources.

## 8. Future Considerations/Phases (Optional)

- Enhanced analytics and reporting capabilities.
- Integration with external services for distribution and marketing.
- Improved security features, including two-factor authentication.
- Support for a wider range of question types and survey logic.

This PRD provides a comprehensive guide to the development and deployment of the survey application, ensuring all stakeholders are aligned with the product vision and requirements.