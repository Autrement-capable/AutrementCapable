<template>
  <div class="skills-wheel-container">
    <!-- Animation de déblocage du badge -->
    <div v-if="showBadgeUnlockAnimation" class="badge-unlock-overlay">
      <div class="badge-unlock-animation">
        <div class="badge-icon">🎯</div>
        <h2>Badge débloqué !</h2>
        <h3>{{ badgeData.name }}</h3>
        <p>{{ badgeData.description }}</p>
        <button @click="closeBadgeAnimation" class="close-animation-btn">Continuer</button>
      </div>
    </div>
    <!-- Header avec personnage guide -->
    <div class="guide-character" v-if="!gameStarted">
      <img src="@/assets/avatars/guide.png" alt="Guide" class="guide-avatar" />
      <div class="speech-bubble">
        <p>Bienvenue dans le jeu de la Roulette des Compétences ! Découvre tes forces et tes domaines d'amélioration en t'amusant.</p>
      </div>
    </div>

    <div class="game-header">
      <h1 class="main-title">Roulette des Compétences</h1>
      <p class="subtitle" v-if="!gameStarted">Tourne la roue, découvre des compétences et indique ton niveau de maîtrise</p>
    </div>
    
    <!-- Écran d'accueil -->
    <div class="welcome-screen" v-if="!gameStarted">
      <div class="welcome-card">
        <div class="card-icon">🎯</div>
        <h2>Comment jouer ?</h2>
        <ol class="instructions-list">
          <li><span class="instruction-step">1</span> Tourne la roue pour découvrir une compétence au hasard</li>
          <li><span class="instruction-step">2</span> Pour chaque compétence, indique si tu la possèdes déjà, si tu souhaites la développer, ou si tu as des difficultés avec</li>
          <li><span class="instruction-step">3</span> À la fin, tu pourras voir un bilan de tes forces et de tes axes d'amélioration</li>
        </ol>
        <button @click="startGame" class="start-button">
          <span class="btn-icon">🎮</span>
          <span class="btn-text">Commencer à jouer</span>
        </button>
      </div>
    </div>
    
    <!-- Zone de jeu principale -->
    <div class="game-playground" v-if="gameStarted">
      <!-- Barre de progression -->
      <div class="progress-container">
        <div class="progress-steps">
          <div class="progress-step" :class="{ 'completed': answeredCount > 0 }">
            <div class="step-icon">🎮</div>
            <div class="step-label">Démarrage</div>
          </div>
          
          <div class="progress-connector"></div>
          
          <div class="progress-step" :class="{ 'completed': answeredCount >= Math.floor(totalSkills/3) }">
            <div class="step-icon">🏃</div>
            <div class="step-label">En cours</div>
          </div>
          
          <div class="progress-connector"></div>
          
          <div class="progress-step" :class="{ 'completed': answeredCount >= Math.floor(totalSkills*2/3) }">
            <div class="step-icon">🔍</div>
            <div class="step-label">Avancé</div>
          </div>
          
          <div class="progress-connector"></div>
          
          <div class="progress-step" :class="{ 'completed': answeredCount >= totalSkills }">
            <div class="step-icon">🏆</div>
            <div class="step-label">Terminé</div>
          </div>
        </div>
        
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
          <div class="progress-text">{{ answeredCount }} / {{ totalSkills }}</div>
        </div>
      </div>
      
      <div class="game-content">
        <!-- Wheel Section using ApexCharts -->
        <div class="wheel-section">
          <div class="wheel-container">
            <div ref="wheelRef" class="wheel">
              <apexchart
                type="pie"
                width="100%"
                height="450"
                :options="chartOptions"
                :series="chartSeries"
              ></apexchart>
            </div>
            
            <div class="wheel-pointer">
              <svg width="40" height="40" viewBox="0 0 40 40" transform="rotate(180)">
                <polygon points="20,0 0,20 40,20" fill="#f44336" />
              </svg>
            </div>
            
            <button 
              class="spin-button"
              :disabled="isSpinning || showAnswerOptions"
              @click="spinWheel"
            >
              <span class="btn-icon">🔄</span>
              <span class="btn-text">Tourner la roue</span>
            </button>
          </div>
        </div>
        
        <!-- Current Skill Section -->
        <div class="skill-section" v-if="showAnswerOptions && currentSkill">
          <div class="skill-card">
            <div class="skill-header">
              <div class="skill-icon-large">{{ getSkillIcon(currentSkill) }}</div>
              <h2 class="skill-title">{{ currentSkill.nom }}</h2>
            </div>
            
            <p class="skill-description">{{ currentSkill.description }}</p>
            
            <h3 class="question-text">Quelle est ta position par rapport à cette compétence ?</h3>
            
            <div class="answers-grid">
              <button 
                v-for="(option, index) in answerOptions" 
                :key="index"
                class="answer-option"
                :class="option.class"
                @click="selectAnswer(option.value)"
              >
                <div class="option-icon">{{ option.icon }}</div>
                <div class="option-text">{{ option.text }}</div>
              </button>
            </div>
            
            <div class="skill-actions">
              <button @click="skipCurrentSkill" class="action-button skip-button">
                <span class="btn-icon">⏭️</span>
                <span class="btn-text">Passer cette compétence</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal Results -->
    <div class="results-overlay" v-if="showResults">
      <div class="results-modal">
        <div class="results-header">
          <div class="results-title-container">
            <div class="results-title-icon">🏆</div>
            <h2 class="results-title">Tes résultats</h2>
          </div>
          <p class="results-subtitle">Voici un résumé de tes réponses sur les compétences</p>
        </div>
        
        <div class="results-grid">
          <div class="result-category strength-category">
            <div class="category-header">
              <div class="category-icon">💪</div>
              <h3>Mes points forts</h3>
            </div>
            <ul class="skills-list">
              <li v-for="(skill, index) in results.strengths" :key="`strength-${index}`" class="skill-item">
                <span class="skill-badge">{{ getSkillIcon(skill) }}</span>
                <span class="skill-name">{{ skill.nom }}</span>
              </li>
              <li v-if="results.strengths.length === 0" class="empty-list">Aucune compétence sélectionnée</li>
            </ul>
          </div>
          
          <div class="result-category improve-category">
            <div class="category-header">
              <div class="category-icon">🌱</div>
              <h3>À développer</h3>
            </div>
            <ul class="skills-list">
              <li v-for="(skill, index) in results.toImprove" :key="`improve-${index}`" class="skill-item">
                <span class="skill-badge">{{ getSkillIcon(skill) }}</span>
                <span class="skill-name">{{ skill.nom }}</span>
              </li>
              <li v-if="results.toImprove.length === 0" class="empty-list">Aucune compétence sélectionnée</li>
            </ul>
          </div>
          
          <div class="result-category difficulty-category">
            <div class="category-header">
              <div class="category-icon">🔍</div>
              <h3>Mes difficultés</h3>
            </div>
            <ul class="skills-list">
              <li v-for="(skill, index) in results.difficulties" :key="`diff-${index}`" class="skill-item">
                <span class="skill-badge">{{ getSkillIcon(skill) }}</span>
                <span class="skill-name">{{ skill.nom }}</span>
              </li>
              <li v-if="results.difficulties.length === 0" class="empty-list">Aucune compétence sélectionnée</li>
            </ul>
          </div>
        </div>
        
        <p class="result-summary">
          Tu as identifié <strong>{{ results.strengths.length }}</strong> points forts et 
          <strong>{{ results.toImprove.length }}</strong> compétences à développer. 
          Continue à travailler sur tes compétences pour progresser !
        </p>
        
        <div class="results-actions">
          <button @click="restartGame" class="action-button restart-button">
            <span class="btn-icon">🔄</span>
            <span class="btn-text">Rejouer</span>
          </button>
          <button @click="closeResults" class="action-button close-button">
            <span class="btn-icon">🏠</span>
            <span class="btn-text">Retour à l'accueil</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getAllSkills } from '@/data/skills-list';
