// Liste standardisée des compétences (skills) pour tous les scénarios
export const skillsList = {
  // Compétences de communication
  communication: {
    assertivite: {
      nom: "Assertivité",
      description: "Capacité à exprimer ses idées et besoins de façon claire et respectueuse"
    },
    communication: {
      nom: "Communication",
      description: "Capacité à transmettre efficacement des informations et à s'exprimer clairement"
    },
    diplomatie: {
      nom: "Diplomatie",
      description: "Habileté à gérer des situations délicates avec tact"
    },
    ecouteActive: {
      nom: "Écoute active",
      description: "Capacité à être attentif et à comprendre les messages des autres"
    },
    negociation: {
      nom: "Négociation",
      description: "Capacité à trouver des compromis et des solutions mutuellement satisfaisantes"
    },
    franchise: {
      nom: "Franchise",
      description: "Capacité à communiquer honnêtement et directement"
    }
  },
  
  // Compétences interpersonnelles
  interpersonnel: {
    empathie: {
      nom: "Empathie",
      description: "Capacité à comprendre et partager les sentiments des autres"
    },
    espritEquipe: {
      nom: "Esprit d'équipe",
      description: "Capacité à travailler efficacement avec d'autres personnes"
    },
    soutien: {
      nom: "Soutien",
      description: "Capacité à encourager et aider les autres"
    },
    mediation: {
      nom: "Médiation",
      description: "Capacité à résoudre des conflits et faciliter la communication entre personnes"
    },
    inclusion: {
      nom: "Inclusion",
      description: "Capacité à intégrer et valoriser la diversité des personnes"
    },
    coaching: {
      nom: "Coaching",
      description: "Capacité à guider et développer les compétences d'autrui"
    }
  },
  
  // Compétences d'adaptation
  adaptation: {
    adaptabilite: {
      nom: "Adaptabilité",
      description: "Capacité à s'ajuster efficacement aux changements"
    },
    initiative: {
      nom: "Initiative",
      description: "Capacité à agir spontanément sans incitation externe"
    },
    reflexionRapide: {
      nom: "Réflexion rapide",
      description: "Capacité à prendre des décisions efficaces sous pression"
    },
    gestionStress: {
      nom: "Gestion du stress",
      description: "Capacité à rester calme et efficace en situation de tension"
    },
    creativite: {
      nom: "Créativité",
      description: "Capacité à trouver des solutions originales et innovantes"
    }
  },
  
  // Compétences professionnelles
  professionnelles: {
    responsabilite: {
      nom: "Responsabilité",
      description: "Capacité à assumer ses actes et leurs conséquences"
    },
    anticipation: {
      nom: "Anticipation",
      description: "Capacité à prévoir et se préparer aux événements futurs"
    },
    observation: {
      nom: "Observation",
      description: "Capacité à remarquer et analyser son environnement"
    },
    apprentissage: {
      nom: "Apprentissage",
      description: "Capacité à acquérir de nouvelles connaissances et compétences"
    },
    gestionTemps: {
      nom: "Gestion du temps",
      description: "Capacité à organiser efficacement ses activités"
    },
    decision: {
      nom: "Prise de décision",
      description: "Capacité à faire des choix éclairés en temps voulu"
    }
  },
  
  // Compétences personnelles
  personnelles: {
    confianceEnSoi: {
      nom: "Confiance en soi",
      description: "Assurance dans ses propres capacités et valeurs"
    },
    autonomie: {
      nom: "Autonomie",
      description: "Capacité à travailler et résoudre des problèmes par soi-même"
    },
    patience: {
      nom: "Patience",
      description: "Capacité à accepter les délais et à persévérer dans la durée"
    },
    curiosite: {
      nom: "Curiosité",
      description: "Désir d'apprendre et de s'intéresser à de nouvelles choses"
    },
    pragmatisme: {
      nom: "Pragmatisme",
      description: "Approche pratique et réaliste des situations"
    },
    assurance: {
      nom: "Assurance",
      description: "Confiance en ses capacités et aisance dans les interactions"
    }
  }
};

// Ajout: Liste des compétences qui peuvent être pénalisées (skills en négatif)
export const penaltySkills = [
  "empathie",
  "assertivite",
  "initiative",
  "communication",
  "espritEquipe",
  "responsabilite",
  "confianceEnSoi",
  "diplomatie",
  "inclusion",
  "mediation"
];

// Fonction pour obtenir toutes les compétences en une seule liste plate
export function getAllSkills() {
  const allSkills = {};
  
  Object.values(skillsList).forEach(category => {
    Object.entries(category).forEach(([key, value]) => {
      allSkills[key] = value;
    });
  });
  
  return allSkills;
}

// Fonction pour obtenir le niveau d'une compétence en fonction du score
export function getSkillLevel(score) {
  if (score <= 0) return "Non développé";
  if (score < 5) return "En développement";
  if (score < 10) return "Intermédiaire";
  if (score < 15) return "Avancé";
  return "Expert";
}

// Fonction pour obtenir une couleur en fonction du niveau
export function getSkillColor(score) {
  if (score <= 0) return "#dc3545"; // rouge
  if (score < 5) return "#ffc107"; // jaune
  if (score < 10) return "#17a2b8"; // bleu clair
  if (score < 15) return "#28a745"; // vert
  return "#007bff"; // bleu
}