from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


async def generate_plan(input_dict: dict):
    first_model = await OpenAI(model_name="text-davinci-003", temperature=0.7)
    template_one = """You are professional tour guide with 20 years of experience and excellent knowledge of every corner of Kazakhstan. Your main task is to generate a tour itinerary for international tourists. Given the cities that user want to visit, number of days for a tour and a aspect of the trip to focus on, it is your job to make a unique plan for travel. 
    Generate a tour in this format: 
    Day 1: City 1
    9 am: breakfast in restaurant ...
    1 pm: lunch in restaurant ...
    5 pm: activity in ...
    7 pm: dinner in restaurant ...

    Day 2: City 2
    ...

    Cities to visit: {cities}
    Number of days: {days}
    Focus of a tour: {aspect}

    Plan: This is a unique plan for travel:"""
    first_prompt_template = await PromptTemplate(
        input_variables=["cities", "days", "aspect"], template=template_one
    )
    first_chain = await LLMChain(llm=first_model, prompt=first_prompt_template)
    return await first_chain.run(
        cities=input_dict["cities"],
        days=input_dict["days"],
        aspect=input_dict["aspect"],
    )


# second_model = OpenAI(temperature=0.7)
# template_two = """You are still professional tour guide with 20 years of experience and excellent knowledge of every corner of Kazakhstan. Your main task is to generate a tour itinerary for international tourists. Given the cities that user want to visit, number of days for a tour and a aspect of the trip to focus on, it is your job to continue the plan of the tour
# Tour plan:
# {tour_plan}

# Continue the plan of the tour:"""

# second_prompt_template = PromptTemplate(
#     input_variables=["tour_plan"], template=template_two
# )
# second_chain = LLMChain(llm=second_model, prompt=second_prompt_template)

# overall_chain = SimpleSequentialChain(chains=[first_chain, second_chain], verbose=True)


# tour = overall_chain.run()
