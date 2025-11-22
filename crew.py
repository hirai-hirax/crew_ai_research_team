from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from tools.google_maps_tool import GoogleMapsDirectionsTool, GoogleMapsDistanceMatrixTool
from tools.openweather_tool import OpenMeteoTool



@CrewBase
class WeekendPlanner:
    """Weekend planning crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def planning_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['planning_manager'],
            verbose=True,
        )

    @task
    def coordinate_planning(self) -> Task:
        return Task(config=self.tasks_config['coordinate_planning'])

    @agent
    def weather_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['weather_specialist'],
            verbose=True,
            tools=[OpenMeteoTool(), SerperDevTool()],
            max_retry_limit=3,
        )

    @task
    def fetch_weather(self) -> Task:
        return Task(config=self.tasks_config['fetch_weather'])

    @agent
    def local_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['local_scout'],
            verbose=True,
            tools=[SerperDevTool()],
            max_retry_limit=3,
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
            tools=[
                SerperDevTool(),
                GoogleMapsDirectionsTool(),
                GoogleMapsDistanceMatrixTool(),
            ],
            max_retry_limit=3,
        )


    @task
    def plan_transport(self) -> Task:
        return Task(config=self.tasks_config['plan_transport'])

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
            agents=[
                self.weather_specialist(),
                self.local_scout(),
                self.recommendation_curator(),
                self.transport_planner(),
                self.itinerary_designer(),
            ],
            tasks=[
                self.coordinate_planning(),
                self.fetch_weather(),
                self.explore_local_options(),
                self.craft_recommendations(),
                self.plan_transport(),
                self.build_itinerary(),
            ],
            process=Process.hierarchical,
            manager_agent=self.planning_manager(),
            verbose=True,
        )
