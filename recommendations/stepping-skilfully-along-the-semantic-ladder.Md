#DRAFT


# Introduction

The semantic ladder is a metaphor for the progression from less expressive semantic artifacts (e.g. term lists, vocabularies) to highly expressive artifacts (e.g. formal ontologies). Here, expressiveness is concerned with how well a machine agent (e.g. a reasoner, a natural language processing agent) can discover how any given term relates to another. Some semantic artifacts will indicate loose associations of terms, while others will use precisely defined relationships, themselves arranged in a semantic structure (e.g. expressing different kinds of spatial relations, "adjacent to", "dorsal to", "anterior to", etc). 
  * In a simple vocabulary, like a term list, a machine agent can look up whether a term is present and lexically aligned to a collection. There is little to no semantic content in such lists, beyond defining a universe of expected terminology.
  * In a structured vocabulary, the terms are embedded in some form of relational framework, expressed through a format like RDF (e.g. "term 1" is_child_of "term 2"). The relations may have arbitrary meaning, and the structures may or may not have formal or consistent semantics. 
  * In a (typical) dictionary, terms are associated with human-readable definitions. This may or may not be of interest to a machine agent, depending on its ability to process natural language.
  * In a thesaurus, terms are related to other terms through relations that express synonymy, antonymy, loose semantic relatedness, exact matches, and similar relations. The Simple Knowledge Organization System (SKOS) is a prominent format for rendering a thesaurus. 
  * In an ontology, formal relationships (axioms) are used to precisely interrelate terms arranged in a superclass-subclass hierarchy, where each subclass inherits all the properties of its superclass. Ontologies are typically "reasoned" (processed through software called a "reasoner") to assess whether the asserted relations are logically coherent and satisfiable. Ontologies are often expressed in the Web Ontology Language (OWL) and its variations.

Choosing what level of the semantic ladder is useful and/or appropriate for your application is a critical decision, and sometimes a mix of artifacts are needed to accomplish an initiative's aims. The recommendations below aim to offer implementation guidance across a range of scenarios. Throughout, it is important to decouple the format/language of a semantic resource, from its actual semantic expressivity: An artifact in an OWL serialisation is not necessarily an ontology, and an artifact in RDF could be anything along the ladder. 


# Recommendations

## Balancing machine- and human-friendliness for organisational terminologies: A dance of SKOS and OWL

**Recommendation: Use SKOS-compliant approaches to publish human-oriented semantic artifacts, and build OWL-compliant, machine-oriented resources upon these.**

At times, an organisation may wish to create a machine-actionable form of the terminology that it relies on. The experts who created these definitions would have reached a consensus and a textual definition, often with several clauses and clarifications, will be present. Two subsequent questions arise: 1) how can we digitise this such that it brings the most value to human and machine agents? and 2) How can we share this widely to promote reuse and semantic harmonisation?

The first question is addressed below, the second in the subsection entitled "Effectively sharing semantic artifacts". 

The first instinct may be to aim as high as possible on the semantic ladder. However, few organisations are prepared to create formal logical artifacts. In the majority of cases, the way an organisation defines their terms will not be "formal" in the sense of the logical formality that ontologies (typically expressed in OWL) require. That is, the relations (object properties) between terms will not have domain and range constraints created to support reasoning and other checks for consistency. In fact, it often is not advisable for an organisation to create such formal artifacts, as much essential nuance may be lost during the process.

In most cases, a better solution would be to digitise and share the terminology using the conventions of SKOS. SKOS embeds a dictionary within a structure that expresses thesaurus-level relationships between terms (e.g. whether a term, or "concept" in SKOS, has a broader, narrower, or simply related meaning relative to another), and has few constraints on definitional forms. Each term has an identifier, and SKOS artifacts can be shared using linked open data norms. The FAO's [AGROVOC](https://www.fao.org/agrovoc/) is an example of a complex, multi-lingual, and multi-nationally managed SKOS-based resource, managed through the VocBench software. SKOS artifacts are, typically, more intuitive to human users and can offer concept collections to further ease human browsing and discovery.

When such a SKOS-based resource is in place, the "official", human-oriented definitional space is set and has a persistent presence on the web (assuming the artifact has been shared through solutions aligned with the LOD and FAIR Principles). At this stage, variants of the official terms that are more logically formalised (and thus more machine-friendly) can be created in one or more ontologies, using the expressive capabilities of OWL. For example, the term [landslide](https://www.eionet.europa.eu/gemet/en/concept/4668) in the General Multilingual Environmental Thesaurus (GEMET) has been formalised in OWL using the Open Biological and Biomedical Ontologies (OBO) Library guidelines in the Environment Ontology (ENVO) class for ["landslide"](http://purl.obolibrary.org/obo/ENVO_01000692) 


## Effectively sharing semantic artifacts



# ... Further sections / examples 
