export const usersList = [
    {
        id: 1,
        name: 'Zebi Lamouche',
        email: 'zebil@mail.com',
    },
    {
        id: 2,
        name: 'Avld Hazari',
        email: 'avldh@mail.com',
    },
    {
        id: 3,
        name: 'Archle Slefa',
        email: 'archles@mail.com',
    },
    {
        id: 4,
        name: 'Élodie Martin',
        email: 'elodiem@mail.com',
    },
    {
        id: 5,
        name: 'Lucas Dubois',
        email: 'lucasd@mail.com',
    },
    {
        id: 6,
        name: 'Chloé Lefevre',
        email: 'chloel@mail.com',
    },
    {
        id: 7,
        name: 'Mathieu Bernard',
        email: 'mathieub@mail.com',
    },
    {
        id: 8,
        name: 'Léa Moreau',
        email: 'leam@mail.com',
    },
    {
        id: 9,
        name: 'Julien Petit',
        email: 'julienp@mail.com',
    },
    {
        id: 10,
        name: 'Sophie Richard',
        email: 'sophier@mail.com',
    },
    {
        id: 11,
        name: 'Thomas Roux',
        email: 'thomasr@mail.com',
    },
    {
        id: 12,
        name: 'Camille Fournier',
        email: 'camillef@mail.com',
    },
    {
        id: 13,
        name: 'Arthur Girard',
        email: 'arthurg@mail.com',
    },
    {
        id: 14,
        name: 'Louise Dupont',
        email: 'louised@mail.com',
    },
    {
        id: 15,
        name: 'Maxime Lambert',
        email: 'maximel@mail.com',
    }
];

export const categoriesList = [
    {
        id: 1,
        nameCode: 'get-started',
        name: 'Get Started',
        description: 'New to the community? Start here!',
        iconName: 'mdi-rocket-launch-outline',
        color: 'green',
    },
    {
        id: 2,
        nameCode: 'accessibility',
        name: 'Accessibility',
        description: 'Discuss tools and solutions to increase accessibility for all users.',
        iconName: 'mdi-magic-staff',
        color: 'blue',
    },
    {
        id: 3,
        nameCode: 'announcement',
        name: 'Announcement',
        description: 'Stay up to date with the latest news and announcements.',
        iconName: 'mdi-bullhorn-outline',
        color: 'orange',
    },
    {
        id: 4,
        nameCode: 'suggestions',
        name: 'Suggestions',
        description: 'Have an idea to improve the community or the platform? Share it here!',
        iconName: 'mdi-lightbulb-on-outline',
        color: 'yellow',
    },
    {
        id: 5,
        nameCode: 'issues',
        name: 'Issues',
        description: 'Report bugs and issues you encounter while using the platform.',
        iconName: 'mdi-bug-outline',
        color: 'red',
    },
    {
        id: 6,
        nameCode: 'off-topic',
        name: 'Off Topic',
        description: 'Discuss anything not related to the other categories.',
        iconName: 'mdi-chat-outline',
        color: 'purple',
    },
    {
        id: 7,
        nameCode: 'your-story',
        name: 'Your Story',
        description: 'Share your story with the community.',
        iconName: 'mdi-pencil-outline',
        color: 'pink',
    },
]

