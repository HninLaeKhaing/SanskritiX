"""Curated introductory learning notes for the classifier's eight labels."""

TRADITIONS = {
    "gond": {
        "title": "Gond painting",
        "region": "Central India, associated with Gond communities.",
        "history": (
            "Gond artists have carried visual practices across generations. "
            "Contemporary Gond painting is also made for paper and canvas, "
            "extending practices associated with homes and community life."
        ),
        "materials": (
            "Materials vary by artist and period. Contemporary works may use "
            "paper or canvas with paint, ink, or other studio materials."
        ),
        "visual_language": (
            "Look for rhythmic line patterns, repeated marks, and lively "
            "figures drawn from animals, plants, stories, and everyday life."
        ),
        "cultural_context": (
            "Gond is a broad community identity, not a single uniform style. "
            "Artists and families have individual approaches; do not treat "
            "one image as representative of every Gond community."
        ),
        "reflection": "What repeated marks or lines guide your eye around the image?",
        "sources": [
            ("Sahapedia: Gond art", "https://www.sahapedia.org/gond-art"),
            (
                "Google Arts & Culture: Gond art collection search",
                "https://artsandculture.google.com/search?q=Gond%20painting",
            ),
        ],
        "question": {
            "prompt": "Which visual clue is often explored when looking closely at Gond painting?",
            "options": [
                "Rhythmic repeated lines and marks",
                "Only single-color geometric floor borders",
                "A painted cloth hung behind a temple image",
            ],
            "answer": "Rhythmic repeated lines and marks",
            "explanation": (
                "Repeated line patterns are a useful visual feature to notice, "
                "though artists' styles vary."
            ),
        },
    },
    "kalighat": {
        "title": "Kalighat painting",
        "region": "Kalighat, Kolkata, in West Bengal.",
        "history": (
            "The style developed around the Kalighat temple area in "
            "nineteenth-century Kolkata. Patua painters made portable works "
            "for visitors and a growing urban audience. Subject matter "
            "included religious figures as well as scenes of contemporary life."
        ),
        "materials": (
            "Many surviving works are watercolour or opaque colour on paper. "
            "The medium and production methods changed over time."
        ),
        "visual_language": (
            "Look for bold, sweeping outlines, simplified forms, strong areas "
            "of colour, and relatively open backgrounds."
        ),
        "cultural_context": (
            "Kalighat paintings are both devotional images and records of "
            "urban visual culture; some works used humour or social commentary."
        ),
        "reflection": "How does the open background affect the way you read the central figure?",
        "sources": [
            (
                "Victoria and Albert Museum: Kalighat collection search",
                "https://collections.vam.ac.uk/search/?q=Kalighat",
            ),
            (
                "Kalighat painting overview",
                "https://en.wikipedia.org/wiki/Kalighat_painting",
            ),
        ],
        "question": {
            "prompt": "Where did Kalighat painting develop?",
            "options": [
                "Around Kalighat in Kolkata",
                "In the Nathdwara temple tradition",
                "In the Himalayan hill courts",
            ],
            "answer": "Around Kalighat in Kolkata",
            "explanation": (
                "The tradition is named for the Kalighat area of Kolkata, "
                "where painters made works for local audiences and visitors."
            ),
        },
    },
    "kangra": {
        "title": "Kangra painting",
        "region": "Kangra and neighbouring hill states of the western Himalayas.",
        "history": (
            "Kangra painting is part of the broader Pahari miniature tradition. "
            "It flourished in the eighteenth and nineteenth centuries under "
            "hill-state patronage; the court of Sansar Chand was an important "
            "centre."
        ),
        "materials": (
            "Traditional miniatures were painted on paper with fine brushes "
            "and carefully layered colour."
        ),
        "visual_language": (
            "Look for delicate lines, lyrical figures, carefully observed "
            "landscapes, and narrative scenes, often drawn from devotional "
            "poetry and stories of Krishna."
        ),
        "cultural_context": (
            "Kangra is one regional school within the diverse Pahari painting "
            "world; neighbouring courts and workshops developed related but "
            "distinct styles."
        ),
        "reflection": "What details in the landscape help set the mood of the scene?",
        "sources": [
            (
                "The Metropolitan Museum of Art: Pahari painting",
                "https://www.metmuseum.org/toah/hd/pahi/hd_pahi.htm",
            ),
            (
                "Kangra painting overview",
                "https://en.wikipedia.org/wiki/Kangra_painting",
            ),
        ],
        "question": {
            "prompt": "Kangra painting belongs to which broader tradition?",
            "options": [
                "Pahari miniature painting",
                "Kalighat pata painting",
                "Kerala temple mural painting",
            ],
            "answer": "Pahari miniature painting",
            "explanation": (
                "Kangra is a regional school within the larger Pahari "
                "miniature-painting tradition."
            ),
        },
    },
    "kerala": {
        "title": "Kerala mural painting",
        "region": "Kerala, especially mural sites in temples and palaces.",
        "history": (
            "Kerala has a long mural tradition visible in religious and "
            "historic buildings. Surviving murals belong to different periods; "
            "each site has its own history and should be studied in context."
        ),
        "materials": (
            "Traditional wall painting used prepared plaster and mineral or "
            "plant-based colours. Materials and conservation conditions differ "
            "between sites."
        ),
        "visual_language": (
            "Look for narrative figures, emphatic outlines, patterned "
            "ornament, and compositions arranged across architectural walls."
        ),
        "cultural_context": (
            "Many murals draw on religious narratives and iconographic "
            "traditions. They are part of a living architectural and ritual "
            "setting, not simply detached pictures."
        ),
        "reflection": "How might the wall, room, or building change the meaning of a mural?",
        "sources": [
            (
                "Kerala Tourism: Kerala mural painting",
                "https://www.keralatourism.org/artforms/kerala-mural-painting/15/",
            ),
            (
                "Kerala mural painting overview",
                "https://en.wikipedia.org/wiki/Kerala_mural_painting",
            ),
        ],
        "question": {
            "prompt": "Where are many historic Kerala murals found?",
            "options": [
                "On walls in temples and palaces",
                "Only on small paper sheets sold at a city shrine",
                "Only on cloth hangings behind a deity",
            ],
            "answer": "On walls in temples and palaces",
            "explanation": (
                "Historic Kerala murals are closely connected with the "
                "architecture of temples, palaces, and other sites."
            ),
        },
    },
    "madhubani": {
        "title": "Madhubani (Mithila) painting",
        "region": "The Mithila region, especially Bihar in India and adjoining areas.",
        "history": (
            "Mithila painting has been practised in domestic and ceremonial "
            "settings, with knowledge passed through families and communities. "
            "Artists later developed work on paper and other portable surfaces "
            "alongside wall and floor painting."
        ),
        "materials": (
            "Traditional surfaces included prepared walls and floors. Artists "
            "have used locally available pigments and tools; contemporary "
            "materials vary."
        ),
        "visual_language": (
            "Look for dense patterning, strong contours, filled backgrounds, "
            "and subjects that may include nature, religious narratives, and "
            "community life."
        ),
        "cultural_context": (
            "Mithila painting includes multiple communities, artists, and "
            "styles. It should not be reduced to one motif or treated as a "
            "single unchanging practice."
        ),
        "reflection": "Which parts of the composition are left unpainted, and which are filled with pattern?",
        "sources": [
            (
                "Madhubani art overview",
                "https://en.wikipedia.org/wiki/Madhubani_art",
            ),
            (
                "Sahapedia: Mithila painting",
                "https://www.sahapedia.org/mithila-painting",
            ),
        ],
        "question": {
            "prompt": "Madhubani painting is also commonly known by what regional name?",
            "options": ["Mithila painting", "Pahari painting", "Pichhwai painting"],
            "answer": "Mithila painting",
            "explanation": (
                "Madhubani painting is also known as Mithila painting, after "
                "the region where the tradition developed."
            ),
        },
    },
    "mandana": {
        "title": "Mandana art",
        "region": "Rajasthan and parts of neighbouring central India.",
        "history": (
            "Mandana is a community-based decorative practice associated with "
            "homes and auspicious occasions. Designs and meanings vary by "
            "place, maker, and event."
        ),
        "materials": (
            "Traditional examples use locally prepared surfaces and contrasting "
            "materials such as white pigment on an earth-coloured ground; exact "
            "materials differ across communities."
        ),
        "visual_language": (
            "Look for repeated geometric borders and motifs drawn on floors or "
            "walls. The design is often understood together with the space and "
            "occasion for which it was made."
        ),
        "cultural_context": (
            "Mandana is a living practice, not merely a fixed catalogue of "
            "motifs. Ask who made a design, where it appears, and what its "
            "community says it means."
        ),
        "reflection": "How does the design relate to the doorway, floor, or other place where it appears?",
        "sources": [
            (
                "Google Arts & Culture: Mandana art collection search",
                "https://artsandculture.google.com/search?q=Mandana%20art%20India",
            ),
            (
                "Sahapedia: Indian visual arts",
                "https://www.sahapedia.org/visual-arts",
            ),
        ],
        "question": {
            "prompt": "What is a useful way to interpret a Mandana design?",
            "options": [
                "Consider its place, maker, and occasion",
                "Assume every motif has one universal meaning",
                "Ignore the surface on which it was made",
            ],
            "answer": "Consider its place, maker, and occasion",
            "explanation": (
                "Mandana designs are best understood in their local and "
                "situational context; meanings can vary."
            ),
        },
    },
    "pichwai": {
        "title": "Pichhwai painting",
        "region": "Strongly associated with Nathdwara in Rajasthan and the Pushtimarg tradition.",
        "history": (
            "Pichhwais developed as devotional paintings used in temple "
            "settings, especially in connection with Shrinathji worship at "
            "Nathdwara. Images may change with festivals, seasons, and ritual "
            "occasions."
        ),
        "materials": (
            "Many pichhwais are painted on cloth, though materials and "
            "techniques differ among artists and periods."
        ),
        "visual_language": (
            "Look for a central devotional figure, carefully arranged "
            "attendants or landscape details, and intricate decoration that "
            "supports the ritual scene."
        ),
        "cultural_context": (
            "A pichhwai is made for a devotional setting as well as for visual "
            "appreciation. Its placement and occasion can be important to "
            "understanding it."
        ),
        "reflection": "What might change in a temple's visual setting from one festival or season to another?",
        "sources": [
            (
                "Pichhwai overview",
                "https://en.wikipedia.org/wiki/Pichhwai",
            ),
            (
                "The Metropolitan Museum of Art: Indian paintings collection",
                "https://www.metmuseum.org/art/collection/search?q=pichhwai",
            ),
        ],
        "question": {
            "prompt": "What is a traditional use of a pichhwai?",
            "options": [
                "A devotional painted hanging used in a temple setting",
                "A small illustrated court manuscript only",
                "A geometric floor design made for a doorway",
            ],
            "answer": "A devotional painted hanging used in a temple setting",
            "explanation": (
                "Pichhwais are devotional paintings, often on cloth, associated "
                "with temple settings and Shrinathji worship."
            ),
        },
    },
    "warli": {
        "title": "Warli painting",
        "region": "Maharashtra, including communities in the state's northern Sahyadri region.",
        "history": (
            "Warli painting is associated with Warli communities and has been "
            "practised in domestic and ceremonial settings. Contemporary "
            "artists also make works on paper and other surfaces."
        ),
        "materials": (
            "Traditional wall paintings use an earth-coloured surface and a "
            "light pigment, often described as rice-paste based. Contemporary "
            "materials vary."
        ),
        "visual_language": (
            "Look for human and animal figures built from simple geometric "
            "shapes, often arranged in scenes of work, dance, or community life."
        ),
        "cultural_context": (
            "Warli is connected with living communities. A visual motif alone "
            "cannot tell you the maker's identity or the full meaning of a work."
        ),
        "reflection": "What kinds of relationships or activities are shown by the figures?",
        "sources": [
            (
                "Warli painting overview",
                "https://en.wikipedia.org/wiki/Warli_painting",
            ),
            (
                "Google Arts & Culture: Warli art collection search",
                "https://artsandculture.google.com/search?q=Warli%20painting",
            ),
        ],
        "question": {
            "prompt": "Which shapes are commonly used to build figures in Warli painting?",
            "options": [
                "Simple geometric forms such as circles and triangles",
                "Only realistic shaded portraits",
                "Calligraphic lettering alone",
            ],
            "answer": "Simple geometric forms such as circles and triangles",
            "explanation": (
                "Geometric forms are a well-known visual feature, but each "
                "artist's work and meaning should be considered individually."
            ),
        },
    },
}

