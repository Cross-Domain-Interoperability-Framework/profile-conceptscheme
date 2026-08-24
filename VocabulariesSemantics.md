# Vocabularies and Semantics

## Introduction:
Communication is based on mutual understanding of the binding between words (labels) and concepts. 
In human language it is not unusual to have concepts that might bind to multiple words (synonymy), and words that might bind to different concepts (polysemy).  
Logic and reasoning operate on concepts. Humans can navigate the ambiguity inherent in natural language; but for computers this is difficult. Automated computation systems require unambiguous one to one binding between concepts and words. Of course, in a computer a word is just a bit stream.  The purpose of the semantic artifacts under consideration is to establish binding between the word/bit streams used by the computer and concepts that humans use to understand the world and make decisions.

In this framework, here’s a view of the semantic ladder:

- A **word list** provides a set of strings. This set will typically be used as a pick list for human users to assign values for categorical variables in data, and by computers to determine if a valid value has been provided for some variable.  The strings only have meaning to a human, and given the prevalence of polysemy, might mean different things to different people. 
- A **dictionary** in common practice is a mapping between words (strings) and possible meanings. Meanings are represented by text definitions. This is useful for people in a scenario “I’m reading this document, and see this word, what does it mean”. The dictionary might have several definitions, but a human can normally figure out which is applicable based on context. With modern natural language processing, a computer might also be able to guess with some probability which definition applies. Note that the widely used ‘Glossary of Geology’ is a dictionary, not a glossary as defined below. 
- A **structured vocabulary** (thesaurus) is a word list with some set of relationships (represented by words) between the words (strings). Some simple inferencing rules might be associated with these relationships that are machine actionable, like “if the user asks for string A, they might be interested in strings B and C” (narrower terms).  Lacking definitions, humans must still interpret the words according to their understanding/context. The asserted relationships to other words typically provide evidence to interpret meaning.
- A **glossary** is a set of words with unique definitions associated with each word. This establishes a one to one relationship between words (strings) and concepts. A glossary can thus be thought of as a set of concepts.


At this point, logic enters the game. Some tidying up of language is necessary. From here on  ‘word’ refers to a string of characters (or its equivalent in natural language sound), and ‘term’ refers to a binding between a word and a concept, implying that there is a definition. 
Glossaries can take various forms. A glossary might include terms for a set of unrelated concepts, like a glossary accompanying a technical paper that defines the terms used in that paper.

- **Classification system**.  A glossary might be a set of terms restricted to some scope, e.g. ‘kinds of business’, ‘kinds of rock’, ‘income level’, ‘nationality’, ‘mammal taxonomy’. This will be called a classification system.  The terms in a classification system can be thought of as locations in a conceptual space. The conceptual space is defined by properties inherent in some kind of entity (rock, person, mammal, business entity), the domain of the classification system. The terms in the classification system might ‘cover’ the conceptual space, that is for each point there is at least one term. The terms might be non-overlapping, such that for each point in the concept space there is exactly one term.  The classification system might be hierarchical with concepts at a higher level subsuming concepts at lower levels.  The questions of covering and non-overlapping apply at each level of the hierarchy.

Classification systems can be ‘flat’, that is without hierarchy. A ‘flat’ system might not have any relationships between terms. 

- **Ontology**.  An ontology is a representation of a conceptualization of some domain. It consists of a set of entities and relationships. To be useful to a human, the concepts for the entities and relationships must be defined in natural language. The ontology representation consists of a set of terms for entities and relationships, and a set of assignments of relationships between the entities. In an automated computation system the relationships between entities translate into various operations between the entities that might produce truth values, or other entities.  These are only useful to humans if the results are 'terms' (have human-intelligible definitions). 

## Implementation/representation

