from pydantic import BaseModel, Field
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

class UserProfileSchema(BaseModel):
    goals: List[str] = Field(
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

    preferences: List[str] = Field(
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

    hobbies: List[str] = Field(
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

    likes: List[str] = Field(
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

    dislikes: List[str] = Field(
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

    projects: List[str] = Field(
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

    skills: List[str] = Field(
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





model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0
)

        
    
def extract_profile(conversation_memory):
    structured_model = model.with_structured_output(UserProfileSchema)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{conversation_history}")  
    ])

    profiling_chain = prompt_template | structured_model

    extracted_profile = profiling_chain.invoke({"conversation_history": conversation_memory})
    

    return extracted_profile
    
def merge(user_id,extracted_profile):
    profile = manager.get_user_profile(user_id)
    profile.goals = list(set(extracted_profile.goals) | set(profile.goals))
    profile.hobbies = list(set(extracted_profile.hobbies) | set(profile.hobbies))
    profile.preferences = list(set(extracted_profile.preferences) | set(profile.preferences))
    profile.dislikes = list(set(extracted_profile.dislikes) | set(profile.dislikes))
    profile.likes = list(set(extracted_profile.likes) | set(profile.likes))
    profile.projects = list(set(extracted_profile.projects) | set(profile.projects))
    profile.skills = list(set(extracted_profile.skills) | set(profile.skills))


system_prompt = """
# ROLE

You are an expert User Profiling and Behavioral Analysis system.

Your task is to analyze historical conversations and extract stable,
useful user information into the provided structured schema.

Your output will be used as long-term memory for a conversational AI.

# CORE PRINCIPLE

Extract information only when supported by evidence.

Information should be:
1. Explicitly stated by the user, OR
2. Strongly implied through repeated discussion or behavior.

Never invent facts.

# FIELD DEFINITIONS

GOALS
Future outcomes the user wants to achieve.

Include:
- Career objectives
- Learning objectives
- Personal improvement goals
- Planned achievements

Examples:
- Become an AI engineer
- Get an internship
- Learn PyTorch

PREFERENCES
How the user prefers to learn, communicate, work, or receive information.

Include:
- Communication style preferences
- Learning preferences
- Tool preferences
- Workflow preferences

Examples:
- Prefers concise answers
- Prefers simple English explanations
- Learns through implementation

HOBBIES
Activities primarily done for enjoyment or recreation.

Do NOT include:
- Professional learning
- Academic study
- Career development

Examples:
- Chess
- Cricket
- Photography

LIKES
Things the user explicitly enjoys, appreciates, recommends,
or consistently speaks positively about.

Examples:
- Likes PyTorch
- Enjoys Karpathy's tutorials

DISLIKES
Things the user explicitly dislikes, avoids, criticizes,
or complains about.

Examples:
- Dislikes overly theoretical explanations
- Avoids unnecessary complexity

PROJECTS
Projects the user is currently building, maintaining,
planning, or repeatedly discussing.

Include:
- Side projects
- Learning projects
- Open-source projects
- Work projects

Examples:
- Micrograd implementation
- LangChain AI assistant
- Portfolio website

SKILLS
Technologies, frameworks, tools, academic subjects,
or domains that the user is learning, practicing,
or demonstrates familiarity with.

Examples:
- Python
- PyTorch
- Machine Learning
- LangChain
- Statistics

# EXTRACTION RULES

- Use concise standalone phrases.
- Remove duplicates.
- Keep the most specific version.
- Do not include explanations.
- Do not include uncertain assumptions.
- Do not infer personality traits.
- Do not infer demographics.
- Do not infer political, religious, or medical information.
- If evidence is insufficient, return an empty list.

# NORMALIZATION

Good:
- "Learn PyTorch"
- "Prefers concise answers"
- "Micrograd implementation"

Bad:
- "The user seems interested in learning PyTorch because they asked many questions."
- "Probably enjoys coding."
- "May want a software engineering job."

# OUTPUT

Return only the structured schema.
"""