import VueApexCharts from "vue3-apexcharts";
import { unlockBadge, isBadgeUnlocked } from '@/utils/badges';

export default {
  name: 'SkillsWheelGame',
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      gameStarted: false,
      isSpinning: false,
      currentChartRotation: 0, // Pour suivre la rotation actuelle
      segments: [],
      currentSegmentIndex: -1,
      currentSkill: null,
      showAnswerOptions: false,
      showResults: false,
      badgeSkillWheelId: 4,
      showBadgeUnlockAnimation: false,
      badgeData: {
        name: "Explorateur de Compétences",
        description: "Bravo ! Tu as complété la Roue des Compétences et découvert tes forces et faiblesses !"
      },
      spinDuration: 3000, // Milliseconds
      minSpins: 2, // Minimum number of full rotations
      maxSpins: 5, // Maximum number of full rotations
      answeredSkills: [],
      totalSkills: 0,
      answerOptions: [
        { value: 'strengths', text: 'Je la possède', icon: '💪', class: 'strength' },
        { value: 'toImprove', text: 'Je veux la développer', icon: '🌱', class: 'improve' },
        { value: 'difficulties', text: 'J\'ai du mal avec', icon: '🔍', class: 'difficulty' },
        { value: 'unknown', text: 'Je ne sais pas', icon: '❓', class: 'unknown' }
      ],
      results: {
        strengths: [],
        toImprove: [],
        difficulties: [],
        unknown: [],
        skipped: []
      },
      chartOptions: {
        chart: {
          type: 'pie',
          animations: {
            enabled: true,
            easing: 'easeinout',
            speed: 800,
            animateGradually: {
              enabled: true,
              delay: 150
            },
            dynamicAnimation: {
              enabled: true,
              speed: 350
            }
          }
        },
        labels: [],
        colors: [],
        plotOptions: {
          pie: {
            startAngle: 0,
            expandOnClick: false,
            donut: {
              size: '0%'
            },
            dataLabels: {
              offset: -30,
            }
          }
        },
        dataLabels: {
          enabled: true,
          formatter: function() {
            return '✨';
          },
          style: {
            fontSize: '24px',
            fontFamily: 'Arial, sans-serif',
            fontWeight: 'normal'
          },
          textAnchor: 'middle',
          distributed: true,
        },
        tooltip: {
          enabled: false
        },
        stroke: {
          width: 2,
          colors: ['#fff']
        },
        legend: {
          show: false
        },
        responsive: [{
          breakpoint: 768,
          options: {
            chart: {
              height: 350
            }
          }
        }],
        states: {
          hover: {
            filter: {
              type: 'none'
            }
          },
          active: {
            filter: {
              type: 'none'
            }
          }
        }
      },
      chartSeries: [], // Sera rempli avec des 1 pour chaque segment
    };
  },
  computed: {
    // Progress percentage for the progress bar
    progressPercentage() {
      if (this.totalSkills === 0) return 0;
      return (this.answeredCount / this.totalSkills) * 100;
    },
    // Count of answered skills
    answeredCount() {
      return this.answeredSkills.length;
    }
  },
  methods: {
    // Initialize game data and state
    startGame() {
      this.gameStarted = true;
      this.loadSkills();
      this.totalSkills = this.segments.length;
      
      // Limiter le nombre total de compétences pour ne pas rendre le jeu trop long
      // Sélectionner aléatoirement 10 compétences si le total est supérieur à 10
      if (this.segments.length > 10) {
        this.segments = this.getRandomSegments(10);
        this.totalSkills = 10;
      }
      
      // Initialiser le graphique ApexCharts avec les compétences
      this.updateChartData();
    },
    
    // Get N random segments
    getRandomSegments(n) {
      let shuffled = [...this.segments];
      let selected = [];
      let count = Math.min(n, shuffled.length);
      
      for (let i = 0; i < count; i++) {
        const randomIndex = Math.floor(Math.random() * shuffled.length);
        selected.push(shuffled[randomIndex]);
        shuffled.splice(randomIndex, 1);
      }
      
      return selected;
    },
    
    // Load skills from the skills-list.js file and create wheel segments
    loadSkills() {
      try {
        const allSkills = getAllSkills();
        if (!allSkills) {
          console.error("Impossible de charger les compétences");
          this.segments = [];
          return;
        }
        
        const skillsList = Object.values(allSkills);
        
        // Create segments for the wheel
        this.segments = skillsList.map(skill => ({ skill }));
        
        // Shuffle the segments to randomize the wheel
        this.shuffleSegments();
        
        console.log("Compétences chargées:", this.segments.length);
      } catch (error) {
        console.error("Erreur lors du chargement des compétences:", error);
        this.segments = [];
      }
    },
    
    // Fisher-Yates shuffle algorithm for segments
    shuffleSegments() {
      for (let i = this.segments.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [this.segments[i], this.segments[j]] = [this.segments[j], this.segments[i]];
      }
    },
    
    // Mettre à jour les données du graphique
    updateChartData() {
      // Définir les labels (noms des compétences)
      this.chartOptions.labels = this.segments.map(segment => 
        segment.skill.nom.length > 12 
          ? segment.skill.nom.slice(0, 10) + '...' 
          : segment.skill.nom
      );
      
      // Définir les séries (valeurs égales pour tous les segments)
      this.chartSeries = this.segments.map(() => 1);
      
      // Définir les couleurs pour chaque segment
      this.chartOptions.colors = this.segments.map((_, index) => this.getSegmentColor(index));

      this.chartOptions.dataLabels.formatter = (val, opts) => {
        const segmentIndex = opts.seriesIndex;
        if (segmentIndex >= 0 && segmentIndex < this.segments.length) {
          return this.getSkillIcon(this.segments[segmentIndex].skill);
        }
        return '✨';
      };
    },
    
    // Spin the wheel to select a random skill
    spinWheel() {
      if (this.isSpinning) return;
      
      this.isSpinning = true;
      this.showAnswerOptions = false;
      
      // Get a random segment that hasn't been answered yet
      const availableIndices = this.segments
        .map((_, index) => index)
        .filter(index => !this.answeredSkills.includes(this.segments[index].skill.nom));
      
      // If all skills have been answered, end the game
      if (availableIndices.length === 0) {
        this.endGame();
        return;
      }
      
      // Select random segment from available ones
      const randomIndex = Math.floor(Math.random() * availableIndices.length);
      this.currentSegmentIndex = availableIndices[randomIndex];
      
      // Play spinning sound if SpeechSynthesis is available
      this.playSpinningSound();
      
      // Préparer l'animation
      const startTime = performance.now();
      const targetRotation = (Math.floor(Math.random() * (this.maxSpins - this.minSpins + 1)) + this.minSpins) * 360;
      const segmentAngle = 360 / this.segments.length;
      const targetSegmentAngle = (this.currentSegmentIndex * segmentAngle) + (segmentAngle / 2);
      
      // Fonction d'animation utilisant requestAnimationFrame
      const animateWheel = (currentTime) => {
        // Calculer la progression (de 0 à 1)
        let progress = (currentTime - startTime) / this.spinDuration;
        
        // Limiter la progression à 1
        if (progress >= 1) {
          progress = 1;
        }
        
        // Appliquer une fonction easing pour un mouvement plus naturel
        // Démarrage lent, accélération, puis ralentissement à la fin
        const easeProgress = progress < 0.5 
          ? 4 * progress * progress * progress 
          : 1 - Math.pow(-2 * progress + 2, 3) / 2;
        
        const rotationForThisStep = targetRotation * easeProgress;
        const finalRotation = rotationForThisStep + targetSegmentAngle;
        
        // Mettre à jour les options du graphique
        this.chartOptions = {
          ...this.chartOptions,
          plotOptions: {
            ...this.chartOptions.plotOptions,
            pie: {
              ...this.chartOptions.plotOptions.pie,
              startAngle: -finalRotation,
              endAngle: 360 - finalRotation
            }
          }
        };
        
        // Forcer le rendu
        this.chartSeries = [...this.chartSeries];
        
        // Continuer l'animation si ce n'est pas terminé
        if (progress < 1) {
          requestAnimationFrame(animateWheel);
        } else {
          // Animation terminée
          this.isSpinning = false;
          this.currentSkill = this.segments[this.currentSegmentIndex].skill;
          this.showAnswerOptions = true;
          this.announceSkill();
          this.highlightSelectedSegment();
        }
      };
      
      // Démarrer l'animation
      requestAnimationFrame(animateWheel);
    },
    
    // Mettre en surbrillance le segment sélectionné
    highlightSelectedSegment() {
      // Créer une nouvelle palette de couleurs avec le segment sélectionné en surbrillance
      const newColors = this.segments.map((_, index) => {
        if (index === this.currentSegmentIndex) {
          // Éclaircir la couleur pour la surbrillance
          return this.lightenColor(this.getSegmentColor(index), 30);
        } else {
          return this.getSegmentColor(index);
        }
      });
      
      // Mettre à jour les options du graphique
      this.chartOptions = {
        ...this.chartOptions,
        colors: newColors
      };
    },
    
    // Éclaircir une couleur HTML
    lightenColor(color, percent) {
      // Convertir la couleur hexadécimale en RGB
      let r = parseInt(color.substring(1, 3), 16);
      let g = parseInt(color.substring(3, 5), 16);
      let b = parseInt(color.substring(5, 7), 16);
      
      // Éclaircir les composantes
      r = Math.min(255, Math.floor(r + (255 - r) * (percent / 100)));
      g = Math.min(255, Math.floor(g + (255 - g) * (percent / 100)));
      b = Math.min(255, Math.floor(b + (255 - b) * (percent / 100)));
      
      // Reconvertir en hexadécimal
      return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
    },
    
    // Record user's answer for the current skill
    selectAnswer(answerType) {
      if (!this.currentSkill) return;
      
      // Assurer que le tableau existe avant d'y ajouter des éléments
      if (!this.results[answerType]) {
        this.results[answerType] = [];
      }
      
      // Add the skill to the appropriate result category
      this.results[answerType].push(this.currentSkill);
      
      // Mark the skill as answered
      this.answeredSkills.push(this.currentSkill.nom);
      
      // Réinitialiser les couleurs du graphique
      this.updateChartData();
      
      // Clear current skill and hide answer options
      this.currentSkill = null;
      this.showAnswerOptions = false;
      
      // Check if all skills have been answered
      if (this.answeredSkills.length >= this.totalSkills) {
        setTimeout(() => {
          this.endGame();
        }, 1000);
      }
    },
    
    // Skip the current skill
    skipCurrentSkill() {
      if (!this.currentSkill) return;
      
      // Assurer que le tableau skipped existe
      if (!this.results.skipped) {
        this.results.skipped = [];
      }
      
      // Add the skill to the skipped category
      this.results.skipped.push(this.currentSkill);
      
      // Mark the skill as answered
      this.answeredSkills.push(this.currentSkill.nom);
      
      // Réinitialiser les couleurs du graphique
      this.updateChartData();
      
      // Clear current skill and hide answer options
      this.currentSkill = null;
      this.showAnswerOptions = false;
      
      // Check if all skills have been answered
      if (this.answeredSkills.length >= this.totalSkills) {
        setTimeout(() => {
          this.endGame();
        }, 1000);
      }
    },
    
    closeBadgeAnimation() {
      this.showBadgeUnlockAnimation = false;
    },

    // Unlock the completion badge and show animation
    unlockCompletionBadge() {
      if (!isBadgeUnlocked(this.badgeSkillWheelId)) {
        const badgeUnlocked = unlockBadge(this.badgeSkillWheelId);
        if (badgeUnlocked) {
          setTimeout(() => {
            this.showBadgeUnlockAnimation = true;
          }, 1500);
        }
      }
    },

    // End the game and show results
    endGame() {
      this.showResults = true;

      // unlock badge and show animation
      this.unlockCompletionBadge();
      
      // Save results to localStorage if needed
      this.saveResults();
    },
    
    // Restart the game with a fresh state
    restartGame() {
      this.currentSegmentIndex = -1;
      this.currentSkill = null;
      this.showAnswerOptions = false;
      this.showResults = false;
      this.answeredSkills = [];
      this.results = {
        strengths: [],
        toImprove: [],
        difficulties: [],
        unknown: [],
        skipped: []
      };
      
      // Shuffler les segments
      this.shuffleSegments();
      
      // Limiter le nombre total de compétences pour ne pas rendre le jeu trop long
      if (this.segments.length > 10) {
        this.segments = this.getRandomSegments(10);
        this.totalSkills = 10;
      }
      
      // Réinitialiser le graphique
      this.updateChartData();
    },
    
    // Close the results modal
    closeResults() {
      this.showResults = false;
      this.gameStarted = false;
    },
    
    // Save results to localStorage
    saveResults() {
      const skillsAssessment = {
        date: new Date().toISOString(),
        strengths: this.results.strengths.map(skill => skill.nom),
        toImprove: this.results.toImprove.map(skill => skill.nom),
        difficulties: this.results.difficulties.map(skill => skill.nom)
      };
      
      // Get existing assessments or create empty array
      const savedAssessments = JSON.parse(localStorage.getItem('skillsAssessments') || '[]');
      
      // Add new assessment
      savedAssessments.push(skillsAssessment);
      
      // Save to localStorage
      localStorage.setItem('skillsAssessments', JSON.stringify(savedAssessments));
    },
    
    // Get color for wheel segment based on index
    getSegmentColor(index) {
      // Array of vibrant, distinct colors for the wheel
      const colors = [
        '#FF9AA2', // soft red
        '#FFB7B2', // light pink
        '#FFDAC1', // light orange
        '#E2F0CB', // light green
        '#B5EAD7', // mint
        '#C7CEEA', // light blue
        '#9FD8DF', // teal
        '#D4A5A5', // mauve
        '#F9C5D5', // pink
        '#D6E2E9', // sky blue
        '#FFFFB5', // light yellow
        '#D8E4FF'  // periwinkle
      ];
      
      return colors[index % colors.length];
    },
    
    // Get icon for a skill
    getSkillIcon(skill) {
      if (!skill) return '✨';
      
      // Créer un dictionnaire pour la correspondance directe entre les noms affichés et les icônes
      const displayNameToIcon = {
        'Assertivité': '🗣️',
        'Communication': '📣',
        'Diplomatie': '🤝',
        'Écoute active': '👂',
        'Négociation': '🔍',
        'Franchise': '💯',
        'Empathie': '❤️',
        'Esprit d\'équipe': '🤲',
        'Soutien': '🙌',
        'Médiation': '⚖️',
        'Inclusion': '🌈',
        'Coaching': '📋',
        'Adaptabilité': '🦎',
        'Initiative': '🚀',
        'Réflexion rapide': '⚡',
        'Gestion du stress': '😌',
        'Créativité': '💡',
        'Responsabilité': '🛡️',
        'Anticipation': '🔮',
        'Observation': '👁️',
        'Apprentissage': '📚',
        'Gestion du temps': '⏱️',
        'Prise de décision': '✅',
        'Confiance en soi': '💪',
        'Autonomie': '🦅',
        'Patience': '🧘',
        'Curiosité': '🔎',
        'Pragmatisme': '🧰',
        'Assurance': '🏆'
      };
      
      // Simplifier notre approche en utilisant directement le nom de la compétence
      if (skill && skill.nom && displayNameToIcon[skill.nom]) {
        return displayNameToIcon[skill.nom];
      }
      
      console.log("Compétence sans icône trouvée:", skill);
      return '✨'; // Icône par défaut
    },
    
    // Play a spinning sound using Web Speech API
    playSpinningSound() {
      if (!('speechSynthesis' in window)) return;
      
      // Cancel any ongoing speech
      window.speechSynthesis.cancel();
      
      // Create and play a short spinning sound
      const utterance = new SpeechSynthesisUtterance('La roue tourne');
      utterance.lang = 'fr-FR';
      utterance.rate = 1.2;
      utterance.pitch = 1.5;
      
      window.speechSynthesis.speak(utterance);
    },
    
    // Announce the selected skill using speech synthesis
    announceSkill() {
      if (!('speechSynthesis' in window) || !this.currentSkill) return;
      
      // Cancel any ongoing speech
      window.speechSynthesis.cancel();
      
      // Create and play the announcement
      const skillName = this.currentSkill.name || this.currentSkill.nom;
      const utterance = new SpeechSynthesisUtterance(`Compétence: ${skillName}`);
      utterance.lang = 'fr-FR';
      
      window.speechSynthesis.speak(utterance);
    }
  }
};
</script>

