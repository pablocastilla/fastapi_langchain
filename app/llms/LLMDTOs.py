# mypy: ignore-errors
# pydantic doesn´t work with mypy, so these DTOs are here without mypy type checking

from pydantic import BaseModel, Field


class EmergencyRoomTriage(BaseModel):
    name: str = Field(description="patient name")
    id_number: str = Field(description="patient identification number")
    medical_specialty: str = Field(description="specialty to which the patient should be referred.In English.")
    urgency: int = Field(description="urgency level of the patient, 1 is the most urgent, 5 is the least urgent.In English.")
    response_to_the_user: str = Field(
        description="go to the waiting room if urgency level is above 1, go to emergency room if urgency level is 1.Use the language of the user."
    )