export const postsList = [
    // Get Started
    {
        id: 1,
        title: 'Welcome to the Community!',
        content: 'Hello everyone! I just joined this community and I am excited to be here. I look forward to connecting with you all and learning more about this platform.',
        authorId: 1,
        categoryNameCode: 'get-started',
        createdAt: '2023-07-02 09:15:00',
        likes: 25,
        replies: [
            {
                content: 'Welcome aboard! Feel free to ask any questions.',
                authorId: 2,
                createdAt: '2024-07-02 09:30:00',
            },
            {
                content: 'Glad to have you here!',
                authorId: 3,
                createdAt: '2024-07-02 10:00:00',
            }
        ],
    },
    {
        id: 2,
        title: 'Getting Started Guide',
        content: 'For all the newcomers, I recommend checking out the getting started guide. It has everything you need to begin your journey here.',
        authorId: 4,
        categoryNameCode: 'get-started',
        createdAt: '2023-06-27 08:45:00',
        likes: 15,
        replies: [
            {
                content: 'The guide was super helpful, thanks!',
                authorId: 5,
                createdAt: '2024-07-03 09:10:00',
            },
            {
                content: 'A must-read for all newbies.',
                authorId: 6,
                createdAt: '2024-07-03 09:30:00',
            }
        ],
    },

    // Accessibility
    {
        id: 3,
        title: 'Accessible Design Tips',
        content: 'Creating accessible content is crucial for inclusive design. Here are some tips to ensure your content is accessible to everyone.',
        authorId: 7,
        categoryNameCode: 'accessibility',
        createdAt: '2024-07-01 14:20:00',
        likes: 30,
        replies: [
            {
                content: 'Thanks for sharing these tips!',
                authorId: 8,
                createdAt: '2024-07-01 15:00:00',
            },
            {
                content: 'This is very helpful!',
                authorId: 9,
                createdAt: '2024-07-01 15:30:00',
            }
        ],
    },
    {
        id: 4,
        title: 'Tools for Accessibility Testing',
        content: 'I found some great tools for testing accessibility. Check them out and let me know what you think!',
        authorId: 10,
        categoryNameCode: 'accessibility',
        createdAt: '2024-07-03 11:50:00',
        likes: 20,
        replies: [
            {
                content: 'These tools are great! Thanks for sharing.',
                authorId: 11,
                createdAt: '2024-07-03 12:10:00',
            },
            {
                content: 'I use some of these tools regularly.',
                authorId: 12,
                createdAt: '2024-07-03 12:40:00',
            }
        ],
    },

    // Announcement
    {
        id: 5,
        title: 'New Feature Release!',
        content: 'We are excited to announce a new feature that will enhance your experience. Check out the details in the link below.',
        authorId: 13,
        categoryNameCode: 'announcement',
        createdAt: '2024-07-01 10:00:00',
        likes: 40,
        replies: [
            {
                content: 'Can’t wait to try this out!',
                authorId: 14,
                createdAt: '2024-07-01 10:30:00',
            },
            {
                content: 'Great addition to the platform.',
                authorId: 15,
                createdAt: '2024-07-01 11:00:00',
            }
        ],
    },
    {
        id: 6,
        title: 'Upcoming Maintenance Downtime',
        content: 'Please note that the platform will be down for maintenance on July 5th from 1 AM to 3 AM. Thank you for your understanding.',
        authorId: 1,
        categoryNameCode: 'announcement',
        createdAt: '2024-07-02 13:45:00',
        likes: 10,
        replies: [
            {
                content: 'Thanks for the heads-up!',
                authorId: 2,
                createdAt: '2024-07-02 14:00:00',
            },
            {
                content: 'Hope the maintenance goes smoothly.',
                authorId: 3,
                createdAt: '2024-07-02 14:30:00',
            }
        ],
    },

    // Suggestions
    {
        id: 7,
        title: 'New Forum Section Suggestion',
        content: 'I think it would be great to have a section dedicated to project showcases. What do you all think?',
        authorId: 4,
        categoryNameCode: 'suggestions',
        createdAt: '2024-07-01 12:30:00',
        likes: 35,
        replies: [
            {
                content: 'I love this idea!',
                authorId: 5,
                createdAt: '2024-07-01 13:00:00',
            },
            {
                content: 'A project showcase section would be awesome.',
                authorId: 6,
                createdAt: '2024-07-01 13:30:00',
            }
        ],
    },
    {
        id: 8,
        title: 'Dark Mode Suggestion',
        content: 'Would anyone else like to see a dark mode option for the platform? It would be easier on the eyes, especially at night.',
        authorId: 7,
        categoryNameCode: 'suggestions',
        createdAt: '2024-07-02 16:15:00',
        likes: 45,
        replies: [
            {
                content: 'Dark mode would be amazing!',
                authorId: 8,
                createdAt: '2024-07-02 16:45:00',
            },
            {
                content: 'Yes, please add dark mode.',
                authorId: 9,
                createdAt: '2024-07-02 17:00:00',
            }
        ],
    },

    // Issues
    {
        id: 9,
        title: 'Login Issue on Mobile',
        content: 'Is anyone else having trouble logging in on their mobile devices? It keeps redirecting me back to the login page.',
        authorId: 10,
        categoryNameCode: 'issues',
        createdAt: '2024-07-01 08:50:00',
        likes: 5,
        replies: [
            {
                content: 'Yes, I am experiencing the same issue.',
                authorId: 11,
                createdAt: '2024-07-01 09:10:00',
            },
            {
                content: 'The same thing is happening to me.',
                authorId: 12,
                createdAt: '2024-07-01 09:30:00',
            }
        ],
    },
    {
        id: 10,
        title: 'Page Loading Error',
        content: 'I keep getting an error message when trying to load the forum page. Anyone else having this problem?',
        authorId: 13,
        categoryNameCode: 'issues',
        createdAt: '2024-07-03 14:25:00',
        likes: 8,
        replies: [
            {
                content: 'I had the same issue, but it seems to be working now.',
                authorId: 14,
                createdAt: '2024-07-03 14:50:00',
            },
            {
                content: 'Try clearing your cache and cookies. It worked for me.',
                authorId: 15,
                createdAt: '2024-07-03 15:00:00',
            }
        ],
    },

    // Off Topic
    {
        id: 11,
        title: 'Favorite Books',
        content: 'What are some of your favorite books? I’m looking for new recommendations.',
        authorId: 1,
        categoryNameCode: 'off-topic',
        createdAt: '2024-07-02 17:40:00',
        likes: 20,
        replies: [
            {
                content: 'I highly recommend "To Kill a Mockingbird".',
                authorId: 2,
                createdAt: '2024-07-02 18:00:00',
            },
            {
                content: 'You should check out "1984" by George Orwell.',
                authorId: 3,
                createdAt: '2024-07-02 18:20:00',
            }
        ],
    },
    {
        id: 12,
        title: 'Favorite Movies',
        content: 'What are some movies you guys absolutely love? I need something good to watch this weekend.',
        authorId: 4,
        categoryNameCode: 'off-topic',
        createdAt: '2024-07-03 19:10:00',
        likes: 25,
        replies: [
            {
                content: 'I love "Inception". It’s a mind-bender!',
                authorId: 5,
                createdAt: '2024-07-03 19:30:00',
            },
            {
                content: 'You should watch "The Shawshank Redemption".',
                authorId: 6,
                createdAt: '2024-07-03 20:00:00',
            }
        ],
    },

    // Your Story
    {
        id: 13,
        title: 'My Journey into Coding',
        content: 'I started learning to code last year, and it has been an incredible journey. Here’s how it all began for me...',
        authorId: 7,
        categoryNameCode: 'your-story',
        createdAt: '2024-07-01 21:45:00',
        likes: 50,
        replies: [
            {
                content: 'Your story is so inspiring!',
                authorId: 8,
                createdAt: '2024-07-01 22:00:00',
            },
            {
                content: 'Thank you for sharing your journey.',
                authorId: 9,
                createdAt: '2024-07-01 22:30:00',
            }
        ],
    },
    {
        id: 14,
        title: 'From Hobby to Career',
        content: 'What started as a hobby has now turned into my career. Here’s how I made the transition...',
        authorId: 10,
        categoryNameCode: 'your-story',
        createdAt: '2024-07-03 23:10:00',
        likes: 35,
        replies: [
            {
                content: 'I’m in the same boat! Thanks for sharing.',
                authorId: 11,
                createdAt: '2024-07-03 23:30:00',
            },
            {
                content: 'Very motivating! Congratulations on your success.',
                authorId: 12,
                createdAt: '2024-07-04 00:00:00',
            }
        ],
    },
];

