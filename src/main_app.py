import os
import streamlit as st
from openai import OpenAIError  # Specific error class for OpenAI API issues

import sys  # <--- IMPORT sys module

# --- Add the project root to the Python path ---
# This allows imports like 'from Agents.PRD_Creator_Agent import PRDCreatorAgent'
# Go up one level from 'src' to 'PrecisionAI'
project_root = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir))
sys.path.append(project_root)
# --- End of path adjustment ---

from Agents.PRD_Creator_Agent import PRDCreatorAgent
from Agents.PRD_Reviewer_Agent import PRDReviewerAgent


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

    st.markdown("---")  # Separator for visual clarity

    # --- Default Values for Pre-population ---
    # These values elaborate on the "SurveyMonkey-like application"
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
            value=default_front_end,  # Pre-populated value
            placeholder="e.g., A responsive web application built with React...",
            help="Describe the user-facing part of your application. Think about the user interface (UI), user experience (UX), and key functionalities users will interact with directly."
        )

        middleware = st.text_area(
            '**Middleware:**',
            value=default_middleware,  # Pre-populated value
            placeholder="e.g., A Node.js API Gateway handling user requests...",
            help="Explain the services that connect your Front End to your Backend. This often includes APIs, business logic, data processing, authentication layers, and integration with external services."
        )

        backend = st.text_area(
            '**Backend:**',
            value=default_backend,  # Pre-populated value
            placeholder="e.g., A Python-based microservices architecture using Flask...",
            help="Detail the server-side components, databases, and core business logic. Consider data storage, server-side processing, external integrations, and security aspects."
        )

    st.markdown("---")  # Another separator

    with st.container():
        st.markdown("#### Additional Context (Optional but Recommended):")
        st.warning(
            "The more detail you provide, the more precise our blueprints will be!")
        others = st.text_area(
            '**Other Key Details/Requirements:**',
            value=default_others,  # Pre-populated value
            placeholder="e.g., Target audience, key performance indicators (KPIs)...",
            help="Use this section for any other critical information that doesn't fit neatly into the above categories, such as target users, business goals, security, performance, scalability, or specific compliance needs."
        )

    st.markdown("---")  # Final separator

    # --- Submit Button ---
    # Use columns to center the button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button('🚀 Generate My Blueprint!', type="primary"):
            # No need for empty check since fields are pre-populated
            user_input = {
                "Front End": front_end,
                "Middleware": middleware,
                "Backend": backend,
                "Other Details": others
            }

            st.success(
                '🎉 Requirements Submitted Successfully! PrecisionAI is now generating your blueprint.')
            st.info(
                "Please wait while our agents collaborate to create your detailed PRD and WBS.")

            # --- Step 1: Generate PRD with Agent #2 ---
            with st.spinner('Generating PRD with Agent #2...'):
                try:
                    # --- Instantiate and run Agent #2 ---
                    prd_creator = PRDCreatorAgent()  # Initialize the agent
                    generated_prd, saved_filepath = prd_creator.generate(
                        user_input["Front End"],
                        user_input["Middleware"],
                        user_input["Backend"],
                        user_input["Other Details"]
                    )

                    # Store PRD content in session state
                    st.session_state['generated_prd'] = generated_prd
                    # Store file path in session state
                    st.session_state['current_prd_filepath'] = saved_filepath
                    # Inform the user about the saved file
                    st.info(f"PRD document saved as: `{saved_filepath}`")
                    st.success("PRD Generation Complete!")

                    st.subheader(
                        "Generated Product Requirements Document (PRD):")
                    st.markdown(generated_prd)  # Display the PRD
                except ValueError as ve:
                    st.error(
                        f"Configuration Error: {ve}. Please ensure OPENAI_API_KEY is set correctly.")
                except OpenAIError as oe:
                    st.error(
                        f"OpenAI API Error: {oe}. Please check your API key and network connection.")
                except Exception as e:
                    st.error(
                        f"An unexpected error occurred during PRD generation: {e}")

                st.markdown("---") # Separator between generation and review

                # --- Step 2: Review PRD with Agent #3 (if PRD was generated successfully) ---
                if generated_prd: # Only proceed if PRD content exists
                    with st.spinner('Reviewing PRD with Agent #3...'):
                        try:
                            prd_reviewer = PRDReviewerAgent()
                            review_feedback = prd_reviewer.review_prd(generated_prd)
                            st.session_state['prd_review_feedback'] = review_feedback
                            st.success("PRD Review Complete!")

                            st.subheader("PRD Reviewer Feedback:")
                            st.markdown(review_feedback)

                        except ValueError as ve:
                            st.error(f"Configuration Error: {ve}. Please ensure OPENAI_API_KEY is set correctly.")
                        except OpenAIError as oe:
                            st.error(f"OpenAI API Error (Agent #3): {oe}. Please check your API key and network connection.")
                        except Exception as e:
                            st.error(f"An unexpected error occurred during PRD review (Agent #3): {e}")


            st.markdown("---")
            st.subheader("Your Input Summary (for verification):")
            # Display input in a clean JSON format for verification
            st.json(user_input)


if __name__ == '__main__':
    main()
