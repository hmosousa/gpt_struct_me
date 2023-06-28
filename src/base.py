"""Base classes for the project."""

from dataclasses import dataclass


class Document:
    """Document with text and annotations."""

    def __init__(self, id: str,  text: str, annotations: list):

        self.id = id

        # Remove DCT from annotations
        for annotation in annotations:
            if annotation.get("temporalfunction") == "Publication_Time":
                self.dct = Timex(**annotation)
                annotations.remove(annotation)
                break

        # Remove metadata from text and fix the annotation offsets.
        title, author, *lines = text.split("\n")
        metadata_offset = len(title) + len(author) + 2
        for annotation in annotations:
            if "offset" in annotation:
                ann_offset = annotation["offset"].split()

                # TODO: we are ignoring discontinuos offsets
                ann_start = int(ann_offset[0])
                ann_end = int(ann_offset[-1])

                annotation["text"] = text[ann_start:ann_end]

                annotation["offset"] = (
                    ann_start - metadata_offset,
                    ann_end - metadata_offset
                )

        self.text = "\n".join(lines)
        self.annotations = annotations

    def __repr__(self) -> str:
        return f"Document(id={self.id})"

    def __str__(self) -> str:
        return self.text

    def _get_annotation_object(self, obj):
        return [obj(**annotation) for annotation in self.annotations if annotation["type"] == obj._tag]

    @property
    def timexs(self):
        return self._get_annotation_object(Timex)

    @property
    def events(self):
        return self._get_annotation_object(Event)

    @property
    def participants(self):
        return self._get_annotation_object(Participant)

    @property
    def measures(self):
        return self._get_annotation_object(Measure)

    @property
    def spatial_relations(self):
        return self._get_annotation_object(SpatialRelation)

    @property
    def tlinks(self):
        return self._get_annotation_object(TLink)

    @property
    def srlinks(self):
        return self._get_annotation_object(SRLink)

    @property
    def alinks(self):
        return self._get_annotation_object(ALink)

    @property
    def slinks(self):
        return self._get_annotation_object(SLink)

    @property
    def olinks(self):
        return self._get_annotation_object(OLink)

    @property
    def qslinks(self):
        return self._get_annotation_object(QSLink)

    @property
    def movelinks(self):
        return self._get_annotation_object(MoveLink)


class Entity:
    def __init__(
        self,
        id: int,
        type: str,
        offset: str,
        text: str,
        **kwargs,
    ):
        self.id = id
        self.type = type
        self.offset = offset
        self.text = text
        for key, value in kwargs.items():
            if key == "class":
                key = "class_"
            setattr(self, key, value)


class Timex(Entity):
    """ Temporal Expression.

    Time_Type: Date|Time|Duration|Set
    TemporalFunction: Value:Publication_Time|None
    """
    _tag = "Time"


class Event(Entity):
    """Event.

    Class: State|Occurrence|Reporting|Perception|Aspectual|I_Action|I_State
    Event_Type: State|Process|Transition
    Pos: Verb|Noun|Adjective|Preposition|None
    Tense: Present|Past|Future|Imperfect|None
    Aspect: Progressive|Perfective|Imperfective|Perfective_Progressive|Imperfective_Progressive|None
    VForm: Gerundive|Infinitive|Participle|None
    Mood: Subjunctive|Conditional|Future|Imperative|None
    Modality: Dever|Poder|Ter_de|Ser_Capaz_de
    Polarity: Neg|Pos
    Movement: Motion_Literal|Motion_Fictive|Motion_intrChange|Non-Motion
    Factuality: Factual|Non_Factual
    """
    _tag = "Event"

    @property
    def attribs(self):
        pass


class Participant(Entity):
    _tag = "Participant"


class Measure(Entity):
    _tag = "Measure"


class SpatialRelation(Entity):
    """ Spacial Relation.

    Type: Topological|Directional|Topo_Directional|Path_Defining|Goal_Defining
    Topological: Disconnected|Ext_Connected|Partial_Overlap|Equal|Tang_pp|Tang_pp_i|Non-Tang_pp|Non-Tang_pp_i|Disjunction_TTP_NTTP
    PathDefining: Start|End|Mids|GoalDefining
    """
    _tag = "Spatial_Relation"


@dataclass
class Link:
    def __init__(
        self,
        id: int,
        type: str,
        relation: str,
        src: str,
        tgt: str,
        **kwargs,
    ):
        self.id = id
        self.type = type
        self.relation = relation
        self.src = src
        self.tgt = tgt
        for key, value in kwargs.items():
            if key == "class":
                key = "class_"
            setattr(self, key, value)


class TLink(Link):
    """Temporal link.

    Possible values:
        - before
        - after
        - includes
        - isIncluded
        - during
        - simultaneous
        - identity
        - begins
        - ends
        - begunBy
        - endedBy
    """
    _tag = "TLINK"


class SRLink(Link):
    """ Semantic role link.

    Possible values:
        - agent
        - source
        - location
        - path
        - goal
        - time
        - theme
        - instrument
        - partner
        - patient
        - pivot
        - cause
        - beneficiary
        - result
        - reason
        - purpose
        - manner
        - medium
        - means
        - setting
        - initialLocation
        - finalLocation
        - distance
        - amount
        - attribute
    """
    _tag = "SRLINK"


class ALink(Link):
    """

    Possible values:
        -initiates
        - culminates
        - terminates
        - continues
        - reinitiates
    """
    _tag = "ALINK"


class SLink(Link):
    """State link.

    Possible values:
        - intensional
        - evidential
        - negEvidential
        - factive
        - counterFactive
        - conditional
    """
    _tag = "SLINK"


class OLink(Link):
    """Occurrence link.

    Possible values:
        - objIdentity
        - partOf
        - subSet
        - memberOf
        - refDisjunct
    """
    _tag = "OLINK"


class QSLink(Link):
    """Quantitative spatial link.

    Possible values:
        - figure
        - ground
    """
    _tag = "QSLINK"


class MoveLink(Link):
    """Move link.

    Possible values:
        - figure
        - spatialRelation
        - targetSpatialRelation
    """
    _tag = "MOVELINK"
