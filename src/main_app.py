import streamlit as st

def main():
    # --- Page Configuration (Optional but Recommended) ---
    st.set_page_config(
        page_title="PrecisionAI - Blueprinting System",
        page_icon="✨", # You can choose a different emoji or path to an image
        layout="centered" # "wide" for more horizontal space
    )

    # --- Title and Header ---
    st.title('✨ PrecisionAI: Intelligent Software Application Blueprinting System')
    st.markdown("""
    Welcome to PrecisionAI! This system helps you articulate your software application vision,
    transforming your high-level ideas into detailed Product Requirements Documents (PRDs)
    and comprehensive Work Breakdown Structures (WBS).
    """)

    st.subheader('💡 Provide Your Application Requirements Below:')

    st.markdown("---") # Separator for visual clarity

    # --- Input Fields with Help Text and Improved Styling ---
    # Using st.container for logical grouping
    with st.container():
        st.markdown("#### Application Architecture Components:")
        st.info("Please describe the core components of your desired application.")

        # Front End Input
        front_end = st.text_area(
            '**Front End:**',
            placeholder="e.g., A responsive web application built with React, featuring user authentication, data visualization dashboards, and a simple content management interface.",
            help="Describe the user-facing part of your application. Think about the user interface (UI), user experience (UX), and key functionalities users will interact with directly."
        )

        # Middleware Input
        middleware = st.text_area(
            '**Middleware:**',
            placeholder="e.g., A Node.js API Gateway handling user requests, data validation, and routing to microservices. It should also include a GraphQL layer for efficient data fetching.",
            help="Explain the services that connect your Front End to your Backend. This often includes APIs, business logic, data processing, authentication layers, and integration with external services."
        )

        # Backend Input
        backend = st.text_area(
            '**Backend:**',
            placeholder="e.g., A Python-based microservices architecture using Flask, with services for user management, product catalog, order processing, and analytics. Data stored in PostgreSQL and MongoDB.",
            help="Detail the server-side components, databases, and core business logic. Consider data storage, server-side processing, external integrations, and security aspects."
        )

    st.markdown("---") # Another separator

    # --- Other Details Input ---
    with st.container():
        st.markdown("#### Additional Context (Optional but Recommended):")
        st.warning("The more detail you provide, the more precise our blueprints will be!")
        others = st.text_area(
            '**Other Key Details/Requirements:**',
            placeholder="e.g., Target audience, key performance indicators (KPIs), specific security requirements (e.g., GDPR compliance), deployment environment considerations (e.g., AWS, Azure), integration with third-party services (e.g., payment gateways, CRM systems).",
            help="Use this section for any other critical information that doesn't fit neatly into the above categories, such as target users, business goals, security, performance, scalability, or specific compliance needs."
        )

    st.markdown("---") # Final separator

    # --- Submit Button ---
    col1, col2, col3 = st.columns([1, 2, 1]) # Use columns to center the button
    with col2:
        if st.button('🚀 Generate My Blueprint!', type="primary"):
            if not front_end and not middleware and not backend:
                st.error("Please provide at least some details for the Front End, Middleware, or Backend to generate a blueprint.")
            else:
                # Store user input in a dictionary
                user_input = {
                    "Front End": front_end,
                    "Middleware": middleware,
                    "Backend": backend,
                    "Other Details": others
                }

                st.success('🎉 Requirements Submitted Successfully! PrecisionAI is now generating your blueprint.')
                st.info("Please wait while our agents collaborate to create your detailed PRD and WBS.")
                # In a real application, you would pass 'user_input' to Agent #2 here
                # Example:
                # generate_prd_and_wbs(user_input)

                st.markdown("---")
                st.subheader("Your Input Summary (for verification):")
                st.json(user_input) # Display input in a clean JSON format for verification

if __name__ == '__main__':
    main()