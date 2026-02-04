"""
DSPy signature definitions for guardrails judge.
"""

import dspy


class GuardrailsJudgeSignature(dspy.Signature):
    """
    DSPy signature for judging whether a request should be answered or blocked.

    This signature defines the input/output contract for the guardrails judge.
    """

    text = dspy.InputField(desc="User's instruction or request to the assistant")
    guardrails = dspy.InputField(
        desc="Safety rules and constraints that determine acceptable vs unacceptable requests"
    )
    expertise = dspy.InputField(
        desc="The area of expertise that the assistant is knowledgeable about"
    )

    answer = dspy.OutputField(
        desc="A Boolean string: 'true' if the request should be answered, 'false' if the request should be blocked"
    )
    reasoning = dspy.OutputField(
        desc="A brief justification for the decision to answer or block the request."
    )