<style scoped>
/* Base Styles */
.skills-wheel-container {
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px;
  color: #333;
  min-height: 100vh;
}

/* Game Header */
.game-header {
  text-align: center;
  margin-bottom: 30px;
}

.main-title {
  font-size: 2.5rem;
  color: #3f51b5;
  margin-bottom: 10px;
  text-align: center;
  position: relative;
  padding-bottom: 10px;
}

.main-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 4px;
  background-color: #ff9800;
  border-radius: 2px;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
  margin: 0;
}

/* Guide Character */
.guide-character {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
}

.guide-avatar {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  border: 3px solid #FFC107;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.speech-bubble {
  position: relative;
  background-color: #FFF;
  border-radius: 15px;
  padding: 15px;
  margin-left: 15px;
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
  max-width: 70%;
}

.speech-bubble:before {
  content: '';
  position: absolute;
  left: -10px;
  top: 50%;
  transform: translateY(-50%);
  border-width: 10px 10px 10px 0;
  border-style: solid;
  border-color: transparent #FFF transparent transparent;
}

.speech-bubble p {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
  line-height: 1.5;
}

/* Ajouter ces styles dans la section <style> existante du composant */

/* Animation du badge débloqué */
.badge-unlock-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1100; /* Plus élevé que les autres modales */
  animation: fadeIn 0.5s ease-out;
}

