# src/main_app.py

import streamlit as st
import os
import sys

# --- Add the project root to the Python path ---
project_root = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir))
sys.path.append(project_root)
# --- End of path adjustment ---

from Agents.Orchestrator_Agent import Orchestrator
from openai import OpenAIError

# --- Configuration ---
# MAX_ITERATIONS is now passed to the Orchestrator
# Define the maximum rounds of iteration for PRD generation/review
MAX_ITERATIONS = 3


def main():
    # --- Page Configuration ---
    st.set_page_config(
        page_title="PrecisionAI - Blueprinting System",
        page_icon="✨",
        layout="centered"
    )

    # --- Title and Header ---
    st.title('✨ PrecisionAI: Intelligent Software Application Blueprinting System')
    st.markdown("""
    Welcome to PrecisionAI! This system helps you articulate your software application vision,
    transforming your high-level ideas into detailed Product Requirements Documents (PRDs)
    and comprehensive Work Breakdown Structures (WBS).
    """)

    st.subheader('💡 Provide Your Application Requirements Below:')

    st.markdown("---")

    # --- Default Values for Pre-population (for easy testing) ---
    default_front_end = """
    A web application built with Streamlit.
    Key features include:
    - User registration and login forms.
    - Dashboard for authenticated users to create new surveys.
    - Survey creation interface: allowing users to define survey title, description, and add various question types (e.g., multiple choice, open-ended text, rating scales).
    - Survey management: view, edit, activate, deactivate, and delete surveys.
    - Shareable survey links for respondents.
    - Real-time display of survey responses (charts/graphs) for survey creators.
    - Responsive design for desktop and mobile access.
    """

    default_middleware = """
    A Flask REST API acting as the central communication layer.
    Key functionalities include:
    - User authentication endpoints (register, login, logout, token management).
    - API endpoints for survey creation, retrieval, update, and deletion (CRUD).
    - API endpoints for managing survey questions and options.
    - API endpoints for collecting survey responses from unauthenticated users.
    - Data validation and sanitization for all incoming requests.
    - Rate limiting for public-facing response submission.
    - Secure handling of user sessions and authentication tokens.
    """

    default_backend = """
    A PostgreSQL database for persistent data storage.
    Database schema will include tables for:
    - Users (username, password hash, email, roles).
    - Surveys (survey ID, title, description, creator ID, status).
    - Questions (question ID, survey ID, question type, question text, options/choices if applicable).
    - Responses (response ID, survey ID, respondent ID/IP, submission timestamp).
    - Answers (answer ID, response ID, question ID, answer value).
    Backend logic for:
    - User authentication and authorization.
    - Storing and retrieving survey definitions and user-submitted responses.
    - Aggregating and processing survey results for analytical display.
    - Data integrity and relationship management within PostgreSQL.
    """

    default_others = """
    **Target Audience:** Businesses and individuals needing to quickly create and distribute surveys for feedback, research, or data collection.
    **Authentication:** Simple username and password authentication for survey creators. Respondents will not require authentication.
    **Scalability:** Initial focus on supporting hundreds of concurrent users; future scaling considerations will be addressed in subsequent phases.
    **Security:** Basic security measures including password hashing, input validation, and protection against common web vulnerabilities (e.g., SQL injection, XSS).
    **Deployment:** Intended for cloud deployment (e.g., Docker containers on AWS ECS or similar).
    """

    # --- Input Fields with Help Text and Pre-populated Values ---
    with st.container():
        st.markdown("#### Application Architecture Components:")
        st.info("Please describe the core components of your desired application.")

        front_end = st.text_area(
            '**Front End:**',
            value=default_front_end,
            placeholder="e.g., A responsive web application built with React...",
            help="Describe the user-facing part of your application. Think about the user interface (UI), user experience (UX), and key functionalities users will interact with directly."
        )

        middleware = st.text_area(
            '**Middleware:**',
            value=default_middleware,
            placeholder="e.g., A Node.js API Gateway handling user requests...",
            help="Explain the services that connect your Front End to your Backend. This often includes APIs, business logic, data processing, authentication layers, and integration with external services."
        )

        backend = st.text_area(
            '**Backend:**',
            value=default_backend,
            placeholder="e.g., A Python-based microservices architecture using Flask...",
            help="Detail the server-side components, databases, and core business logic. Consider data storage, server-side processing, external integrations, and security aspects."
        )

    st.markdown("---")

    with st.container():
        st.markdown("#### Additional Context (Optional but Recommended):")
        st.warning(
            "The more detail you provide, the more precise our blueprints will be!")
        others = st.text_area(
            '**Other Key Details/Requirements:**',
            value=default_others,
            placeholder="e.g., Target audience, key performance indicators (KPIs)...",
            help="Use this section for any other critical information that doesn't fit neatly into the above categories, such as target users, business goals, security, performance, scalability, or specific compliance needs."
        )

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button('🚀 Generate My Blueprint!', type="primary"):
            user_input = {
                "Front End": front_end,
                "Middleware": middleware,
                "Backend": backend,
                "Other Details": others
            }

            if not any(user_input.values()):
                st.error(
                    "Please provide at least some details in the input fields.")
                return  # Exit if no input

            st.success(
                '🎉 Requirements Submitted Successfully! PrecisionAI is now initiating multi-agent collaboration for your blueprint.')
            st.info(
                f"Starting iterative PRD generation and review for up to {MAX_ITERATIONS} rounds (handled by Orchestrator)...")

            # Initialize the Orchestrator
            try:
                orchestrator = Orchestrator(
                    max_review_iterations=MAX_ITERATIONS)
            except Exception as e:
                st.error(
                    f"Failed to initialize Orchestrator: {e}. Please check your environment setup (e.g., OPENAI_API_KEY).")
                return

            current_prd_content = None
            saved_prd_filepath = None

            try:
                # Run the PRD workflow using the Orchestrator
                with st.spinner('Orchestrating PRD generation and review... This may take a few moments.'):
                    final_prd_content, final_prd_path = orchestrator.run_prd_workflow(
                        front_end_reqs=user_input["Front End"],
                        middleware_reqs=user_input["Middleware"],
                        backend_reqs=user_input["Backend"],
                        other_details=user_input["Other Details"]
                    )
                st.success('✅ Orchestration Complete!')
                current_prd_content = final_prd_content
                saved_prd_filepath = final_prd_path

            except ValueError as ve:
                st.error(
                    f"Configuration Error during orchestration: {ve}. Please ensure OPENAI_API_KEY is set correctly.")
            except OpenAIError as oe:
                st.error(f"OpenAI API Error during orchestration: {oe}.")
            except IOError as ioe:
                st.error(f"File Saving Error during orchestration: {ioe}.")
            except Exception as e:
                st.error(
                    f"An unexpected error occurred during orchestration: {e}.")

            st.markdown("---")
            st.subheader("Final Orchestration Summary:")

            if current_prd_content:
                st.markdown(
                    f"**Final PRD (Saved to: `{saved_prd_filepath}`):**")
                st.markdown(current_prd_content)
            else:
                st.warning(
                    "No PRD was successfully generated by the Orchestrator.")

            st.markdown("---")
            st.subheader("Your Original Input Summary:")
            st.json(user_input)


if __name__ == '__main__':
    main()
