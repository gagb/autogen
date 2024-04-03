import functools
from dataclasses import dataclass
from typing import Any, List, Dict, Optional, Type, cast, Set, Callable

from textual import on
from textual import work
from textual.screen import ModalScreen
from textual.containers import ScrollableContainer, Grid, Container, Horizontal, Vertical
from textual.widgets import (
    Footer,
    Header,
    Markdown,
    Static,
    Input,
    DirectoryTree,
    Label,
    Switch,
    Collapsible,
    LoadingIndicator,
    Button,
    TabbedContent,
    ListView,
    ListItem,
    TextArea,
)
from textual.reactive import reactive
from textual.message import Message

@dataclass
class AgentMessage:
    role: str
    content: str

    def __str__(self):
        return f"{self.role}:\n{self.content}"

@dataclass
class State:
    name: str
    description: str
    tags: List[str]

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        if isinstance(other, State):
            return self.name == other.name and self.description == other.description and self.tags == other.tags
        return False

    def __hash__(self):
        return hash((self.name, self.description, tuple(self.tags)))

@dataclass
class StateSpace:
    states: Set[State]

    def __str__(self):
        return " ".join([str(state) for state in self.states])

    def filter_states(self, condition: Callable[State, bool]) -> "StateSpace":
        filtered_states = {state for state in self.states if condition(state)}
        return StateSpace(filtered_states)

@dataclass
class MessageProfile:
    message: AgentMessage
    cost: float
    duration: float
    states: Set[State]  # unorddered collection of states

    def __str__(self):
        repr = f"Cost: {self.cost}\tDuration: {self.duration}\t"
        for state in self.states:
            repr += str(state) + " "
        return repr

class ProfilerContainer(ScrollableContainer):
    """
    A container for displaying the profiling information.
    """

    root_id = 0
    chat_history = reactive(list)

    def compose(self) -> ComposeResult:
        yield Markdown(f"## Profiling Information for Root Message ID: {self.root_id}")
        for msg in self.chat_history:
            yield Markdown(f"{msg['role']}:\n{msg['content']}")
