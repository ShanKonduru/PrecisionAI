from Agents.Base_Agent import BaseAgent


class PRDCreatorAgent(BaseAgent):
    """
    Agent #2: Specializes in generating comprehensive Product Requirements Documents (PRDs).
    Inherits from BaseAgent for OpenAI API interaction.
    """

    def __init__(self, model: str = "gpt-4o", temperature: float = 0.7, max_tokens: int = 2500):
        """
        Initializes the PRDCreatorAgent.
        Sets a higher max_tokens default suitable for PRD generation.
        """
        super().__init__(model=model, temperature=temperature, max_tokens=max_tokens)
        self.agent_name = "PRD Creator Agent"

    def generate(self, front_end_reqs: str, middleware_reqs: str, backend_reqs: str, other_details: str) -> str:
        """
        Generates a Product Requirements Document (PRD) based on input specifications.

        Args:
            front_end_reqs (str): Description of front-end requirements.
            middleware_reqs (str): Description of middleware requirements.
            backend_reqs (str): Description of backend requirements.
            other_details (str): Any additional project details or requirements.

        Returns:
            str: The generated PRD document.
        """
        system_message = f"""
You are an expert Product Manager tasked with creating a comprehensive and detailed Product Requirements Document (PRD). Your goal is to translate high-level technical specifications into a clear, actionable document for development teams and stakeholders.

**Input Specifications for the Application:**
- Front End: {front_end_reqs}
- Middleware: {middleware_reqs}
- Backend: {backend_reqs}
- Other Details: {other_details}

**PRD Structure Requirements:**

Your PRD must include, but not be limited to, the following sections. Ensure each section is thoroughly populated with relevant details based on the provided inputs and logical assumptions to create a complete product vision:

1.  **Introduction/Overview:** Briefly describe the product, its purpose, and the problem it solves.
2.  **Goals & Objectives:** What are the key business and user goals for this application?
3.  **User Stories/Personas:** Define the primary user roles and at least 3-5 user stories (e.g., "As a [user role], I want to [action] so that [benefit]").
4.  **Functional Requirements:** Detail what the system *must do* from a user's perspective, specifically broken down by Front End, Middleware, and Backend components.
    * **Front End Features:** List user-facing functionalities and UI interactions.
    * **Middleware Services:** Describe the logic, APIs, and data orchestration handled by middleware.
    * **Backend Capabilities:** Outline database interactions, business logic, authentication, and external integrations.
5.  **Non-Functional Requirements:** Cover aspects like performance, security, scalability, usability, and reliability.
6.  **Scope & Exclusions:** Clearly define what is in scope for this version and what is explicitly out of scope.
7.  **Assumptions & Constraints:** List any assumptions made and known limitations or constraints.
8.  **Future Considerations/Phases (Optional):** Briefly mention potential future enhancements.

Format the PRD clearly with headings and subheadings for readability. Ensure the language is precise and unambiguous.
"""
        try:
            # Call the LLM using the inherited method from BaseAgent
            generated_prd = self._call_llm(system_message=system_message)
            return generated_prd
        except Exception as e:
            # Re-raise or handle as appropriate for your application flow
            return f"Error from {self.agent_name}: {e}"
