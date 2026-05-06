from typing import Literal, Optional
from langchain_core.messages import BaseMessage
from langfuse.langchain import CallbackHandler
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

# Define Schema
class AgentState(TypedDict):
    onboarding_done: bool
    user_age: int
    age_rating_filter: list[str]
    preferred_genres: list[str]
    onboarding_answer: str
    answer: str
    tool_calls: list[dict]
    messages: list[BaseMessage]
    session_id: Optional[str]

    route: Literal['retrieval', 'airing']
    next_agent: str

    retrieval_mode: Literal['exact', 'similar', 'discover']
    retrieval_target: str
    target_type: str
    retrieval_result: list[dict]
    retrieval_attempt: int
    retrieval_query: str

    sentiment_tone: str
    sentiment_keywords: list[str]
    sentiment_modifier: str
    diversity_modifier: str
    divergence_level: int

    seen_titles: list[str]

    recommendations: list[dict]
    recommendation_attempts: int

    airing_results: list[dict]
    airing_attempt: int

    validator_approved: bool
    validator_target: str
    validator_issues: list[str]    

# Router to retrieve/airing
def router_retrieve_airing(state: AgentState) -> Literal['retrieval_agent', 'airing_agent']:
    return 'airing_agent' if state.get('route') == 'airing' else 'retrieval_agent'

def validation(state: AgentState) -> Literal['retrieval_agent', 'sentiment_agent', 'airing_agent', 'wait_node']:
    """Validation always goes to wait_node - never directly to END"""
    route = state.get('route', 'retrieval')
    target = state.get('validator_target', 'done')
    
    # If validation approved, go to wait_node
    if state.get('validator_approved', False):
        return 'wait_node'

    # Retry for airing flow
    if route == 'airing':
        if state.get('airing_attempt', 0) < 2:
            return 'airing_agent'
        return 'wait_node'
    
    # Retry for retrieval flow
    if target == 'retrieval' and state.get('retrieval_attempt', 0) < 2:
        return 'retrieval_agent'
 
    if target == 'sentiment' and state.get('recommendation_attempts', 0) < 2:
        return 'sentiment_agent'
    
    return 'wait_node'

def after_wait_node(state: AgentState) -> Literal['router_agent', 'end']:
    """Wait node checks user input - only END ends the graph"""
    messages = state.get('messages', [])
    if messages and hasattr(messages[-1], 'content'):
        last_content = messages[-1].content.lower().strip()
        if last_content == 'end':
            return 'end'
    
    # Reset state for new query
    state['validator_approved'] = False
    state['recommendations'] = []
    state['airing_results'] = []
    state['retrieval_result'] = []
    
    return 'router_agent'

def graphy(onboarding_agent, router_agent, retrieval_agent, sentiment_agent, recommendation_agent, airing_agent, supervisor_agent) -> StateGraph:
    g = StateGraph(AgentState)
    
    g.add_node('onboarding_agent', onboarding_agent)
    g.add_node('router_agent', router_agent)
    g.add_node('retrieval_agent', retrieval_agent)
    g.add_node('sentiment_agent', sentiment_agent)
    g.add_node('recommendation_agent', recommendation_agent)
    g.add_node('airing_agent', airing_agent)
    g.add_node('supervisor_agent', supervisor_agent)
    g.add_node('wait_node', lambda state, config=None: state)

    g.add_edge(START, 'onboarding_agent')
    g.add_edge('onboarding_agent', 'router_agent')
    
    g.add_conditional_edges('router_agent', router_retrieve_airing, 
        {'retrieval_agent': 'retrieval_agent', 'airing_agent': 'airing_agent'})
    
    g.add_edge('retrieval_agent', 'sentiment_agent')
    g.add_edge('sentiment_agent', 'recommendation_agent')
    g.add_edge('recommendation_agent', 'supervisor_agent')
    
    g.add_edge('airing_agent', 'supervisor_agent')

    g.add_conditional_edges('supervisor_agent', validation, {
        'retrieval_agent': 'retrieval_agent',
        'sentiment_agent': 'sentiment_agent',
        'airing_agent': 'airing_agent',
        'wait_node': 'wait_node'})
    
    g.add_conditional_edges('wait_node', after_wait_node, {
        'router_agent': 'router_agent',
        'end': END})
    
    return g.compile()

def run_graph(state: AgentState, movie_graph) -> dict:
    cb = CallbackHandler()
    return movie_graph.invoke(state, config={'callbacks': [cb]},)

def initial_state(session_id:str = 'new') -> AgentState:
    return AgentState(onboarding_done= False,
        user_age = -1,
        age_rating_filter = [],
        preferred_genres = [],
        onboarding_answer = '',
        answer = '',
        tool_calls = [],
        messages = [],
        session_id = session_id,
        route = 'retrieval',
        next_agent = 'onboarding_agent',
        retrieval_mode = 'discover',
        retrieval_target = '',
        target_type = 'none',
        retrieval_result = [],
        retrieval_attempt = 0,
        retrieval_query = '',
        sentiment_tone = '',
        sentiment_keywords = [],
        sentiment_modifier = '',
        diversity_modifier = '',
        divergence_level = 0,
        seen_titles = [],
        recommendations = [],
        recommendation_attempts = 0,
        airing_results = [],
        airing_attempt = 0,
        validator_approved = False,
        validator_target = 'done',
        validator_issues = [],)