"""All the constants that are defined a priori."""

ENTITIES = {
    "event triggers": {

        "definition": "An event refers to any occurrence, incident, action or state that takes place or holds within a specified period of time. This includes both concrete actions, such as physical movements and behaviors, as well as more abstract events, such as changes in emotional states or the passage of time or stative situations that hold during a time interval. Events have temporal relevance and can be directly related to temporal expressions. Events can be related to changes in the text and are often used to advance the plot and develop characters, but also to describe characters, objects, circumstances, places or states.",

        "classes": "State, Occurrence, Reporting, Perception, Aspectual, Intensional Action, and Intensional State"
    },

    "participants": {

        "definition": "Participants refer to individuals, groups, organizations, or other entities that are actively involved in or impacted by an event or state. They are typically identified based on their relevance and significance to the situation, and may be explicitly mentioned or inferred from the context. Participants can take on a variety of roles, such as actors, agents, patients, victims, or observers, and their actions and interactions can shape the course of events.",

        "classes": "Person, Organization, Object, Location, Nature, Facility, and Other"
    },

    "time expressions": {

        "definition": "Temporal expressions are linguistic elements that allow us to communicate information about time. In addition to representing specific points in time, they can also be used to classify time periods according to units such as seconds, minutes, hours, days, weeks, months, and years.",

        "classes": "Date, Time, Duration, and Set"
    }
}
