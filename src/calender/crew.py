import mcp
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel
import os



@CrewBase
class Calender():
    """Calender crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def calendar_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['calendar_manager'], 
            mcps = [
                "crewai-amp:research-tools"
            ],
            cache=True,
            verbose=True
        )

    @task
    def execution_task(self) -> Task:
        return Task(
            config=self.tasks_config['execution_task'], 
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Calender crew"""
       
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=False
        )
