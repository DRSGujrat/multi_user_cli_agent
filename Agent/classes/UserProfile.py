from dataclasses import dataclass, field
from pydantic import BaseModel,Field


class UserProfileSchema(BaseModel):
    goals: list[str] = Field(
        default_factory=list,
        description="""
        Objectives the user wants to achieve, is actively working toward,
        or plans to accomplish in the future.

        Examples:
        - Get an AI internship
        - Become an AI engineer
        - Learn PyTorch
        - Build an AI agent
        - Improve coding skills
        """
    )

    preferences: list[str] = Field(
        default_factory=list,
        description="""
        Consistent ways the user prefers information, workflows,
        tools, communication styles, or learning methods.

        Examples:
        - Prefers simple explanations
        - Prefers concise answers
        - Learns by building projects
        - Prefers Python over Java
        """
    )

    hobbies: list[str] = Field(
        default_factory=list,
        description="""
        Recreational activities primarily done for enjoyment rather
        than career, work, or academic goals.

        Examples:
        - Playing chess
        - Cricket
        - Photography
        - Reading fiction
        """
    )

    likes: list[str] = Field(
        default_factory=list,
        description="""
        Things the user explicitly enjoys, appreciates, recommends,
        or consistently speaks positively about.

        Examples:
        - Likes PyTorch
        - Enjoys Andrej Karpathy videos
        - Likes dark mode
        """
    )

    dislikes: list[str] = Field(
        default_factory=list,
        description="""
        Things the user explicitly dislikes, avoids, complains about,
        or expresses frustration with.

        Examples:
        - Dislikes verbose explanations
        - Dislikes memorization-based learning
        - Avoids unnecessary complexity
        """
    )

    projects: list[str] = Field(
        default_factory=list,
        description="""
        Personal, academic, professional, or side projects the user
        is building, maintaining, planning, or repeatedly discussing.

        Examples:
        - Micrograd implementation
        - LangChain AI agent
        - Personal portfolio website
        - TinyGPT project
        """
    )

    skills: list[str] = Field(
        default_factory=list,
        description="""
        Technologies, tools, subjects, frameworks, or domains that
        the user is learning, practicing, or already demonstrates
        competence in.

        Examples:
        - Python
        - PyTorch
        - Machine Learning
        - LangChain
        - Statistics
        - Data Structures and Algorithms
        """
    )


@dataclass
class UserProfile:
    goals: list[str] = field(default_factory=list)
    preferences: list[str] = field(default_factory=list)
    likes: list[str] = field(default_factory=list)
    dislikes: list[str] = field(default_factory=list)
    hobbies: list[str] = field(default_factory=list)
    projects: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "goals" : self.goals,
            "preferences" : self.preferences,
            "likes" : self.likes,
            "dislikes" : self.dislikes,
            "hobbies" : self.hobbies,
            "projects": self.projects,
            "skills" : self.skills
        }
    @classmethod
    def from_dict(cls,data):
        
        return cls(
            goals = data['goals'],
            preferences = data['preferences'],
            likes = data['likes'],
            dislikes = data['dislikes'],
            hobbies = data['hobbies'],
            projects = data['projects'],
            skills = data['skills']
        )

    def to_prompt(self) -> str:
        goals =",".join(self.goals) or "Not Defined"
        preferences = ",".join(self.preferences) or "Not Defined"
        likes = ",".join(self.likes) or "Not Defined"
        dislikes = ",".join(self.dislikes) or "Not Defined"
        hobbies = ",".join(self.hobbies) or "Not Defined"
        projects = ",".join(self.projects) or "Not Defined"
        skills = ",".join(self.skills) or "Not defined"


        return f""" User prefers {preferences} ,
        user goals are {goals}, 
        interests of user are {likes},
        hobbies of user are {hobbies}, 
        the user does not like {dislikes}, 
        the user is working on {projects}
        and the current skills of user are {skills}"""