export const scenarios = [
    {
        id: 1,
        titre: "Un inconnu en difficulté",
        contexteIntro: "Tu rentres tranquillement chez toi après une longue journée. Soudain, tu remarques qu'une personne âgée trébuche et tombe sur le trottoir. Quelques passants hésitent à intervenir.",
        contexte: [
          { personnage: "Passant 1", avatar: "femme-daffaires.png", texte: "Oh… Elle est tombée !" },
          { personnage: "Passant 2", avatar: "passant2.png", texte: "Quelqu'un devrait faire quelque chose..." },
          { personnage: "Personne âgée", avatar: "personne_agee.png", texte: "Aïe... J'ai mal au poignet..." }
        ],
        question: "Que fais-tu ?",
        reponses: [
          { id: "A", texte: "Tu aides immédiatement la personne à se relever.", skills: { empathie: 5, initiative: 4 } },
          { id: "B", texte: "Tu appelles les secours et attends avec elle.", skills: { responsabilite: 4, espritEquipe: 3 } },
          { id: "C", texte: "Tu observes si quelqu'un d'autre intervient.", skills: { observation: 4 }, penalties: { initiative: 2, empathie: 1 } },
          { id: "D", texte: "Tu continues ta route.", skills: { }, penalties: { empathie: 5, responsabilite: 4 } }
        ]
    },
    {
        id: 2,
        titre: "Conflit au supermarché",
        contexteIntro: "Tu fais des courses dans un supermarché bondé. Après plusieurs minutes dans la file d'attente, quelqu'un passe devant toi. D'autres clients semblent mécontents, mais personne n'ose parler.",
        contexte: [
          { personnage: "Client derrière", avatar: "femme.png", texte: "Vous avez vu ? Il passe devant tout le monde !" },
          { personnage: "Caissier", avatar: "femme-caissiere.png", texte: "Veuillez respecter la file, s'il vous plaît." }
        ],
        question: "Comment réagis-tu ?",
        reponses: [
          { id: "A", texte: "Tu fais remarquer calmement la file d'attente.", skills: { assertivite: 5, diplomatie: 4 } },
          { id: "B", texte: "Tu attends que quelqu'un d'autre réagisse.", skills: { patience: 4 }, penalties: { assertivite: 3, espritEquipe: 2 } },
          { id: "C", texte: "Tu fais une remarque sèche.", skills: { assertivite: 4 }, penalties: { diplomatie: 3 } },
          { id: "D", texte: "Tu ignores la situation.", skills: { patience: 3 }, penalties: { assertivite: 4, espritEquipe: 2 } }
        ]
    },
    {
        id: 3,
        titre: "Un ami en difficulté",
        contexteIntro: "Un ami proche t'appelle, visiblement bouleversé. Il a vécu une mauvaise journée et cherche du soutien. Tu sens qu'il a besoin de parler, mais aussi de conseils.",
        contexte: [
          { personnage: "Alex", avatar: "passant2.png", texte: "Franchement, j'en peux plus… Mon stage est horrible, mon tuteur me critique tout le temps." },
          { personnage: "Toi", avatar: "toi.png", texte: "Ça n'a pas l'air simple… Qu'est-ce qu'il s'est passé aujourd'hui ?" },
          { personnage: "Alex", avatar: "passant2.png", texte: "Je crois que je vais tout arrêter." }
        ],
        question: "Que fais-tu ?",
        reponses: [
          { id: "A", texte: "Tu l'écoutes attentivement avant de donner ton avis.", skills: { empathie: 5, ecouteActive: 4 } },
          { id: "B", texte: "Tu lui dis : 'Ne te laisse pas faire, défends-toi !'", skills: { soutien: 4, assertivite: 3 } },
          { id: "C", texte: "Tu lui réponds : 'Si c'est trop dur, arrête, tu trouveras autre chose.'", skills: { pragmatisme: 4 }, penalties: { empathie: 3, soutien: 2 } },
          { id: "D", texte: "Tu proposes de chercher ensemble des solutions.", skills: { espritEquipe: 5, coaching: 4 } }
        ]
    },
    {
        id: 4,
        titre: "Erreur au restaurant",
        contexteIntro: "Tu es au restaurant avec des amis. Après avoir attendu longtemps, tu reçois un plat qui ne correspond pas à ta commande. Le serveur semble pressé.",
        contexte: [
          { personnage: "Serveur", avatar: "serveur.png", texte: "Voici votre commande !" },
          { personnage: "Toi", avatar: "toi.png", texte: "Hmm… Ce n'est pas ce que j'avais demandé." },
          { personnage: "Serveur", avatar: "serveur.png", texte: "Oh, vraiment ? Désolé ! Vous voulez que je change ?" }
        ],
        question: "Comment réagis-tu ?",
        reponses: [
          { id: "A", texte: "Tu demandes calmement à recevoir le bon plat.", skills: { assertivite: 5, communication: 4 } },
          { id: "B", texte: "Tu ne dis rien et manges quand même.", skills: { patience: 3 }, penalties: { assertivite: 4, confianceEnSoi: 2 } },
          { id: "C", texte: "Tu fais une remarque sèche : C'est pas sérieux !'", skills: { assertivite: 4 }, penalties: { diplomatie: 3 } },
          { id: "D", texte: "Tu demandes si un geste commercial est possible.", skills: { negociation: 5, confianceEnSoi: 4 } }
        ]
    },
    {
        id: 5,
        titre: "Panne de bus",
        contexteIntro: "Tu es dans un bus, en route pour un rendez-vous important. Soudain, le bus tombe en panne. Il reste peu de temps avant ton entretien.",
        contexte: [
          { personnage: "Conducteur", avatar: "conducteur.png", texte: "Désolé, tout le monde descend, le bus ne repartira pas." },
          { personnage: "Passager", avatar: "femme.png", texte: "On fait quoi, là ? On va être en retard !" },
          { personnage: "Toi", avatar: "toi.png", texte: "L'entretien commence dans 15 minutes..." }
        ],
        question: "Que fais-tu ?",
        reponses: [
          { id: "A", texte: "Tu regardes sur ton téléphone une alternative rapide.", skills: { reflexionRapide: 5, adaptabilite: 4 } },
          { id: "B", texte: "Tu appelles ton recruteur pour prévenir de ton retard.", skills: { communication: 5, anticipation: 4 } },
          { id: "C", texte: "Tu demandes à un passager de partager un taxi.", skills: { initiative: 4, espritEquipe: 4 } },
          { id: "D", texte: "Tu attends que la situation se règle toute seule.", skills: { patience: 4 }, penalties: { initiative: 4, anticipation: 3 } }
        ]
    },
    {
        id: 6,
        titre: "Conflit en classe",
        contexteIntro: "Pendant un travail de groupe en classe, l'un de tes camarades critique tes idées devant tout le monde. L'ambiance devient tendue.",
        contexte: [
            { personnage: "Camarade", avatar: "passant2.png", texte: "Ton idée est nulle, on devrait faire autrement." },
            { personnage: "Autre élève", avatar: "femme.png", texte: "Euh… Calmez-vous." },
        ],
        question: "Que fais-tu ?",
        reponses: [
            { id: "A", texte: "Tu proposes de discuter calmement.", skills: { mediation: 5, empathie: 4 } },
            { id: "B", texte: "Tu défends tes idées avec fermeté.", skills: { assertivite: 5, confianceEnSoi: 4 } },
            { id: "C", texte: "Tu proposes à l'enseignant d'intervenir.", skills: { responsabilite: 4, decision: 3 } },
            { id: "D", texte: "Tu restes silencieux.", skills: { observation: 4, gestionStress: 3 }, penalties: { assertivite: 4, confianceEnSoi: 3 } }
        ]
    },
    {
        id: 7,
        titre: "Première journée de stage",
        contexteIntro: "C'est ton premier jour de stage dans une entreprise. Ton tuteur te donne une tâche que tu ne comprends pas bien.",
        contexte: [
            { personnage: "Tuteur", avatar: "homme-daffaire.png", texte: "Voici ta première tâche, tu peux t'y mettre." },
            { personnage: "Toi", avatar: "toi.png", texte: "(Je ne suis pas sûr de tout comprendre…)" }
        ],
        question: "Que fais-tu ?",
        reponses: [
            { id: "A", texte: "Tu demandes des précisions au tuteur.", skills: { communication: 5, curiosite: 4 } },
            { id: "B", texte: "Tu essaies de trouver la solution seul.", skills: { autonomie: 5, initiative: 4 } },
            { id: "C", texte: "Tu observes comment font tes collègues.", skills: { observation: 4, apprentissage: 4 } },
            { id: "D", texte: "Tu fais au mieux, même si tu n'es pas sûr.", skills: { confianceEnSoi: 4 }, penalties: { communication: 3, curiosite: 2 } }
        ]
    },
    {
        id: 8,
        titre: "Inclusion dans une activité de groupe",
        contexteIntro: "Tu organises une activité en groupe. L'un des participants utilise une prothèse de bras et semble avoir du mal avec l'exercice manuel proposé.",
        contexte: [
            { personnage: "Participant", avatar: "passant2.png", texte: "Je crois que je ne pourrai pas faire ça... J'ai trop mal au bras." },
            { personnage: "Toi", avatar: "toi.png", texte: "(Je vois que tu rencontres des difficultés avec cet exercice...)" },
        ],
        question: "Comment réagis-tu ?",
        reponses: [
            { id: "A", texte: "Tu modifies l'activité pour que tout le monde puisse participer.", skills: { creativite: 5, inclusion: 4 } },
            { id: "B", texte: "Tu lui proposes une autre tâche adaptée.", skills: { adaptabilite: 5, espritEquipe: 4 } },
            { id: "C", texte: "Tu l'encourages à essayer, en proposant de l'aider.", skills: { soutien: 4, coaching: 5 } },
            { id: "D", texte: "Tu continues l'activité telle quelle.", skills: { gestionTemps: 3 }, penalties: { inclusion: 3, empathie: 3 } }
        ]
    },
    {
        id: 9,
        titre: "Réunion d'équipe difficile",
        contexteIntro: "Tu participes à une réunion d'équipe importante. L'un de tes collègues présente une idée que tu sais être problématique, mais qui semble enthousiasmer le reste de l'équipe. Tu as des informations qui pourraient remettre en question cette proposition.",
        contexte: [
            { personnage: "Collègue", avatar: "homme-daffaire.png", texte: "Je suis sûr que cette approche va doubler notre efficacité !" },
            { personnage: "Chef d'équipe", avatar: "femme-daffaires.png", texte: "Cela semble prometteur. Quelqu'un a-t-il des questions ou remarques ?" },
            { personnage: "Toi", avatar: "toi.png", texte: "(Je sais que ce projet pourrait poser des problèmes techniques majeurs...)" }
        ],
        question: "Comment réagis-tu ?",
        reponses: [
            { 
                id: "A", 
                texte: "Tu expliques calmement les problèmes potentiels, avec des faits précis.", 
                skills: { assertivite: 4, communication: 5, diplomatie: 4 } 
            },
            { 
                id: "B", 
                texte: "Tu proposes de discuter en privé avec ton collègue après la réunion.", 
                skills: { diplomatie: 5, responsabilite: 3 },
                penalties: { assertivite: 2, communication: 1 }
            },
            { 
                id: "C", 
                texte: "Tu restes silencieux pour ne pas créer de tension dans l'équipe.", 
                skills: { observation: 3 },
                penalties: { assertivite: 4, responsabilite: 3, espritEquipe: 2 }
            },
            { 
                id: "D", 
                texte: "Tu suggères une phase de test avant de déployer l'idée complètement.", 
                skills: { diplomatie: 4, pragmatisme: 5, anticipation: 4 } 
            }
        ]
    },
    {
        id: 10,
        titre: "Formation d'un nouveau collègue",
        contexteIntro: "Tu es chargé de former un nouveau collègue qui rejoint votre équipe. Cette personne semble avoir du mal à comprendre certains aspects du travail et commence à se décourager après plusieurs tentatives infructueuses.",
        contexte: [
            { personnage: "Nouveau collègue", avatar: "passant2.png", texte: "Je n'y arrive vraiment pas... Je ne suis peut-être pas fait pour ce poste." },
            { personnage: "Toi", avatar: "toi.png", texte: "Je vois que tu rencontres des difficultés." },
            { personnage: "Nouveau collègue", avatar: "passant2.png", texte: "Oui, et j'ai peur de ne jamais réussir à m'adapter..." }
        ],
        question: "Comment poursuis-tu la formation ?",
        reponses: [
            { 
                id: "A", 
                texte: "Tu proposes une approche différente, plus adaptée à son style d'apprentissage.", 
                skills: { adaptabilite: 5, coaching: 5, empathie: 4 } 
            },
            { 
                id: "B", 
                texte: "Tu lui montres pas à pas comment réaliser la tâche, en expliquant chaque étape.", 
                skills: { patience: 4, communication: 5, soutien: 4 } 
            },
            { 
                id: "C", 
                texte: "Tu lui rappelles que tout le monde passe par des difficultés au début et partages ta propre expérience.", 
                skills: { empathie: 5, soutien: 4, communication: 3 } 
            },
            { 
                id: "D", 
                texte: "Tu divises les tâches en étapes plus petites et facilement réalisables pour créer des succès rapides.", 
                skills: { coaching: 4, creativite: 3, pragmatisme: 5 } 
            }
        ]
    },
];
