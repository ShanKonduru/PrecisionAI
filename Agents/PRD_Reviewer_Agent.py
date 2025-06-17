# Agents/PRD_Reviewer_Agent.py

import os
from Agents.Base_Agent import BaseAgent # Ensure this import path is correct


class PRDReviewerAgent(BaseAgent):
    """
    Agent #3: Specializes in meticulously reviewing Product Requirements Documents (PRDs).
    Inherits from BaseAgent for OpenAI API interaction.
    """

    def __init__(self, model: str = "gpt-4o", temperature: float = 0.5, max_tokens: int = 1500):
        """
        Initializes the PRDReviewerAgent.
        Sets a slightly lower temperature for more focused and critical feedback.
        Sets max_tokens suitable for a detailed review.
        """
        super().__init__(model=model, temperature=temperature, max_tokens=max_tokens)
        self.agent_name = "PRD Reviewer Agent"

    def generate(self, prd_document: str) -> str:
        """
        Public method to initiate the PRD review process.
        Acts as a wrapper around the internal _review_prd method.

        Args:
            prd_document (str): The content of the PRD document to be reviewed.

        Returns:
            str: The structured feedback for revision.
        """
        try:
            # Call the internal method that contains the actual review logic
            feedback = self.review_prd(prd_document)
            return feedback
        except Exception as e:
            # Catch exceptions from _review_prd and re-raise with more context
            raise Exception(f"Error during PRD review generation by {self.agent_name}: {e}")


    def review_prd(self, prd_document: str) -> str:
        """
        Reviews a provided PRD document and generates detailed, actionable feedback.

        Args:
            prd_document (str): The content of the PRD document to be reviewed.

        Returns:
            str: The structured feedback for revision.
        """
        system_message = f"""
You are an expert and highly critical Product Requirements Document (PRD) reviewer. Your task is to meticulously evaluate the completeness, clarity, consistency, and feasibility of the provided PRD.

**PRD Document for Review:**
{prd_document}

**Your Review must provide detailed, actionable feedback for revision, structured as follows:**

1.  **Overall Assessment:** A brief summary of the PRD's strengths and weaknesses.
2.  **Section-Specific Feedback:** For each of the following sections, identify specific areas for improvement, suggest missing details, highlight ambiguities, or point out inconsistencies. If a section is missing or incomplete, explicitly state that.
    * Introduction/Overview
    * Goals & Objectives
    * User Stories/Personas (Are they clear, complete, and sufficient?)
    * Functional Requirements (Front End, Middleware, Backend - Are they clearly defined, exhaustive, and unambiguous for each layer?)
    * Non-Functional Requirements (Are they adequately covered and measurable?)
    * Scope & Exclusions (Is the scope clear and well-defined?)
    * Assumptions & Constraints (Are all critical assumptions and constraints listed?)
3.  **Cross-Cutting Issues:**
    * **Clarity & Conciseness:** Are there any areas that are confusing, overly verbose, or vague?
    * **Consistency:** Are there any contradictions or inconsistencies within the document?
    * **Feasibility:** Are the requirements realistic and achievable given typical development constraints?
    * **Testability:** Are the requirements clear enough to be tested?
4.  **Prioritized Recommendations:** List the top 3-5 most critical changes that *must* be addressed in the next iteration, ordered by impact.

Your feedback should be direct, constructive, and aimed at helping the PRD creator (Agent #2) produce a high-quality, finalized PRD within the next 2-3 iterations.
"""
        try:
            # Call the LLM using the inherited method from BaseAgent
            # For a review, a user message might not be strictly necessary,
            # as the system message fully defines the task.
            review_feedback = self._call_llm(system_message=system_message)
            return review_feedback
        except Exception as e:
            raise Exception(f"Error from {self.agent_name}: {e}")