.badge-unlock-animation {
  background-color: #fff;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  max-width: 400px;
  box-shadow: 0 0 30px rgba(255, 152, 0, 0.6); /* Couleur adaptée au thème Roue des Compétences */
  animation: scaleIn 0.5s ease-out;
}

.badge-unlock-animation .badge-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: pulse 2s infinite;
  color: #FF9800; /* Couleur adaptée au thème */
}

.badge-unlock-animation h2 {
  color: #FF9800; /* Couleur adaptée au thème */
  font-size: 2rem;
  margin-bottom: 10px;
}

.badge-unlock-animation h3 {
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.badge-unlock-animation p {
  color: #666;
  margin-bottom: 20px;
}

.close-animation-btn {
  background-color: #FF9800; /* Couleur adaptée au thème */
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 50px;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-animation-btn:hover {
  background-color: #F57C00; /* Version plus foncée */
  transform: scale(1.05);
}

/* Ces animations sont déjà définies dans votre CSS, mais je les inclus au cas où */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

/* Welcome Screen */
.welcome-screen {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  align-items: center;
  margin: 40px 0;
}

.welcome-card {
  flex: 1;
  min-width: 300px;
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 20px;
  color: #ff9800;
}

.welcome-card h2 {
  font-size: 1.8rem;
  color: #3f51b5;
  margin-bottom: 20px;
}

.instructions-list {
  text-align: left;
  padding-left: 10px;
  margin-bottom: 30px;
}

.instructions-list li {
  margin-bottom: 15px;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 15px;
}

.instruction-step {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background-color: #3f51b5;
  color: white;
  border-radius: 50%;
  flex-shrink: 0;
}

/* Start Button */
.start-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 15px 30px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-top: 20px;
  height: auto;
  width: auto;
}

.start-button:hover {
  background-color: #388E3C;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.btn-icon {
  font-size: 1.3rem;
}

/* Game Playground */
.game-playground {
  margin-top: 30px;
}

/* Progress Container */
.progress-container {
  margin-bottom: 30px;
}

.progress-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 2;
}

