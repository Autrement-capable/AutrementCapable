// GameDashboard.vue
<template>
  <div class="game-dashboard">
    <div class="dashboard-header">
      <h1>{{ userName }}'s Room</h1>
      <div class="user-stats">
        <div class="stat">
          <span class="stat-label">Points:</span>
          <span class="stat-value">{{ userPoints }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Level:</span>
          <span class="stat-value">{{ userLevel }}</span>
        </div>
        <div class="achievements-counter">
          <span class="star-icon">⭐</span>
          <span>{{ completedAchievements.length }}/{{ achievements.length }}</span>
        </div>
      </div>
    </div>
    
    <room-dashboard @object-interaction="handleInteraction"></room-dashboard>
    
    <div v-if="showFeedback" class="feedback-container" :class="feedbackType">
      <div class="feedback-content">
        <h3>{{ feedbackTitle }}</h3>
        <p>{{ feedbackMessage }}</p>
        <button @click="closeFeedback">Continuer</button>
      </div>
    </div>
    
    <div class="achievements-panel">
      <h2>Mes accomplissements</h2>
      <div class="achievements-list">
        <div 
          v-for="achievement in achievements" 
          :key="achievement.id"
          class="achievement-item"
          :class="{ 'completed': isAchievementCompleted(achievement.id) }"
        >
          <div class="achievement-icon">{{ achievement.icon }}</div>
          <div class="achievement-info">
            <h4>{{ achievement.title }}</h4>
            <p>{{ achievement.description }}</p>
          </div>
          <div class="achievement-status">
            {{ isAchievementCompleted(achievement.id) ? '✓' : '?' }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RoomDashboard from './RoomDashboard.vue';

export default {
  name: 'GameDashboard',
  components: {
    RoomDashboard
  },
  data() {
    return {
      userName: 'Joueur',
      userPoints: 0,
      userLevel: 1,
      lastAction: null,
      actionCounts: {
        sleep: 0,
        read: 0,
        work: 0,
        change: 0
      },
      showFeedback: false,
      feedbackTitle: '',
      feedbackMessage: '',
      feedbackType: 'info',
      completedAchievements: [],
      achievements: [
        {
          id: 'first_read',
          title: 'Premier livre',
          description: 'Lire un livre pour la première fois',
          icon: '📚',
          condition: (state) => state.actionCounts.read >= 1
        },
        {
          id: 'study_hard',
          title: 'Étudiant assidu',
          description: 'Lire 5 livres',
          icon: '🧠',
          condition: (state) => state.actionCounts.read >= 5
        },
        {
          id: 'good_sleep',
          title: 'Bonne nuit',
          description: 'Aller dormir pour la première fois',
          icon: '😴',
          condition: (state) => state.actionCounts.sleep >= 1
        },
        {
          id: 'hard_worker',
          title: 'Travailleur',
          description: 'Travailler au bureau 3 fois',
          icon: '💼',
          condition: (state) => state.actionCounts.work >= 3
        },
        {
          id: 'fashion',
          title: 'À la mode',
          description: 'Changer de vêtements 2 fois',
          icon: '👕',
          condition: (state) => state.actionCounts.change >= 2
        },
        {
          id: 'balanced',
          title: 'Équilibré',
          description: 'Effectuer chaque activité au moins une fois',
          icon: '⚖️',
          condition: (state) => {
            return Object.values(state.actionCounts).every(count => count >= 1);
          }
        }
      ]
    };
  },
  computed: {
    pointsToNextLevel() {
      return this.userLevel * 100;
    }
  },
  methods: {
    handleInteraction(data) {
      // Enregistrer la dernière action
      this.lastAction = data;
      
      // Incrémenter le compteur d'actions
      if (this.actionCounts[data.action] !== undefined) {
        this.actionCounts[data.action]++;
      }
      
      // Ajouter des points selon l'action
      const pointsMap = {
        read: 15,
        work: 20,
        sleep: 10,
        change: 5
      };
      
      const pointsEarned = pointsMap[data.action] || 5;
      this.userPoints += pointsEarned;
      
      // Vérifier si le niveau augmente
      this.checkLevelUp();
      
      // Vérifier les accomplissements
      this.checkAchievements();
      
      // Afficher le feedback
      this.showActionFeedback(data.action, pointsEarned);
    },
    
    checkLevelUp() {
      if (this.userPoints >= this.userLevel * 100) {
        this.userLevel++;
        this.showLevelUpFeedback();
      }
    },
    
    checkAchievements() {
      const state = {
        userPoints: this.userPoints,
        userLevel: this.userLevel,
        actionCounts: this.actionCounts,
        lastAction: this.lastAction
      };
      
      // Vérifier chaque accomplissement non complété
      this.achievements.forEach(achievement => {
        if (!this.isAchievementCompleted(achievement.id) && achievement.condition(state)) {
          this.completeAchievement(achievement);
        }
      });
    },
    
    completeAchievement(achievement) {
      // Ajouter l'accomplissement à la liste des complétés
      this.completedAchievements.push(achievement.id);
      
      // Bonus de points pour l'accomplissement
      this.userPoints += 50;
      
      // Afficher le feedback d'accomplissement
      setTimeout(() => {
        this.showAchievementFeedback(achievement);
      }, 1000);
    },
    
    isAchievementCompleted(achievementId) {
      return this.completedAchievements.includes(achievementId);
    },
    
    showActionFeedback(action, points) {
      const actionMessages = {
        read: {
          title: 'Lecture en cours',
          message: `Vous avez lu un livre et gagné ${points} points!`
        },
        work: {
          title: 'Au travail!',
          message: `Vous avez travaillé au bureau et gagné ${points} points!`
        },
        sleep: {
          title: 'Repos bien mérité',
          message: `Vous vous êtes reposé et avez gagné ${points} points!`
        },
        change: {
          title: 'Changement de style',
          message: `Vous avez changé de vêtements et gagné ${points} points!`
        }
      };
      
      const feedback = actionMessages[action] || {
        title: 'Action effectuée',
        message: `Vous avez effectué une action et gagné ${points} points!`
      };
      
      this.feedbackTitle = feedback.title;
      this.feedbackMessage = feedback.message;
      this.feedbackType = 'info';
      this.showFeedback = true;
    },
    
    showLevelUpFeedback() {
      this.feedbackTitle = 'Niveau supérieur!';
      this.feedbackMessage = `Félicitations! Vous avez atteint le niveau ${this.userLevel}!`;
      this.feedbackType = 'success';
      this.showFeedback = true;
    },
    
    showAchievementFeedback(achievement) {
      this.feedbackTitle = 'Nouvel accomplissement débloqué!';
      this.feedbackMessage = `${achievement.icon} ${achievement.title}: ${achievement.description}`;
      this.feedbackType = 'achievement';
      this.showFeedback = true;
    },
    
    closeFeedback() {
      this.showFeedback = false;
    }
  }
};
</script>

<style scoped>
.game-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.user-stats {
  display: flex;
  gap: 20px;
}

.stat {
  background-color: #f0f8ff;
  padding: 8px 15px;
  border-radius: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-label {
  font-weight: bold;
  margin-right: 5px;
}

.stat-value {
  font-size: 1.2em;
  color: #4682b4;
}

.achievements-counter {
  display: flex;
  align-items: center;
  gap: 5px;
  background-color: #fff8e1;
  padding: 8px 15px;
  border-radius: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.star-icon {
  font-size: 1.2em;
  color: #ffd700;
}

.feedback-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.feedback-content {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  max-width: 400px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.feedback-content h3 {
  margin-top: 0;
}

.feedback-content button {
  background-color: #4682b4;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  margin-top: 15px;
  font-family: inherit;
}

.feedback-container.info .feedback-content {
  border-top: 5px solid #4682b4;
}

.feedback-container.success .feedback-content {
  border-top: 5px solid #2e8b57;
}

.feedback-container.achievement .feedback-content {
  border-top: 5px solid #ffd700;
  background-color: #fffaf0;
}

.achievements-panel {
  margin-top: 30px;
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.achievements-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.achievement-item {
  display: flex;
  align-items: center;
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
}

.achievement-item:hover {
  transform: translateY(-3px);
}

.achievement-item.completed {
  background-color: #f0fff0;
  border-left: 4px solid #2e8b57;
}

.achievement-icon {
  font-size: 2em;
  margin-right: 15px;
  opacity: 0.7;
}

.achievement-item.completed .achievement-icon {
  opacity: 1;
}

.achievement-info {
  flex: 1;
}

.achievement-info h4 {
  margin: 0 0 5px 0;
}

.achievement-info p {
  margin: 0;
  font-size: 0.9em;
  color: #666;
}

.achievement-status {
  font-size: 1.5em;
  margin-left: 10px;
}

.achievement-item.completed .achievement-status {
  color: #2e8b57;
}
</style>