ADDITIONAL_QUESTIONS = {
    "gond": [
        {
            "prompt": "Which subjects may appear in contemporary Gond paintings?",
            "options": [
                "Animals, plants, stories, and everyday life",
                "Only maps of modern cities",
                "Only architectural floor plans",
            ],
            "answer": "Animals, plants, stories, and everyday life",
            "explanation": (
                "Gond artists work with varied subjects, including living "
                "beings, stories, and experiences from their worlds."
            ),
        },
        {
            "prompt": "What is a respectful way to describe Gond art?",
            "options": [
                "Recognize many artists and approaches within Gond communities",
                "Assume every Gond artist uses an identical style",
                "Treat one image as representing every Gond community",
            ],
            "answer": "Recognize many artists and approaches within Gond communities",
            "explanation": (
                "Gond is a broad community identity. Artists' approaches differ "
                "and should not be flattened into one formula."
            ),
        },
    ],
    "kalighat": [
        {
            "prompt": "Who were among the painters associated with Kalighat works?",
            "options": [
                "Patua painters",
                "Only palace miniature painters from Kangra",
                "Only mural conservators",
            ],
            "answer": "Patua painters",
            "explanation": (
                "Patua painters made works around the Kalighat area for local "
                "audiences, pilgrims, and visitors."
            ),
        },
        {
            "prompt": "Besides religious subjects, what could Kalighat paintings depict?",
            "options": [
                "Everyday life and social themes",
                "Only astronomical charts",
                "Only landscapes without figures",
            ],
            "answer": "Everyday life and social themes",
            "explanation": (
                "Kalighat works could respond to contemporary urban life as "
                "well as devotional themes."
            ),
        },
    ],
    "kangra": [
        {
            "prompt": "Which themes are often found in Kangra miniature painting?",
            "options": [
                "Narrative and devotional scenes, including Krishna stories",
                "Only geometric floor patterns",
                "Only modern industrial machinery",
            ],
            "answer": "Narrative and devotional scenes, including Krishna stories",
            "explanation": (
                "Kangra miniatures often draw on narrative and devotional "
                "subjects, including poetry and stories of Krishna."
            ),
        },
        {
            "prompt": "What does the word 'Pahari' refer to in this art context?",
            "options": [
                "A group of painting traditions from Himalayan hill regions",
                "A single pigment used on cloth",
                "A type of temple floor design",
            ],
            "answer": "A group of painting traditions from Himalayan hill regions",
            "explanation": (
                "Pahari describes a wider family of painting traditions from "
                "the Himalayan hill regions; Kangra is one regional school."
            ),
        },
    ],
    "kerala": [
        {
            "prompt": "Why should a mural be studied in its original building context?",
            "options": [
                "Its architecture and setting can shape how it is experienced",
                "The wall surface never affects the artwork",
                "Every mural was made as a portable paper picture",
            ],
            "answer": "Its architecture and setting can shape how it is experienced",
            "explanation": (
                "A mural belongs to a wall and a site; its placement and "
                "architectural setting are part of its experience."
            ),
        },
        {
            "prompt": "What is a careful way to think about the dates of Kerala murals?",
            "options": [
                "Different sites and paintings can belong to different periods",
                "Every surviving mural must be the same age",
                "All Kerala murals were painted in one year",
            ],
            "answer": "Different sites and paintings can belong to different periods",
            "explanation": (
                "Kerala's mural heritage spans multiple sites and periods, so "
                "specific works need site-specific research."
            ),
        },
    ],
    "madhubani": [
        {
            "prompt": "How was knowledge of Mithila painting often passed on?",
            "options": [
                "Through families and communities across generations",
                "Only through printed factory manuals",
                "Only through royal courts outside the region",
            ],
            "answer": "Through families and communities across generations",
            "explanation": (
                "Mithila painting has been sustained through community and "
                "family practices, while artists and formats have also changed."
            ),
        },
        {
            "prompt": "Which statement best describes Madhubani/Mithila painting today?",
            "options": [
                "A varied tradition practised by many artists and communities",
                "A style with one unchanging motif and one maker",
                "An art form limited to one modern material",
            ],
            "answer": "A varied tradition practised by many artists and communities",
            "explanation": (
                "There are different artists, communities, subjects, and "
                "materials within the broader Mithila painting tradition."
            ),
        },
    ],
    "mandana": [
        {
            "prompt": "Where might Mandana designs traditionally be made?",
            "options": [
                "On floors or walls in domestic spaces",
                "Only inside bound books",
                "Only on large temple cloth hangings",
            ],
            "answer": "On floors or walls in domestic spaces",
            "explanation": (
                "Mandana designs are associated with decorated floors and "
                "walls; their location and occasion matter."
            ),
        },
        {
            "prompt": "Why should viewers avoid assigning one universal meaning to every Mandana motif?",
            "options": [
                "Meanings can depend on local community, maker, and occasion",
                "All motifs have a single globally fixed meaning",
                "The design's context is never relevant",
            ],
            "answer": "Meanings can depend on local community, maker, and occasion",
            "explanation": (
                "Interpretation should be grounded in the context and knowledge "
                "of the people who make and use the designs."
            ),
        },
    ],
    "pichwai": [
        {
            "prompt": "Which devotional figure is strongly associated with many Pichhwai paintings?",
            "options": [
                "Shrinathji, a form of Krishna",
                "Only the Buddha",
                "Only a historical court ruler",
            ],
            "answer": "Shrinathji, a form of Krishna",
            "explanation": (
                "Many Pichhwais are connected with Shrinathji worship in the "
                "Pushtimarg tradition."
            ),
        },
        {
            "prompt": "Why might a temple display different Pichhwai images at different times?",
            "options": [
                "Images can relate to seasons, festivals, or rituals",
                "The paintings are randomly changed with no context",
                "A Pichhwai is always a permanent outdoor sign",
            ],
            "answer": "Images can relate to seasons, festivals, or rituals",
            "explanation": (
                "Some temple Pichhwais are selected to suit a devotional "
                "calendar, season, or occasion."
            ),
        },
    ],
    "warli": [
        {
            "prompt": "What scenes may Warli paintings communicate?",
            "options": [
                "Community activities, work, dance, and relationships with nature",
                "Only isolated royal portraits",
                "Only written lists of dates",
            ],
            "answer": "Community activities, work, dance, and relationships with nature",
            "explanation": (
                "Warli imagery can depict collective life and relationships "
                "with the natural world."
            ),
        },
        {
            "prompt": "What is an important limit when interpreting a Warli image?",
            "options": [
                "Visual motifs alone do not reveal the artist's identity or full meaning",
                "The style proves who made every image",
                "Every motif has the same meaning in every community",
            ],
            "answer": "Visual motifs alone do not reveal the artist's identity or full meaning",
            "explanation": (
                "A classifier can suggest a visual resemblance, but it cannot "
                "establish authorship, identity, or cultural meaning."
            ),
        },
    ],
}


def quiz_questions(tradition_name: str) -> list[dict[str, object]]:
    if tradition_name not in TRADITIONS:
        raise ValueError(f"Unknown tradition: {tradition_name}")
    return [
        TRADITIONS[tradition_name]["question"],
        *ADDITIONAL_QUESTIONS[tradition_name],
    ]


def validate_traditions(class_names: list[str]) -> None:
    missing = sorted(set(class_names) - TRADITIONS.keys())
    if missing:
        raise ValueError(
            "No learning content is available for model classes: "
            + ", ".join(missing)
        )
