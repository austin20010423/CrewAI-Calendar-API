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
    def task_deconstructor(self) -> Agent:
        return Agent(
            config=self.agents_config['task_deconstructor'], 
            max_iter=1,
            verbose=False
        )

    @agent
    def intelligence_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['intelligence_scout'], 
            mcps = [
                "crewai-amp:research-tools"
            ],
            cache=True,
            max_iter=1,
            verbose=False
        )
    
    @agent
    def strategic_prioritizer(self) -> Agent:
        return Agent(
            config=self.agents_config['strategic_prioritizer'], 
            max_iter=1,
            inject_date=True,
            verbose=False
        )


    @task
    def deconstruction_task(self) -> Task:
        return Task(
            config=self.tasks_config['deconstruction_task'], 
            async_execution=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], 
            async_execution=True
        )

    @task
    def prioritization_task(self) -> Task:
        return Task(
            config=self.tasks_config['prioritization_task'], 
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