.step-icon {
  width: 40px;
  height: 40px;
  background-color: #e9ecef;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  margin-bottom: 5px;
  border: 2px solid #ced4da;
  position: relative;
}

.step-label {
  font-size: 0.8rem;
  color: #6c757d;
}

.progress-step.completed .step-icon {
  background-color: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.progress-step.completed .step-label {
  color: #4CAF50;
  font-weight: bold;
}

.progress-connector {
  height: 2px;
  background-color: #ced4da;
  flex-grow: 1;
  margin: 0 -5px;
  position: relative;
  top: -22px;
  z-index: 1;
}

.progress-bar {
  width: 100%;
  height: 16px;
  background-color: #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #8BC34A);
  border-radius: 8px;
  transition: width 0.5s ease;
}

.progress-text {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333;
  font-weight: bold;
  font-size: 0.75rem;
}

/* Game Content */
.game-content {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  margin: 30px 0;
}

/* Wheel Section - Mise à jour pour ApexCharts */
.wheel-section {
  flex: 1;
  min-width: 350px;
  display: flex;
  justify-content: center;
}

.wheel-container {
  position: relative;
  width: 450px;
  height: 450px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.wheel {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  overflow: visible;
  background-color: transparent;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
}

.wheel-pointer {
  position: absolute;
  top: -20px;
  z-index: 20;
}

.spin-button {
  margin-top: 30px;
  padding: 12px 25px;
  background-color: #FF9800;
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.spin-button:hover:not(:disabled) {
  background-color: #F57C00;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.spin-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  opacity: 0.7;
}

/* Skill Section */
.skill-section {
  flex: 1;
  min-width: 300px;
}

.skill-card {
  background-color: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.5s ease;
}

.skill-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.skill-icon-large {
  font-size: 2.5rem;
  margin-right: 15px;
  width: 60px;
  height: 60px;
  background-color: #e3f2fd;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.skill-title {
  font-size: 1.8rem;
  color: #3f51b5;
  margin: 0;
}

.skill-description {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #555;
  margin-bottom: 20px;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 10px;
  border-left: 4px solid #3f51b5;
}

.question-text {
  font-size: 1.3rem;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.answers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 25px;
}

.answer-option {
  background-color: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  height: 100px;
  height: 120px;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.answer-option:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.option-icon {
  font-size: 2.2rem;
  margin-bottom: 10px;
}

.option-text {
  font-size: 0.9rem;
  font-weight: bold;
  line-height: 1.3;
  overflow-wrap: break-word;
  word-wrap: break-word;
  hyphens: auto;
  color: #4e504e;
}

.answer-option.strength {
  border-color: #4CAF50;
}

.answer-option.strength:hover {
  background-color: #E8F5E9;
}

.answer-option.improve {
  border-color: #2196F3;
}

.answer-option.improve:hover {
  background-color: #E3F2FD;
}

.answer-option.difficulty {
  border-color: #FF9800;
}

.answer-option.difficulty:hover {
  background-color: #FFF3E0;
}

.answer-option.unknown {
  border-color: #9E9E9E;
}

.answer-option.unknown:hover {
  background-color: #F5F5F5;
}

.skill-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* Game Actions */
.game-actions {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.action-button {
  padding: 12px 25px;
  border: none;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.skip-button {
  background-color: #9E9E9E;
  color: white;
}

.skip-button:hover {
  background-color: #757575;
}

.end-button {
  background-color: #3f51b5;
  color: white;
}

.end-button:hover {
  background-color: #303F9F;
}

/* Results Modal */
.results-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.results-modal {
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.5s ease;
}

.results-header {
  text-align: center;
  margin-bottom: 30px;
}

.results-title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.results-title-icon {
  font-size: 2.5rem;
  margin-right: 15px;
  color: #ff9800;
}

.results-title {
  font-size: 2.2rem;
  color: #3f51b5;
  margin: 0;
}

.results-subtitle {
  font-size: 1.2rem;
  color: #666;
  margin: 0;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.result-category {
  background-color: #f8f9fa;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.category-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e0e0e0;
}

.category-icon {
  font-size: 1.8rem;
  margin-right: 10px;
}

.result-category h3 {
  font-size: 1.3rem;
  color: #333;
  margin: 0;
}

.strength-category .category-icon {
  color: #4CAF50;
}

.strength-category .category-header {
  border-bottom-color: #4CAF50;
}

.improve-category .category-icon {
  color: #2196F3;
}

.improve-category .category-header {
  border-bottom-color: #2196F3;
}

.difficulty-category .category-icon {
  color: #FF9800;
}

.difficulty-category .category-header {
  border-bottom-color: #FF9800;
}

.skills-list {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 300px;
  overflow-y: auto;
}

.skill-item {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: white;
  border-radius: 10px;
  margin-bottom: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  animation: fadeIn 0.5s ease;
}

.skill-badge {
  width: 36px;
  height: 36px;
  background-color: #f5f5f5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  margin-right: 10px;
  flex-shrink: 0;
}

.skill-name {
  font-size: 1rem;
  color: #333;
}

.empty-list {
  text-align: center;
  color: #999;
  font-style: italic;
  padding: 15px;
}

.result-summary {
  text-align: center;
  font-size: 1.1rem;
  color: #555;
  margin: 25px 0;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 10px;
}

.results-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.restart-button {
  background-color: #4CAF50;
  color: white;
}

.restart-button:hover {
  background-color: #388E3C;
}

.close-button {
  background-color: #9E9E9E;
  color: white;
}

.close-button:hover {
  background-color: #757575;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from { transform: translateY(50px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* Responsive Styles */
@media (max-width: 768px) {
  .wheel-container {
    width: 350px;
    height: 350px;
  }
  
  .answers-grid {
    grid-template-columns: 1fr;
  }
  
  .results-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .wheel-container {
    width: 280px;
    height: 280px;
  }

  .game-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .game-actions .action-button {
    width: 80%; /* Rend les boutons plus larges sur mobile */
    max-width: 300px;
  }
}

/* ApexCharts specific overrides */
:deep(.apexcharts-pie-label),
:deep(.apexcharts-datalabel) {
  fill: #333 !important;
  font-size: 12px !important;
  font-weight: bold !important;
  filter: none !important;
}

:deep(.apexcharts-tooltip) {
  display: none !important; /* Désactiver les tooltips */
}

/* Accessibility Enhancements */
.skills-wheel-container:focus-within {
  outline: 3px solid #2196F3;
}

button:focus {
  outline: 3px solid #2196F3;
  outline-offset: 3px;
}

/* Animation pause for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
  button,
  .skill-item,
  .answer-option,
  .results-modal {
    animation: none !important;
    transition: none !important;
  }
}
</style>