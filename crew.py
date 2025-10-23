from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool


@CrewBase
class Research():
    """Research crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'


    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config['researcher'], verbose=True, tools=[SerperDevTool()])

    @agent
    def reviewer(self) -> Agent:
        return Agent(config=self.agents_config['reviewer'], verbose=True)


    @task
    def propose(self) -> Task:
        return Task(config=self.tasks_config['propose'])

    @task
    def review(self) -> Task:
        return Task(config=self.tasks_config['review'])

    @task
    def finalize(self) -> Task:
        return Task(config=self.tasks_config['finalize'])


    @crew
    def crew(self) -> Crew:
        """Creates the Research crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
C