# Agents/PRD_Creator_Agent.py

import os
import re # Import regex for version number parsing
from Agents.Base_Agent import BaseAgent # Ensure this import path is correct

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
        # Determine the project root to create the 'output' folder correctly
        # This assumes PRD_Creator_Agent.py is in Agents/ and output is a sibling of Agents/
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.output_folder = os.path.join(self.project_root, "output")
        os.makedirs(self.output_folder, exist_ok=True) # Ensure output folder exists on init

    def _get_next_version_number(self, document_type: str) -> int:
        """
        Determines the next sequential version number for a document type (e.g., 'PRD')
        in the output folder. Looks for files like 'PRD_vX.md' and returns X + 1.
        """
        max_version = 0
        # Iterate over files in the output folder
        for filename in os.listdir(self.output_folder):
            # Check if the file starts with the document type prefix and ends with .md
            if filename.startswith(f"{document_type}_v") and filename.endswith(".md"):
                # Use regex to extract the version number
                match = re.match(rf"{document_type}_v(\d+)\.md", filename)
                if match:
                    version = int(match.group(1)) # Convert extracted string to integer
                    if version > max_version:
                        max_version = version # Update max_version if current file has a higher version
        return max_version + 1 # Return the next available version number

    def _save_document(self, document_content: str, document_type: str, version: int) -> str:
        """
        Saves the generated document to the 'output' folder with versioning.
        The filename format will be '{document_type}_v{version}.md'.

        Args:
            document_content (str): The content of the document to save.
            document_type (str): The type of document (e.g., "PRD", "WBS").
            version (int): The version number for the document.

        Returns:
            str: The full path to the saved file.
        """
        filename = f"{document_type}_v{version}.md"
        filepath = os.path.join(self.output_folder, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(document_content)
            return filepath
        except IOError as e:
            raise IOError(f"Failed to save document to {filepath}: {e}")

    def generate(self, front_end_reqs: str, middleware_reqs: str, backend_reqs: str, other_details: str) -> tuple[str, str]:
        """
        Generates a Product Requirements Document (PRD) based on input specifications
        and saves it to the 'output' folder with automatic versioning.

        Args:
            front_end_reqs (str): Description of front-end requirements.
            middleware_reqs (str): Description of middleware requirements.
            backend_reqs (str): Description of backend requirements.
            other_details (str): Any additional project details or requirements.

        Returns:
            tuple[str, str]: A tuple containing the generated PRD document content
                             and the full path to the saved PRD file.
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
            # Call the LLM to generate the PRD content
            generated_prd = self._call_llm(system_message=system_message)

            # Determine the next version number for PRDs
            next_version = self._get_next_version_number("PRD")

            # Save the generated PRD content to a file
            saved_filepath = self._save_document(generated_prd, "PRD", next_version)

            # Return both the content and the file path
            return generated_prd, saved_filepath
        except Exception as e:
            # Re-raise the exception after printing, allowing main_app.py to catch it
            raise Exception(f"Error from {self.agent_name}: {e}")