from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool


@CrewBase
class Research:
    """Research crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['reviewer'],
            verbose=True,
        )

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
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )


@CrewBase
class WeekendPlanner:
    """Weekend planning crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def weather_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['weather_specialist'],
            verbose=True,
            tools=[SerperDevTool()],
        )

    @task
    def fetch_weather(self) -> Task:
        return Task(config=self.tasks_config['fetch_weather'])

    @agent
    def calendar_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['calendar_analyst'],
            verbose=True,
        )

    @task
    def analyze_calendar(self) -> Task:
        return Task(config=self.tasks_config['analyze_calendar'])

    @agent
    def local_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['local_scout'],
            verbose=True,
            tools=[SerperDevTool()],
        )

    @task
    def explore_local_options(self) -> Task:
        return Task(config=self.tasks_config['explore_local_options'])

    @agent
    def recommendation_curator(self) -> Agent:
        return Agent(
            config=self.agents_config['recommendation_curator'],
            verbose=True,
        )

    @task
    def craft_recommendations(self) -> Task:
        return Task(config=self.tasks_config['craft_recommendations'])

    @agent
    def transport_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['transport_planner'],
            verbose=True,
            tools=[SerperDevTool()],
        )

    @task
    def plan_transport(self) -> Task:
        return Task(config=self.tasks_config['plan_transport'])

    @agent
    def calendar_scheduler(self) -> Agent:
        return Agent(
            config=self.agents_config['calendar_scheduler'],
            verbose=True,
        )

    @task
    def schedule_calendar_entry(self) -> Task:
        return Task(config=self.tasks_config['schedule_calendar_entry'])

    @agent
    def itinerary_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['itinerary_designer'],
            verbose=True,
        )

    @task
    def build_itinerary(self) -> Task:
        return Task(config=self.tasks_config['build_itinerary'])

    @crew
    def crew(self) -> Crew:
        """Creates the Weekend planning crew"""

        return Crew(
            agents=self.agents,
            tasks=[
                self.fetch_weather(),
                self.analyze_calendar(),
                self.explore_local_options(),
                self.craft_recommendations(),
                self.plan_transport(),
                self.schedule_calendar_entry(),
                self.build_itinerary(),
            ],
            process=Process.sequential,
            verbose=True,
        )