SKOS is an RDF vocabulary for representing structured vocabularies, glossaries, or classification systems (as discussed above). The relationships between objects in a SKOS vocabulary are basically broader, narrower, and related. The objects in a SKOS vocabulary are called ‘concepts’; the minimal [SKOS concept](https://www.w3.org/TR/2009/NOTE-skos-primer-20090818/#secconcept) is simply an identifier, so a minimal SKOS vocabulary is essentially equivalent to a word list, given that words exist because they represent concepts. The SKOS relationships allow representation of a structured vocabulary. The addition of definitions bound to SKOS concepts allows representation of a glossary or classification system. The logical constraints on covering and non-overlapping concepts must be determined by a human parsing the concept definitions. SKOS makes a clear distinction between the identifier for a SKOS concept, and the words used by people to identify the concept (prefLabel, altLabel).

OWL is an RDF vocabulary that, like SKOS, allows construction of a set of entity and relationship concepts with identifiers. OWL defines a much richer set of relationships between entities that allows a more extensive set of automated operations (inferencing). For instance ‘given that entity X exists, entities Y and Z must exist, or ‘if entity M has a relationship N  to some other entity, then the kind of entity M must be Q’. This inferencing capability provides tools to create more interesting applications validating data, assisting user workflows, suggesting courses of action to name a few.

## Recommendations
Be clear on the distinction between concepts (ideas) and words as labels for concepts.

Think about these questions-- What is the domain of interest (the concept space)?   What are the properties of entities in that space that differentiate values (terms). What am I going to use this vocabulary for?

Create text definitions for the concepts you need for your application.  Review these for logical consistency—are the concepts unique/non-overlapping? Do they need to be? Are all the possible values of interest defined (covering). Are the definitions unambiguous?  Generally this can be done in a text document or spreadsheet to start.  The critical goal is good definitions that will be understood by your application developers and users, and not lead to bad data.

Decide how you’re going to represent your vocabulary. This could range from a text file defining the words in a word list, a SKOS structured vocabulary, glossary, or classification system, or an OWL representation with semantically precise relationships between entities and properties of those entities.
- “everybody knows what my words mean, I don’t need to insult them by providing definitions”.  STOP here, you’re in the wrong community.
- Text file (doc, web page) or spreadsheet with definitions. For human users, who will need to know where this set of definitions reside. Minimal effort, but at least you’ve reviewed your terminology and defined what your words mean so your data should be consistent.
- I want people to be able to find definitions for the terms I use in my data. Follow the guidance in ‘Ten simple rules for making a vocabulary FAIR’  ([Cox et al, 2021](https://doi.org/10.1371/journal.pcbi.1009041)).  Most important here are : assign identifiers for each term, make identifiers resolvable on the web to get human and machine-readable representations, include metadata to establish the source of the vocabulary and the definitions to establish trust.
- Machine readable representation—this should be determined by how the vocabulary will be used , both for internal purposes, and to support any business requirements.

REMEMBER, all of this is predicated on starting with a clear scope for your vocabulary and clearly defining the concepts in that scope. From these text definitions, representations of any complexity can be constructed if they are clear and logically coherent.

## sidebar

As an example of the problems, lets look at the definitions of 'landslide'.   [landslide](https://www.eionet.europa.eu/gemet/en/concept/4668) in the General Multilingual Environmental Thesaurus (GEMET)  > "Mass-movement landforms and processes involving the downslope transport, under gravitationary influence of soil and rock material en masse."

and in the Open Biological and Biomedical Ontologies (OBO) Library guidelines in the Environment Ontology (ENVO) class for 

["landslide process"](http://purl.obolibrary.org/obo/ENVO_01000692) > A landslide is a process whereby a large mass of earth and rocks moves down a hill or a mountainside.
 or 
 
["landslide"](http://purl.obolibrary.org/obo/ENVO_00000520) > A mound of earth material, at the base of a slope and the associated scoured area.

The GEMET defintion includes landform and process; in ENVO there are separate concepts for the process and the landform. The ENVO process definition cross references the GEMET definition.

Both of these definitions do not entertain 'landslide' as an event, which is another common usage. Semantic interoperability would require distinguishing 'landslide' as a geomorphic feature (landform), process (one kind of mass-wasting), or event.

Consider-- 'landslide hazard' is the probability of a landslide event in some place; assessment of this hazard would be based on the occurrence of 'landslide landforms' in the area, and modeling based on understanding of the physiography and underlying geology along with a 'landslide process' model. 
