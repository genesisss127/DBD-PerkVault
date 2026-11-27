
from pydantic import BaseModel, ConfigDict, Field


class PerkBase(BaseModel):
    name: str = Field(min_length=1, description="The name of the survivor perk")
    character: str = Field(default="", description="The survivor associated with the perk")
    description: str = Field(default="", description="A description of what the perk does")
    icon: str | None = Field(default=None, description="Optional URL or path to the perk icon")


class PerkCreate(PerkBase):
    pass


class PerkResponse(PerkBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PerkUpdate(PerkBase):
    pass
