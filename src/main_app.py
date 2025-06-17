# src/main_app.py

import streamlit as st
import os
import sys

# --- Add the project root to the Python path ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(project_root)
# --- End of path adjustment ---

# Import your agent classes
from Agents.Base_Agent  import BaseAgent
from Agents.PRD_Creator_Agent import PRDCreatorAgent
from Agents.PRD_Reviewer_Agent import PRDReviewerAgent
from openai import OpenAIError

# --- Configuration ---
MAX_ITERATIONS = 3 # Define the maximum rounds of iteration for PRD generation/review

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
        st.warning("The more detail you provide, the more precise our blueprints will be!")
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
                st.error("Please provide at least some details in the input fields.")
                return # Exit if no input

            st.success('🎉 Requirements Submitted Successfully! PrecisionAI is now initiating multi-agent collaboration for your blueprint.')
            st.info(f"Starting iterative PRD generation and review for up to {MAX_ITERATIONS} rounds...")

            # Initialize history in session state to store all PRDs and feedbacks
            if 'prd_orchestration_history' not in st.session_state:
                st.session_state['prd_orchestration_history'] = []
            st.session_state['prd_orchestration_history'].clear() # Clear previous runs

            current_prd_content = None
            current_feedback = None

            # Instantiate agents once outside the loop for efficiency
            prd_creator = PRDCreatorAgent()
            prd_reviewer = PRDReviewerAgent()

            for i in range(MAX_ITERATIONS):
                st.subheader(f"--- Iteration {i + 1} ---")

                # Step 1: Generate/Revise PRD with Agent #2
                with st.spinner(f'Generating/Revising PRD (Iteration {i + 1}) with Agent #2...'):
                    try:
                        # For the first round, just generate. For subsequent, provide feedback.
                        if i == 0:
                            current_prd_content, saved_prd_filepath = prd_creator.generate(
                                user_input["Front End"],
                                user_input["Middleware"],
                                user_input["Backend"],
                                user_input["Other Details"]
                            )
                        else:
                            # Pass all original inputs AND the previous feedback for revision
                            current_prd_content, saved_prd_filepath = prd_creator.generate(
                                user_input["Front End"],
                                user_input["Middleware"],
                                user_input["Backend"],
                                user_input["Other Details"],
                                previous_feedback=current_feedback # Pass the feedback to the generator
                            )

                        st.success(f"PRD Generation/Revision Complete (Iteration {i + 1})!")
                        st.info(f"PRD saved as: `{saved_prd_filepath}`")
                        st.markdown("#### Generated/Revised PRD:")
                        st.markdown(current_prd_content)

                        # Store this round's PRD in history
                        st.session_state['prd_orchestration_history'].append({
                            'iteration': i + 1,
                            'type': 'PRD',
                            'content': current_prd_content,
                            'filepath': saved_prd_filepath
                        })

                    except ValueError as ve:
                        st.error(f"Configuration Error: {ve}. Please ensure OPENAI_API_KEY is set correctly.")
                        break # Stop loop on critical config error
                    except OpenAIError as oe:
                        st.error(f"OpenAI API Error (Iteration {i + 1}, Agent #2): {oe}. Stopping iterations.")
                        break # Stop loop on API error
                    except IOError as ioe:
                        st.error(f"File Saving Error (Iteration {i + 1}, Agent #2): {ioe}. Stopping iterations.")
                        break # Stop loop on file error
                    except Exception as e:
                        st.error(f"An unexpected error occurred during PRD generation/revision (Iteration {i + 1}, Agent #2): {e}. Stopping iterations.")
                        break # Stop loop on any other error

                st.markdown("---")

                # Step 2: Review PRD with Agent #3 (Only if PRD was generated/revised successfully in this iteration)
                if current_prd_content:
                    with st.spinner(f'Reviewing PRD (Iteration {i + 1}) with Agent #3...'):
                        try:
                            current_feedback = prd_reviewer.generate(current_prd_content) # Call generate for the reviewer
                            st.success(f"PRD Review Complete (Iteration {i + 1})!")
                            st.markdown("#### Reviewer Feedback:")
                            st.markdown(current_feedback)

                            # Store this round's feedback in history
                            st.session_state['prd_orchestration_history'].append({
                                'iteration': i + 1,
                                'type': 'Review Feedback',
                                'content': current_feedback
                            })

                        except ValueError as ve:
                            st.error(f"Configuration Error: {ve}. Please ensure OPENAI_API_KEY is set correctly.")
                            break
                        except OpenAIError as oe:
                            st.error(f"OpenAI API Error (Iteration {i + 1}, Agent #3): {oe}. Stopping iterations.")
                            break
                        except Exception as e:
                            st.error(f"An unexpected error occurred during PRD review (Iteration {i + 1}, Agent #3): {e}. Stopping iterations.")
                            break
                else:
                    st.warning(f"Skipping PRD review for Iteration {i + 1} as no PRD content was generated.")
                    break # Stop if PRD generation failed

                # Decide whether to continue to the next iteration
                if i < MAX_ITERATIONS - 1:
                    st.markdown("---")
                    st.info(f"Proceeding to Iteration {i + 2} to incorporate feedback...")
                else:
                    st.markdown("---")
                    st.success(f"Orchestration complete after {MAX_ITERATIONS} iterations.")

            st.markdown("---")
            st.subheader("Final Orchestration Summary:")

            if st.session_state['prd_orchestration_history']:
                final_prd_entry = next((item for item in reversed(st.session_state['prd_orchestration_history']) if item['type'] == 'PRD'), None)
                if final_prd_entry:
                    st.markdown(f"**Final PRD (Iteration {final_prd_entry['iteration']}, Saved to: `{final_prd_entry['filepath']}`):**")
                    st.markdown(final_prd_entry['content'])
                else:
                    st.warning("No PRD was successfully generated during the iterations.")

                st.markdown("### Full Orchestration History:")
                for item in st.session_state['prd_orchestration_history']:
                    if item['type'] == 'PRD':
                        st.markdown(f"**Iteration {item['iteration']} PRD (Saved to: `{item['filepath']}`):**")
                        with st.expander(f"View PRD Content (Iteration {item['iteration']})"):
                            st.markdown(item['content'])
                    elif item['type'] == 'Review Feedback':
                        st.markdown(f"**Iteration {item['iteration']} Review Feedback:**")
                        with st.expander(f"View Feedback Content (Iteration {item['iteration']})"):
                            st.markdown(item['content'])
                    st.markdown("---") # Separator between history items
            else:
                st.warning("No orchestration history available. An error might have occurred early on.")

            st.markdown("---")
            st.subheader("Your Original Input Summary:")
            st.json(user_input)

if __name__ == '__main__':
    main()